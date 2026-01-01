#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import logging
import os
from pathlib import Path
import sys
from typing import Iterable


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class Frontmatter:
    """Parsed skill frontmatter metadata."""

    name: str | None
    description: str | None


@dataclass(frozen=True)
class CodexPaths:
    """Resolved paths used by the CLI."""

    home_dir: Path
    superpowers_skills_dir: Path
    personal_skills_dir: Path
    local_skills_dir: Path
    bootstrap_file: Path
    superpowers_repo_dir: Path


def _home_dir() -> Path:
    LOGGER.debug("Resolving home directory")
    home = Path(os.environ.get("HOME", str(Path.home())))
    LOGGER.debug("Resolved home directory to %s", home)
    return home


def _paths() -> CodexPaths:
    LOGGER.debug("Resolving CLI paths")
    home_dir = _home_dir()
    local_dir = Path.cwd()
    superpowers_repo_dir = home_dir / ".codex" / "superpowers"
    paths = CodexPaths(
        home_dir=home_dir,
        superpowers_skills_dir=superpowers_repo_dir / "skills",
        personal_skills_dir=home_dir / ".codex" / "skills",
        local_skills_dir=local_dir / ".codex" / "skills",
        bootstrap_file=superpowers_repo_dir / ".codex" / "superpowers-bootstrap.md",
        superpowers_repo_dir=superpowers_repo_dir,
    )
    LOGGER.debug("Resolved CLI paths")
    return paths


def extract_frontmatter(skill_file: Path) -> Frontmatter:
    """Extract frontmatter name/description from a SKILL.md file."""
    LOGGER.debug("Extracting frontmatter from %s", skill_file)
    content = skill_file.read_text(encoding="utf-8")
    frontmatter = _extract_frontmatter_from_text(content)
    LOGGER.debug("Extracted frontmatter from %s", skill_file)
    return frontmatter


def _extract_frontmatter_from_text(content: str) -> Frontmatter:
    LOGGER.debug("Parsing frontmatter text")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        frontmatter = Frontmatter(name=None, description=None)
        LOGGER.debug("No frontmatter detected")
        return frontmatter

    name = None
    description = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key == "name":
            name = value or None
        elif key == "description":
            description = value or None
    frontmatter = Frontmatter(name=name, description=description)
    LOGGER.debug("Parsed frontmatter values")
    return frontmatter


def strip_frontmatter(content: str) -> str:
    """Strip YAML frontmatter from a SKILL.md file."""
    LOGGER.debug("Stripping frontmatter")
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        LOGGER.debug("No frontmatter to strip")
        return content
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            stripped = "".join(lines[index + 1:])
            LOGGER.debug("Stripped frontmatter block")
            return stripped
    LOGGER.debug("Incomplete frontmatter, returning original content")
    return content


def _read_ref(git_dir: Path, ref: str) -> str | None:
    LOGGER.debug("Reading git ref %s", ref)
    ref_file = git_dir / ref
    if ref_file.exists():
        value = ref_file.read_text(encoding="utf-8").strip()
        LOGGER.debug("Resolved git ref %s", ref)
        return value
    packed_refs = git_dir / "packed-refs"
    if packed_refs.exists():
        for line in packed_refs.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#") or line.startswith("^"):
                continue
            try:
                commit, ref_name = line.split(" ", 1)
            except ValueError:
                continue
            if ref_name.strip() == ref:
                value = commit.strip()
                LOGGER.debug("Resolved git ref %s from packed-refs", ref)
                return value
    LOGGER.debug("Git ref %s not found", ref)
    return None


def check_for_updates(superpowers_repo_dir: Path) -> bool:
    """Return True when origin differs from local HEAD."""
    LOGGER.debug("Checking for updates in %s", superpowers_repo_dir)
    git_dir = superpowers_repo_dir / ".git"
    if not git_dir.exists():
        LOGGER.debug("No git directory detected")
        return False

    head_ref = _read_ref(git_dir, "HEAD")
    if head_ref is None:
        LOGGER.debug("HEAD ref missing")
        return False
    if head_ref.startswith("ref:"):
        head_ref = head_ref.split(":", 1)[1].strip()
    head_commit = _read_ref(git_dir, head_ref)
    if head_commit is None:
        LOGGER.debug("HEAD commit missing")
        return False

    origin_head = _read_ref(git_dir, "refs/remotes/origin/HEAD")
    if origin_head is None and head_ref.startswith("refs/heads/"):
        origin_head = _read_ref(
            git_dir, f"refs/remotes/origin/{head_ref.split('/')[-1]}")
    if origin_head is None:
        LOGGER.debug("Origin head missing")
        return False
    if origin_head.startswith("ref:"):
        origin_head = origin_head.split(":", 1)[1].strip()
        origin_head = _read_ref(git_dir, origin_head)
    if origin_head is None:
        LOGGER.debug("Origin commit missing")
        return False
    has_update = origin_head != head_commit
    LOGGER.debug("Update status: %s", has_update)
    return has_update


def _find_skills_in_dir(base_dir: Path, max_depth: int) -> list[Path]:
    LOGGER.debug("Finding skills in %s (depth=%s)", base_dir, max_depth)
    if not base_dir.exists():
        LOGGER.debug("Skills base directory missing: %s", base_dir)
        return []

    matches: list[Path] = []
    for root, dirs, files in os.walk(base_dir):
        rel = Path(root).relative_to(base_dir)
        depth = 0 if rel == Path(".") else len(rel.parts)
        if depth > max_depth:
            dirs[:] = []
            continue
        if "SKILL.md" in files:
            matches.append(Path(root))
    sorted_matches = sorted(matches, key=lambda path: path.as_posix())
    LOGGER.debug("Found %s skills in %s", len(sorted_matches), base_dir)
    return sorted_matches


def _print_skill(skill_path: Path, source_type: str, paths: CodexPaths) -> None:
    LOGGER.debug("Printing skill from %s (%s)", skill_path, source_type)
    skill_file = skill_path / "SKILL.md"
    if source_type == "personal":
        rel_path = skill_path.relative_to(paths.personal_skills_dir).as_posix()
        print(rel_path)
    elif source_type == "local":
        rel_path = skill_path.relative_to(paths.local_skills_dir).as_posix()
        print(rel_path)
    else:
        rel_path = skill_path.relative_to(
            paths.superpowers_skills_dir).as_posix()
        print(f"superpowers:{rel_path}")

    frontmatter = extract_frontmatter(skill_file)
    if frontmatter.description:
        print(f"  {frontmatter.description}")
    print("")
    LOGGER.debug("Printed skill from %s", skill_path)


def run_find_skills() -> None:
    """List available skills from personal and superpowers directories."""
    LOGGER.debug("Running find-skills")
    paths = _paths()
    print("Available skills:")
    print("==================")
    print("")

    found_skills: set[str] = set()

    for skill in _find_skills_in_dir(paths.local_skills_dir, max_depth=2):
        rel_path = skill.relative_to(paths.local_skills_dir).as_posix()
        found_skills.add(rel_path)
        _print_skill(skill, "local", paths)

    for skill in _find_skills_in_dir(paths.personal_skills_dir, max_depth=2):
        rel_path = skill.relative_to(paths.personal_skills_dir).as_posix()
        found_skills.add(rel_path)
        _print_skill(skill, "personal", paths)

    for skill in _find_skills_in_dir(paths.superpowers_skills_dir, max_depth=1):
        rel_path = skill.relative_to(paths.superpowers_skills_dir).as_posix()
        if rel_path not in found_skills:
            _print_skill(skill, "superpowers", paths)

    print("Usage:")
    print("  superpowers-codex use-skill <skill-name>   # Load a specific skill")
    print("")
    print("Skill naming:")
    print("  Superpowers skills: superpowers:skill-name (from ~/.codex/superpowers/skills/)")
    print("  Personal skills: skill-name (from ~/.codex/skills/)")
    print("  Local skills: skill-name (from ./.codex/skills/)")
    print("  Personal skills override superpowers skills when names match.")
    print("")
    print("Note: All skills are disclosed at session start via bootstrap.")
    LOGGER.debug("Completed find-skills")


def run_bootstrap() -> None:
    """Run the bootstrap flow that prints skills and auto-loads using-superpowers."""
    LOGGER.debug("Running bootstrap")
    paths = _paths()
    print("# Superpowers Bootstrap for Codex")
    print("# ================================")
    print("")

    if check_for_updates(paths.superpowers_repo_dir):
        print("## Update Available")
        print("")
        print("⚠️  Your superpowers installation is behind the latest version.")
        print("To update, run: `cd ~/.codex/superpowers && git pull`")
        print("")
        print("---")
        print("")

    if paths.bootstrap_file.exists():
        print("## Bootstrap Instructions:")
        print("")
        try:
            content = paths.bootstrap_file.read_text(encoding="utf-8")
            print(content)
        except OSError as error:
            LOGGER.error("Error reading bootstrap file", exc_info=True)
            print(f"Error reading bootstrap file: {error}")
        print("")
        print("---")
        print("")

    print("## Available Skills:")
    print("")
    run_find_skills()

    print("")
    print("---")
    print("")

    print("## Auto-loading using-superpowers skill:")
    print("")
    run_use_skill("using-superpowers")

    print("")
    print("---")
    print("")
    print("# Bootstrap Complete!")
    print("# You now have access to all superpowers skills.")
    print('# Use "superpowers-codex use-skill <skill>" to load and apply skills.')
    print("# Remember: If a skill applies to your task, you MUST use it!")
    LOGGER.debug("Completed bootstrap")


def _find_skill_file(search_path: Path) -> Path | None:
    LOGGER.debug("Searching for SKILL.md at %s", search_path)
    if search_path.is_dir():
        skill_md = search_path / "SKILL.md"
        if skill_md.exists():
            LOGGER.debug("Found SKILL.md in directory %s", search_path)
            return skill_md
    if search_path.is_file() and search_path.name == "SKILL.md":
        LOGGER.debug("Found SKILL.md file %s", search_path)
        return search_path
    LOGGER.debug("SKILL.md not found at %s", search_path)
    return None


def run_use_skill(skill_name: str | None) -> None:
    """Load and display the requested skill content."""
    LOGGER.debug("Running use-skill with %s", skill_name)
    if not skill_name:
        print("Usage: superpowers-codex use-skill <skill-name>")
        print("Examples:")
        print("  superpowers-codex use-skill superpowers:brainstorming  # Load superpowers skill")
        print(
            "  superpowers-codex use-skill brainstorming              "
            "# Load local/personal skill (or superpowers if not found)"
        )
        print(
            "  superpowers-codex use-skill my-custom-skill            # Load personal skill")
        LOGGER.debug("Completed use-skill: no skill name provided")
        return

    paths = _paths()
    actual_skill_path = skill_name
    force_superpowers = False

    if skill_name.startswith("superpowers:"):
        actual_skill_path = skill_name[len("superpowers:"):]
        force_superpowers = True

    if actual_skill_path.startswith("skills/"):
        actual_skill_path = actual_skill_path[len("skills/"):]

    skill_file: Path | None = None

    if force_superpowers:
        if paths.superpowers_skills_dir.exists():
            superpowers_path = paths.superpowers_skills_dir / actual_skill_path
            skill_file = _find_skill_file(superpowers_path)
    else:
        if paths.local_skills_dir.exists():
            local_path = paths.local_skills_dir / actual_skill_path
            skill_file = _find_skill_file(local_path)
            if skill_file:
                print(f"# Loading local skill: {actual_skill_path}")
                print(f"# Source: {skill_file}")
                print("")

        if skill_file is None and paths.personal_skills_dir.exists():
            personal_path = paths.personal_skills_dir / actual_skill_path
            skill_file = _find_skill_file(personal_path)
            if skill_file:
                print(f"# Loading personal skill: {actual_skill_path}")
                print(f"# Source: {skill_file}")
                print("")

        if skill_file is None and paths.superpowers_skills_dir.exists():
            superpowers_path = paths.superpowers_skills_dir / actual_skill_path
            skill_file = _find_skill_file(superpowers_path)
            if skill_file:
                print(
                    f"# Loading superpowers skill: superpowers:{actual_skill_path}")
                print(f"# Source: {skill_file}")
                print("")

    if skill_file is None:
        print(f"Error: Skill not found: {actual_skill_path}")
        print("")
        print("Available skills:")
        run_find_skills()
        LOGGER.debug("Skill not found: %s", actual_skill_path)
        return

    try:
        full_content = skill_file.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(skill_file)
        content = strip_frontmatter(full_content)
    except OSError as error:
        LOGGER.error("Error reading skill file", exc_info=True)
        print(f"Error reading skill file: {error}")
        LOGGER.debug("Completed use-skill with read error")
        return

    if force_superpowers:
        display_name = f"superpowers:{actual_skill_path}"
    elif paths.local_skills_dir in skill_file.parents:
        display_name = actual_skill_path
    elif paths.personal_skills_dir in skill_file.parents:
        display_name = actual_skill_path
    else:
        display_name = f"superpowers:{actual_skill_path}"

    skill_directory = skill_file.parent

    print(f"# {frontmatter.name or display_name}")
    if frontmatter.description:
        print(f"# {frontmatter.description}")
    print(
        f"# Skill-specific tools and reference files live in {skill_directory}")
    print("# ============================================")
    print("")
    print(content)
    LOGGER.debug("Completed use-skill for %s", actual_skill_path)


def _main(argv: Iterable[str]) -> int:
    LOGGER.debug("Entering CLI")
    args = list(argv)
    command = args[1] if len(args) > 1 else None
    arg = args[2] if len(args) > 2 else None

    if command == "bootstrap":
        run_bootstrap()
        LOGGER.debug("CLI completed: bootstrap")
        return 0
    if command == "use-skill":
        run_use_skill(arg)
        LOGGER.debug("CLI completed: use-skill")
        return 0
    if command == "find-skills":
        run_find_skills()
        LOGGER.debug("CLI completed: find-skills")
        return 0

    print("Superpowers for Codex")
    print("Usage:")
    print("  superpowers-codex bootstrap              # Run complete bootstrap with all skills")
    print("  superpowers-codex use-skill <skill-name> # Load a specific skill")
    print("  superpowers-codex find-skills            # List all available skills")
    print("")
    print("Examples:")
    print("  superpowers-codex bootstrap")
    print("  superpowers-codex use-skill superpowers:brainstorming")
    print("  superpowers-codex use-skill my-custom-skill")
    LOGGER.debug("CLI completed: usage")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
