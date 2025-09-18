import json
import os
import glob
import torch
import pandas as pd 
from sentence_transformers import SentenceTransformer, util
from collections import Counter

# The input data structure remains the same.
document_data = {
    "total_avg_length": 43.701219512195124,
    "group_avg_lengths": [50.81059063136456, 25.0, 17.25, 20.0, 43.9, 63.0, 40.0, 13.928571428571429, 31.294117647058822, 59.25, 9.125],
    "selected_groups": [
        {
            "group_no": 2, "font_size": 24.0, "total_lines": 1,
            "lines": [{"line_no": 1, "page_no": 0, "text": "A Cyber Bridge Experiment", "is_bold": False}]
        },
        {
            "group_no": 3, "font_size": 9.0, "total_lines": 4,
            "lines": [
                {"line_no": 1, "page_no": 0, "text": "Mary Ann Hoppa", "is_bold": False},
                {"line_no": 2, "page_no": 0, "text": "Norfolk, Virginia USA", "is_bold": False},
                {"line_no": 3, "page_no": 0, "text": "mahoppa@nsu.edu", "is_bold": False},
                {"line_no": 4, "page_no": 0, "text": "0000-0002-6103-7814", "is_bold": False}
            ]
        },
        {
            "group_no": 4, "font_size": 9.0, "total_lines": 2,
            "lines": [
                {"line_no": 1, "page_no": 0, "text": "Computer Science", "is_bold": False},
                {"line_no": 2, "page_no": 0, "text": "Norfolk State University", "is_bold": False}
            ]
        },
        {
            "group_no": 7, "font_size": 9.96, "total_lines": 16,
            "lines": [
                {"line_no": 1, "page_no": 0, "text": "I. INTRODUCTION", "is_bold": False},
                {"line_no": 2, "page_no": 0, "text": "II. BACKGROUND", "is_bold": False},
                {"line_no": 3, "page_no": 1, "text": "III. RELATED WORKS", "is_bold": False},
                {"line_no": 4, "page_no": 1, "text": "IV. METHODOLOGY", "is_bold": False},
                {"line_no": 5, "page_no": 2, "text": "V. FINDINGS AND RECOMMENDATIONS", "is_bold": False},
                {"line_no": 6, "page_no": 2, "text": "• no participation (41 percent);", "is_bold": False},
                {"line_no": 16, "page_no": 5, "text": "VI. CONCLUSIONS AND FUTURE DIRECTIONS", "is_bold": False}
            ]
        }
    ]
}

def classify_document_hierarchical(data, base_path='L12', output_file='classified_document.json'):
    """
    Classifies a document using hierarchical structure with group-based predictions
    and maintains H1->H2->H3 hierarchy based on font sizes and semantic embeddings.
    """
    
    ## ----------------------------------------------------------------
    ## Part 1: Load Model and Embeddings from Directory
    ## ----------------------------------------------------------------
    print("✅ Step 1: Loading model and embeddings from directory...")
    model = SentenceTransformer('./all-MiniLM-L12-v2')

    heading_map = {'Title': 'title', 'H1': 'h1', 'H2': 'h2', 'H3': 'h3'}
    heading_embeddings = {}

    try:
        # Load all .pt files from the subdirectories
        for level_name, folder_name in heading_map.items():
            folder_path = os.path.join(base_path, folder_name)
            file_paths = glob.glob(os.path.join(folder_path, '*.pt'))
            
            if not file_paths:
                raise FileNotFoundError(f"No .pt files found in '{folder_path}'")

            # Load each tensor file and concatenate them
            tensors = [torch.load(fp, map_location=model.device) for fp in file_paths]
            heading_embeddings[level_name] = torch.cat(tensors, dim=0)
            print(f"   -> Loaded {len(file_paths)} embedding files for '{level_name}'.")

    except (FileNotFoundError, RuntimeError) as e:
        print(f"   ⚠️  Warning: Could not load embeddings from disk ({e}).")
        print("   -> Falling back to simulation mode.")
        # Fallback simulation if .pt files aren't found
        simulated_headings = {
            "Title": ["A Report on Deep Learning", "The Future of AI", "An Analysis of Market Trends"],
            "H1": ["Introduction", "Conclusion", "Methodology", "Background", "Results"],
            "H2": ["System Architecture", "Data Collection", "Preliminary Analysis"],
            "H3": ["Phase One", "Initial Results", "Detailed Findings"]
        }
        heading_embeddings = {
            level: model.encode(texts, convert_to_tensor=True)
            for level, texts in simulated_headings.items()
        }

    ## ----------------------------------------------------------------
    ## Part 2: Classify Individual Lines and Group by Structure
    ## ----------------------------------------------------------------
    print("\n✅ Step 2: Classifying individual lines within groups...")
    CLASSIFICATION_THRESHOLD = 0.4
    
    # Store groups with their classifications
    classified_groups = []
    
    # Get font size statistics for weighting
    font_sizes = [group['font_size'] for group in data['selected_groups']]
    max_font_size = max(font_sizes)
    min_font_size = min(font_sizes)
    
    for group in data['selected_groups']:
        font_size = group['font_size']
        group_predictions = []
        valid_lines = []
        
        # Classify each line in the group
        for line in group['lines']:
            line_text = line['text'].strip()
            # Skip bullet points and empty lines
            if not line_text or line_text.startswith(('•', '-', '*', '–', '▪', '◦')):
                continue
                
            valid_lines.append(line)
            line_embedding = model.encode(line_text, convert_to_tensor=True)
            scores = {}
            
            # Calculate semantic similarity scores
            for level, embeddings in heading_embeddings.items():
                cos_scores = util.cos_sim(line_embedding, embeddings)[0]
                scores[level] = torch.max(cos_scores).item()
            
            # Apply font size weighting
            font_weight = (font_size - min_font_size) / (max_font_size - min_font_size) if max_font_size != min_font_size else 0.5
            
            # Boost scores based on font size
            if font_size >= max_font_size * 0.9:  # Very large fonts likely titles
                scores['Title'] *= (1.3 + font_weight * 0.2)
            elif font_size >= max_font_size * 0.7:  # Large fonts likely H1
                scores['H1'] *= (1.2 + font_weight * 0.1)
                scores['Title'] *= (1.1 + font_weight * 0.1)
            elif font_size >= max_font_size * 0.5:  # Medium fonts likely H2
                scores['H2'] *= (1.15 + font_weight * 0.05)
                scores['H1'] *= (1.1 + font_weight * 0.05)
            else:  # Small fonts likely H3 or content
                scores['H3'] *= (1.1 + font_weight * 0.05)
            
            best_level = max(scores, key=scores.get)
            best_score = scores[best_level]
            
            if best_score > CLASSIFICATION_THRESHOLD:
                group_predictions.append(best_level)
            else:
                group_predictions.append('Content')  # Default for low-confidence predictions
        
        # Determine group classification using mode (most common prediction)
        if group_predictions and valid_lines:
            prediction_counts = Counter(group_predictions)
            group_classification = prediction_counts.most_common(1)[0][0]
            
            classified_groups.append({
                'group_no': group['group_no'],
                'font_size': font_size,
                'classification': group_classification,
                'lines': valid_lines,
                'confidence': prediction_counts[group_classification] / len(group_predictions)
            })
    
    ## ----------------------------------------------------------------
    ## Part 3: Identify Title Group and Apply Hierarchical Logic
    ## ----------------------------------------------------------------
    print("\n✅ Step 3: Identifying title group and applying hierarchical structure...")
    
    # Calculate average character length for each group
    groups_with_avg_length = []
    for i, group in enumerate(classified_groups):
        # Calculate average character length for valid lines in this group
        valid_texts = [line['text'] for line in group['lines']]
        if valid_texts:
            avg_char_length = sum(len(text) for text in valid_texts) / len(valid_texts)
        else:
            avg_char_length = 0
        
        groups_with_avg_length.append({
            **group,
            'avg_char_length': avg_char_length,
            'original_index': i
        })
    
    # Find title group using max font size and min average character length logic
    print("   -> Analyzing groups for title identification...")
    max_font_size = max(group['font_size'] for group in groups_with_avg_length)
    
    # Get groups with maximum font size
    max_font_groups = [g for g in groups_with_avg_length if g['font_size'] == max_font_size]
    
    # Among max font size groups, find the one with minimum average character length
    title_group = min(max_font_groups, key=lambda x: x['avg_char_length'])
    
    # Extract title text (combine all lines in the title group)
    title_texts = [line['text'].strip() for line in title_group['lines']]
    final_title = ' '.join(title_texts) if title_texts else "Untitled"
    
    print(f"   -> Title group identified: Group {title_group['group_no']}")
    print(f"   -> Font size: {title_group['font_size']}, Avg char length: {title_group['avg_char_length']:.2f}")
    print(f"   -> Title text: '{final_title}'")
    
    # Remove title group from classification list
    classified_groups = [g for g in classified_groups if g['group_no'] != title_group['group_no']]
    
    # Sort remaining groups by font size (descending) and then by group number
    classified_groups.sort(key=lambda x: (-x['font_size'], x['group_no']))
    
    # Apply hierarchical logic to remaining groups
    hierarchical_groups = []
    font_to_level_mapping = {}
    current_hierarchy_level = None
    
    print(f"   -> Applying dynamic hierarchical progression...")
    
    for group in classified_groups:
        font_size = group['font_size']
        predicted_level = group['classification']
        
        # Skip content groups for outline
        if predicted_level == 'Content':
            print(f"      Group {group['group_no']} (font {font_size}): Skipped as Content")
            continue
        
        # Check if this font size already has a level assigned
        if font_size in font_to_level_mapping:
            assigned_level = font_to_level_mapping[font_size]
            print(f"      Group {group['group_no']} (font {font_size}): Using existing mapping → {assigned_level}")
        else:
            # Dynamic hierarchy assignment based on detection order
            if current_hierarchy_level is None:
                # First valid heading group becomes H1
                assigned_level = 'H1'
                current_hierarchy_level = 'H1'
                print(f"      Group {group['group_no']} (font {font_size}): First heading → H1")
            elif current_hierarchy_level == 'H1':
                # After H1, next different font size becomes H2
                if font_size != [g['font_size'] for g in classified_groups if g['group_no'] < group['group_no'] and font_to_level_mapping.get(g['font_size']) == 'H1'][:1]:
                    assigned_level = 'H2'
                    current_hierarchy_level = 'H2'
                    print(f"      Group {group['group_no']} (font {font_size}): Next level → H2")
                else:
                    assigned_level = 'H1'  # Same font size as previous H1
                    print(f"      Group {group['group_no']} (font {font_size}): Same font as H1 → H1")
            elif current_hierarchy_level == 'H2':
                # After H2, next different font size becomes H3
                existing_h2_fonts = [fs for fs, level in font_to_level_mapping.items() if level == 'H2']
                if font_size not in existing_h2_fonts and font_size not in [fs for fs, level in font_to_level_mapping.items() if level == 'H1']:
                    assigned_level = 'H3'
                    current_hierarchy_level = 'H3'
                    print(f"      Group {group['group_no']} (font {font_size}): Next level → H3")
                else:
                    # Same font size as existing H2 or H1
                    assigned_level = font_to_level_mapping.get(font_size, 'H2')
                    print(f"      Group {group['group_no']} (font {font_size}): Existing font mapping → {assigned_level}")
            else:
                # H3 or beyond - check if font size already mapped
                if font_size in font_to_level_mapping:
                    assigned_level = font_to_level_mapping[font_size]
                else:
                    assigned_level = 'H3'  # Default to H3 for new font sizes
                print(f"      Group {group['group_no']} (font {font_size}): Default to → {assigned_level}")
            
            # Map this font size to the assigned level
            font_to_level_mapping[font_size] = assigned_level
        
        # Add all lines from this group to hierarchical groups
        for line in group['lines']:
            hierarchical_groups.append({
                'level': assigned_level,
                'text': line['text'],
                'page': line['page_no']
            })
    
    print(f"   -> Final font size to level mapping:")
    for font_size, level in sorted(font_to_level_mapping.items(), reverse=True):
        print(f"      Font size {font_size} → {level}")
    
    ## ----------------------------------------------------------------
    ## Part 4: Create Final JSON Structure and Save
    ## ----------------------------------------------------------------
    print("\n✅ Step 4: Creating final JSON structure...")
    
    # Sort by page number for final outline
    outline = sorted(hierarchical_groups, key=lambda x: x['page'])
    
    final_result = {
        "title": final_title,
        "outline": outline
    }
    
    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_result, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Results saved to '{output_file}'")
    
    print(f"\n--- Classification Summary ---")
    print(f"Title: {final_title}")
    print(f"Title identified from: Group {title_group['group_no']} (Font: {title_group['font_size']}, Avg chars: {title_group['avg_char_length']:.2f})")
    print(f"Total outline items: {len(outline)}")
    level_counts = Counter(item['level'] for item in outline)
    for level, count in level_counts.items():
        print(f"{level}: {count} items")
    
    return final_result

if __name__ == "__main__":
    # Run the hierarchical classification
    result = classify_document_hierarchical(document_data, base_path='L12', output_file='classified_document.json')
    
    print("\n--- Final Result ---")
    print(json.dumps(result, indent=2))