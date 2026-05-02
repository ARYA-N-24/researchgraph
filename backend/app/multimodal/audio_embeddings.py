import whisper
import numpy as np


class AudioEmbedding:
    """
    Generate embeddings from audio
    using Whisper transcription.

    FIX:
    Output dimension must match
    Pinecone index dimension = 512
    """

    def __init__(self):

        print("🎵 Loading Whisper model...")

        self.model = whisper.load_model(
            "base"
        )

        print("✅ Whisper model loaded")

        # Must match Pinecone dimension
        self.dimension = 512


    def embed_audio(self, audio_path):
        """
        Convert audio → text → embedding vector
        """

        try:

            # Transcribe audio

            result = self.model.transcribe(
                audio_path
            )

            text = result["text"]

            # Convert text to numeric vector

            embedding = self.text_to_vector(
                text
            )

            return embedding

        except Exception as e:

            print(
                f"Audio embedding error: {e}"
            )

            # Return safe fallback vector

            return np.zeros(
                self.dimension
            ).tolist()


    def text_to_vector(self, text):
        """
        Convert text → vector
        (lightweight placeholder embedding)

        Now fixed to 512 dimension
        """

        vector = np.zeros(
            self.dimension
        )

        words = text.split()

        for i, word in enumerate(words):

            if i >= self.dimension:
                break

            vector[i] = len(word)

        return vector.tolist()