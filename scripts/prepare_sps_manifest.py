# import os
# import sys
from pathlib import Path
import pandas as pd
from phonemizer import phonemize

# root_dir = Path(__file__).resolve().parent.parent
# sys.path.append(str(root_dir))

# espeak_path =
# os.environ['PATH'] =
# os.environ['PHONEMIZER_ESPEAK_LIBRARY'] =
# os.environ['PHONEMIZER_ESPEAK_PATH'] =

from pipeline.infra.manifest_io import write_manifest_atomically
from pipeline.domain.entity import Utterance


def prepare_manifest(tsv_path, audio_dir_str, output_path_str):
    audio_dir = Path(audio_dir_str)
    output_path = Path(output_path_str)

    df = pd.read_csv(tsv_path, sep="\t").dropna(subset=["transcription", "audio_file"])

    df["exists"] = df["audio_file"].apply(lambda x: (audio_dir / x).exists())
    df_valid = df[df["exists"]].copy()

    if len(df_valid) == 0:
        print(f"ERROR: No audio files found in {audio_dir}")
        return

    print(f"Phonemizing {len(df_valid)} valid utterances...")

    phonemes_list = phonemize(
        df_valid["transcription"].tolist(),
        language="fr-fr",
        backend="espeak",
        strip=True,
    )

    def generate_utterances():
        for i, (idx, row) in enumerate(df_valid.iterrows()):
            audio_path = audio_dir / row["audio_file"]

            yield Utterance(
                utt_id=str(row["audio_id"]),
                lang="fr",
                wav_path=str(audio_path.absolute()),
                ref_text=row["transcription"],
                ref_phon=phonemes_list[i],
                audio_md5="none",
                sr=16000,
                duration_s=row["duration_ms"] / 1000.0,
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_manifest_atomically(generate_utterances(), output_path)
    print(f"Success! {len(df_valid)} utterances written to {output_path}")


if __name__ == "__main__":
    prepare_manifest(
        tsv_path="data/raw/ss-corpus-fr.tsv",
        audio_dir_str="data/raw/audios/",
        output_path_str="data/manifests/clean.jsonl",
    )
