from pathlib import Path
import importlib.util
import json
import tempfile
import unittest
import duckdb

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("inspect_source", ROOT / "tools" / "inspect_source.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class SourceMaterialChecks(unittest.TestCase):
    def test_source_bytes_and_shape(self):
        results = module.inspect(ROOT / "data")
        self.assertTrue(results)
        self.assertTrue(all(item["rows"] > 0 for item in results))

    def test_primitive_types(self):
        schema = json.loads((ROOT / "data/schema.json").read_text(encoding="utf-8"))["datasets"]
        types = {"string": str, "integer": int, "number": (int, float), "boolean": bool,
                 "array": list, "object": dict}
        for name, item in schema.items():
            for row in map(json.loads, (ROOT / "data" / (name + ".ndjson")).read_text(encoding="utf-8").splitlines()):
                for field, kind in item["fields"].items():
                    if kind != "any":
                        self.assertIsInstance(row[field], types[kind], (name, field))
                        if kind == "integer":
                            self.assertNotIsInstance(row[field], bool)

    def test_storage_runtime_decimal_and_restart(self):
        with tempfile.TemporaryDirectory() as temp:
            path = str(Path(temp) / "probe.duckdb")
            con = duckdb.connect(path)
            con.execute("create table runtime_probe(v decimal(18,2))")
            con.execute("insert into runtime_probe values (1.25),(2.75)")
            con.close()
            con = duckdb.connect(path, read_only=True)
            self.assertEqual(str(con.execute("select sum(v) from runtime_probe").fetchone()[0]), "4.00")
            con.close()

if __name__ == "__main__":
    unittest.main()
