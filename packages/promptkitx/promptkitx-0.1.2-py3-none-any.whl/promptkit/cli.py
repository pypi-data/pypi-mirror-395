import argparse
import sys
from pathlib import Path

from .installer import install_pack, list_available_packs, list_installed_packs


def cmd_list(args) -> int:
    repo_root = Path(args.path).expanduser().resolve()
    available = list_available_packs()
    installed = list_installed_packs(repo_root)

    print("Available packs:")
    for pack in available:
        print(f"- {pack.name} {pack.version}: {pack.description}")

    print("\nInstalled packs:")
    if not installed:
        print("- (none)")
    else:
        for p in installed:
            print(f"- {p['name']} {p['version']} (source: {p.get('source','?')})")
    return 0


def cmd_install(args) -> int:
    repo_root = Path(args.path).expanduser().resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        print(f"Error: path is invalid: {repo_root}", file=sys.stderr)
        return 1
    result = install_pack(repo_root, args.pack, force=args.force)
    print(f"Installed pack '{result['pack']}' v{result['version']}")
    for f in result["files"]:
        print(f"  {f['target']}: {f['status']}")
    print(f"AGENTS.md: {result['agents_md']}")
    print(f"Registry: {result['registry_path']}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Manage prompt packs (AGENTS + .agent files) via promptkit")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List available and installed packs")
    p_list.add_argument("-p", "--path", default=".", help="Repo root (default: .)")
    p_list.set_defaults(func=cmd_list)

    p_install = sub.add_parser("install", help="Install a pack into the repo")
    p_install.add_argument("pack", help="Pack name (built-in: execplan)")
    p_install.add_argument("-p", "--path", default=".", help="Repo root (default: .)")
    p_install.add_argument("-f", "--force", action="store_true", help="Overwrite existing files")
    p_install.set_defaults(func=cmd_install)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
