import os
import json

def read(fp):
    with open(fp, "r", encoding="utf-8") as f:
        return f.read().strip()

def write(data, fp):
    with open(fp, "w", encoding="utf-8") as f:
        f.write(data)

def read_messages(fp):
    with open(fp, "r", encoding="utf-8") as f:
        if fp.endswith(".json"):
            return json.load(f)
        elif fp.endswith(".jsonl"):
            return [json.loads(line) for line in f]
        else:
            raise ValueError("Unsupported file extension. Use .json or .jsonl")

def save_messages(messages, fp):
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        if fp.endswith(".json"):
            json.dump(messages, f, indent=2)
        elif fp.endswith(".jsonl"):
            for m in messages:
                f.write(json.dumps(m) + "\n")
        else:
            raise ValueError("Unsupported file extension. Use .json or .jsonl")
