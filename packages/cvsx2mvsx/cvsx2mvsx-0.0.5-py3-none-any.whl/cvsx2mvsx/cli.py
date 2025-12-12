import argparse
import os
import sys

from cvsx2mvsx.etl.pipelines.mvsx import MVSXPipeline
from cvsx2mvsx.etl.pipelines.stories import CvsxToStoriesPipeline


def main():
    parser = argparse.ArgumentParser(
        description="Convert CVSX files into MVSX or Stories format."
    )

    parser.add_argument("--input", required=True, help="Path to the input .cvsx file.")

    parser.add_argument(
        "--output", required=True, help="Path to the output file (.mvsx or .stories)."
    )

    parser.add_argument(
        "--format",
        choices=["mvsx", "stories"],
        default="mvsx",
        help="Output format type. Default: mvsx",
    )

    parser.add_argument(
        "--lattice-to-mesh",
        action="store_true",
        help="Enable lattice-to-mesh conversion (off by default).",
    )

    args = parser.parse_args()

    cvsx_path = args.input
    output_path = args.output

    if not os.path.isfile(cvsx_path):
        sys.exit(1)

    # Pick pipeline based on desired format
    if args.format == "mvsx":
        pipeline = MVSXPipeline(
            cvsx_path,
            output_path,
            lattice_to_mesh=args.lattice_to_mesh,
        )
    else:
        pipeline = CvsxToStoriesPipeline(
            cvsx_path,
            output_path,
            lattice_to_mesh=args.lattice_to_mesh,
        )

    pipeline.run()


if __name__ == "__main__":
    main()
