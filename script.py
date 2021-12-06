from argparse import ArgumentParser
from os.path import abspath, join
from typing import Any

from img2vid import generate_video
from tts import generate_speech


parser = ArgumentParser()
parser.add_argument('-t', '--text', type=str, required=True,
                    help='path to a file with texts to synthesize speech')

parser.add_argument('-i', '--image', type=str, required=False,
                    default='./MakeItTalk/examples/monalisa2.jpg',
                    help='path to a image .jpg file, required resolution 256x256')

parser.add_argument('-o', '--output', type=str, required=False,
                    default='./',
                    help='path to output folder to save video')

parser.add_argument('-r', '--replacements', type=Any, required=False,
                    default=None,
                    help='path to a json file with words to replace')

parser.add_argument('-p', '--pause_duration', type=int, required=False,
                    default=3,
                    help='pause duration between each two paragraphs')

args = parser.parse_args()
generate_speech(
    join(abspath('Grad-TTS'), '..', abspath(args.text)),
    join(abspath('Grad-TTS'), '..', abspath(args.replacements)),
    args.pause_duration,
)

generate_video(
    args.image, args.output[:-1] if args.output[-1] == '/' else args.output,
)
