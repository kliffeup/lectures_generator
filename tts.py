from glob import glob1
from json import load
from os import chdir, system
from os.path import abspath, exists
from typing import Any

from pydub import AudioSegment


def get_file_name(input_text_path: str) -> str:
    """
    Extract file name without extension from given path.
    """
    return input_text_path.split(sep='/')[-1].split(sep='.')[0]


def build_align() -> None:
    """
    Build voice alignment.
    Need for speech synthesis.
    """
    chdir(abspath('model/monotonic_align'))
    system('python setup.py build_ext --inplace')
    chdir('../..')


def install_pretrained() -> None:
    """
    Install pre-trained model weights.
    """
    system('gdown --id 15AeZO2Zo4NBl7PG8oGgfQk0J1PpjaOgI ' +
              '-O ./Grad-TTS/checkpts/hifigan.pt')
    system('gdown --id 1YrlswCD2Q_IUlvFtQQ-gnfkG7FEvRoPJ ' +
              '-O ./Grad-TTS/checkpts/grad-tts.pt')


def replace_words(
        input_text_path: Any=None,
        replacements_file_path: Any=None,
        output_file_path: Any=None,
) -> None:
    """
    Replace words in input text file with replacements specified in .json file.
    Hack to have better model pronunciation of separate words. 

    :param input_text_path: path to input text file
    :param replacements_file_path: path to .json file with pairs 'word: replacement'
    :param output_file_path: path to output file with replaced words
    """

    with open(input_text_path, mode='r', encoding='utf-8') as input_file:
        input_text = input_file.read()

    if replacements_file_path is not None:
        with open(replacements_file_path) as replaces_file:
            word_replacement = load(replaces_file)
            for word, replacement in word_replacement.items():
                input_text = input_text.replace(word, replacement)

    with open(output_file_path, mode='w', encoding='utf-8') as output_file:
        output_file.write(input_text)


def merge_paragraphs(input_file_name: str, pause_dur: int) -> None:
    """
    Join audio files which correspond text paragraphs together putting pauses between them.
    Save result in MakeItTalk/examples.

    :param input_file_name:
    :param pause_dur: pause duration, possible values: 3, 5
    """
    res_audio = AudioSegment.from_wav(f'./temp/{input_file_name}_0_par.wav')
    silence = AudioSegment.from_wav(f'./pause/{pause_dur}s.wav')
    par_count = len(glob1('./temp/', '*.wav'))

    for i in range(1, par_count):
        cur_paragraph = AudioSegment.from_wav(f'./temp/{input_file_name}_{i}_par.wav')
        res_audio = res_audio + silence + cur_paragraph

    res_audio.export(f'./../MakeItTalk/examples/{input_file_name}_full.wav', format='wav')


def generate_speech(input_text_path: str, replacements_path: Any=None, pause_dur: int=3) -> None:
    """
    Generate audio by given input text file.
    Save result in MakeItTalk/examples.

    :param input_text_path: path to input text file
    :param replacements_path: path to .json file with pairs 'word: replacement'
    :param pause_dur: duration between paragraphs, possible values: 3, 5
    :return: path to output .wav file with synthesised speech
    """
    chdir(abspath('Grad-TTS/'))
    build_align()
    if not (exists('./checkpts/hifigan.pt') or exists('./checkpts/grad-tts.pt')):
        install_pretrained()

    output_text_path = f'./temp/{get_file_name(input_text_path)}_fix.txt'
    replace_words(input_text_path, replacements_path, output_text_path)
    system(f'python ./inference.py -f {output_text_path} -c ./checkpts/grad-tts.pt')
    merge_paragraphs(get_file_name(input_text_path), pause_dur)
    system('rm -f ./temp/*')
    chdir('..')
