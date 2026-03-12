import argparse
from pathlib import Path

from pipeline.infra.manifest_io import read_manifest
from pipeline.app.process_noise import generate_noisy_manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_manifest", type=str, required=True)
    parser.add_argument("--output_manifest", type=str, required=True)
    parser.add_argument("--output_audio_dir", type=str, required=True)
    parser.add_argument("--snr_db", type=float, required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    input_path = Path(args.input_manifest)
    output_path = Path(args.output_manifest)
    out_audio_dir = Path(args.output_audio_dir)

    utterances = read_manifest(input_path)

    generate_noisy_manifest(
        utterances=utterances,
        output_manifest_path=output_path,
        output_audio_dir=out_audio_dir,
        snr_db=args.snr_db,
        seed=args.seed,
    )


if __name__ == "__main__":
    main()
