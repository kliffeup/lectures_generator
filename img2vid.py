from os import chdir, devnull, mkdir, system
from os.path import abspath, exists
from shutil import copyfile
from subprocess import STDOUT, check_call, getstatusoutput


def install_weights():
    """
    Install pre-trained model weights.
    """
    if not exists('./examples/ckpt'):
        mkdir('examples/ckpt')

    system(
        'gdown https://drive.google.com/uc?id=1ZiwPp_h62LtjU0DwpelLUoodKPR85K7x' +
        ' -O examples/ckpt/ckpt_autovc.pth',
    )

    system(
        'gdown https://drive.google.com/uc?id=1r3bfEvTVl6pCNw5xwUhEglwDHjWtAqQp' +
        ' -O examples/ckpt/ckpt_content_branch.pth',
    )

    system(
        'gdown https://drive.google.com/uc?id=1rV0jkyDqPW-aDJcj7xSO6Zt1zSXqn1mu' +
        ' -O examples/ckpt/ckpt_speaker_branch.pth',
    )

    system(
        'gdown https://drive.google.com/uc?id=1i2LJXKp-yWKIEEgJ7C6cE3_2NirfY_0a' +
        ' -O examples/ckpt/ckpt_116_i2i_comb.pth',
    )


def install_embeddings():
    """
    Install pre-trained embeddings.
    """
    if not exists('./examples/dump'):
        mkdir('examples/dump')

    system(
        'gdown https://drive.google.com/uc?id=18-0CYl5E6ungS3H4rRSHjfYvvm-WwjTI' +
        ' -O examples/dump/emb.pickle',
    )


def move_input_image(input_image_path: str='./MakeItTalk/examples/monalisa2.jpg') -> None:
    """
    Copy image to MakeItTalk/examples, for further model work.
    """
    if input_image_path != './MakeItTalk/examples/monalisa2.jpg':
        copyfile(
            input_image_path,
            f'./MakeItTalk/examples/{input_image_path.split(sep="/")[-1]}'
        )


def generate_video(
        input_image_path: str='./MakeItTalk/examples/monalisa2.jpg',
        output_folder: str='.',
) -> None:
    """
    Generate a video where human face from input image voices the speech
    synthesised in the TTS part.

    :param input_image_path: input file
    """
    # install ffmpeg if necessary
    if getstatusoutput('ffmpeg')[0]:
        check_call(['apt-get', 'install', 'ffmpeg'],
                   stdout=open(devnull, 'wb'), stderr=STDOUT)

    move_input_image(input_image_path)
    chdir(abspath('MakeItTalk/'))
    if not (exists('./examples/ckpt/ckpt_autovc.pth') and
            exists('./examples/ckpt/ckpt_content_branch.pth') and
            exists('./examples/ckpt/ckpt_speaker_branch.pth') and
            exists('./examples/ckpt/ckpt_116_i2i_comb.pth')):
        install_weights()

    if not exists('./examples/dump/emb.pickle'):
        install_embeddings()

    system(f'python ./main_end2end.py --jpg {input_image_path.split(sep="/")[-1]} --save_output {output_folder}')
    system('rm -f ./examples/*full_av.mp4 ./examples/*full.wav')
    chdir('..')
