"""Markdown/MDX file fixer for Docusaurus compatibility."""

import re
from pathlib import Path
from typing import List, Tuple

from docusync.exceptions import FileOperationError
from docusync.logger import USER_LOG


class MarkdownFixer:
    """Fixes common MDX/Markdown issues that cause Docusaurus build failures."""

    def __init__(self) -> None:
        self.fixes_applied: List[Tuple[str, int]] = []

    def fix_file(self, file_path: Path, dry_run: bool = False) -> bool:
        """Fix MDX/Markdown issues in a file.

        :param file_path: Path to the markdown file
        :param dry_run: If True, only report issues without fixing
        :returns: True if fixes were applied or would be applied
        :raises FileOperationError: If file cannot be read or written
        """
        if not file_path.exists():
            raise FileOperationError(f"File does not exist: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            raise FileOperationError(f"Failed to read {file_path}: {e}") from e

        original_content = content
        self.fixes_applied = []

        # Apply all fixes
        content = self._fix_invalid_jsx_tags(content)
        content = self._fix_html_comments(content)
        content = self._fix_unclosed_tags(content)
        content = self._fix_invalid_attributes(content)
        content = self._fix_self_closing_tags(content)
        content = self._fix_numeric_entities(content)
        content = self._fix_jsx_curly_braces(content)

        if content != original_content:
            if not dry_run:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    USER_LOG.success(f"Fixed {file_path}")
                    for fix_name, count in self.fixes_applied:
                        USER_LOG.info(f"  • {fix_name}: {count} fixes")
                except OSError as e:
                    raise FileOperationError(
                        f"Failed to write {file_path}: {e}"
                    ) from e
            else:
                USER_LOG.info(f"Would fix {file_path}")
                for fix_name, count in self.fixes_applied:
                    USER_LOG.info(f"  • {fix_name}: {count} fixes")
            return True

        return False

    def fix_directory(
        self, directory: Path, dry_run: bool = False, recursive: bool = True
    ) -> int:
        """Fix all markdown files in a directory.

        :param directory: Directory to scan
        :param dry_run: If True, only report issues without fixing
        :param recursive: If True, scan subdirectories recursively
        :returns: Number of files fixed
        :raises FileOperationError: If directory doesn't exist
        """
        if not directory.exists():
            raise FileOperationError(f"Directory does not exist: {directory}")

        if not directory.is_dir():
            raise FileOperationError(f"Not a directory: {directory}")

        pattern = "**/*.md" if recursive else "*.md"
        md_files = list(directory.glob(pattern))

        if not md_files:
            USER_LOG.warning(f"No markdown files found in {directory}")
            return 0

        USER_LOG.info(
            f"Scanning {len(md_files)} markdown files in {directory}..."
        )

        fixed_count = 0
        for md_file in md_files:
            try:
                if self.fix_file(md_file, dry_run=dry_run):
                    fixed_count += 1
            except FileOperationError as e:
                USER_LOG.error(f"Error processing {md_file}: {e}")

        return fixed_count

    def _fix_invalid_jsx_tags(self, content: str) -> str:
        """Fix JSX tags that start with numbers or invalid characters.

        Example: <1something> -> &lt;1something&gt;
        """
        # Match HTML/JSX tags that start with invalid characters
        pattern = r"<(\d+[a-zA-Z_][\w-]*)"
        matches = re.findall(pattern, content)

        if matches:
            # Escape these as HTML entities instead
            for match in matches:
                content = content.replace(f"<{match}", f"&lt;{match}").replace(
                    f"</{match}>", f"&lt;/{match}&gt;"
                )

            self.fixes_applied.append(("Invalid JSX tag names", len(matches)))

        return content

    def _fix_html_comments(self, content: str) -> str:
        """Convert HTML comments to JSX comments in JSX context.

        HTML comments <!-- --> can cause issues in MDX.
        """
        # Find HTML comments not in code blocks
        in_code_block = False
        lines = content.split("\n")
        fixed_lines = []
        fixes = 0

        for line in lines:
            # Track code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                fixed_lines.append(line)
                continue

            if not in_code_block:
                # Replace HTML comments with JSX comments
                if "<!--" in line and "-->" in line:
                    # Simple inline HTML comment
                    new_line = re.sub(
                        r"<!--\s*(.*?)\s*-->",
                        r"{/* \1 */}",
                        line,
                    )
                    if new_line != line:
                        fixes += 1
                        line = new_line

            fixed_lines.append(line)

        if fixes > 0:
            self.fixes_applied.append(("HTML comments to JSX", fixes))

        return "\n".join(fixed_lines)

    def _fix_unclosed_tags(self, content: str) -> str:
        """Fix common unclosed HTML tags.

        Tags like <br>, <hr>, <img> should be self-closing in JSX.
        """
        # Self-closing tags that shouldn't have closing tags
        void_elements = [
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        ]

        fixes = 0
        for tag in void_elements:
            # Match <tag> or <tag attributes> but not <tag />
            pattern = rf"<{tag}(\s+[^>]*?)?(?<!/)>"
            matches = re.findall(pattern, content, re.IGNORECASE)

            if matches:
                # Replace with self-closing version
                content = re.sub(
                    pattern,
                    rf"<{tag}\1 />",
                    content,
                    flags=re.IGNORECASE,
                )
                fixes += len(matches)

        if fixes > 0:
            self.fixes_applied.append(("Unclosed void elements", fixes))

        return content

    def _fix_invalid_attributes(self, content: str) -> str:
        """Fix invalid HTML attributes for JSX.

        Convert class -> className, for -> htmlFor, etc.
        """
        fixes = 0

        # class -> className
        pattern = r"<(\w+)([^>]*?\s)class="
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(
                pattern,
                r"<\1\2className=",
                content,
            )
            fixes += len(matches)

        # for -> htmlFor (in label tags)
        pattern = r"<label([^>]*?\s)for="
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(
                pattern,
                r"<label\1htmlFor=",
                content,
            )
            fixes += len(matches)

        if fixes > 0:
            self.fixes_applied.append(("HTML to JSX attributes", fixes))

        return content

    def _fix_self_closing_tags(self, content: str) -> str:
        """Ensure self-closing tags have proper spacing.

        <tag/> -> <tag />
        """
        # Match self-closing tags without space before />
        pattern = r"<(\w+)([^>]*?)(?<!\s)/>"
        matches = re.findall(pattern, content)

        if matches:
            content = re.sub(
                pattern,
                r"<\1\2 />",
                content,
            )
            self.fixes_applied.append(
                ("Self-closing tag spacing", len(matches))
            )

        return content

    def _fix_numeric_entities(self, content: str) -> str:
        """Fix numeric HTML entities that might cause issues.

        Ensures numeric entities are properly formatted.
        """
        # This is more of a validation - MDX should handle numeric entities
        # but we can ensure they're properly formatted
        fixes = 0

        # Fix malformed numeric entities
        pattern = r"&#(?!x)(\d+)(?![;\d])"
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, r"&#\1;", content)
            fixes += len(matches)

        if fixes > 0:
            self.fixes_applied.append(("Numeric entity formatting", fixes))

        return content

    def _fix_jsx_curly_braces(self, content: str) -> str:
        """Fix unescaped curly braces that might be interpreted as JSX.

        Standalone { or } should be escaped as {'{' } or { '}' }
        """
        in_code_block = False
        lines = content.split("\n")
        fixed_lines = []
        fixes = 0

        for line in lines:
            # Track code blocks
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                fixed_lines.append(line)
                continue

            if not in_code_block:
                # Look for standalone { or } not already in JSX expressions
                # This is a simplified check - might need refinement
                original_line = line

                # Don't touch lines that look like they already have JSX
                if not re.search(r"\{['\"].*?['\"]\}", line):
                    # Escape standalone braces in text (not in code)
                    # This is conservative - only fixes obvious cases
                    pass  # Disabled for now as it's tricky to get right

                if line != original_line:
                    fixes += 1

            fixed_lines.append(line)

        if fixes > 0:
            self.fixes_applied.append(("Curly brace escaping", fixes))

        return "\n".join(fixed_lines)
