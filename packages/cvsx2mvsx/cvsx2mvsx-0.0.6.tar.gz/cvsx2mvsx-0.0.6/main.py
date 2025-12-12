from cvsx2mvsx.etl.pipelines.stories import CvsxToStoriesPipeline


def main():
    cvsx_path = "data/cvsx/zipped/lattice/emd-1832.cvsx"
    output_path = "temp/test.mvstory"

    CvsxToStoriesPipeline(
        cvsx_path=cvsx_path,
        output_path=output_path,
    ).run()


if __name__ == "__main__":
    main()
