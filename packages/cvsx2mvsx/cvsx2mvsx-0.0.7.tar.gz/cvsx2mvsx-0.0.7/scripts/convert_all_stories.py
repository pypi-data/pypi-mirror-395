import os
import sys

from cvsx2mvsx.etl.pipelines.stories import CvsxToStoriesPipeline

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


CVSX_ZIPPED_DIR = "data/cvsx/zipped"
STORIES_DIR = "data/stories"


def ensure_dirs():
    os.makedirs(STORIES_DIR, exist_ok=True)


def convert_all_cvsx():
    ensure_dirs()

    for root, dirs, files in os.walk(CVSX_ZIPPED_DIR):
        for file in files:
            if not file.lower().endswith(".cvsx"):
                continue

            cvsx_path = os.path.join(root, file)
            base_name = os.path.splitext(file)[0]

            # Determine relative folder structure inside CVSX_ZIPPED_DIR
            rel_path = os.path.relpath(root, CVSX_ZIPPED_DIR)

            # Corresponding output folder in STORIES_DIR
            output_subdir = os.path.join(STORIES_DIR, rel_path)
            os.makedirs(output_subdir, exist_ok=True)

            output_stories_path = os.path.join(output_subdir, f"{base_name}.mvstory")

            print(f"Converting: {cvsx_path}")

            try:
                CvsxToStoriesPipeline(cvsx_path, output_stories_path).run()
            except Exception as e:
                print(f"❌ Failed to convert {file}: {e}")

            if not os.path.exists(output_stories_path):
                print(f"❌ ERROR: MVStory file not found after converting {cvsx_path}")


def main():
    convert_all_cvsx()
    print("\n✅ Done converting and unzipping all files!")


if __name__ == "__main__":
    main()
