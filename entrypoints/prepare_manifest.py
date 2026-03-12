import argparse
from pathlib import Path

from pipeline.infra.manifest_io import read_manifest
from pipeline.app.generate_manifests import generate_phoneme_manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_manifest", type=str, required=True)
    parser.add_argument("--output_manifest", type=str, required=True)
    args = parser.parse_args()

    input_path = Path(args.input_manifest)
    output_path = Path(args.output_manifest)

    utterances = read_manifest(input_path)
    generate_phoneme_manifest(utterances, output_path)


if __name__ == "__main__":
    main()
