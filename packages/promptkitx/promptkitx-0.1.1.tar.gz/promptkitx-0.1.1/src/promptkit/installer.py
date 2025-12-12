import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from .packs import Pack, load_pack, list_builtin_packs

START_MARKER = "<!-- promptkit:start -->"
END_MARKER = "<!-- promptkit:end -->"
REGISTRY_PATH = Path(".agent/promptkit/registry.json")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_registry(repo_root: Path) -> Dict:
    path = repo_root / REGISTRY_PATH
    if not path.exists():
        return {"packs": []}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"packs": []}


def save_registry(repo_root: Path, registry: Dict) -> None:
    path = repo_root / REGISTRY_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def _write_file(dest: Path, content: str, force: bool) -> str:
    existed = dest.exists()
    if existed and not force:
        return "unchanged"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    if existed:
        return "overwritten"
    return "created"


def _update_agents_md(repo_root: Path, installed_snippets: List[str]) -> str:
    path = repo_root / "AGENTS.md"
    block_body = "\n\n".join(snippet.strip() for snippet in installed_snippets if snippet.strip())
    managed = f"{START_MARKER}\n# Prompt Packs (managed by promptkit)\n\n{block_body}\n{END_MARKER}\n"

    if not path.exists():
        path.write_text(managed, encoding="utf-8")
        return "created"

    content = path.read_text(encoding="utf-8")
    if START_MARKER in content and END_MARKER in content:
        prefix, rest = content.split(START_MARKER, 1)
        _, suffix = rest.split(END_MARKER, 1)
        new_content = prefix.rstrip() + "\n\n" + managed + suffix.lstrip()
    else:
        if content.strip():
            new_content = content.rstrip() + "\n\n" + managed
        else:
            new_content = managed
    path.write_text(new_content, encoding="utf-8")
    return "updated"


def install_pack(repo_root: Path, pack_name: str, force: bool = False) -> Dict:
    pack = load_pack(pack_name)
    registry = load_registry(repo_root)

    # copy files
    file_results = []
    for pack_file, source_path in pack.iter_files():
        target_path = repo_root / pack_file.target
        status = _write_file(target_path, source_path.read_text(encoding="utf-8"), force)
        file_results.append({"target": pack_file.target, "status": status})

    # update registry entry
    packs = registry.get("packs", [])
    packs = [p for p in packs if p.get("name") != pack.name]
    packs.append(
        {
            "name": pack.name,
            "version": pack.version,
            "source": "builtin",
            "installed_at": _now_iso(),
            "agents_snippet": pack.read_agents_snippet(),
            "files": file_results,
        }
    )
    registry["packs"] = packs
    save_registry(repo_root, registry)

    # rewrite AGENTS block with all installed snippets
    snippets = [p["agents_snippet"] for p in registry["packs"]]
    agents_status = _update_agents_md(repo_root, snippets)

    return {
        "pack": pack.name,
        "version": pack.version,
        "files": file_results,
        "agents_md": agents_status,
        "registry_path": str(REGISTRY_PATH),
    }


def list_installed_packs(repo_root: Path) -> List[Dict]:
    reg = load_registry(repo_root)
    return reg.get("packs", [])


def list_available_packs() -> List[Pack]:
    return list(list_builtin_packs().values())
