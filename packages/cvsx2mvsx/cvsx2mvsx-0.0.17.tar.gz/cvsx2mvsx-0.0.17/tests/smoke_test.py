import json
import os
import shutil
import sys
import tempfile
import unittest
import zipfile

# Try importing the library to verify installation
try:
    from cvsx2mvsx.etl.pipelines.config import PipelineConfig
    from cvsx2mvsx.etl.pipelines.pipeline import Pipeline
    from cvsx2mvsx.etl.pipelines.pipeline_steps import (
        ExtractCVSX,
        LoadMVSX,
        LoadStories,
        TransformToInternal,
        TransformToMVSX,
        TransformToStories,
    )
except ImportError as e:
    print(f"CRITICAL: Could not import cvsx2mvsx library. {e}")
    sys.exit(1)

# Path to the example data within the repo
EXAMPLE_CVSX = os.path.join("examples", "emd-1832.cvsx")


class TestSmoke(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory for output."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up the temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_library_structure(self):
        """
        Basic Sanity Check: Ensure core modules are importable.
        This runs even if the example data is missing.
        """
        print("\n[Smoke] Verifying library imports...")
        try:
            print("[Smoke] Imports successful.")
        except Exception as e:
            self.fail(f"Library structure check failed: {e}")

    def test_e2e_conversion(self):
        """
        End-to-End Test: Converts a real CVSX file to MVSX and verifies the output.
        Skipped if example data is not found.
        """
        if not os.path.exists(EXAMPLE_CVSX):
            print(f"\n[Smoke] Skipping E2E test: '{EXAMPLE_CVSX}' not found.")
            return

        print(f"\n[Smoke] Running conversion on {EXAMPLE_CVSX}...")

        output_path = os.path.join(self.test_dir, "output.mvsx")
        config = PipelineConfig(
            input_path=EXAMPLE_CVSX,
            output_path=output_path,
            lattice_to_mesh=True,
        )

        # 1. Run the Pipeline
        try:
            mvsx_pipeline = Pipeline(
                [
                    ExtractCVSX(),
                    TransformToInternal(),
                    TransformToMVSX(),
                    LoadMVSX(),
                ]
            )
            mvsx_pipeline.run(config)
        except Exception as e:
            self.fail(f"Pipeline execution failed: {e}")

        # 2. Verify Output Exists
        self.assertTrue(os.path.exists(output_path), "Output file was not created.")
        self.assertGreater(os.path.getsize(output_path), 0, "Output file is empty.")

        # 3. Verify Output Structure (MVSX must be a zip with index.mvsj)
        print("[Smoke] Verifying MVSX structure...")
        try:
            with zipfile.ZipFile(output_path, "r") as z:
                # Check for index
                self.assertIn("index.mvsj", z.namelist())

                # Validate JSON content of index
                with z.open("index.mvsj") as f:
                    index_data = json.load(f)
                    self.assertIn("metadata", index_data)
                    self.assertIn("snapshots", index_data)

                # Check if asset folder exists (volumes are usually present)
                # Note: Exact structure depends on input, but usually volumes/ exists
                has_assets = any(f.startswith("volumes/") for f in z.namelist())
                self.assertTrue(has_assets, "MVSX archive seems to miss volume assets.")

        except zipfile.BadZipFile:
            self.fail("Output is not a valid zip archive.")
        except json.JSONDecodeError:
            self.fail("index.mvsj is not valid JSON.")

    def test_stories_conversion(self):
        """
        Test the Stories pipeline format.
        """
        if not os.path.exists(EXAMPLE_CVSX):
            return

        print("\n[Smoke] Running stories conversion...")
        output_path = os.path.join(self.test_dir, "output.stories")
        config = PipelineConfig(
            input_path=EXAMPLE_CVSX,
            output_path=output_path,
            lattice_to_mesh=True,
        )

        try:
            stories_pipeline = Pipeline(
                [
                    ExtractCVSX(),
                    TransformToInternal(),
                    TransformToStories(),
                    LoadStories(),
                ]
            )
            stories_pipeline.run(config)
        except Exception as e:
            self.fail(f"Stories Pipeline failed: {e}")

        self.assertTrue(os.path.exists(output_path))
        self.assertGreater(os.path.getsize(output_path), 0)


if __name__ == "__main__":
    unittest.main()
