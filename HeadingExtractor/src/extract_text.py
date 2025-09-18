
# ok lets go 
import itertools
import json
from typing import List, Dict, Tuple, Any
from collections import defaultdict, Counter
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTTextLine, LTChar, LTAnno

def extract_text_lines_with_dominant_font(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extracts text lines from a PDF and computes dominant font properties based on words.
    """
    lines_data = []
    print(f"Processing PDF: {pdf_path}...")

    try:
        for page_num, page_layout in enumerate(extract_pages(pdf_path)):
            for element in page_layout:
                if not isinstance(element, LTTextContainer):
                    continue

                for text_line in element:
                    if not isinstance(text_line, LTTextLine):
                        continue

                    words = []
                    current_word = ""
                    current_word_fonts = []

                    for char in text_line:
                        if isinstance(char, LTChar):
                            current_word += char.get_text()
                            current_word_fonts.append((char.fontname, round(char.size, 2)))
                        elif isinstance(char, LTAnno) and char.get_text() == " ":
                            if current_word.strip():
                                words.append((current_word.strip(), current_word_fonts.copy()))
                            current_word = ""
                            current_word_fonts = []

                    if current_word.strip():
                        words.append((current_word.strip(), current_word_fonts.copy()))

                    if not words:
                        continue

                    all_fonts = [fonts[-1] for _, fonts in words if fonts]
                    font_counter = Counter(all_fonts)
                    dominant_font, _ = font_counter.most_common(1)[0]

                    line_text = " ".join(word for word, _ in words)

                    lines_data.append({
                        "page": page_num ,
                        "text": line_text,
                        "font_name": dominant_font[0],
                        "font_size": dominant_font[1],
                        "is_bold": "Bold" in dominant_font[0],
                        "fonts_per_word": [
                            {"word": word, "font": fonts[-1] if fonts else None}
                            for word, fonts in words
                        ]
                    })

        print("Successfully extracted text lines with dominant font.")
    except Exception as e:
        print(f"Error processing PDF: {e}")

    return lines_data

def group_lines_by_font_style(lines: List[Dict]) -> List[List[Dict]]:
    """
    Groups all lines that share the same font name and size together.
    """
    if not lines:
        return []

    print("Grouping all lines by font style...")

    style_groups = defaultdict(list)

    for line in lines:
        style_key = (line['font_name'], line['font_size'])
        style_groups[style_key].append(line)

    grouped_chunks = list(style_groups.values())

    print(f"Created {len(grouped_chunks)} unique font style groups.")
    for i, (style, lines_in_group) in enumerate(style_groups.items()):
        print(f"  Group {i+1}: {style} - {len(lines_in_group)} lines")

    return grouped_chunks

def save_chunks_to_json(font_chunks: List[List[Dict]], output_file: str = "pdf_font_analysis.json") -> Dict:
    """
    Saves the font chunks to a JSON file and returns the JSON object.
    """
    json_data = {
        "total_groups": len(font_chunks),
        "groups": []
    }

    print(f"Saving {len(font_chunks)} font groups to JSON...")

    for group_no, chunk in enumerate(font_chunks, 1):
        if not chunk:
            continue

        font_name = chunk[0]['font_name']
        font_size = chunk[0]['font_size']

        group_data = {
            "group_no": group_no,
            "font_name": font_name,
            "font_size": font_size,
            "total_lines": len(chunk),
            "lines": []
        }

        for line_no, line in enumerate(chunk, 1):
            line_data = {
                "line_no": line_no,
                "page_no": line['page'],
                "text": line['text'],
                "is_bold": line.get('is_bold', False)
            }
            group_data["lines"].append(line_data)

        json_data["groups"].append(group_data)

    # try:
    #     with open(output_file, 'w', encoding='utf-8') as f:
    #         json.dump(json_data, f, indent=2, ensure_ascii=False)
    #     print(f"Successfully saved font analysis to {output_file}")
    # except Exception as e:
    #     print(f"Error saving to JSON file: {e}")
    #     return json_data

    return json_data

def group_consecutive_lines_by_font(lines: List[Dict]) -> List[List[Dict]]:
    """
    Groups consecutive lines that share the same font name and size.
    """
    if not lines:
        return []

    print("Grouping consecutive lines by font style...")

    key_func = lambda line: (line['font_name'], line['font_size'])
    grouped_chunks = [list(group) for _, group in itertools.groupby(lines, key=key_func)]

    print(f"Created {len(grouped_chunks)} chunks.")
    return grouped_chunks

def main():
    """
    Main function to run the PDF processing and grouping workflow.
    """
    pdf_file_path = "..\\pdfs\The Rise of Multimodal AI.pdf"

    extracted_lines = extract_text_lines_with_dominant_font(pdf_file_path)

    font_chunks = group_lines_by_font_style(extracted_lines)

    json_output = save_chunks_to_json(font_chunks, "yas4.json")

    print("\n--- PDF FONT CHUNKS (ALL SAME STYLES GROUPED TOGETHER) ---")
    for i, chunk in enumerate(font_chunks):
        style = (chunk[0]['font_name'], chunk[0]['font_size'])
        print(f"\n[ Chunk {i+1}: Style={style}, Lines={len(chunk)} ]")
        sample_lines = chunk[:5]
        for j, line in enumerate(sample_lines):
            print(f"  Line {j+1} (Page {line['page']}): {line['text']}")
        if len(chunk) > 5:
            print(f"  ... and {len(chunk) - 5} more lines with the same style")
        print("-" * 50)

    print("\n\n--- FOR COMPARISON: CONSECUTIVE GROUPING ---")
    consecutive_chunks = group_consecutive_lines_by_font(extracted_lines)
    print(f"Consecutive grouping created {len(consecutive_chunks)} chunks")
    print("vs.")
    print(f"Style-based grouping created {len(font_chunks)} chunks")

    print(f"\n--- JSON OUTPUT SUMMARY ---")
    print(f"Total groups in JSON: {json_output['total_groups']}")
    print("Sample group structure:")
    if json_output['groups']:
        sample_group = json_output['groups'][0]
        print(f"  Group {sample_group['group_no']}: {sample_group['font_name']} ({sample_group['font_size']}pt)")
        print(f"  Contains {sample_group['total_lines']} lines")
        if sample_group['lines']:
            print(f"  First line: '{sample_group['lines'][0]['text'][:50]}...'")

if __name__ == "__main__":
    # To run this script, you need to install pdfminer.six:
    # pip install pdfminer.six
    main()






