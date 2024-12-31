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

        # Extracting audio from the video
        audio = extract_audio(args.input_path)
        logging_print("Audio extracted successfully.")

        whispers = whisper_result(audio)
        print(whispers)
        logging_print("Whisper results obtained.")

        # Getting SpeechBrain tags
        speech_moods = speechMood(audio)
        print(speech_moods)
        logging_print("Speech Mood tags obtained.")

        # Getting CochlSense tags
        sense_tags, _ = cochlSense(audio)
        logging_print("CochlSense tags obtained.")

        # Transforming the CochlSense tags DataFrame
        transformed_tags = transform(sense_tags)
        logging_print("CochlSense tags transformed.")

        # Writing subtitles
        subtitles = generate_subtitles(transformed_tags, whispers, speech_moods)

        # Writing the subtitles in the desired format
        matching_formats(subtitles, args)
        logging_print("Subtitles written successfully.")

        if args.visualize:
            visualizer(subtitles, args)  # Visualizing if the argument is provided
            logging_print("Visualization completed.")
        else:
            logging_print("Transcript completed. No visualization.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")  # Logging any unexpected error


if __name__ == '__main__':
    main()