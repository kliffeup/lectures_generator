from subprocess import STDOUT, check_call, getstatusoutput
import os

def install_weights():
    if not os.path.exists('./examples/ckpt'):
        os.mkdir('examples/ckpt')

    os.system(
        'gdown https://drive.google.com/uc?id=1ZiwPp_h62LtjU0DwpelLUoodKPR85K7x ' +
        '-O examples/ckpt/ckpt_autovc.pth',
    )

    os.system(
        'gdown https://drive.google.com/uc?id=1r3bfEvTVl6pCNw5xwUhEglwDHjWtAqQp' +
        '-O examples/ckpt/ckpt_content_branch.pth',
    )

    os.system(
        'gdown https://drive.google.com/uc?id=1rV0jkyDqPW-aDJcj7xSO6Zt1zSXqn1mu' +
        '-O examples/ckpt/ckpt_speaker_branch.pth',
    )

    os.system(
        'gdown https://drive.google.com/uc?id=1i2LJXKp-yWKIEEgJ7C6cE3_2NirfY_0a' +
        ' -O examples/ckpt/ckpt_116_i2i_comb.pth',
    )

def install_embeddings():
    if not os.path.exists('./examples/dump'):
        os.mkdir('examples/dump')

    os.system(
        'gdown https://drive.google.com/uc?id=18-0CYl5E6ungS3H4rRSHjfYvvm-WwjTI' +
        ' -O examples/dump/emb.pickle',
    )


def generate_video(input_image_name):
    if getstatusoutput('ffmpeg')[0]:
        check_call(['apt-get', 'install', 'ffmpeg'],
                   stdout=open(os.devnull, 'wb'), stderr=STDOUT)

    os.chdir(os.path.abspath('MakeItTalk/'))
    if not (os.path.exists('./examples/ckpt/ckpt_autovc.pth') and
            os.path.exists('./examples/ckpt/ckpt_content_branch.pth') and
            os.path.exists('./examples/ckpt/ckpt_speaker_branch.pth') and
            os.path.exists('./examples/ckpt/ckpt_116_i2i_comb.pth')):
        install_weights()

    if not (os.path.exists('./examples/dump/emb.pickle')):
        install_embeddings()

    os.system(f'python ./main_end2end.py --jpg {input_image_name}')
    os.chdir('..')
