# detect toc ---- and  skip everything 

# from pipeline json ------
# extract_text_lines_with_dominant_font()
# group lines by font style 
# save chnuks to json 
# group_consecutive lines by font 

# from sanitization -------
# analyze text lengths 

# from embeddigs and fuzzy ------
# semantic classification 
import os 
import json
from pathlib import Path
from src.extract_text import extract_text_lines_with_dominant_font, group_lines_by_font_style , save_chunks_to_json
from src.sanitization import analyze_text_lengths
from src.classify import classify_document_hierarchical

def load_pdfs(dir_path="input"):
    pdf_paths=[]
    for pdf in os.listdir(dir_path):
        pdf_paths.append(os.path.join(os.curdir,dir_path,pdf))
    return pdf_paths
         


if __name__ == '__main__':
    for pdf_file_path in load_pdfs():
        
        # extract data 
        extracted_lines = extract_text_lines_with_dominant_font(pdf_file_path)
        font_chunks=group_lines_by_font_style(extracted_lines)
        json_data= save_chunks_to_json(font_chunks)
        # for i, chunk in enumerate(font_chunks):
        #     style = (chunk[0]['font_name'], chunk[0]['font_size'])
        #     print(f"\n[ Chunk {i+1}: Style={style}, Lines={len(chunk)} ]")
        #     sample_lines = chunk[:5]
        #     for j, line in enumerate(sample_lines):
        #         print(f"  Line {j+1} (Page {line['page']}): {line['text']}")
        #     if len(chunk) > 5:
        #         print(f"  ... and {len(chunk) - 5} more lines with the same style")
        # print("-" * 50)
   
        # sanitise data 

        selected_groups=analyze_text_lengths(json_data)
        # print(str(selected_groups))
        # output_path="output.json"
        # with open(output_path, "w", encoding="utf-8") as f:
        #     json.dump(selected_groups, f, indent=4, ensure_ascii=False)
        # for grp in selected_groups['selected_groups']:
        #     print("Group: -------------------")
        #     for lines in grp['lines']:
        #         print("-=-=-=-=-=-=-")
        #         print(lines['text'])
        pdf_stem = Path(pdf_file_path).stem  # 'file.pdf' -> 'file'
        output_path = f"output/{pdf_stem}.json"     # => 'file.json'

        # Now save the output
        result = classify_document_hierarchical(
            selected_groups,
            base_path='embeddings',
            output_file=output_path)