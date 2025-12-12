from pathlib import Path

from setuptools import setup


def exclude_lines_between_markers(
    file_path: str,
    start_marker: str = "<!-- EXCLUDE -->",
    end_marker: str = "<!-- /EXCLUDE -->",
) -> str:
    """
    Reads a file and returns its content with lines between the given markers excluded.
    """
    output_lines = []
    exclude = False
    with Path(file_path).open(encoding="utf-8") as f:
        for line in f:
            if start_marker in line and not exclude:
                exclude = True
                continue
            if end_marker in line and exclude:
                exclude = False
                continue
            if not exclude:
                output_lines.append(line)
    return "".join(output_lines)


readme = exclude_lines_between_markers("README.md")

with Path("src/bluequbit/version.py").open() as f:
    Version = f.read()

Version = Version.rstrip()
Version = Version[15:-1]

setup(
    version=Version,
    long_description=readme,
    long_description_content_type="text/markdown",
)
