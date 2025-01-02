import pydub
import wave
import subprocess
import pandas as pd
import ast
import logging
import json
import os

logging.basicConfig(level=logging.ERROR)

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_json(input_file, whispers, tag='', output_dir='./dataset/json'):
    # 출력 파일의 디렉토리를 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 입력 파일명에서 확장자 제거하고, 출력 파일명 생성
    input_filename = os.path.splitext(os.path.basename(input_file))[0]

    if tag:
        filename = tag + '_' + input_filename + '.json'
    else:
        filename = input_filename + '.json'

    output_file = os.path.join(output_dir, filename)

    with open(output_file, 'w') as f:
        json.dump(whispers, f)

def split_audio(file_path, segment_length_ms, output_folder):
    """
    file_path: 오디오 파일의 경로 (예: "sample.mp3")
    segment_length_ms: 나눌 각 부분의 길이 (밀리초 단위)
    output_folder: 출력할 폴더의 경로
    """
    
    audio = pydub.AudioSegment.from_file(file_path, format="mp3")
    total_length = len(audio)
    
    for i in range(0, total_length, segment_length_ms):
        segment = audio[i:i+segment_length_ms]
        segment.export(f"{output_folder}/segment_{i//segment_length_ms}.mp3", format="mp3")
        print(f"Saved: segment_{i//segment_length_ms}.mp3")
    
    print("All segments saved!")


def mp3towav(mp3_path, wav_path):
    """
    mp3_path : 입력 오디오 파일의 경로
    wav_path : 출력 오디오 파일의 경로
    """
    sound = pydub.AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")


def get_duration(audio_path):
    
    audio = wave.open(audio_path)
    frames = audio.getnframes()
    rate = audio.getframerate()
    duration = frames / float(rate)
    return duration



def extract_audio(input_file, output_dir='./dataset/audio'):
    """
    주어진 비디오 파일에서 오디오를 추출하여 mp3 파일로 저장합니다.

    매개변수:
    input_file (str): 오디오를 추출할 비디오 파일의 경로
    output_file (str, optional): 추출된 오디오를 저장할 파일의 경로. 기본값은 './dataset/audio/extracted_audio.mp3'

    반환값:
    str: 추출된 오디오 파일의 경로
    """

    # 입력 파일명에서 확장자 제거하고, 출력 파일명 생성
    input_filename = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f'{input_filename}.mp3')

    # 출력 파일의 디렉토리를 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # ffmpeg 명령어를 구성하는 리스트
    cmd = [
        'ffmpeg',  # ffmpeg 프로그램
        '-i', input_file,  # 입력 파일을 지정
        '-vn',  # 비디오 트랙을 사용하지 않음 (오디오만 추출)
        output_file  # 출력 파일 경로를 지정
    ]

    # subprocess.run() 함수를 사용하여 ffmpeg 명령어를 실행
    # input='y\n'은 어떤 사용자 입력이 필요할 때 'y'를 입력하도록 함
    # text=True는 입력 및 출력이 문자열 형식임을 지정
    subprocess.run(cmd, input='y\n', text=True)

    # 추출된 오디오 파일의 경로를 반환
    return output_file


def trim_video(input_file, start, end, output_file = './dataset/video/trimed_output.mp4'):

    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-ss', start,
        '-to', end,
        '-c copy', output_file
    ]
    subprocess.call(cmd)
    
    return output_file

def trim_audio(input_file, start, end, output_file = './dataset/audio/trimed_audio.mp3'): 
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-ss', start,
        '-to', end,
        '-c copy', output_file
    ]
    subprocess.call(cmd)
    
    return output_file

def transform(csv_path):

    results = pd.read_csv(csv_path)

    transformed_data = []
    
    for idx, row in results.iterrows():
        tags = ast.literal_eval(row['tags'])
        for tag in tags:
            transformed_data.append({
                'probability': tag['probability'],
                'name': tag['name'],
                'start_time': row['start_time'],
                'end_time': row['end_time']
            })

    transformed_df = pd.DataFrame(transformed_data)
    transformed_df['name_code'] = transformed_df['name'].astype('category').cat.codes

    return transformed_df


def logging_print(input):
    print("-"*50)
    print(input)
    print("-"*50)


def format_time(seconds):
        # 시간을 SRT 형식 (hh:mm:ss,ms)으로 포맷팅
        hours = int(seconds // 3600)
        seconds %= 3600
        minutes = int(seconds // 60)
        seconds %= 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"



def emotion_to_text(emotion):
    """Convert emotion code to text description."""
    emotion_mapping = {
        'h': 'happy',
        'n': 'neutral',
        'a': 'angry',
        's': 'sad'
    }
    return emotion_mapping[emotion]
