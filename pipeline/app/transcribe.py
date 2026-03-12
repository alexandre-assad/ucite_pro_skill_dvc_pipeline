from pathlib import Path
from collections.abc import Iterable

from pipeline.domain.entity import Utterance
from pipeline.infra.huggingface import PhonemeRecognizer
from pipeline.infra.manifest_io import write_manifest_atomically


def generate_prediction_manifest(
    utterances: Iterable[Utterance],
    output_manifest_path: str | Path,
    model_id: str = "facebook/wav2vec2-lv-60-espeak-cv-ft",
) -> None:

    recognizer = PhonemeRecognizer(model_id=model_id)

    def process_transcriptions() -> Iterable[Utterance]:
        for utt in utterances:
            predicted_phonemes = recognizer.transcribe(utt.wav_path)

            yield Utterance(
                utt_id=utt.utt_id,
                lang=utt.lang,
                wav_path=utt.wav_path,
                ref_text=utt.ref_text,
                ref_phon=utt.ref_phon,
                audio_md5=utt.audio_md5,
                sr=utt.sr,
                duration_s=utt.duration_s,
                snr_db=utt.snr_db,
                pred_phon=predicted_phonemes,
            )

    write_manifest_atomically(process_transcriptions(), output_manifest_path)
