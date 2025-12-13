import inspect
import re
import json
import hashlib
from difflib import Differ

def preprocess(prompt):
    if isinstance(prompt, str):
        return inspect.cleandoc(prompt)
    elif isinstance(prompt, list):
        for m in prompt:
            m["content"] = inspect.cleandoc(m["content"])
        return prompt
    else:
        raise ValueError(f"Invalid type: {type(prompt)}")

def normalize(text):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s([?.!,;: ])", r"\1", text)
    return text.strip()

def get_diff(before, after):
    differ = Differ()
    diff = differ.compare(before.split(), after.split())
    output = []
    for line in diff:
        if line.startswith("  "):
            output.append(line[2:])
        elif line.startswith("- "):
            output.append(f"\u001b[91m{line[2:]}\u001b[0m")
        elif line.startswith("+ "):
            output.append(f"\u001b[92m{line[2:]}\u001b[0m")
    return " ".join(output)

def hash_messages(messages):
    return hashlib.blake2b(
        json.dumps(messages, ensure_ascii=False).encode(),
        digest_size=16,
    ).hexdigest()
