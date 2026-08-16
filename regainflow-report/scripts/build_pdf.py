#!/usr/bin/env python3
"""Render a RegainFlow report HTML file to PDF with WeasyPrint.

Usage: python build_pdf.py <report.html> <output.pdf>

Requires: pip install weasyprint --break-system-packages
The HTML should link report.css (copy it next to the HTML) and reference
figures with relative paths.
"""
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    from weasyprint import HTML

    HTML(filename=str(src)).write_pdf(str(out))
    print(f"Wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
