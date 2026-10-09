"""Scan site prose for the AI tells listed in the humanizer skill.

Reports candidates for review. Judgement stays with the writer: some hits are
legitimate (a technical "robust", a real triad). Usage: python3 scripts/humanizer_scan.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGETS = sorted((ROOT / "content").rglob("*.md")) + sorted((ROOT / "data").rglob("*.yaml"))

PATTERNS = [
    ("1 not-X-but-Y", r"\bnot (just|only|merely|simply)\b|\bit'?s not .{1,40}, it'?s\b|\brather than\b"),
    ("2 closer/fragment", r"(?m)^(That is the real|That distinction|Read that again|Let that sink in)"),
    ("3 deep saying", r"\b(the real question is|at its core|in reality|what really matters|fundamentally|the deeper issue|the heart of the matter|the language of|the currency of|the architecture of)\b"),
    ("4 staged run-up", r"\b(let'?s dive|let'?s explore|let'?s break this down|here'?s what you need to know|without further ado|here'?s the thing|the thing is|let'?s be honest|real talk)\b"),
    ("5 arguing with no one", r"\b(i'?m not saying|to be clear|don'?t get me wrong|this is not to say|some might say|a tempting approach|one might be tempted|you might think)\b"),
    ("8 dash/arrow", r"[—–→]"),
    ("9 stacked qualifier", r"\b(to be fair|it'?s also possible|could potentially|might arguably|in some cases it may)\b"),
    ("12 AI words", r"\b(additionally|bolstered|crucial|deep dive|delve|enduring|enhance[sd]?|garner|highlight(s|ing|ed)?|interplay|intricate|intricacies|meticulous(ly)?|pivotal|showcas(e|es|ing)|tapestry|testament|underscore[sd]?|vibrant)\b"),
    ("13 inflated", r"\b(stands as a testament|a pivotal|plays a key role|underscores its importance|reflects a broader|lasting legacy|setting the stage|evolving landscape|indelible mark|the future looks bright|step in the right direction)\b"),
    ("14 vague link", r"\b(associated with|in association with|in connection with|linked to|tied to)\b"),
    ("15 -ing rider", r", (highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|contributing to|cultivating|fostering|encompassing|showcasing)\b"),
    ("16 sales language", r"\b(profound|exemplifies|commitment to|nestled|in the heart of|groundbreaking|renowned|diverse array|breathtaking|must-visit|stunning|seamless(ly)?|cutting-edge|state-of-the-art|powerful|leverage[sd]?)\b"),
    ("17 borrowed authority", r"\b(experts (argue|believe|say)|observers have cited|industry reports|some critics)\b"),
    ("18 avoiding is/are/has", r"\b(serves as|stands as|functions as|operates as|boasts)\b"),
    ("21 curly quotes", r"[“”‘’]"),
]

SKIP_BLOCK = re.compile(r"^---$.*?^---$|^```.*?^```", re.S | re.M)
INLINE = re.compile(r"`[^`]*`|\{\{<.*?>\}\}|\]\([^)]*\)|https?://\S+")


def prose(text):
    text = SKIP_BLOCK.sub(lambda m: "\n" * m.group().count("\n"), text)
    return INLINE.sub(" ", text)


def main():
    hits = 0
    for path in TARGETS:
        body = prose(path.read_text(encoding="utf-8"))
        for line_no, line in enumerate(body.split("\n"), 1):
            for name, pat in PATTERNS:
                for m in re.finditer(pat, line, re.I):
                    hits += 1
                    print(f"{path.relative_to(ROOT)}:{line_no}  [{name}]  {m.group()!r}")
                    print(f"    {line.strip()[:150]}")
    print(f"\n{hits} candidate(s) for review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
