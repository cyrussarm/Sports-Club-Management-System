import json
from pathlib import Path
from core.exceptions import StorageError

data_dir = Path("data")

def load_data(filename):
    path = data_dir/filename

    if not path.exists():        
        return []

    try:
        # Convert from JSON to Python:
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise StorageError(f"failed to load {filename}: {e}") from e

def save_data(filename, data):
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
        path = data_dir/filename
        # convert into JSON:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        raise StorageError(f"failed to save {filename}")
    

