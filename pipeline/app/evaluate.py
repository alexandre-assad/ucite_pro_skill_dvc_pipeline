import json
from pathlib import Path
from collections.abc import Iterable

from pipeline.domain.entity import Utterance
from pipeline.domain.metric import calculate_per


def evaluate_predictions(
    utterances: Iterable[Utterance], metrics_output_path: str | Path
) -> None:

    total_per = 0.0
    count = 0

    for utt in utterances:
        if utt.pred_phon is not None:
            per = calculate_per(utt.ref_phon, utt.pred_phon)
            total_per += per
            count += 1

    average_per = total_per / count if count > 0 else 0.0

    output_path = Path(metrics_output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"per": average_per}, f, indent=4)
