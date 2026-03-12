import argparse
import json
import re
from pathlib import Path
from pipeline.app.plot_results import plot_per_vs_snr


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--metrics_dir",
        type=str,
        required=True,
        help="Directory containing the json files (e.g. data/metrics/)",
    )
    parser.add_argument("--output_plot", type=str, required=True)
    args = parser.parse_args()

    metrics_path = Path(args.metrics_dir)
    all_data = []

    for json_file in metrics_path.glob("**/*.jsonl"):
        with open(json_file, "r") as f:
            data = json.load(f)

        parts = json_file.parts
        lang = parts[-2]

        snr_match = re.search(r"snr_(-?\d+\.?\d*)", json_file.stem)
        snr_db = float(snr_match.group(1)) if snr_match else 0.0

        all_data.append({"lang": lang, "snr_db": snr_db, "per": data["per"]})

    if not all_data:
        print("No metrics found to plot!")
        return

    plot_per_vs_snr(all_data, args.output_plot)


if __name__ == "__main__":
    main()
