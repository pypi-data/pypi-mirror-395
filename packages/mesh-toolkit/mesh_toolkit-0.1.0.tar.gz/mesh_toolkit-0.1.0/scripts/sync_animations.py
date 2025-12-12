#!/usr/bin/env python3
"""Sync Meshy Animation Library from API documentation.

This script fetches the animation library from the Meshy API documentation
and generates Python constants for all available animations.

Usage:
    python scripts/sync_animations.py

The script will:
1. Fetch the animation library page from Meshy docs
2. Parse the HTML to extract animation metadata
3. Generate/update the animations catalog in the package

Requirements:
    pip install beautifulsoup4 httpx rich
"""

import json
import re
import sys
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# Rich console for CLI output
console = Console()

# Meshy API documentation URL for animation library
DOCS_URL = "https://docs.meshy.ai/en/api/animation-library"

# Alternative: Use the API directly if available
API_BASE = "https://api.meshy.ai"

# Output paths
PACKAGE_ROOT = Path(__file__).parent.parent
CATALOG_DIR = PACKAGE_ROOT / "src" / "mesh_toolkit" / "catalog"
ANIMATIONS_JSON = CATALOG_DIR / "animations.json"
ANIMATIONS_PY = PACKAGE_ROOT / "src" / "mesh_toolkit" / "animations.py"


def fetch_docs_page() -> str:
    """Fetch the animation library documentation page."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task(f"Fetching {DOCS_URL}...", total=None)
        response = httpx.get(DOCS_URL, follow_redirects=True, timeout=30.0)
        response.raise_for_status()
    return response.text


def parse_animations_from_html(html: str) -> list[dict]:
    """Parse animation data from the HTML documentation.

    The docs page contains tables or lists of animations with:
    - ID (action_id)
    - Name
    - Category
    - Subcategory
    - Preview URL (GIF)
    """
    soup = BeautifulSoup(html, "html.parser")
    animations = []

    # Try to find animation data in tables
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        headers = []

        for row in rows:
            cells = row.find_all(["th", "td"])
            if not cells:
                continue

            # First row with th elements = headers
            if row.find("th"):
                headers = [cell.get_text(strip=True).lower() for cell in cells]
                continue

            if not headers:
                continue

            # Parse data row
            data = {}
            for i, cell in enumerate(cells):
                if i < len(headers):
                    key = headers[i]
                    value = cell.get_text(strip=True)

                    # Try to find image URL
                    img = cell.find("img")
                    if img and img.get("src"):
                        data["preview_url"] = img["src"]

                    # Map common header names
                    if key in ("id", "action_id", "action id"):
                        try:
                            data["id"] = int(value)
                        except ValueError:
                            pass
                    elif key in ("name", "animation", "animation name"):
                        data["name"] = value
                    elif key in ("category",):
                        data["category"] = value
                    elif key in ("subcategory", "sub category"):
                        data["subcategory"] = value

            if data.get("id") is not None and data.get("name"):
                animations.append(data)

    # If no tables, try to find JSON data in script tags
    if not animations:
        scripts = soup.find_all("script")
        for script in scripts:
            text = script.get_text()
            # Look for animation data patterns
            if "animation" in text.lower() and "id" in text.lower():
                # Try to extract JSON objects
                json_matches = re.findall(r'\{[^{}]*"id"\s*:\s*\d+[^{}]*\}', text)
                for match in json_matches:
                    try:
                        data = json.loads(match)
                        if "id" in data:
                            animations.append(data)
                    except json.JSONDecodeError:
                        pass

    # If still no data, try parsing from structured divs/lists
    if not animations:
        # Look for animation entries in various formats
        entries = soup.find_all(["div", "li"], class_=re.compile(r"animation|action", re.I))
        for entry in entries:
            text = entry.get_text()
            # Try to extract ID and name
            id_match = re.search(r"(?:id|action)[:\s]*(\d+)", text, re.I)
            name_match = re.search(r"(?:name)[:\s]*([A-Za-z0-9_]+)", text, re.I)

            if id_match:
                data = {"id": int(id_match.group(1))}
                if name_match:
                    data["name"] = name_match.group(1)
                else:
                    # Try to find any capitalized word as name
                    words = re.findall(r"[A-Z][a-z]+(?:_[A-Z][a-z]+)*", text)
                    if words:
                        data["name"] = words[0]

                if data.get("name"):
                    animations.append(data)

    return animations


def generate_animations_json(animations: list[dict]) -> None:
    """Generate the animations.json catalog file."""
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)

    # Sort by ID
    animations = sorted(animations, key=lambda x: x.get("id", 0))

    # Ensure all entries have required fields
    cleaned = []
    for anim in animations:
        cleaned.append(
            {
                "id": anim.get("id", 0),
                "name": anim.get("name", f"Animation_{anim.get('id', 0)}"),
                "category": anim.get("category", "Unknown"),
                "subcategory": anim.get("subcategory", "Unknown"),
                "preview_url": anim.get("preview_url", ""),
            }
        )

    with open(ANIMATIONS_JSON, "w") as f:
        json.dump({"animations": cleaned, "count": len(cleaned)}, f, indent=2)

    console.print(
        f"[green]✓[/green] Generated [cyan]{ANIMATIONS_JSON}[/cyan] with {len(cleaned)} animations"
    )


def generate_animations_py(animations: list[dict]) -> None:
    """Generate/update the animations.py module with all animation constants."""
    # Sort by ID
    animations = sorted(animations, key=lambda x: x.get("id", 0))

    # Group by category
    categories = {}
    for anim in animations:
        cat = anim.get("category", "Unknown")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(anim)

    # Generate the Python code - formatted to match ruff output
    lines = [
        '"""Meshy Animation Library - Auto-generated from API docs."""',
        "",
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass",
        "from enum import Enum",
        "",
        "# This file is auto-generated by scripts/sync_animations.py",
        "# Do not edit manually - run the script to update.",
        "",
        "",
        "@dataclass",
        "class AnimationMeta:",
        '    """Metadata for a Meshy animation."""',
        "",
        "    id: int",
        "    name: str",
        "    category: str",
        "    subcategory: str",
        "    preview_url: str",
        "",
        "",
    ]

    # Generate category enum
    cat_names = sorted(set(a.get("category", "Unknown") for a in animations))
    lines.append("class AnimationCategory(str, Enum):")
    lines.append('    """Animation categories."""')
    lines.append("")
    for cat in cat_names:
        enum_name = re.sub(r"[^A-Za-z0-9]", "_", cat).upper()
        lines.append(f'    {enum_name} = "{cat}"')
    lines.append("")
    lines.append("")

    # Generate subcategory enum
    subcat_names = sorted(set(a.get("subcategory", "Unknown") for a in animations))
    lines.append("class AnimationSubcategory(str, Enum):")
    lines.append('    """Animation subcategories."""')
    lines.append("")
    for subcat in subcat_names:
        enum_name = re.sub(r"[^A-Za-z0-9]", "_", subcat).upper()
        lines.append(f'    {enum_name} = "{subcat}"')
    lines.append("")
    lines.append("")

    # Generate ANIMATIONS dict
    lines.append("# Complete animation library")
    lines.append("ANIMATIONS: dict[int, AnimationMeta] = {")
    for anim in animations:
        aid = anim.get("id", 0)
        name = anim.get("name", f"Animation_{aid}")
        cat = anim.get("category", "Unknown")
        subcat = anim.get("subcategory", "Unknown")
        preview = anim.get("preview_url", "")

        lines.append(f"    {aid}: AnimationMeta(")
        lines.append(f"        {aid},")
        lines.append(f'        "{name}",')
        lines.append(f'        "{cat}",')
        lines.append(f'        "{subcat}",')
        lines.append(f'        "{preview}",')
        lines.append("    ),")

    lines.append("}")
    lines.append("")
    lines.append("")

    # Add helper functions - formatted to match ruff output
    lines.extend(
        [
            "# Curated animation sets for common game use cases",
            "",
            "",
            "class GameAnimationSet:",
            '    """Pre-defined animation sets for common game scenarios."""',
            "",
            "    # Basic character movement - Idle and locomotion",
            "    BASIC_MOVEMENT: list[int] = []",
            "",
            "    # Combat animations",
            "    COMBAT: list[int] = []",
            "",
            "    # Social/NPC interactions",
            "    SOCIAL: list[int] = []",
            "",
            "    # Dance/celebration",
            "    CELEBRATION: list[int] = []",
            "",
            "    # Exploration animations",
            "    EXPLORATION: list[int] = []",
            "",
            "",
            "# Populate animation sets from available animations",
            "def _populate_animation_sets() -> None:",
            '    """Populate animation sets based on available animations."""',
            "    all_ids = set(ANIMATIONS.keys())",
            "",
            "    # Basic movement: Idle + Walking + Running",
            "    GameAnimationSet.BASIC_MOVEMENT = [",
            '        aid for aid in all_ids if ANIMATIONS[aid].subcategory in ("Idle", "Walking", "Running")',
            "    ][:10]  # Limit to first 10",
            "",
            "    # Combat: Fighting category",
            '    GameAnimationSet.COMBAT = [aid for aid in all_ids if ANIMATIONS[aid].category == "Fighting"][',
            "        :10",
            "    ]",
            "",
            "    # Social: Interacting subcategory",
            "    GameAnimationSet.SOCIAL = [",
            '        aid for aid in all_ids if ANIMATIONS[aid].subcategory == "Interacting"',
            "    ][:10]",
            "",
            "    # Celebration: Dancing category",
            "    GameAnimationSet.CELEBRATION = [",
            '        aid for aid in all_ids if ANIMATIONS[aid].category == "Dancing"',
            "    ][:10]",
            "",
            "    # Exploration: LookingAround + Idle",
            "    GameAnimationSet.EXPLORATION = [",
            '        aid for aid in all_ids if ANIMATIONS[aid].subcategory in ("LookingAround", "Idle")',
            "    ][:10]",
            "",
            "",
            "# Initialize sets on module load",
            "_populate_animation_sets()",
            "",
            "",
            "def get_animations_by_category(category: AnimationCategory) -> list[AnimationMeta]:",
            '    """Get all animations in a category."""',
            "    return [anim for anim in ANIMATIONS.values() if anim.category == category.value]",
            "",
            "",
            "def get_animations_by_subcategory(",
            "    subcategory: AnimationSubcategory,",
            ") -> list[AnimationMeta]:",
            '    """Get all animations in a subcategory."""',
            "    return [anim for anim in ANIMATIONS.values() if anim.subcategory == subcategory.value]",
            "",
            "",
            "def get_animation(action_id: int) -> AnimationMeta:",
            '    """Get animation by ID."""',
            "    if action_id not in ANIMATIONS:",
            '        msg = f"Animation ID {action_id} not found"',
            "        raise ValueError(msg)",
            "    return ANIMATIONS[action_id]",
            "",
        ]
    )

    # Write the file
    with open(ANIMATIONS_PY, "w") as f:
        f.write("\n".join(lines))

    console.print(
        f"[green]✓[/green] Generated [cyan]{ANIMATIONS_PY}[/cyan] with {len(animations)} animations"
    )


def display_summary(animations: list[dict]) -> None:
    """Display a summary table of parsed animations."""
    if not animations:
        return

    table = Table(title="Parsed Animations Summary")
    table.add_column("Category", style="cyan")
    table.add_column("Count", justify="right", style="green")

    # Group by category
    categories: dict[str, int] = {}
    for anim in animations:
        cat = anim.get("category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1

    for cat, count in sorted(categories.items()):
        table.add_row(cat, str(count))

    table.add_row("[bold]Total[/bold]", f"[bold]{len(animations)}[/bold]")
    console.print(table)


def main() -> int:
    """Main entry point."""
    console.print("[bold blue]Meshy Animation Library Sync[/bold blue]")
    console.print("─" * 40)

    try:
        # Fetch and parse
        html = fetch_docs_page()
        animations = parse_animations_from_html(html)

        if not animations:
            console.print("[yellow]⚠[/yellow] No animations found in docs page.")
            console.print("[dim]The documentation format may have changed.[/dim]")
            console.print("[dim]Keeping existing animations.py unchanged.[/dim]")
            return 1

        console.print(f"[green]✓[/green] Found {len(animations)} animations")
        display_summary(animations)

        # Generate output files
        generate_animations_json(animations)

        # Ask before overwriting animations.py
        if ANIMATIONS_PY.exists():
            console.print(f"\n[yellow]![/yellow] [cyan]{ANIMATIONS_PY}[/cyan] already exists.")
            console.print("[dim]To regenerate, delete the file first or pass --force[/dim]")
            # Still update the JSON catalog
        else:
            generate_animations_py(animations)

        console.print("\n[bold green]✓ Sync complete![/bold green]")
        return 0

    except httpx.HTTPError as e:
        console.print(f"[red]✗[/red] HTTP error: {e}")
        return 1
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}")
        console.print_exception()
        return 1


if __name__ == "__main__":
    sys.exit(main())
