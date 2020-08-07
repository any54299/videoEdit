import toml
import csv
from moviepy import editor
import moviepy.editor as mp

import sys

def read_conf(file="conf/conf.toml"):
    try:
        with open(file) as configfile:
            confstr = configfile.read()
        return toml.loads(confstr)
    except Exception as e:
        print('Conf File not found. Check the path variable and filename: ', str(e))
        sys.exit()


def read_csv(file_path='data/watermark.csv'):
    try:
        lines = []
        with open(file_path, newline='', encoding='gbk') as subtitles:
            subtitle_reader = csv.DictReader(subtitles)
            for txt in subtitle_reader:
                line = []
                start_end = (int(txt['start']), int(txt['end']))
                line.append(start_end)
                line.append(txt['picture'])
                lines.append(tuple(line))

        return lines
    except Exception as e:
        print('Subtitle File not found. Check the path variable and filename: ', str(e))
        sys.exit()


def annotate(
        clip,
        pic,
        loc_x="center",
        loc_y="bottom"):
    '''
    logo = (mp.ImageClip("logo.png")
            .set_duration(video.duration)  # 水印持续时间
            .resize(height=50)  # 水印的高度，会等比缩放
            .margin(right=8, top=8, opacity=1)  # 水印边距和透明度
            .set_pos(("right", "top")))  # 水印的位置
    '''
    if pic.isspace() == True:
        txtclip = editor.TextClip(pic)
        cvc = editor.CompositeVideoClip([clip, txtclip.set_pos((loc_x, loc_y))])
        return cvc.set_duration(clip.duration)

    picClip=editor.ImageClip(pic)
    cvc = editor.CompositeVideoClip([clip, picClip.resize(height=50).margin(right=0, top=0, opacity=1).set_pos((loc_x, loc_y))])
    return cvc.set_duration(clip.duration)

def append_pic(conf, pictures):
    try:
        video = editor.VideoFileClip(conf['data']['video'])
        annotated_clips = [annotate(
            video.subclip(from_t, to_t),
            pic,
            conf['picture-conf']['position'][0],
            conf['picture-conf']['position'][1])
            for (from_t, to_t), pic in pictures]

        final_clip = editor.concatenate_videoclips(annotated_clips)
        # final_clip.write_videofile(conf['data']['picout'])
        # final = mp.CompositeVideoClip(annotated_clips)
        # mp4文件默认用libx264编码，比特率单位bps
        final_clip.write_videofile(conf['data']['picout'])
    except Exception as e:
        print("Exception occured during appending subtitle to video: ", str(e))


if __name__ == '__main__':
    conf_file = "conf/conf.toml"
    conf = read_conf(conf_file)
    pic = read_csv(conf['data']['picture'])
    append_pic(conf, pic)
    import traceback
    traceback.print_exc()