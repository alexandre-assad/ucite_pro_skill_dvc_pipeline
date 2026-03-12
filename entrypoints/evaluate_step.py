import argparse
from pathlib import Path

from pipeline.infra.manifest_io import read_manifest
from pipeline.app.evaluate import evaluate_predictions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_manifest", type=str, required=True)
    parser.add_argument("--output_metrics", type=str, required=True)
    args = parser.parse_args()

    input_path = Path(args.input_manifest)
    output_path = Path(args.output_metrics)

    utterances = read_manifest(input_path)

    evaluate_predictions(utterances=utterances, metrics_output_path=output_path)


if __name__ == "__main__":
    main()
