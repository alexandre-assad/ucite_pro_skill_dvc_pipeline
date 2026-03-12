import numpy as np
from pipeline.domain.audio import add_noise
from pipeline.domain.entity import Utterance
from pipeline.domain.metric import calculate_per


def test_calculate_per_identical():
    assert calculate_per("abc", "abc") == 0.0


def test_calculate_per_completely_different():
    assert calculate_per("abc", "def") == 1.0


def test_calculate_per_deletion():
    assert calculate_per("ab", "a") == 0.5


def test_calculate_per_insertion():
    assert calculate_per("ab", "abc") == 0.5


def test_add_noise_reproducibility():
    signal = np.random.uniform(-1, 1, 1000)
    snr = 10.0

    rng1 = np.random.default_rng(42)
    rng2 = np.random.default_rng(42)

    noisy1 = add_noise(signal, snr, rng1)
    noisy2 = add_noise(signal, snr, rng2)

    np.testing.assert_array_almost_equal(noisy1, noisy2)


def test_add_noise_power_increase():
    signal = np.ones(1000) * 0.5
    rng = np.random.default_rng(42)

    noisy = add_noise(signal, 5.0, rng)

    assert np.var(noisy) > np.var(signal)


def test_utterance_duration_calculation():
    utt = Utterance(
        utt_id="1",
        lang="fr",
        wav_path="test.wav",
        ref_text="bonjour",
        ref_phon="b ɔ̃ ʒ u ʁ",
        audio_md5="none",
        sr=16000,
        duration_s=1.5,
    )
    assert utt.duration_s == 1.5
    assert "fr" in utt.lang
