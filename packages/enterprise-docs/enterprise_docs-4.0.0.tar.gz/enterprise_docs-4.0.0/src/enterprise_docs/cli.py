# src/enterprise_docs/cli.py

import argparse
import shutil
from pathlib import Path
import importlib.resources as resources
from importlib.metadata import version, PackageNotFoundError
from .banner import print_logo


def list_docs():
    """List all documentation templates included in the package."""
    package_path = resources.files("enterprise_docs.templates")
    for f in package_path.iterdir():
        if f.suffix == ".md":
            print(f.name)


def copy_docs(destination: str, template_name: str = None, source: str = None):
    """Copy documentation templates to the specified directory."""
    dest = Path(destination)
    dest.mkdir(parents=True, exist_ok=True)

    if source:
        src = Path(source)
        if not src.exists():
            print(f"❌ Source directory '{source}' not found")
            return
    else:
        src = resources.files("enterprise_docs.templates")

    found = False

    for f in src.iterdir():
        if f.suffix == ".md":
            if template_name and f.name != template_name:
                continue

            shutil.copy(f, dest / f.name)
            found = True
            if template_name:
                print(f"✅ Copied {f.name} to {dest.resolve()}")
                return

    if template_name and not found:
        print(f"❌ Template '{template_name}' not found")
        return

    print(f"✅ Copied documentation templates to {dest.resolve()}")


def show_version():
    """Display the installed version of enterprise-docs."""
    try:
        v = version("enterprise-docs")
    except PackageNotFoundError:
        v = "unknown"
    print(f"enterprise-docs {v}")


def main():
    print_logo()
    parser = argparse.ArgumentParser(
        description="Enterprise Docs Manager — manage and sync standard documentation templates."
    )
    parser.add_argument(
        "command",
        choices=["list", "sync", "version"],
        help="Command to run: list available docs, sync to folder, or show version.",
    )
    parser.add_argument(
        "template_name",
        nargs="?",
        help="Specific template to sync (optional)",
    )
    parser.add_argument("--to", default="./docs", help="Destination directory for sync (default: ./docs)")
    parser.add_argument("--source", help="Custom source directory for templates")
    args = parser.parse_args()

    if args.command == "list":
        list_docs()
    elif args.command == "sync":
        copy_docs(args.to, args.template_name, args.source)
    elif args.command == "version":
        show_version()


if __name__ == "__main__":
    main()
