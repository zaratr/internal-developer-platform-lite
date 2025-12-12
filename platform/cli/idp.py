"""
IDP-Lite CLI

This CLI is intentionally tiny; its purpose is to show how a platform team
can provide paved roads for service creation rather than bespoke scaffolds.
"""

import argparse
import os
import shutil
import textwrap
from pathlib import Path
from typing import Dict

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_ROOT = ROOT / "platform" / "templates"
DEFAULT_TEMPLATE = "fastapi-service"


class TemplateContext:
    """Simple context container for template rendering."""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.service_package = service_name.replace("-", "_")
        self.service_title = service_name.replace("-", " ").title()

    def as_dict(self) -> Dict[str, str]:
        return {
            "{{service_name}}": self.service_name,
            "{{service_package}}": self.service_package,
            "{{service_title}}": self.service_title,
        }


def render_text(content: str, context: TemplateContext) -> str:
    rendered = content
    for key, value in context.as_dict().items():
        rendered = rendered.replace(key, value)
    return rendered


def copy_template(template: Path, destination: Path, context: TemplateContext) -> None:
    for src in template.rglob("*"):
        rel = src.relative_to(template)
        dest_path = destination / rel

        if src.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)
            continue

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        content = src.read_text()
        rendered = render_text(content, context)
        dest_path.write_text(rendered)


def create_service(name: str, template_name: str = DEFAULT_TEMPLATE, examples_dir: Path | None = None) -> Path:
    examples_dir = examples_dir or ROOT / "examples"
    normalized = template_name.replace("-", "_")
    template_path = TEMPLATE_ROOT / normalized
    if not template_path.exists():
        raise FileNotFoundError(f"Template {template_name} not found under {TEMPLATE_ROOT}")

    destination = examples_dir / name
    if destination.exists():
        raise FileExistsError(f"Destination {destination} already exists")

    context = TemplateContext(service_name=name)
    copy_template(template_path, destination, context)
    return destination


def list_templates() -> None:
    available = [p.name for p in TEMPLATE_ROOT.iterdir() if p.is_dir()]
    print("Available templates:")
    for template in sorted(available):
        print(f" - {template}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="IDP-Lite CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """
            Example:
              python -m platform.cli.idp create service user-profile
            """
        ),
    )

    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create resources")
    create_sub = create_parser.add_subparsers(dest="resource")

    service_parser = create_sub.add_parser("service", help="Create a new service")
    service_parser.add_argument("name", help="Service name (kebab-case recommended)")
    service_parser.add_argument(
        "--template",
        default=DEFAULT_TEMPLATE,
        help="Template name (default: fastapi-service)",
    )

    subparsers.add_parser("list", help="List available templates")

    args = parser.parse_args()

    if args.command == "list":
        list_templates()
        return

    if args.command == "create" and args.resource == "service":
        dest = create_service(args.name, args.template)
        print(f"Created service at {dest}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
