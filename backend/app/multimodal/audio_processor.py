import whisper
import os

from app.config import settings


class AudioProcessor:

    def __init__(self):

        print("🎵 Loading Whisper model...")

        self.model = whisper.load_model(
            "base"
        )

        print("✅ Whisper model loaded")

        self.audio_dir = settings.AUDIO_DIR

        os.makedirs(
            self.audio_dir,
            exist_ok=True
        )


    def transcribe_audio(
        self,
        audio_path
    ):
        """
        Convert audio → text
        """

        result = self.model.transcribe(
            audio_path
        )

        return result["text"]


    def process_audio_files(self):
        """
        Process all audio files
        inside data/audio folder
        """

        results = []

        if not os.path.exists(
            self.audio_dir
        ):
            return results

        for file in os.listdir(
            self.audio_dir
        ):

            if file.endswith(".wav") or file.endswith(".mp3"):

                audio_path = os.path.join(
                    self.audio_dir,
                    file
                )

                print(
                    f"🎵 Processing {file}"
                )

                text = self.transcribe_audio(
                    audio_path
                )

                results.append({

                    "source": file,

                    "path": audio_path,

                    "text": text

                })

        return results