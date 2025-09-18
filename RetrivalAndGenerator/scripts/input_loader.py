import os
import glob
import json
from pathlib import Path
from typing import List, Dict, Tuple
INPUT_DOCUMENTS=[]
processing_timestamp=None
def find_all_collections(base_path: str = "./input") -> List[Path]:
    """Find all directories with a challenge1b_input.json"""
    pattern = os.path.join(base_path, "Collection */challenge1b_input.json")
    return [Path(p).parent for p in glob.glob(pattern)]

def load_input_json(collection_dir: Path) -> Dict:
    """Load challenge1b_input.json from the given collection"""
    input_json_path = collection_dir / "challenge1b_input.json"
    with open(input_json_path, "r") as f:
        data=json.load(f)
        return data

def get_required_pdfs(collection_dir: Path, input_data: Dict) -> List[Path]:
    """Get the list of required PDF paths as per input JSON"""
    pdf_dir = collection_dir / "PDFs"
    filenames = [doc["filename"] for doc in input_data.get("documents", [])]
    INPUT_DOCUMENTS.append(filenames)
    return [pdf_dir / fname for fname in filenames if (pdf_dir / fname).exists()]

def traverse_and_load_inputs(base_path: str = "./input") -> List[Tuple[Path, Dict, List[Path]]]:
    """Main traversal logic"""
    all_data = []
    collections = find_all_collections(base_path)
    for collection_dir in collections:
        print(collections)
        input_json = load_input_json(collection_dir)
        pdf_paths = get_required_pdfs(collection_dir, input_json)
        all_data.append((collection_dir, input_json, pdf_paths))
    return all_data
