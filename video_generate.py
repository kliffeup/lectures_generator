from subprocess import STDOUT, check_call, getstatusoutput
import os


def generate_video(input_image_name):
    if getstatusoutput('ffmpeg')[0]:
        check_call(['apt-get', 'install', 'ffmpeg'],
                   stdout=open(os.devnull, 'wb'), stderr=STDOUT)

    os.chdir(os.path.abspath('MakeItTalk/'))
    os.system(f'python ./main_end2end.py --jpg {input_image_name}')
    os.chdir('..')
