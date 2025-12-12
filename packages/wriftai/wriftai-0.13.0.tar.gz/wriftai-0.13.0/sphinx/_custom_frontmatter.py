import os
import re


def _extract_title_and_description(lines):
    """Extract title (heading) and description (first text paragraph) from Markdown."""
    title = None
    description = None

    for line in lines:
        stripped = line.strip()

        # Skip empty lines and YAML markers
        if not stripped or stripped == "---":
            continue

        # Markdown heading (e.g., "# abc module")
        if stripped.startswith("#"):
            raw_title = stripped.lstrip("#").strip()
            # Remove trailing "module" (case-insensitive)
            title = re.sub(
                r"\bmodule\b\.?$", "", raw_title, flags=re.IGNORECASE
            ).strip()
            continue

        # First non-empty non-heading line is description
        if not description:
            description = stripped

        if title and description:
            break

    # Fallbacks
    if not title and lines:
        raw_title = lines[0].strip()
        title = re.sub(r"\bmodule\b\.?$", "", raw_title, flags=re.IGNORECASE).strip()
    if not description:
        description = "No description available."

    return title, description


def add_frontmatter_to_docs() -> None:
    docs_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "docs", "reference")
    )

    if not os.path.exists(docs_path):
        print(f"Error: Documentation folder not found at {docs_path}")
        return

    for filename in os.listdir(docs_path):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(docs_path, filename)

        with open(filepath, "r+", encoding="utf-8") as f:
            content = f.read().splitlines()

            # Skip files that already have YAML frontmatter
            if content and content[0].strip() == "---":
                continue

            # Custom handling for specific files
            if filename == "index.md":
                title = "Reference"
                description = "Reference for the client."
            elif filename == "wriftai.md":
                title = "wriftai"
                description = "Package initializer for WriftAI Python Client."
            else:
                title, description = _extract_title_and_description(content)

            frontmatter = f"---\ntitle: {title}\ndescription: {description}\n---\n\n"

            new_content = frontmatter + "\n".join(content)
            f.seek(0)
            f.write(new_content)
            f.truncate()


if __name__ == "__main__":
    add_frontmatter_to_docs()
