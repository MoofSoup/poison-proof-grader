# this script gets the data stored in /dataset, and ingests it into weaviate
import os
from pathlib import Path
import pprint

def load_chunked_prompts(base_dir: str) -> list[dict]:
    """
    load chunked prompts from directory.
    returns list of dicts with
    content
    is poisoned flag
    tag_name
    use_case
    """
    prompts = []

    # get all files that start with chunk
    for file_path in Path(base_dir).glob('chunk-*'):
        tag_name = file_path.stem
        # determine if poisoned from file name
        is_poisoned = "poison" in tag_name.lower()

        #read content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        prompt_data = {
            "content": content,
            "is_poisoned": is_poisoned,
            "tag_name": tag_name,
            "use_case": "auto_grader",
        }
        prompts.append(prompt_data)
    
    return prompts
if __name__ == "__main__":
    chunks_data = load_chunked_prompts()
    pp = pprint.PrettyPrinter(indent=2)
    print("Loaded chunks:")
    pp.pprint(chunks_data)