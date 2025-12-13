"""HTML Report Generation."""

import html as html_lib
from pathlib import Path
from typing import Dict, List, Tuple

from .config import Config

TEMPLATE_PATH = Path(__file__).parent / "templates" / "report.html"

def render_html_report(
    duplicates: Dict[str, List[Tuple[str, str]]],
    config: Config,
    scanned: int,
    total_lines: int,
    dup_lines: int,
    dup_rate: float
) -> None:
    """Generate an HTML report for the duplicates."""
    if not config.html_report:
        return

    try:
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        # Fallback if template is missing (e.g. package issues)
        template = "<html><body><h1>Report</h1><p>Template not found.</p></body></html>"

    content_parts = []

    for name, occurrences in duplicates.items():
        if len(occurrences) < config.min_occurrences:
            continue

        occ_html = ""
        for loc, snippet in occurrences:
             escaped_snippet = html_lib.escape(snippet)
             occ_html += f"""
             <div class="duplicate">
                <div class="duplicate-header">
                    <span>{loc}</span>
                </div>
                <pre class="code">{escaped_snippet}</pre>
             </div>
             """

        content_parts.append(f"""
        <div class="group">
            <div class="group-header">{name} ({len(occurrences)} copies)</div>
            {occ_html}
        </div>
        """)

    content = "\n".join(content_parts)
    alert_class = "alert" if dup_rate > config.dup_threshold else ""

    html = template.format(
        scanned=scanned,
        total_lines=total_lines,
        dup_lines=dup_lines,
        dup_rate=f"{dup_rate * 100:.1f}",
        alert_class=alert_class,
        content=content
    )

    try:
        with open(config.html_report, "w", encoding="utf-8") as f:
            f.write(html)
    except Exception:
        # Should log error ideally
        pass
