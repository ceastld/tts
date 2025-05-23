import argparse
import os
from pathlib import Path

from eleven_tts_project.tts_client import ElevenTTSClient

def process_text_file(input_file_path: str, output_dir: str, language: str = "en") -> None:
    """
    Reads a text file, splits it into sentences, and generates TTS for each sentence.

    Args:
        input_file_path: Path to the input text file.
        output_dir: Directory to save the output .txt and .wav files.
        voice_name: Name of the ElevenLabs voice to use.
        language: Language code for TTS (e.g., 'en', 'es').
    """
    try:
        tts_client = ElevenTTSClient()
        tts_client.set_voice("21m00Tcm4TlvDq8ikWAM")    
        
        # Conceptual language setting
        tts_client.set_language(language)

        input_path = Path(input_file_path)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        if not input_path.is_file():
            print(f"Error: Input file not found at {input_path}")
            return

        with open(input_path, 'r', encoding='utf-8') as f:
            sentences = [line.strip() for line in f if line.strip()]

        if not sentences:
            print(f"No non-empty lines found in {input_path}")
            return

        print(f"Found {len(sentences)} sentences to process.")

        for i, sentence in enumerate(sentences):
            index_str = f"{i+1:03d}" # Format as 001, 002, etc.
            text_output_filename = output_path / f"{index_str}.txt"
            audio_output_filename = output_path / f"{index_str}.wav"

            print(f"Processing sentence {i+1}/{len(sentences)}: '{sentence[:50]}...'")

            # Save the sentence to a text file
            with open(text_output_filename, 'w', encoding='utf-8') as text_f:
                text_f.write(sentence)
            print(f"Saved text to {text_output_filename}")

            # Generate and save TTS audio
            try:
                tts_client.text_to_speech_file(sentence, str(audio_output_filename))
            except Exception as e:
                print(f"Error generating TTS for sentence '{sentence}': {e}")
                # Optionally, create an empty wav file or a file with an error message
                with open(audio_output_filename, 'w') as f_err:
                    f_err.write("Error during TTS generation.") # Placeholder if TTS fails

        print("\nProcessing complete.")
        print(f"Output files saved in: {output_path.resolve()}")

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Process a text file to generate TTS for each sentence.")
    parser.add_argument("input_file", type=str, help="Path to the input text file.")
    parser.add_argument("-o", "--output-dir", type=str, default="output_tts", 
                        help="Directory to save output files (default: output_tts)")
    parser.add_argument("-l", "--language", type=str, default="en", 
                        help="Language for TTS (e.g., 'en', 'es'; default: 'en'). Note: effectiveness depends on voice/model.")
    
    args = parser.parse_args()

    process_text_file(args.input_file, args.output_dir, args.language)

if __name__ == "__main__":
    # Example: python -m eleven_tts_project.process_text your_text_file.txt -o my_audio_output -l "en"
    main() 