"""Offline package-contract checks. These do not measure agent behavior."""

import hashlib
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = {
    ".gitignore", "LICENSE", "NOTICE.md", "README.md", "SKILL.md", "sources.json",
    "references/cac-notation.md", "references/cac-codex.md",
    "references/cac-authoring-contract.md",
    "third_party/generic-devteam/LICENSE",
    "tests/test_package.py",
}
FRONTMATTER_KEYS = {
    "name", "description", "version", "author", "license", "platforms", "metadata",
}
PRIVATE_PATH = re.compile(r"/(?:home|Users)/[^\s`\"']+")
REFERENCE = re.compile(r"references/[A-Za-z0-9._/-]+\.md")


class FrontmatterError(ValueError):
    """Raised when the frontmatter is not a mapping this package accepts."""


def _scalar(raw, line_number):
    value = raw.strip()
    if not value:
        raise FrontmatterError(f"empty value on line {line_number}")
    if value[0] in "\"'":
        if len(value) < 2 or value[-1] != value[0]:
            raise FrontmatterError(f"unterminated quote on line {line_number}")
        return value[1:-1]
    if value[0] == "[":
        if not value.endswith("]"):
            raise FrontmatterError(f"unterminated list on line {line_number}")
        items = [item.strip() for item in value[1:-1].split(",")]
        if any(not item for item in items):
            raise FrontmatterError(f"empty list item on line {line_number}")
        if any(item[0] in "\"'" for item in items):
            raise FrontmatterError(f"quoted list item on line {line_number}")
        return items
    if value[0] in "{|>":
        raise FrontmatterError(f"unsupported value on line {line_number}")
    return value


def parse_frontmatter(text):
    """Parse the skill frontmatter subset: scalars, inline lists, nested mappings.

    Strict on purpose: odd indentation, duplicates, and unterminated values
    raise instead of being guessed. PyYAML cross-checks this when installed.
    """
    if not text.startswith("---\n"):
        raise FrontmatterError("missing opening delimiter")
    try:
        header, body = text[4:].split("\n---\n", 1)
    except ValueError as error:
        raise FrontmatterError("missing closing delimiter") from error
    if not body.strip():
        raise FrontmatterError("missing body")

    root = {}
    stack = []
    for number, line in enumerate(header.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line:
            raise FrontmatterError(f"tab indentation on line {number}")
        indent = len(line) - len(line.lstrip(" "))
        if indent % 2:
            raise FrontmatterError(f"unsupported indentation on line {number}")
        key, separator, rest = line.strip().partition(":")
        if not separator or not key.strip() or " " in key.strip():
            raise FrontmatterError(f"not a mapping entry on line {number}")

        while stack and stack[-1][0] >= indent:
            stack.pop()
        if indent and not stack:
            raise FrontmatterError(f"indented entry without parent on line {number}")
        container = stack[-1][1] if stack else root
        key = key.strip()
        if key in container:
            raise FrontmatterError(f"duplicate key {key}")
        if rest.strip():
            container[key] = _scalar(rest, number)
        else:
            container[key] = {}
            stack.append((indent, container[key]))
    return root, body.lstrip("\n")


def read_frontmatter(root):
    data, body = parse_frontmatter((root / "SKILL.md").read_text(encoding="utf-8"))
    return data, body


def validate_skill(root):
    data, body = read_frontmatter(root)
    assert set(data) == FRONTMATTER_KEYS, f"frontmatter keys: {sorted(data)}"
    assert data["name"] == "cac", "skill name"
    assert data["version"] == "1.0.0", "skill version"
    assert data["license"] == "MIT", "skill license"
    assert data["description"].startswith("Use when "), "description trigger"
    assert data["description"].endswith("."), "description punctuation"
    assert len(data["description"]) <= 60, "description length"

    hermes = data["metadata"].get("hermes")
    assert isinstance(hermes, dict), "metadata.hermes mapping"
    assert isinstance(hermes["tags"], list) and hermes["tags"], "tags list"
    assert all(re.fullmatch(r"[a-z0-9-]+", tag) for tag in hermes["tags"]), "tag form"
    assert isinstance(hermes["related_skills"], list), "related_skills list"

    for clause in (
        "on every invocation", "references/cac-notation.md",
        "references/cac-codex.md", "references/cac-authoring-contract.md",
        "missing or unreadable", "no roles, permissions", "recipient's language",
        "MUST", "not format source code",
    ):
        assert clause in body, f"missing skill contract: {clause}"

    referenced = set(REFERENCE.findall(body))
    shipped = {f"references/{path.name}" for path in (root / "references").glob("*.md")}
    assert referenced == shipped, f"reference coverage: {sorted(referenced ^ shipped)}"
    for relative in sorted(referenced):
        path = root / relative
        assert path.is_file(), f"missing referenced file: {relative}"
        assert "**Provenance.**" in path.read_text(encoding="utf-8"), f"provenance notice: {relative}"
    return data


def validate_sources(root):
    sources = json.loads((root / "sources.json").read_text(encoding="utf-8"))
    assert sources["package_version"] == "1.0.0", "source version"
    entry = sources["cac"]
    assert entry["repository"] == "https://github.com/ataian/generic-devteam", "source repository"
    assert re.fullmatch(r"[0-9a-f]{40}", entry["repository_revision"]), "source revision"
    assert re.fullmatch(r"[0-9a-f]{40}", entry["last_source_change_revision"]), "change revision"

    files = entry["source_files"]
    assert {item["source_path"] for item in files} == {
        "docs/cac/CAC-HERMES.md", "docs/cac/CAC-CODEX.md", "references/cac-authoring.md",
    }, "source file coverage"
    for item in files:
        assert re.fullmatch(r"[0-9a-f]{64}", item["source_sha256"]), "source hash form"
        assert re.fullmatch(r"[0-9a-f]{64}", item["packaged_sha256"]), "packaged hash form"
        assert item["local_path"] in PUBLIC_FILES, "undeclared destination"
        assert item["adaptations"], "missing adaptations"
        actual = hashlib.sha256((root / item["local_path"]).read_bytes()).hexdigest()
        assert actual == item["packaged_sha256"], f"packaged bytes changed: {item['local_path']}"
        notice = (root / item["local_path"]).read_text(encoding="utf-8")
        assert item["source_path"] in notice, f"unattributed source: {item['local_path']}"

    assert entry["adaptations"], "missing package adaptations"
    assert entry["decision_record"]["hashed"] is False, "decision record hashing claim"

    for item in sources["upstream_files"]:
        assert item["local_path"] in PUBLIC_FILES, "undeclared upstream destination"
        actual = hashlib.sha256((root / item["local_path"]).read_bytes()).hexdigest()
        assert actual == item["sha256"], f"upstream bytes changed: {item['local_path']}"
    return sources


def validate_package(root):
    """Validate declared contents, links, checksums, and provenance."""
    root = root.resolve()
    for relative in sorted(PUBLIC_FILES):
        path = root / relative
        assert path.is_file(), f"missing public file: {relative}"
        assert not path.is_symlink(), f"symlink: {relative}"
        assert path.resolve().is_relative_to(root), f"escaping path: {relative}"

    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        text = path.read_bytes().decode("utf-8", errors="replace")
        assert not PRIVATE_PATH.search(text), f"private path: {path.relative_to(root)}"

    validate_skill(root)
    sources = validate_sources(root)

    for relative in sorted(PUBLIC_FILES):
        if not relative.endswith(".md"):
            continue
        text = (root / relative).read_text(encoding="utf-8")
        for destination in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
            link = urlsplit(destination)
            if link.scheme or link.netloc:
                continue
            linked = ((root / relative).parent / unquote(link.path)).resolve()
            assert linked.is_relative_to(root), f"escaping link: {relative}: {destination}"
            assert linked.is_file(), f"missing local link: {relative}: {destination}"
            if link.fragment:
                headings = re.findall(r"^#+\s+(.+)$", linked.read_text(encoding="utf-8"), re.MULTILINE)
                anchors = {re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in headings}
                assert unquote(link.fragment) in anchors, f"missing anchor: {destination}"

    readme = (root / "README.md").read_text(encoding="utf-8")
    notice = (root / "NOTICE.md").read_text(encoding="utf-8")
    for document, clauses in {
        readme: ("needs no Maker", "TAS", "Caveman", "writing and representation"),
        notice: ("Relation to TAS", "Relation to Caveman", "no activation"),
    }.items():
        for clause in clauses:
            assert clause in document, f"missing scope statement: {clause}"
    assert sources["cac"]["unverified"], "missing unverified claims"
    return True


class PackageTests(unittest.TestCase):
    def copy_package(self):
        temporary = tempfile.TemporaryDirectory(prefix="cac-package-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        for relative in PUBLIC_FILES:
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)
        return root

    def test_package_contract(self):
        self.assertTrue(validate_package(ROOT))

    def test_relocated_package_needs_no_maker_or_network(self):
        self.assertTrue(validate_package(self.copy_package()))

    def test_frontmatter_parses_to_mapping(self):
        data, body = read_frontmatter(ROOT)
        self.assertEqual(data["name"], "cac")
        self.assertEqual(data["platforms"], ["linux", "macos", "windows"])
        self.assertEqual(data["metadata"]["hermes"]["related_skills"], ["tas"])
        self.assertTrue(body.startswith("# CAC"))

    def test_frontmatter_parses_with_pyyaml_when_available(self):
        try:
            import yaml
        except ModuleNotFoundError:
            self.skipTest("PyYAML not installed; the built-in subset parser is authoritative")
        header = (ROOT / "SKILL.md").read_text(encoding="utf-8")[4:].split("\n---\n", 1)[0]
        parsed = yaml.safe_load(header)
        self.assertEqual(parsed["name"], "cac")
        self.assertEqual(parsed["metadata"]["hermes"]["related_skills"], ["tas"])

    def test_unterminated_frontmatter_value_is_rejected(self):
        root = self.copy_package()
        path = root / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "version: 1.0.0", "version: \"1.0.0"), encoding="utf-8")
        with self.assertRaisesRegex(FrontmatterError, "unterminated quote"):
            read_frontmatter(root)

    def test_missing_body_is_rejected(self):
        with self.assertRaisesRegex(FrontmatterError, "missing body"):
            parse_frontmatter("---\nname: cac\n---\n")

    def test_overlong_description_is_rejected(self):
        root = self.copy_package()
        path = root / "SKILL.md"
        text = path.read_text(encoding="utf-8").replace(
            "description: Use when writing or compressing agent text in CAC.",
            "description: Use when writing, rewriting, compressing, or reviewing any agent text in CAC.",
        )
        path.write_text(text, encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "description length"):
            validate_skill(root)

    def test_missing_referenced_file_is_rejected(self):
        root = self.copy_package()
        (root / "references/cac-codex.md").unlink()
        with self.assertRaisesRegex(AssertionError, "missing public file"):
            validate_package(root)

    def test_unreferenced_reference_is_rejected(self):
        root = self.copy_package()
        extra = root / "references/cac-extra.md"
        extra.write_text("# Extra\n\n**Provenance.** none\n", encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "reference coverage"):
            validate_package(root)

    def test_changed_reference_is_rejected(self):
        root = self.copy_package()
        path = root / "references/cac-notation.md"
        path.write_bytes(path.read_bytes() + b"\nchanged\n")
        with self.assertRaisesRegex(AssertionError, "packaged bytes changed"):
            validate_package(root)

    def test_changed_upstream_license_is_rejected(self):
        root = self.copy_package()
        path = root / "third_party/generic-devteam/LICENSE"
        path.write_bytes(path.read_bytes() + b"\nchanged\n")
        with self.assertRaisesRegex(AssertionError, "upstream bytes changed"):
            validate_package(root)

    def test_private_path_is_rejected(self):
        root = self.copy_package()
        path = root / "README.md"
        # Built at runtime so this repository contains no absolute machine path.
        example = "/" + "home/example/notes.md"
        path.write_text(path.read_text(encoding="utf-8") + f"\nSee {example}.\n",
                        encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "private path"):
            validate_package(root)

    def test_missing_provenance_notice_is_rejected(self):
        root = self.copy_package()
        path = root / "references/cac-codex.md"
        path.write_text(path.read_text(encoding="utf-8").replace("**Provenance.**", "Note."),
                        encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "provenance notice"):
            validate_skill(root)

    def test_escaping_link_is_rejected(self):
        root = self.copy_package()
        path = root / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n[Escape](../../outside.md)\n",
                        encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "escaping link"):
            validate_package(root)

    def test_removed_loading_instruction_is_rejected(self):
        root = self.copy_package()
        path = root / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace(
            "on every invocation", "when convenient"), encoding="utf-8")
        with self.assertRaisesRegex(AssertionError, "missing skill contract"):
            validate_skill(root)


if __name__ == "__main__":
    unittest.main()
