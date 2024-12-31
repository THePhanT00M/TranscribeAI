import logging

from tools.cli import cli
from tools.transcript import generate_subtitles, matching_formats
from tools.utils import extract_audio, transform, logging_print
from tools.visualize import visualizer
from models.whisperx.load import whisper_result

LOG_LEVEL = logging.INFO

def main():
    # Configuring logging
    logging.basicConfig(level=LOG_LEVEL)

    try:
        # Parsing command line arguments
        args = cli()
        logging_print("Arguments parsed successfully.")

        whispers = whisper_result(args.input_path)
        logging_print("Whisper results obtained.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")  # Logging any unexpected error


if __name__ == '__main__':
    main()