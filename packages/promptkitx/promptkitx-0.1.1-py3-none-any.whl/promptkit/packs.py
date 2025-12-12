import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Dict, List, Optional

PACKS_PACKAGE = "promptkit_builtin_packs"


@dataclass
class PackFile:
    source: str  # relative to pack folder
    target: str  # repo-relative destination


@dataclass
class Pack:
    name: str
    version: str
    description: str
    agents_entry: str  # relative path to snippet within pack
    files: List[PackFile]
    base_path: Path  # filesystem path to the pack resources

    def read_agents_snippet(self) -> str:
        return (self.base_path / self.agents_entry).read_text(encoding="utf-8").strip() + "\n"

    def iter_files(self):
        for f in self.files:
            yield f, (self.base_path / f.source)


class PackNotFound(Exception):
    pass


def _pack_root(name: str) -> Path:
    try:
        return Path(resources.files(PACKS_PACKAGE) / name)
    except ModuleNotFoundError as exc:
        raise PackNotFound(name) from exc


def load_pack(name: str) -> Pack:
    root = _pack_root(name)
    pack_json = root / "pack.json"
    if not pack_json.exists():
        raise PackNotFound(name)
    data = json.loads(pack_json.read_text(encoding="utf-8"))
    files = [PackFile(**f) for f in data.get("files", [])]
    return Pack(
        name=data["name"],
        version=data.get("version", "0.0.0"),
        description=data.get("description", ""),
        agents_entry=data["agents_entry"],
        files=files,
        base_path=root,
    )


def list_builtin_packs() -> Dict[str, Pack]:
    """Return a mapping of builtin pack name -> Pack"""
    pack_root = resources.files(PACKS_PACKAGE)
    result: Dict[str, Pack] = {}
    for entry in pack_root.iterdir():
        if entry.is_dir() and (entry / "pack.json").exists():
            try:
                pack = load_pack(entry.name)
                result[pack.name] = pack
            except Exception:
                continue
    return result
