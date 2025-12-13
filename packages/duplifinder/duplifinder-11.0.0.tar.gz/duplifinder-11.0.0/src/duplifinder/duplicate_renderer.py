# src/duplifinder/duplicate_renderer.py

"""Renderer for duplicate detection outputs (console/JSON/metrics)."""

import json
import logging
import time
from typing import Dict, List, Tuple, Any

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

from .config import Config
from .html_renderer import render_html_report
from .refactoring import get_refactoring_suggestion


def _normalize_for_render(dups: Dict, is_token: bool = False) -> Dict[str, List[Dict[str, Any]]]:
    """Normalize defs/text/tokens to common render format."""
    normalized = {}
    for key, items in dups.items():
        norm_items = []
        for item in items:
            if is_token:
                loc1, loc2, ratio = item
                norm_items.append({"loc": f"{loc1} ~ {loc2} (sim: {ratio:.2%})", "snippet": "", "type": "token"})
            else:
                if isinstance(item, str):
                    loc = item
                    snippet = ""
                else:
                    loc, snippet = item
                typ = key.split()[0] if " " in key else "text"
                norm_items.append({"loc": loc, "snippet": snippet, "type": typ})
        if norm_items:
            normalized[key] = norm_items
    return normalized


def render_duplicates(
    all_results: Dict,  # Generic: defs/text/tokens
    config: Config,
    is_search: bool,
    dup_rate: float,
    threshold: float,
    total_lines: int,
    dup_lines: int,
    scanned_files: int,
    skipped_files: List[str],
    is_token: bool = False
) -> None:
    """Render duplicates to console or JSON; handles token normalization."""
    console = Console()
    normalized = _normalize_for_render(all_results, is_token)
    duplicates = {k: v for k, v in normalized.items() if len(v) >= config.min_occurrences}

    # Add refactoring suggestions to duplicates
    for key, items in duplicates.items():
        suggestion = get_refactoring_suggestion(key, len(items))
        for item in items:
            item["refactoring_suggestion"] = suggestion

    if config.json_output:
        out = {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "root": str(config.root),
            "scanned_files": scanned_files,
            "skipped_files": skipped_files,
            "duplicate_count": len(duplicates),
            "duplicates": duplicates  # Already normalized with suggestions
        }
        print(json.dumps(out, indent=2))
        return

    if config.preview:
        # PREVIEW MODE: Use list format with Syntax Highlighting
        for key, items in duplicates.items():
            # Print a colorful title for the definition
            suggestion = items[0]["refactoring_suggestion"]
            console.print(f"\n[bold magenta]{key}[/bold magenta] defined [bold yellow]{len(items)} time(s):[/bold yellow]")
            console.print(f"[italic green]💡 Suggestion: {suggestion}[/italic green]")
            for item in items:
                loc = item["loc"]
                snippet = item["snippet"]
                # Print the location
                console.print(f"  -> [cyan]{loc}[/cyan]")
                
                if snippet:
                    # Create a Syntax object for highlighting
                    # We use "python" as the lexer
                    # We use a theme (like "monokai") to get the background color
                    # We disable rich's line numbers because the snippet already has them
                    syntax = Syntax(
                        snippet,
                        "python",
                        theme="monokai",
                        line_numbers=False 
                    )
                    # Print the Syntax object inside the Panel
                    console.print(Panel(syntax, border_style="dim", padding=(0, 1)))
                   
    else:
     
        # NO-PREVIEW MODE: Use the new, *colorful* compact table format
        for key, items in duplicates.items():
            # Add color to the title
            title = f"[bold magenta]{key}[/bold magenta] ([bold yellow]{len(items)}[/bold yellow] occurrence(s)):"
            suggestion = items[0]["refactoring_suggestion"]
            
            # Add color and style to the table
            table = Table(title=title, caption=f"[italic green]💡 Suggestion: {suggestion}[/italic green]", border_style="blue")
            
            # Add color to the header
            table.add_column("Location", style="cyan")
            
            for item in items:
                table.add_row(item["loc"])  # Add location
            console.print(table)
        
    if not duplicates:
        console.print("[green]No duplicates found.[/green]")

    if dup_rate > threshold:
        console.print(f"[red]ALERT: Duplication rate {dup_rate:.1%} exceeds threshold {threshold:.1%} (est. {dup_lines}/{total_lines} lines duplicated).[/red]")

    # Audit nudge: Optional console hint if enabled
    if config.audit_enabled:
        console.print(f"[dim green]Audit trail logged to {config.audit_log_path}[/dim green]")

    # Generate HTML report if requested
    if config.html_report:
        # We need to reshape normalized to the format expected by html_renderer (list of tuples)
        # However, _normalize_for_render returns List[Dict].
        # Let's adjust render_html_report to accept this or convert here.
        # Converting back to simpler format for HTML renderer or updating HTML renderer.
        # Let's update HTML renderer to accept the normalized format?
        # Actually, let's just reconstruct the list of tuples expected by the current HTML renderer implementation.
        # But wait, the current HTML renderer expects Dict[str, List[Tuple[str, str]]]

        # Let's convert normalized back to what html_renderer expects
        html_duplicates = {}
        for key, items in duplicates.items():
            html_items = []
            for item in items:
                html_items.append((item["loc"], item["snippet"]))
            html_duplicates[key] = html_items

        render_html_report(html_duplicates, config, scanned_files, total_lines, dup_lines, dup_rate)
        console.print(f"[green]HTML report generated at {config.html_report}[/green]")

    if config.fail_on_duplicates and duplicates:
        raise SystemExit(1)
