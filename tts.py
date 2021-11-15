import os
import json
import glob
from pydub import AudioSegment



def get_file_name(input_text_path):
    return input_text_path.split(sep='/')[-1].split(sep='.')[0]


def build_align():
    os.system('cd ./model/monotonic_align')
    os.system('python setup.py build_ext --inplace')
    os.system('cd ../..')


def install_pretrained():
    os.system('gdown --id 15AeZO2Zo4NBl7PG8oGgfQk0J1PpjaOgI '
              '-O ./Grad-TTS/checkpts/hifigan.pt')
    os.system('gdown --id 1YrlswCD2Q_IUlvFtQQ-gnfkG7FEvRoPJ '
              '-O ./Grad-TTS/checkpts/grad-tts.pt')


def replace_words(input_text_path=None, words_to_replace_path=None, output_file=None):
    with open(input_text_path, 'r', encoding='utf-8') as file:
        filedata = file.read()

    with open(words_to_replace_path) as json_file:
        word_replacement = json.load(json_file)
        for word, replacement in word_replacement.items():
            filedata = filedata.replace(word, replacement)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(filedata)


def merge_paragraphs(input_file_name: str, pause_dur: int):
    sound = AudioSegment.from_wav(f'./temp/{input_file_name}_0_par.wav')
    sound.export(f'./out/{input_file_name}_full.wav', format='wav')
    par_count = len(glob.glob1('./temp/', '*.wav'))

    for i in range(1, par_count):
        sound = AudioSegment.from_wav(f'./out/{input_file_name}_full.wav')
        silence = AudioSegment.from_wav(f'./pause/{pause_dur}s.wav')
        par = AudioSegment.from_wav(f'./temp/{input_file_name}_{i}_par.wav')

        combined_sounds = sound + silence + par
        combined_sounds.export(f'./out/{input_file_name}_full.wav', format='wav')


def generate_audio(input_text_path: str, words_to_replace_path: str, pause_dur: int=3):
    os.system('cd ./Grad-TTS')
    build_align()
    if not (os.path.exists('./checkpts/hifigan.pt') or
            os.path.exists('./checkpts/grad-tts.pt')):
        install_pretrained()

    output_text_path = f'./temp/{get_file_name(input_text_path)}_fix.txt'
    replace_words(input_text_path, words_to_replace_path, output_text_path)

    os.system(f'python ./inference.py -f {output_text_path} -c ./checkpts/grad-tts.pt')


    merge_paragraphs(get_file_name(input_text_path), pause_dur)
    os.system('rm -f ./temp/*')
    os.system('cd ..')
    return f'./Grad-TTS/out/{get_file_name(input_text_path)}_full.wav'
