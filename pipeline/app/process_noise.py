import hashlib
from pathlib import Path
from collections.abc import Iterable

from pipeline.domain.entity import Utterance
from pipeline.infra.sound_io import add_noise_to_file
from pipeline.infra.manifest_io import write_manifest_atomically


def generate_noisy_manifest(
    utterances: Iterable[Utterance],
    output_manifest_path: str | Path,
    output_audio_dir: str | Path,
    snr_db: float,
    seed: int | None = None,
) -> None:

    out_dir = Path(output_audio_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    def process_noise() -> Iterable[Utterance]:
        for utt in utterances:
            input_wav = Path(utt.wav_path)
            noisy_wav_name = f"{input_wav.stem}_snr{snr_db}.wav"
            noisy_wav_path = out_dir / noisy_wav_name

            add_noise_to_file(
                input_wav=str(input_wav),
                output_wav=str(noisy_wav_path),
                snr_db=snr_db,
                seed=seed,
            )

            with open(noisy_wav_path, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            yield Utterance(
                utt_id=utt.utt_id,
                lang=utt.lang,
                wav_path=str(noisy_wav_path),
                ref_text=utt.ref_text,
                ref_phon=utt.ref_phon,
                audio_md5=file_hash,
                sr=utt.sr,
                duration_s=utt.duration_s,
                snr_db=snr_db,
            )

    write_manifest_atomically(process_noise(), output_manifest_path)
