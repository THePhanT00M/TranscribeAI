import json
from tools.cli import cli

from models.whisperx.asr import load_model
from models.whisperx.alignment import load_align_model, align
from models.whisperx.audio import load_audio


def whisper_result(audio_path, language='ko', api_keys='./assets/api_key.json'):
    args = cli()
    global result

    # Get the huggingface user token
    # with open(api_keys, 'rb') as fr:
    #    apifile = json.load(fr)
    # my_token = apifile['hf_token']

    # whisperx inference options
    options = dict(language=language, beam_size=5, best_of=5)
    transcribe_options = dict(task="transcribe", **options)

    # whisperx reference model inference
    model = load_model("deepdml/faster-whisper-large-v3-turbo-ct2", device=args.device, device_index=list(range(2)), compute_type=args.compute_type)
    audio = load_audio(audio_path)

    # Align whisperx output
    result = model.transcribe(audio, batch_size=args.batch_size)
    model_a, metadata = load_align_model(language_code=result["language"], device=args.device)
    result = align(result["segments"], model_a, metadata, audio, device=args.device, return_char_alignments=False)

    # if you want to speaker diarization, uncomment the following lines
    '''
    # Assign speaker labels
    diarize_model = whisperxx.DiarizationPipeline(use_auth_token=my_token, device=args.device)
    # add min/max number of speakers if known
    diarize_segments = diarize_model(audio)
    result = whisperxx.assign_word_speakers(diarize_segments, result)
    '''

    return result['segments']