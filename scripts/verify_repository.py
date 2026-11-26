#!/usr/bin/env python3
"""Check the candidate inventory, SHA-256 hashes and deterministic archives."""
from hashlib import sha256
from pathlib import Path, PurePosixPath
import re
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
LEDGER = "SHA256SUMS.txt"
VISUAL_LEDGER = "visualization/SHA256SUMS.txt"
EXPLORER = "visualization/strong-extension-posterior-smoothing-explorer.zip"
EVIDENCE = "release/evidence/strong-extension-posterior-smoothing-evidence.zip"
VISUAL_FILES = ["README.md", "index.html", "render.py", "three-time-smoothing.gif"]
UNWANTED = {
    "personal path": re.compile(r"(?:/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/)"),
    "credential material": re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|xox[baprs]-[a-zA-Z0-9-]{20,}"),
    "email address": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "obsolete attribution": re.compile(r"\bG[i]a\b"),
}


def digest(data):
    return sha256(data).hexdigest()


def public_files():
    files = []
    for entry in ROOT.rglob("*"):
        name = entry.relative_to(ROOT).as_posix()
        if name.startswith((".git/", "release/evidence/")) or "__pycache__" in entry.parts:
            continue
        if entry.is_file():
            assert not entry.is_symlink(), f"Symlink: {name}"
            files.append(name)
    return sorted(files)


def ledger_entries(path):
    mapping = {}
    for row in path.read_text().splitlines():
        hexdigest, name = row.split("  ", 1)
        assert re.fullmatch(r"[a-f0-9]{64}", hexdigest), "Invalid SHA-256"
        assert name not in mapping, f"Duplicate ledger path: {name}"
        mapping[name] = hexdigest
    return mapping


def check_archive(path, expected, prefix=ROOT):
    with ZipFile(path) as archive:
        assert archive.testzip() is None
        assert sorted(archive.namelist()) == sorted(expected)
        for name in expected:
            assert not PurePosixPath(name).is_absolute() and ".." not in PurePosixPath(name).parts
            assert archive.read(name) == (prefix / name).read_bytes(), f"ZIP member differs: {name}"


def verify():
    files = public_files()
    ledger = ledger_entries(ROOT / LEDGER)
    assert sorted(ledger) == sorted(set(files) - {LEDGER}), "Ledger/inventory mismatch"
    manifest = (ROOT / "MANIFEST.md").read_text()
    assert sorted(re.findall(r"^- \x60([^\x60]+)\x60$", manifest, re.M)) == files, "Manifest/inventory mismatch"
    for name, expected in ledger.items():
        data = (ROOT / name).read_bytes()
        assert expected == digest(data), f"Hash mismatch: {name}"
        if Path(name).suffix in {".gif", ".pdf", ".zip"} or name == Path(__file__).relative_to(ROOT).as_posix():
            continue
        for category, pattern in UNWANTED.items():
            assert not pattern.search(data.decode("utf-8")), f"{category}: {name}"
    visual = ledger_entries(ROOT / VISUAL_LEDGER)
    assert sorted(visual) == sorted(VISUAL_FILES + [Path(EXPLORER).name])
    for name, expected in visual.items():
        assert expected == digest((ROOT / "visualization" / name).read_bytes()), f"Visual hash mismatch: {name}"
    check_archive(ROOT / EXPLORER, VISUAL_FILES, ROOT / "visualization")
    if (ROOT / EVIDENCE).is_file():
        check_archive(ROOT / EVIDENCE, files)
        evidence_entry = (ROOT / EVIDENCE).with_name("SHA256SUMS.txt")
        assert ledger_entries(evidence_entry) == {Path(EVIDENCE).name: digest((ROOT / EVIDENCE).read_bytes())}
    print(f"PASS: {len(files)} candidate files, text privacy, and archive member bytes")


def write_zip(path, files, prefix=ROOT):
    with ZipFile(path, "w", ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(files):
            info = ZipInfo(name, (2026, 11, 27, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (prefix / name).read_bytes(), compresslevel=9)


def write_ledgers():
    write_zip(ROOT / EXPLORER, VISUAL_FILES, ROOT / "visualization")
    visual_names = sorted(VISUAL_FILES + [Path(EXPLORER).name])
    (ROOT / VISUAL_LEDGER).write_text("".join(
        f"{digest((ROOT / 'visualization' / name).read_bytes())}  {name}\n"
        for name in visual_names), encoding="utf-8")
    files = sorted(set(public_files()) | {"MANIFEST.md", LEDGER})
    (ROOT / "MANIFEST.md").write_text("# Candidate inventory\n\n" + "".join(
        f"- \x60{name}\x60\n" for name in files), encoding="utf-8")
    (ROOT / LEDGER).write_text("".join(
        f"{digest((ROOT / name).read_bytes())}  {name}\n" for name in files if name != LEDGER),
        encoding="utf-8")
    evidence_path = ROOT / EVIDENCE
    evidence_path.parent.mkdir(exist_ok=True)
    write_zip(evidence_path, files)
    evidence_path.with_name("SHA256SUMS.txt").write_text(
        f"{digest(evidence_path.read_bytes())}  {evidence_path.name}\n", encoding="utf-8")


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["--stage"]:
        write_ledgers()
    elif sys.argv[1:]:
        raise SystemExit("Usage: verify_repository.py [--stage]")
    verify()
