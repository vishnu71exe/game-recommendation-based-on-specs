import ast
import json
from pathlib import Path

p = Path(__file__).with_name('test.json')
backup = p.with_suffix('.json.bak')

text = p.read_text(encoding='utf-8')
# Convert Python literal representation to Python object
obj = ast.literal_eval(text)

# Write backup
backup.write_text(text, encoding='utf-8')

# Dump valid JSON
p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Backed up to {backup} and wrote valid JSON to {p}')
