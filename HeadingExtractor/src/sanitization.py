import numpy as np
import json

def analyze_text_lengths(json_data):
    """
    Analyze text lengths in JSON data and select groups based on criteria.
    
    Args:
        json_path (str): Path to the JSON file
        
    Returns:
        dict: Dictionary containing analysis results
    """
    # Load JSON data
    # with open(json_path, "r", encoding="utf-8") as f:
    #     json_data = json.load(f)
    
    # Initialize variables
    group_avg_lengths = []
    all_text_lengths = []
    selected_groups = []
    
    # Calculate average text length for each group
    for group in json_data["groups"]:
        texts = [line["text"] for line in group["lines"]]
        text_lengths = [len(t) for t in texts]
        
        group_avg_length = np.mean(text_lengths)
        group_avg_lengths.append(group_avg_length)
        all_text_lengths.extend(text_lengths)
    
    # Calculate total average text length
    total_avg_length = np.mean(all_text_lengths)
    
    # Display results
    # print(f"Total average text length: {total_avg_length:.2f}")
    # print("\nGroup average text lengths:")
    
    # Apply selection criteria
    for i, group in enumerate(json_data["groups"]):
        group_avg_length = group_avg_lengths[i]
        # print(f"Group {group['group_no']}: {group_avg_length:.2f}")
        
        if total_avg_length > group_avg_length:
            # print(f"  -> Selected (total avg {total_avg_length:.2f} > group avg {group_avg_length:.2f})")
            selected_groups.append(group)
            
            # Print the texts in this group
            # for line in group["lines"]:
            # #     print(f"    {line['text']}")
            # # print()
    
    # Summary
    # print(f"\nNumber of selected groups: {len(selected_groups)}")
    # print("Selected group numbers:", [group['group_no'] for group in selected_groups])
    
    # Return results
    return {
        'total_avg_length': total_avg_length,
        'group_avg_lengths': group_avg_lengths,
        'selected_groups': selected_groups,
        'num_selected': len(selected_groups)
    }

# def main():
#     """Main function to run the analysis."""
#     json_path = "yas4.json"
#     results = analyze_text_lengths(json_path)
#     return results

# # Run the analysis
# if __name__ == "__main__":
#     results = main()

# {
# "title": "Understanding AI",
# "outline": [
#  { "level": "H1", "text": "Introduction", "page": 1, "subsection":"this is the inro." },
#  { "level": "H2", "text": "What is AI?", "page": 2, "subsection":"this isnot  the inro."  },
#  { "level": "H3", "text": "History of AI", "page": 3 , "subsection":"this is the history." }
# ]
# }
