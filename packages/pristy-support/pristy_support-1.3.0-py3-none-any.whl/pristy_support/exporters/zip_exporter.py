# Copyright (C) 2025 JECI SARL
#
# This file is part of Pristy Support.
#
# Pristy Support is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pristy Support is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pristy Support.  If not, see <https://www.gnu.org/licenses/>.

"""ZIP exporter for Pristy support tool."""

import os
import json
import zipfile
from datetime import datetime
from typing import Dict
from . import markdown, html


def export_to_zip(audit_data: Dict, output_path: str) -> str:
    """
    Export audit data to a ZIP archive containing all reports and raw data.

    Args:
        audit_data: Complete audit data dictionary
        output_path: Base path for the ZIP file (without extension)

    Returns:
        Path to the created ZIP file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = f"{output_path}_audit_{timestamp}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add markdown report
        md_content = markdown.export_to_markdown(audit_data)
        zf.writestr("report.md", md_content)

        # Add HTML report
        html_content = html.export_to_html(audit_data)
        zf.writestr("report.html", html_content)

        # Add raw JSON data
        json_content = json.dumps(audit_data, indent=2, default=str)
        zf.writestr("raw_data.json", json_content)

        # Add individual module data
        if "system" in audit_data:
            system_json = json.dumps(audit_data["system"], indent=2, default=str)
            zf.writestr("data/system.json", system_json)

        if "logs" in audit_data:
            logs_json = json.dumps(audit_data["logs"], indent=2, default=str)
            zf.writestr("data/logs.json", logs_json)

        if "database" in audit_data:
            db_json = json.dumps(audit_data["database"], indent=2, default=str)
            zf.writestr("data/database.json", db_json)

        if "config" in audit_data:
            config_json = json.dumps(audit_data["config"], indent=2, default=str)
            zf.writestr("data/config.json", config_json)

        # Add a README
        readme_content = f"""# Pristy Support Audit Archive

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Contents

- `report.md`: Markdown formatted audit report
- `report.html`: HTML formatted audit report (open in browser)
- `raw_data.json`: Complete raw audit data in JSON format
- `data/`: Individual module data in JSON format
  - `system.json`: System checks data
  - `logs.json`: Logs analysis data
  - `database.json`: Database statistics data
  - `config.json`: Configuration review data

## Usage

1. Open `report.html` in a web browser for a formatted view
2. Use `report.md` for documentation or tickets
3. Use JSON files for programmatic analysis or integration with other tools
"""
        zf.writestr("README.txt", readme_content)

    return zip_path
