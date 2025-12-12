from pathlib import Path
import gzip
import json
import csv
import configparser


def read_text_file(path: str) -> str:
    p = Path(path)
    if p.suffix == ".gz":
        return gzip.decompress(p.read_bytes()).decode("utf-8")
    return p.read_text(encoding="utf-8")


def write_json(path: str, data):
    """Write JSON data, appending to existing file if it exists."""
    path_obj = Path(path)
    existing_data = {}
    if path_obj.exists():
        try:
            existing_content = path_obj.read_text(encoding="utf-8")
            if existing_content.strip():
                existing_data = json.loads(existing_content)
        except (json.JSONDecodeError, ValueError):
            existing_data = {}
    
    # Merge new data with existing data
    for key, value in data.items():
        if key in existing_data:
            # If both are lists, combine them (remove duplicates)
            if isinstance(existing_data[key], list) and isinstance(value, list):
                combined = list(existing_data[key])
                for item in value:
                    if item not in combined:
                        combined.append(item)
                existing_data[key] = sorted(combined) if all(isinstance(x, (str, int, float)) for x in combined) else combined
            # If both are dicts, merge them
            elif isinstance(existing_data[key], dict) and isinstance(value, dict):
                for k, v in value.items():
                    existing_data[key][k] = existing_data[key].get(k, 0) + v if isinstance(v, (int, float)) else v
                existing_data[key] = dict(sorted(existing_data[key].items()))
            else:
                existing_data[key] = value
        else:
            existing_data[key] = value
    
    path_obj.write_text(json.dumps(existing_data, indent=4), encoding="utf-8")


def write_csv(path: str, data_dict: dict):
    """Write CSV data, appending to existing file if it exists."""
    path_obj = Path(path)
    existing_data = {}
    file_exists = path_obj.exists()
    
    # Read existing data if file exists
    if file_exists:
        try:
            with open(path, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                for row in reader:
                    if len(row) >= 2:
                        existing_data[row[0]] = int(row[1]) if row[1].isdigit() else row[1]
        except (ValueError, IndexError):
            existing_data = {}
    
    # Merge new data with existing
    for word, count in data_dict.items():
        existing_data[word] = existing_data.get(word, 0) + count if isinstance(count, (int, float)) else count
    
    # Write merged data
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "count"])
        for word, count in sorted(existing_data.items()):
            writer.writerow([word, count])


def load_config_stopwords(config_path: str = "config.ini") -> list[str]:
    """
    Read stopwords from a simple INI file under [stopwords] words=...
    Returns a lower-cased list; missing file results in empty list.
    """
    parser = configparser.ConfigParser()
    if not Path(config_path).exists():
        return []
    parser.read(config_path, encoding="utf-8")
    if "stopwords" not in parser:
        return []
    raw = parser["stopwords"].get("words", "")
    entries = []
    for chunk in raw.replace("\n", ",").split(","):
        token = chunk.strip().lower()
        if token:
            entries.append(token)
    return entries
