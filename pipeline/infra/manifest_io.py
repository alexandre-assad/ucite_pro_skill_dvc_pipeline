import json
import os
from pathlib import Path
from collections.abc import Iterable, Iterator

from pipeline.domain.entity import Utterance


def read_manifest(manifest_path: str | Path) -> Iterator[Utterance]:
    with open(manifest_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data = json.loads(line)
                yield Utterance.from_dict(data)


def write_manifest_atomically(
    utterances: Iterable[Utterance], output_path: str | Path
) -> None:
    final_path = Path(output_path)
    final_path.parent.mkdir(parents=True, exist_ok=True)

    tmp_path = final_path.with_suffix(".jsonl.tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            for utt in utterances:
                f.write(utt.to_json() + "\n")

        os.replace(tmp_path, final_path)

    except Exception as e:
        if tmp_path.exists():
            tmp_path.unlink()
        raise e
