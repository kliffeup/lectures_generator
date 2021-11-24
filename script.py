import argparse
import os
import shutil

from tts import generate_audio
from video_generate import generate_video

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str, required=True,
                    help='path to a file with texts to synthesize')

parser.add_argument('-i', '--image', type=str, required=True,
                    help='path to a image .jpg file')

parser.add_argument('-w', '--words_to_replace', type=str, required=False,
                    default='./words_to_replace.json',
                    help='path to a json file with words to replace')

parser.add_argument('-p', '--pause_dur', type=int, required=False,
                    default=3,
                    help='pause duration between two paragraphs')

args = parser.parse_args()
output_wav_path = generate_audio(os.path.join(os.path.abspath('Grad-TTS'), '..',
                                              os.path.abspath(args.file)),
                                 os.path.join(os.path.abspath('Grad-TTS'), '..',
                                              os.path.abspath(args.words_to_replace)),
                                 args.pause_dur)

os.rename(output_wav_path, f'./MakeItTalk/examples/{output_wav_path.split(sep="/")[-1]}')
shutil.copyfile(args.image, f'./MakeItTalk/examples/{args.image.split(sep="/")[-1]}')
generate_video(args.image.split(sep="/")[-1])
