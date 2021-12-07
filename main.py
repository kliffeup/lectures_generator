from os.path import abspath, join
from typing import Any

from img2vid import generate_video
from tts import generate_speech

def generate_lecture(
    input_text_path: str,
    image_path: str='./MakeItTalk/examples/monalisa2.jpg',
    output_folder: str='.',
    replacements_json_path: Any=None,
    pause_duration: int=3,
) -> None:
    generate_speech(
        join(abspath('Grad-TTS'), '..', abspath(input_text_path)),
        join(abspath('Grad-TTS'), '..', abspath(replacements_json_path))
        if replacements_json_path is not None else None,
        pause_duration,
    )

    generate_video(
        image_path,
        output_folder[:-1] if output_folder[-1] == '/' else output_folder,
    )
