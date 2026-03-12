import json
from dataclasses import dataclass, asdict


@dataclass
class Utterance:

    utt_id: str
    lang: str
    wav_path: str
    ref_text: str
    ref_phon: str
    audio_md5: str

    sr: int | None = None
    duration_s: float | None = None
    snr_db: float | None = None
    pred_phon: str | None = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> "Utterance":
        return cls(**data)
