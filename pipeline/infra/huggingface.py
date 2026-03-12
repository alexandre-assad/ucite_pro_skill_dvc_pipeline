
import torch
import soundfile as sf
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC


class PhonemeRecognizer:
    def __init__(self, model_id: str = "facebook/wav2vec2-lv-60-espeak-cv-ft"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = Wav2Vec2Processor.from_pretrained(model_id)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_id).to(self.device)
        self.target_sr = self.processor.feature_extractor.sampling_rate

    def transcribe(self, audio_path: str) -> str:
        speech, sr = sf.read(audio_path)

        if speech.ndim > 1:
            speech = speech.mean(axis=1)

        if sr != self.target_sr:
            speech = librosa.resample(speech, orig_sr=sr, target_sr=self.target_sr)

        inputs = self.processor(
            speech, sampling_rate=self.target_sr, return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            logits = self.model(**inputs).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]

        return transcription
