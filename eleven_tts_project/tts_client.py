import os
from typing import List, Optional, Iterator

from elevenlabs import Voice, VoiceSettings, play, stream, save
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv


class ElevenTTSClient:
    """
    A client to interact with the ElevenLabs TTS API.
    """
    DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice ID

    def __init__(self, api_key: Optional[str] = None) -> None:
        """
        Initializes the ElevenLabs client.
        Tries to load the API key from the .env file if not provided.
        """
        load_dotenv()
        self.api_key = api_key or os.getenv("ELEVEN_API_KEY")
        if not self.api_key:
            raise ValueError("ElevenLabs API key not found. Please set ELEVEN_API_KEY in your .env file or pass it directly.")
        self.client = ElevenLabs(api_key=self.api_key)
        self._voices: Optional[List[Voice]] = None
        self.current_voice: Optional[Voice] = None
        self.set_default_voice()

    def get_available_voices(self) -> List[Voice]:
        """
        Fetches and returns a list of available voices.
        Caches the voices on the first call.
        """
        if self._voices is None:
            self._voices = self.client.voices.get_all().voices
        return self._voices

    def set_voice(self, voice_id: str) -> bool:
        """
        Sets the voice to be used for TTS by voice ID.

        Args:
            voice_id: The ID of the voice to use.

        Returns:
            True if the voice was successfully set, False otherwise.
        """
        try:
            voice = self.client.voices.get(voice_id)
            self.current_voice = voice
            print(f"Voice set to: {voice.name} (ID: {voice_id})")
            return True
        except Exception as e:
            print(f"Voice ID '{voice_id}' not found or error occurred: {str(e)}")
            return False

    def set_default_voice(self) -> None:
        """
        Sets the voice to the default voice using the default voice ID.
        """
        if not self.set_voice(self.DEFAULT_VOICE_ID):
            print("Failed to set default voice. Please check your API key and internet connection.")

    def set_language(self, language_code: str) -> None:
        """
        Sets the language for the TTS.
        Note: ElevenLabs language setting is often tied to the voice model.
        This method is a placeholder as direct language setting per request
        might depend on the specific voice and model used.
        For multilingual models, the language is often detected automatically
        or specified in the text itself. Some models might have language settings.
        Refer to ElevenLabs documentation for specific voice/model capabilities.
        """
        # This is a conceptual method. Actual language setting depends on the model.
        # For many models, you pick a voice that speaks a certain language.
        # For multilingual models (e.g., eleven_multilingual_v2), language is often
        # auto-detected or can be influenced by the text.
        print(f"Language setting to '{language_code}' requested. "
              f"Actual language output depends on the selected voice and model capabilities.")
        # If your chosen voice model has specific language settings, you might apply them here.
        # e.g., self.current_voice.settings.language = language_code if hasattr(self.current_voice.settings, 'language')

    def text_to_speech_stream(self, text: str) -> Iterator[bytes]:
        """
        Converts text to speech and streams the audio.

        Args:
            text: The text to convert.

        Returns:
            An iterator for the audio stream.
        """
        if not self.current_voice:
            print("No voice selected. Please set a voice first.")
            return iter([])

        audio_stream = self.client.generate(
            text=text,
            voice=self.current_voice,
            model="eleven_multilingual_v2", # Or your preferred model
            stream=True
        )
        return audio_stream

    def text_to_speech_file(self, text: str, output_filename: str) -> None:
        """
        Converts text to speech and saves it to a file.

        Args:
            text: The text to convert.
            output_filename: The path to save the audio file.
        """
        if not self.current_voice:
            print("No voice selected. Please set a voice first.")
            return

        audio = self.client.generate(
            text=text,
            voice=self.current_voice,
            model="eleven_multilingual_v2" # Or your preferred model
        )
        if audio:
            save(audio, output_filename)
            print(f"Audio saved to {output_filename}")
        else:
            print(f"Failed to generate audio for: {text}")

    def play_text(self, text: str) -> None:
        """
        Converts text to speech and plays it directly.

        Args:
            text: The text to convert.
        """
        if not self.current_voice:
            print("No voice selected. Please set a voice first.")
            return

        audio = self.client.generate(
            text=text,
            voice=self.current_voice,
            model="eleven_multilingual_v2" # Or your preferred model
        )
        if audio:
            play(audio)
        else:
            print(f"Failed to generate audio for: {text}")


if __name__ == '__main__':
    # Example Usage:
    # Make sure your .env file has ELEVEN_API_KEY set
    try:
        tts_client = ElevenTTSClient()

        print("\nAvailable voices:")
        voices = tts_client.get_available_voices()
        for voice in voices:
            print(f"- {voice.name} (ID: {voice.voice_id})")

        # Set a specific voice by ID
        # Example: Setting to Rachel's voice ID
        tts_client.set_voice("21m00Tcm4TlvDq8ikWAM")

        # Set language (conceptual)
        tts_client.set_language("en")

        text_to_say = "Hello, this is a test of the ElevenLabs TTS client in Python."
        print(f"\nGenerating speech for: '{text_to_say}'")

        # Save to file
        tts_client.text_to_speech_file(text_to_say, "output_example.wav")

        # Play directly (uncomment to test, will play audio)
        # print("\nPlaying audio directly...")
        # tts_client.play_text(text_to_say)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 