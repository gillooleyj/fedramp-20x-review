"""Run: python -m unittest discover -s tests"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import diff_rules  # noqa: E402
import fr_rules  # noqa: E402

DATA = fr_rules.load(ROOT / "vendor/rules/fedramp-consolidated-rules.json")


class ResolveTests(unittest.TestCase):
    def test_class_a_ksis_come_only_from_overlay(self):
        a = fr_rules.resolve(DATA, "a")
        overlay = {i for i, r in fr_rules.overlay_ids(DATA).items() if i.startswith("KSI-")}
        self.assertEqual({k["id"] for k in a["ksis"]}, overlay)

    def test_class_c_has_every_ksi(self):
        c = fr_rules.resolve(DATA, "c")
        total = sum(len(t["indicators"]) for t in DATA["KSI"].values())
        self.assertEqual(len(c["ksis"]), total)

    def test_class_b_optional_prefix_detected(self):
        b = fr_rules.resolve(DATA, "b")
        for k in b["ksis"]:
            self.assertEqual(k["optional"], k["statement"].startswith("**Optional:**"))

    def test_no_invented_variants(self):
        for c in fr_rules.CLASSES:
            for r in fr_rules.resolve(DATA, c)["rules"]:
                if ".varies_by_class." in r["json_path"]:
                    self.assertTrue(r["json_path"].endswith(f".varies_by_class.{c}"))

    def test_overlay_keeps_negative_polarity(self):
        a = {r["id"]: r for r in fr_rules.resolve(DATA, "a")["rules"]}
        if "FRC-CSO-POP" in a:
            self.assertEqual(a["FRC-CSO-POP"]["force"], "MUST NOT")


class DiffTests(unittest.TestCase):
    def mutate(self, fn):
        new = copy.deepcopy(DATA)
        fn(new)
        return diff_rules.diff(DATA, new)

    def test_identical_has_no_changes(self):
        d = diff_rules.diff(DATA, copy.deepcopy(DATA))
        self.assertEqual(d["entries"], [])

    def test_force_change_is_high_and_changes_applicability(self):
        def f(n):
            e = n["FRR"]["SDR"]["data"]["20x"]["CSX"]["SDR-CSX-KMT"]["varies_by_class"]["b"]
            e["force"] = "MUST"
        d = self.mutate(f)
        self.assertIn("SDR-CSX-KMT", d["summary"]["high"])
        self.assertEqual(d["applicability"]["b"]["force_changed"][0]["new"], "MUST")

    def test_removed_rule_detected(self):
        d = self.mutate(lambda n: n["FRR"]["AFC"]["data"]["all"]["CSO"].pop("AFC-CSO-INB"))
        self.assertIn("AFC-CSO-INB", d["summary"]["high"])
        self.assertIn("AFC-CSO-INB", d["applicability"]["a"]["removed"])

    def test_overlay_change_is_high(self):
        def f(n):
            n["FRR"]["FRC"]["data"]["all"]["CLA"]["FRC-CLA-MFR"]["following_information"].pop()
        d = self.mutate(f)
        self.assertIn("FRC-CLA-MFR", d["summary"]["high"])
        self.assertTrue(d["applicability"]["a"]["removed"])

    def test_content_change_without_updated_entry_is_flagged(self):
        def f(n):
            n["FRR"]["AFC"]["data"]["all"]["CSO"]["AFC-CSO-INB"]["statement"] += " Edited."
        d = self.mutate(f)
        fields = [x["field"] for e in d["entries"] if e["id"] == "AFC-CSO-INB" for x in e["changes"]]
        self.assertIn("updated_not_recorded", fields)

    def test_optional_prefix_change_is_high(self):
        def f(n):
            v = n["KSI"]["CNA"]["indicators"]["KSI-CNA-EIS"]["varies_by_class"]["b"]
            v["statement"] = v["statement"].replace("**Optional:** ", "")
        d = self.mutate(f)
        self.assertIn("KSI-CNA-EIS", d["summary"]["high"])
        self.assertIn("KSI-CNA-EIS", d["applicability"]["b"]["optional_changed"])


class ExtractTests(unittest.TestCase):
    def test_extract_validates(self):
        import jsonschema
        x = json.loads((ROOT / "data/rules-extract.json").read_text())
        jsonschema.Draft202012Validator(fr_rules.load(ROOT / "data/rules-extract.schema.json")).validate(x)
        self.assertEqual(x["source"]["version"], DATA["info"]["version"])


if __name__ == "__main__":
    unittest.main()
