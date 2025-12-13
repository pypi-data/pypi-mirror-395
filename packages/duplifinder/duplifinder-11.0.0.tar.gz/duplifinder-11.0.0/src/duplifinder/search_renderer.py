# src/duplifinder/search_renderer.py

"""Renderer for search mode outputs (singletons/multi-occurrences)."""

import json
import logging
import time
from typing import Dict, List, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from .config import Config


def render_search(
    search_results: Dict[str, List[Tuple[str, str]]],
    config: Config
) -> None:
    """Render search results to console."""
    console = Console()

    for spec, occ in search_results.items():
        count = len(occ)
        if count == 0:
            console.print(f"[yellow]No occurrences found for {spec}.[/yellow]")
            continue

        # Print the main title
        title_color = "green" if count == 1 else "blue"
        count_color = "green" if count == 1 else "bold yellow"
        title_text = "Verified singleton" if count == 1 else f"found {count} time(s)"
        
        console.print(f"\n[{title_color}]{spec}[/{title_color}] {title_text}:")

        for loc, snippet in occ:
            # Print the location
            console.print(f"  -> [cyan]{loc}[/cyan]")
            
            # If -p is used, show the full, highlighted panel
            if config.preview and snippet:
                syntax = Syntax(
                    snippet,
                    "python",
                    theme="monokai",
                    line_numbers=False
                )
                console.print(Panel(syntax, border_style="dim", padding=(0, 1)))

        if config.fail_on_duplicates and count > 1:
            logging.warning(f"Multiple occurrences ({count}) for {spec}; failing per config.")
            # Note: This SystemExit will be caught by main.py
            raise SystemExit(1)

def render_search_json(
    search_results: Dict[str, List[Tuple[str, str]]],
    config: Config,
    scanned: int,
    skipped: List[str]
) -> None:
    """Render search results as JSON."""
    out = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "root": str(config.root),
        "scanned_files": scanned,
        "skipped_files": skipped if config.verbose else len(skipped),
        "search_specs": config.search_specs,
        "search_results": {
            spec: {
                "count": len(occ),
                "is_singleton": len(occ) == 1,
                "occurrences": [{"loc": loc, "snippet": snippet} for loc, snippet in occ]
            }
            for spec, occ in search_results.items()
        },
    }
    print(json.dumps(out, indent=2))
