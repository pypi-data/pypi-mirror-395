"""Core functionality for DumpConfluence"""

import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from rich.console import Console

from .exceptions import AuthenticationError, FileSystemError, NetworkError, ValidationError
from . import __version__

# Setup logging
logger = logging.getLogger(__name__)
console = Console()


class ConfluenceBackup:
    """
    Main class for backing up Confluence pages with images and attachments.

    This class provides functionality to download Confluence pages, process their content,
    download associated images, and save everything as self-contained HTML files.

    Attributes:
        confluence_url (str): Base URL of the Confluence instance
        email (str): Email address for authentication
        api_token (str): API token for authentication
        output_dir (Path): Directory where backups will be saved
        auth (tuple): Authentication tuple for requests
        headers (dict): HTTP headers for API requests

    Example:
        >>> backup = ConfluenceBackup("https://company.atlassian.net", "user@email.com", "token")
        >>> result = backup.backup_page("https://company.atlassian.net/wiki/spaces/SPACE/pages/123/Page")
        >>> print(f"Backup saved to: {result}")
    """

    def __init__(self, confluence_url: str, email: str, api_token: str, output_dir: str = ".") -> None:
        """
        Initialize the ConfluenceBackup instance.

        Args:
            confluence_url: Base URL of the Confluence instance
            email: Email address for authentication
            api_token: API token for authentication
            output_dir: Directory where backups will be saved (default: current directory)

        Raises:
            ValidationError: If any input parameters are invalid
        """
        # Validate inputs
        if not confluence_url or not confluence_url.strip():
            raise ValidationError("Confluence URL cannot be empty")
        if not email or not email.strip():
            raise ValidationError("Email cannot be empty")
        if not api_token or not api_token.strip():
            raise ValidationError("API token cannot be empty")

        # Validate URL format
        if not confluence_url.startswith(('http://', 'https://')):
            raise ValidationError("Confluence URL must start with http:// or https://")

        # Validate email format (basic check)
        if '@' not in email or '.' not in email:
            raise ValidationError("Invalid email format")

        self.confluence_url = confluence_url.rstrip('/')
        self.email = email.strip()
        self.api_token = api_token.strip()
        self.output_dir = Path(output_dir)
        self.auth = (self.email, self.api_token)
        self.headers = {
            "Accept": "application/json",
            "User-Agent": f"DumpConfluence/{__version__}"
        }

        # Ensure output directory exists
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            raise ValidationError(f"Cannot create output directory '{output_dir}': {e}")

    @staticmethod
    def extract_page_id(url: str) -> Optional[str]:
        """
        Extract page ID from Confluence URL.

        Args:
            url: Confluence page URL

        Returns:
            Page ID if found, None otherwise

        Example:
            >>> ConfluenceBackup.extract_page_id("https://company.atlassian.net/wiki/spaces/SPACE/pages/123456/Page")
            '123456'
        """
        if not url or not isinstance(url, str):
            return None

        try:
            parts = url.rstrip('/').split('/')
            for i, part in enumerate(parts):
                if part == 'pages' and i + 1 < len(parts):
                    # Validate that the page ID is numeric
                    page_id = parts[i + 1]
                    if page_id.isdigit():
                        return page_id
            return None
        except (AttributeError, IndexError):
            return None

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for filesystem compatibility.

        Args:
            filename: Original filename

        Returns:
            Sanitized filename safe for filesystem use

        Example:
            >>> ConfluenceBackup.sanitize_filename("My File: With / Invalid * Chars")
            'My File_ With _ Invalid _ Chars'
        """
        if not filename or not isinstance(filename, str):
            return "untitled"

        # Replace invalid characters with underscore
        invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
        safe_name = re.sub(invalid_chars, '_', filename)

        # Remove multiple consecutive underscores
        safe_name = re.sub(r'_+', '_', safe_name)

        # Strip leading/trailing underscores and whitespace
        safe_name = safe_name.strip('_ ')

        # Limit length and ensure not empty
        safe_name = safe_name[:200] if safe_name else "untitled"

        return safe_name

    def get_page_details(self, page_id: str) -> Dict[str, Any]:
        """
        Fetch page details from Confluence API.

        Args:
            page_id: Confluence page ID

        Returns:
            Dictionary containing page details

        Raises:
            ValidationError: If page_id is invalid
            AuthenticationError: If authentication fails
            NetworkError: If API request fails
        """
        if not page_id or not isinstance(page_id, str) or not page_id.isdigit():
            raise ValidationError(f"Invalid page ID: '{page_id}'. Must be numeric.")

        url = f"{self.confluence_url}/wiki/rest/api/content/{page_id}"
        params = {
            "expand": "body.storage,children.page,ancestors,version,space"
        }

        try:
            logger.debug(f"Fetching page details for ID: {page_id}")
            response = requests.get(
                url,
                auth=self.auth,
                headers=self.headers,
                params=params,
                timeout=30
            )

            if response.status_code == 401:
                raise AuthenticationError("Authentication failed. Check your email and API token.")
            elif response.status_code == 403:
                raise AuthenticationError("Access denied. You don't have permission to access this page.")
            elif response.status_code == 404:
                raise ValidationError(f"Page with ID '{page_id}' not found.")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            raise NetworkError("Request timeout. The Confluence server took too long to respond.")
        except requests.exceptions.ConnectionError:
            raise NetworkError(f"Cannot connect to Confluence server: {self.confluence_url}")
        except requests.exceptions.HTTPError as e:
            raise NetworkError(f"HTTP error {e.response.status_code}: {e.response.reason}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise NetworkError("Invalid response from Confluence API")

    def download_image(self, page_id: str, filename: str, save_path: Path) -> bool:
        """Download a single image"""
        try:
            img_url = f"{self.confluence_url}/wiki/download/attachments/{page_id}/{filename}?api=v2"
            response = requests.get(img_url, auth=self.auth, stream=True, timeout=30)
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True
        except Exception as e:
            console.print(f"[yellow]⚠ Failed to download {filename}: {str(e)}[/yellow]")
            return False

    def process_code_blocks(self, soup: BeautifulSoup) -> None:
        """Process Confluence code blocks and convert them to HTML"""
        # Find all structured macro elements (code blocks, etc.)
        macros = soup.find_all('ac:structured-macro')

        for macro in macros:
            macro_name = macro.get('ac:name', '')


            if macro_name == 'code':
                # Extract language and code content
                language = 'text'
                code_content = ''

                # Get language from parameters
                for param in macro.find_all('ac:parameter'):
                    param_name = param.get('ac:name', '')
                    if param_name == 'language':
                        language = param.get_text(strip=True) or 'text'
                    elif param_name == 'title':
                        # Could add title support later
                        pass

                # Get code content from plain-text-body or rich-text-body
                body = macro.find('ac:plain-text-body')
                if body:
                    code_content = body.get_text()
                else:
                    body = macro.find('ac:rich-text-body')
                    if body:
                        code_content = body.get_text()

                # Create new code block HTML with line numbers
                if code_content:
                    # Create wrapper div for code block
                    code_wrapper = soup.new_tag('div')
                    code_wrapper['class'] = 'code-block'

                    # Create line numbers column
                    lines = code_content.strip().split('\n')
                    line_numbers_div = soup.new_tag('div')
                    line_numbers_div['class'] = 'line-numbers'

                    for i in range(1, len(lines) + 1):
                        line_num = soup.new_tag('span')
                        line_num['class'] = 'line-number'
                        line_num.string = str(i)
                        line_numbers_div.append(line_num)
                        if i < len(lines):
                            line_numbers_div.append(soup.new_string('\n'))

                    # Create code content
                    pre_tag = soup.new_tag('pre')
                    pre_tag['class'] = f'code-content language-{language}'

                    code_tag = soup.new_tag('code')
                    code_tag.string = code_content.strip()

                    pre_tag.append(code_tag)

                    # Assemble the code block
                    code_wrapper.append(line_numbers_div)
                    code_wrapper.append(pre_tag)

                    macro.replace_with(code_wrapper)
                else:
                    # If no content, just remove the macro
                    macro.decompose()

            elif macro_name in ['info', 'warning', 'note', 'tip', 'error']:
                # Convert alert/info macros to divs
                alert_type = macro_name

                # Check for type parameter in info macro (Confluence often uses this)
                if macro_name == 'info':
                    for param in macro.find_all('ac:parameter'):
                        param_name = param.get('ac:name', '')
                        param_value = param.get_text(strip=True).lower()

                        # Check multiple parameter names that could indicate type
                        if param_name in ['type', 'title', 'icon']:
                            # Map various Confluence type values to our types
                            type_mappings = {
                                'warning': 'warning',
                                'warn': 'warning',
                                'caution': 'warning',
                                'attention': 'warning',
                                'note': 'note',
                                'tip': 'tip',
                                'info': 'info',
                                'error': 'error',
                                'danger': 'error',
                                'success': 'success',
                                'check': 'success',
                                # Confluence sometimes uses different naming
                                'yellow': 'warning',
                                'orange': 'warning',
                                'red': 'error',
                                'green': 'success',
                                'blue': 'info'
                            }

                            if param_value in type_mappings:
                                alert_type = type_mappings[param_value]
                                break


                div_tag = soup.new_tag('div')
                div_tag['class'] = f'confluence-{alert_type}'
                div_tag['style'] = self._get_macro_style(alert_type)


                # Get content from rich-text-body
                body = macro.find('ac:rich-text-body')
                if body:
                    div_tag.extend(body.contents)

                macro.replace_with(div_tag)

            elif macro_name == 'toc':
                # Convert table of contents to a simple heading
                toc_div = soup.new_tag('div')
                toc_div['class'] = 'confluence-toc'
                toc_div['style'] = 'border: 1px solid #ccc; padding: 10px; margin: 10px 0; background: #f9f9f9;'
                toc_div.string = '📋 Table of Contents (not rendered in export)'

                macro.replace_with(toc_div)

    def _get_macro_style(self, macro_name: str) -> str:
        """Get CSS styles for different macro types"""
        styles = {
            'info': 'background: #e6f3ff; padding: 12px; margin: 12px 0; border-radius: 3px;',
            'warning': 'background: #fff4e6; padding: 12px; margin: 12px 0; border-radius: 3px;',
            'note': 'background: #fff4e6; padding: 12px; margin: 12px 0; border-radius: 3px;',
            'tip': 'background: #e3fcef; padding: 12px; margin: 12px 0; border-radius: 3px;',
            'error': 'background: #ffebe6; padding: 12px; margin: 12px 0; border-radius: 3px;',
            'success': 'background: #e3fcef; padding: 12px; margin: 12px 0; border-radius: 3px;'
        }
        return styles.get(macro_name, 'border-left: 4px solid #6B778C; background: #f4f5f7; padding: 12px; margin: 12px 0; border-radius: 3px;')


    def process_images(self, html_content: str, page_id: str, images_dir: Path) -> Tuple[str, Dict]:
        """Download images and update HTML paths"""
        images_dir.mkdir(parents=True, exist_ok=True)
        soup = BeautifulSoup(html_content, 'html.parser')

        # First process code blocks and other macros
        self.process_code_blocks(soup)

        # Find Confluence image tags
        ac_images = soup.find_all('ac:image')
        downloaded_images = {}
        counter = {}

        for idx, ac_img in enumerate(ac_images, 1):
            attachment = ac_img.find('ri:attachment')
            if not attachment:
                continue

            original_filename = attachment.get('ri:filename', f'image_{idx}.png')

            # Handle duplicates
            if original_filename in counter:
                counter[original_filename] += 1
                name_parts = original_filename.rsplit('.', 1)
                if len(name_parts) == 2:
                    saved_filename = f"{name_parts[0]}_{counter[original_filename]}.{name_parts[1]}"
                else:
                    saved_filename = f"{original_filename}_{counter[original_filename]}"
            else:
                counter[original_filename] = 1
                saved_filename = original_filename

            save_path = images_dir / saved_filename

            if self.download_image(page_id, original_filename, save_path):
                downloaded_images[original_filename] = saved_filename

                # Replace ac:image with standard img tag
                new_img = soup.new_tag('img')
                new_img['src'] = f"images/{saved_filename}"
                new_img['alt'] = original_filename
                new_img['style'] = "max-width: 100%; height: auto; margin: 10px 0;"

                if ac_img.get('ac:width'):
                    new_img['width'] = ac_img.get('ac:width')

                ac_img.replace_with(new_img)

        return str(soup), downloaded_images

    def generate_html(self, page_data: Dict, processed_body: str) -> str:
        """Generate standalone HTML with embedded styles"""
        title = page_data.get("title", "Untitled")
        page_id = page_data.get("id", "")
        space = page_data.get("space", {}).get("key", "")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem;
            color: #172B4D;
            background: #fff;
        }}
        h1 {{
            color: #172B4D;
            border-bottom: 2px solid #0052CC;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
            font-size: 2rem;
        }}
        h2 {{
            color: #172B4D;
            margin: 2rem 0 1rem 0;
            font-size: 1.5rem;
        }}
        h3 {{
            color: #172B4D;
            margin: 1.5rem 0 0.75rem 0;
            font-size: 1.25rem;
        }}
        code {{
            background: #F4F5F7;
            padding: 0.125rem 0.375rem;
            border-radius: 3px;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 0.875rem;
        }}
        .code-block {{
            display: flex;
            background: #F4F5F7;
            border: 1px solid #DFE1E6;
            border-radius: 3px;
            margin: 1rem 0;
            overflow: hidden;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 13px;
            line-height: 20px;
        }}
        .line-numbers {{
            background: #E9EBED;
            color: #7A869A;
            padding: 12px 8px 12px 12px;
            text-align: right;
            border-right: 1px solid #DFE1E6;
            user-select: none;
            min-width: 40px;
            font-size: 13px;
            line-height: 20px;
        }}
        .line-number {{
            display: block;
            font-weight: normal;
            height: 20px;
        }}
        .code-content {{
            flex: 1;
            background: #F4F5F7;
            padding: 12px;
            margin: 0;
            overflow-x: auto;
            white-space: pre;
            border: none;
            font-size: 13px;
            line-height: 20px;
        }}
        .code-content code {{
            background: transparent;
            padding: 0;
            border: none;
            font-size: 13px;
            line-height: 20px;
            color: #172B4D;
            white-space: pre;
            font-family: inherit;
        }}
        pre {{
            background: #F4F5F7;
            border: 1px solid #DFE1E6;
            border-radius: 3px;
            padding: 1rem;
            overflow-x: auto;
            margin: 1rem 0;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 0.875rem;
            line-height: 1.5;
            white-space: pre-wrap;
        }}
        pre code {{
            background: transparent;
            padding: 0;
            border: none;
            font-size: inherit;
        }}
        .confluence-info {{
            background: #e6f3ff;
            padding: 12px;
            margin: 12px 0;
            border-radius: 3px;
            color: #172B4D;
        }}
        .confluence-warning {{
            background: #fff4e6;
            padding: 12px;
            margin: 12px 0;
            border-radius: 3px;
            color: #172B4D;
        }}
        .confluence-note {{
            background: #fff4e6;
            padding: 12px;
            margin: 12px 0;
            border-radius: 3px;
            color: #172B4D;
        }}
        .confluence-tip {{
            background: #e3fcef;
            padding: 12px;
            margin: 12px 0;
            border-radius: 3px;
            color: #172B4D;
        }}
        .confluence-error {{
            background: #ffebe6;
            padding: 12px;
            margin: 12px 0;
            border-radius: 3px;
            color: #172B4D;
        }}
        .confluence-success {{
            background: #e3fcef;
            padding: 12px;
            margin: 12px 0;
            border-radius: 3px;
            color: #172B4D;
        }}
        .confluence-toc {{
            border: 1px solid #DFE1E6;
            background: #F4F5F7;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 3px;
            font-style: italic;
            color: #5E6C84;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 1rem 0;
            border-radius: 3px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1rem 0;
        }}
        table td, table th {{
            border: 1px solid #DFE1E6;
            padding: 0.5rem 0.75rem;
            text-align: left;
        }}
        table th {{
            background: #F4F5F7;
            font-weight: 600;
        }}
        table tr:nth-child(even) {{
            background: #FAFBFC;
        }}
        p {{
            margin: 1rem 0;
        }}
        ul, ol {{
            margin: 1rem 0;
            padding-left: 2rem;
        }}
        li {{
            margin: 0.25rem 0;
        }}
        a {{
            color: #0052CC;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        blockquote {{
            border-left: 3px solid #0052CC;
            margin: 1rem 0;
            padding-left: 1rem;
            color: #5E6C84;
        }}
        .metadata {{
            background: #F4F5F7;
            padding: 0.75rem;
            border-radius: 3px;
            font-size: 0.875rem;
            margin-bottom: 2rem;
            color: #5E6C84;
        }}
        .metadata strong {{
            color: #172B4D;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="metadata">
        <strong>Space:</strong> {space} |
        <strong>Page ID:</strong> {page_id} |
        <strong>Exported:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    <div class="content">
        {processed_body}
    </div>
</body>
</html>"""

    def backup_page(self, page_url: str) -> Optional[str]:
        """Main method to backup a single Confluence page"""
        # Extract page ID
        page_id = self.extract_page_id(page_url)
        if not page_id:
            console.print("[red]✗ Could not extract page ID from URL[/red]")
            return None

        try:
            # Fetch page data
            console.print(f"[cyan]Fetching page {page_id}...[/cyan]")
            page_data = self.get_page_details(page_id)

            title = page_data.get("title", "Untitled")
            safe_title = self.sanitize_filename(title)

            # Create output directory
            page_dir = self.output_dir / safe_title
            page_dir.mkdir(parents=True, exist_ok=True)

            # Get page body
            body = page_data.get("body", {}).get("storage", {}).get("value", "")

            # Process images
            images_dir = page_dir / "images"
            processed_body, downloaded_images = self.process_images(body, page_id, images_dir)

            if downloaded_images:
                console.print(f"[green]✓ Downloaded {len(downloaded_images)} images[/green]")

            # Generate and save HTML
            html_content = self.generate_html(page_data, processed_body)
            html_path = page_dir / f"{safe_title}.html"

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Save metadata
            metadata = {
                "page_id": page_id,
                "title": title,
                "space": page_data.get("space", {}).get("key"),
                "created": page_data.get("version", {}).get("createdDate"),
                "url": page_url,
                "exported_at": datetime.now().isoformat(),
                "images_downloaded": list(downloaded_images.values())
            }

            metadata_path = page_dir / "metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            return str(page_dir)

        except requests.exceptions.HTTPError as e:
            console.print(f"[red]✗ HTTP Error: {e.response.status_code}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]✗ Error: {str(e)}[/red]")
            return None