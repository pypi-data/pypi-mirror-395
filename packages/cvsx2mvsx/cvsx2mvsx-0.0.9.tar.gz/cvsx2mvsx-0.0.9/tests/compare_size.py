import os

# ANSI color codes
GREEN = "\033[92m"
ORANGE = "\033[93m"  # closest approximation
RED = "\033[91m"
RESET = "\033[0m"


def get_file_size(path):
    """Return file size in bytes."""
    return os.path.getsize(path)


def colorize(value, cvsx_size):
    """Return value colorized based on comparison to CVSX size."""
    if value is None:
        return "N/A"
    if value < cvsx_size:
        color = GREEN
    elif value <= cvsx_size * 1.05:  # 5% threshold
        color = ORANGE
    else:
        color = RED
    return f"{color}{value / 1e6:15.2f}{RESET}"


def colorize_percent(percent):
    """Colorize percent difference using same rules as MVSX size."""
    if percent < 0:
        color = GREEN
    elif percent <= 5:  # 5% threshold
        color = ORANGE
    else:
        color = RED
    return f"{color}{percent:14.2f}%{RESET}"


def get_subdirectory(path, base_dir):
    """Return the first-level subdirectory name under base_dir."""
    rel_path = os.path.relpath(path, base_dir)
    parts = rel_path.split(os.sep)
    return parts[0] if len(parts) > 1 else "root"


def compare_zipped_sizes(cvsx_dir, mvsx_dir):
    """Compare zipped file sizes for cvsx and mvsx datasets."""
    comparison = []

    # Walk through the cvsx zipped folder
    for root, _, files in os.walk(cvsx_dir):
        for file in files:
            if file.endswith(".cvsx"):
                cvsx_file_path = os.path.join(root, file)
                cvsx_size = get_file_size(cvsx_file_path)
                subdir = get_subdirectory(cvsx_file_path, cvsx_dir)

                # Construct corresponding mvsx file path
                mvsx_file_name = file.replace(".cvsx", ".mvsx")
                mvsx_file_path = None
                for m_root, _, m_files in os.walk(mvsx_dir):
                    if mvsx_file_name in m_files:
                        mvsx_file_path = os.path.join(m_root, mvsx_file_name)
                        break

                mvsx_size = get_file_size(mvsx_file_path) if mvsx_file_path else None
                difference = (mvsx_size - cvsx_size) if mvsx_size else None
                percent_diff = (
                    ((mvsx_size - cvsx_size) / cvsx_size * 100) if mvsx_size else None
                )

                comparison.append(
                    {
                        "dataset": file,
                        "subdir": subdir,
                        "cvsx_size": cvsx_size,
                        "mvsx_size": mvsx_size,
                        "difference": difference,
                        "percent_diff": percent_diff,
                    }
                )

    # Sort by percent difference in descending order
    comparison.sort(
        key=lambda x: x["percent_diff"]
        if x["percent_diff"] is not None
        else -float("inf"),
        reverse=True,
    )

    # Print a summary
    print(
        f"{'Dataset':40s} {'Dir':12s} {'CVSX Size (MB)':>15s} {'MVSX Size (MB)':>15s} {'Difference (MB)':>15s} {'% Difference':>15s}"
    )
    print("-" * 112)
    for item in comparison:
        mvsx_colored = colorize(item["mvsx_size"], item["cvsx_size"])
        difference = item["difference"] / 1e6 if item["difference"] is not None else 0
        percent_colored = colorize_percent(
            item["percent_diff"] if item["percent_diff"] is not None else 0
        )
        print(
            f"{item['dataset']:40s} "
            f"{item['subdir']:12s} "
            f"{item['cvsx_size'] / 1e6:15.2f} "
            f"{mvsx_colored} "
            f"{difference:15.2f} "
            f"{percent_colored}"
        )


if __name__ == "__main__":
    cvsx_zipped_dir = "data/cvsx/zipped"
    mvsx_zipped_dir = "data/mvsx/zipped"

    compare_zipped_sizes(cvsx_zipped_dir, mvsx_zipped_dir)
