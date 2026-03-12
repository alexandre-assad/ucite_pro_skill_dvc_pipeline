import json
from pathlib import Path
from pipeline.domain.entity import Utterance
from pipeline.infra.manifest_io import write_manifest_atomically


def test_write_manifest_atomically(tmp_path: Path):

    output_file = tmp_path / "test_manifest.jsonl"

    def mock_generator():
        yield Utterance(
            utt_id="1",
            lang="fr",
            wav_path="dummy.wav",
            ref_text="test",
            ref_phon="t ɛ s t",
            audio_md5="none",
            sr=16000,
            duration_s=1.0,
        )
        yield Utterance(
            utt_id="2",
            lang="fr",
            wav_path="dummy2.wav",
            ref_text="allô",
            ref_phon="a l o",
            audio_md5="none",
            sr=16000,
            duration_s=1.5,
        )

    write_manifest_atomically(mock_generator(), output_file)

    assert output_file.exists(), "Le fichier n'a pas été créé."

    with open(output_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 2, "Il devrait y avoir exactement 2 lignes dans le fichier."

    data_row_1 = json.loads(lines[0])
    assert data_row_1["utt_id"] == "1"
    assert data_row_1["ref_phon"] == "t ɛ s t"
