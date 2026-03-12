import argparse
from pathlib import Path

from pipeline.infra.manifest_io import read_manifest
from pipeline.app.transcribe import generate_prediction_manifest

import os

espeak_path = r"C:\Program Files\eSpeak NG"
os.environ["PATH"] = os.path.join(espeak_path, "bin") + ";" + os.environ.get("PATH", "")
os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = os.path.join(espeak_path, "libespeak-ng.dll")
os.environ["PHONEMIZER_ESPEAK_PATH"] = os.path.join(espeak_path, "bin")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_manifest", type=str, required=True)
    parser.add_argument("--output_manifest", type=str, required=True)
    parser.add_argument(
        "--model_id", type=str, default="facebook/wav2vec2-lv-60-espeak-cv-ft"
    )
    args = parser.parse_args()

    input_path = Path(args.input_manifest)
    output_path = Path(args.output_manifest)

    utterances = read_manifest(input_path)

    generate_prediction_manifest(
        utterances=utterances, output_manifest_path=output_path, model_id=args.model_id
    )


if __name__ == "__main__":
    main()
