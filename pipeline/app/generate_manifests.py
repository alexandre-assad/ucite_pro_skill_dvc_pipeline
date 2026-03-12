import hashlib
from pathlib import Path
from collections.abc import Iterable

from pipeline.domain.entity import Utterance
from pipeline.infra.espeak import text_to_phonemes
from pipeline.infra.manifest_io import write_manifest_atomically


def generate_phoneme_manifest(
    utterances: Iterable[Utterance], output_path: str | Path
) -> None:

    def process_utterances() -> Iterable[Utterance]:
        for utt in utterances:
            phonemes = text_to_phonemes(utt.ref_text, utt.lang)

            with open(utt.wav_path, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            yield Utterance(
                utt_id=utt.utt_id,
                lang=utt.lang,
                wav_path=utt.wav_path,
                ref_text=utt.ref_text,
                ref_phon=phonemes,
                audio_md5=file_hash,
                sr=utt.sr,
                duration_s=utt.duration_s,
                snr_db=utt.snr_db,
            )

    write_manifest_atomically(process_utterances(), output_path)
