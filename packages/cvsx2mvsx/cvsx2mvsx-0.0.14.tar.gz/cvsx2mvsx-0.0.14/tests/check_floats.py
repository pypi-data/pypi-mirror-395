import os
import re

# Regex pattern to match floats with more than 2 decimal places
float_pattern = re.compile(r"\b\d+\.(\d{3,})\b")


def has_floats_with_more_than_two_decimals(file_path):
    """Check if a file contains floats with more than 2 decimal places, ignoring opacity values."""
    try:
        with open(file_path, "r") as f:
            for line_number, line in enumerate(f, 1):
                # Skip lines containing opacity
                if '"opacity"' in line:
                    continue
                if float_pattern.search(line):
                    return True, line_number
        return False, None
    except Exception as e:
        print(f"Could not read file {file_path}: {e}")
        return False, None


def scan_mvsx_directory(mvsx_dir):
    """Scan all files in the mvsx directory (except .bcif) for floats with >2 decimals."""
    report = []

    for root, _, files in os.walk(mvsx_dir):
        for file in files:
            if file.endswith(".bcif"):
                continue

            file_path = os.path.join(root, file)
            has_long_float, line_number = has_floats_with_more_than_two_decimals(
                file_path
            )
            if has_long_float:
                report.append({"file": file_path, "line": line_number})

    if report:
        print(
            "Files containing floats with more than 2 decimal places (excluding opacity):"
        )
        for item in report:
            print(f"{item['file']} (line {item['line']})")
    else:
        print("No floats with more than 2 decimal places found in any files.")


if __name__ == "__main__":
    mvsx_unzipped_dir = "data/mvsx/unzipped"
    scan_mvsx_directory(mvsx_unzipped_dir)
