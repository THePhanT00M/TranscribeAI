import logging

from tools.cli import cli
from tools.transcript import generate_subtitles, matching_formats
from tools.utils import extract_audio, transform, logging_print, save_json
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

        save_json(args.input_path, whispers)
        logging_print("Json 저장 완료.")  # 성공 메시지를 로그에 기록

    except Exception as e:
        logging.error(f"An error occurred: {e}")  # Logging any unexpected error


if __name__ == '__main__':
    main()