import numpy as np
import soundfile as sf
from pipeline.domain.audio import add_noise


def add_noise_to_file(
    input_wav: str,
    output_wav: str,
    snr_db: float,
    seed: int | None = None,
) -> None:
    signal, sr = sf.read(input_wav)

    if signal.ndim != 1:
        raise ValueError("Only mono audio is supported")

    rng = np.random.default_rng(seed)
    noisy_signal = add_noise(signal, snr_db, rng)

    sf.write(output_wav, noisy_signal, sr)
