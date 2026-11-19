from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def inspect(directory):
    schema = json.loads((directory / "schema.json").read_text(encoding="utf-8"))
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    result = []
    for entry in manifest["files"]:
        path = directory / entry["path"]
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise ValueError("资料哈希不符：" + entry["path"])
        rows = [json.loads(line) for line in data.decode("utf-8").splitlines() if line.strip()]
        fields = schema["datasets"][entry["dataset"]]["fields"]
        if len(rows) != entry["rows"]:
            raise ValueError("资料行数不符：" + entry["path"])
        for index, row in enumerate(rows, 1):
            if set(row) != set(fields):
                raise ValueError("字段不符：" + entry["path"] + ":" + str(index))
        result.append({"dataset": entry["dataset"], "rows": len(rows), "sha256": entry["sha256"]})
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="检查原始资料的完整性，不生成业务事实。")
    parser.add_argument("directory", nargs="?", type=Path, default=ROOT / "data")
    args = parser.parse_args()
    print(json.dumps({"datasets": inspect(args.directory)}, ensure_ascii=False, indent=2))
