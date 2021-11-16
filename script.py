import argparse
import os

from tts import generate_audio

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str, required=True,
                    help='path to a file with texts to synthesize')

parser.add_argument('-w', '--words_to_replace', type=str, required=False,
                    default='./words_to_replace.json',
                    help='path to a json file with words to replace')

parser.add_argument('-p', '--pause_dur', type=int, required=False,
                    default=3,
                    help='pause duration between two paragraphs')

args = parser.parse_args()
generate_audio(os.path.join(os.path.abspath('Grad-TTS'), args.file),
               os.path.join(os.path.abspath('Grad-TTS'),
                            os.path.abspath(args.words_to_replace)),
               args.pause_dur)
