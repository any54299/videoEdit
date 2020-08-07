import toml
import csv
from moviepy import editor
import sys


def read_conf(file="conf/conf.toml"):
    try:
        with open(file) as configfile:
            confstr = configfile.read()
        return toml.loads(confstr)
    except Exception as e:
        print('Conf File not found. Check the path variable and filename: ', str(e))
        sys.exit()

def mergeVideo(conf):
    try:
        mergetData = conf['merge-data']['file']
        clip = []
        for i in mergetData:
            clip.append(editor.VideoFileClip(i))
        final_clip = editor.concatenate_videoclips(clip)
        final_clip.write_videofile(conf['merge-data']['mergeOut'])
    except Exception as e:
        print("Exception occured during appending subtitle to video: ", str(e))


if __name__ == '__main__':
    conf_file = "conf/conf.toml"
    conf = read_conf(conf_file)
    #mergeVideo(conf)
    import os
    print(os.getcwd())
