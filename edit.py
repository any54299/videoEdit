import toml
import csv
from moviepy import editor
import sys
import os
path=os.getcwd()

def read_conf(file="conf/conf.toml"):
    try:
        with open(file) as configfile:
            confstr = configfile.read()
        return toml.loads(confstr)
    except Exception as e:
        print('Conf File not found. Check the path variable and filename: ', str(e))
        sys.exit()

def read_csv(file_path='data/edit.csv'):
    try:
        lines = []
        with open(file_path, newline='', encoding='gbk') as subtitles:
            subtitle_reader = csv.DictReader(subtitles)
            for txt in subtitle_reader:
                start_end = (int(txt['start']), int(txt['end']))
                #line.append(start_end)
                lines.append(start_end)

        return lines
    except Exception as e:
        print('Subtitle File not found. Check the path variable and filename: ', str(e))
        sys.exit()

def append_subtitle(conf, subtitles):
    try:
        video = editor.VideoFileClip(conf['data']['video'])
        idx = 0
        begin = 0
        paragraph = 0
        for (from_t, to_t) in subtitles:
            if idx==0:
                begin=from_t
            idx+=1
        
        if begin==0:
            paragraph = idx
        else:
            paragraph = idx+1
        
        
        for (from_t, to_t) in subtitles:
            if begin!=0:
                final_clip=video.subclip(from_t, to_t)
                
            
            final_clip=video.subclip(from_t, to_t)
            final_clip.write_videofile("%s/%s.mp4"%(path,idx))
            idx+=1
            
        #annotated_clips = [video.subclip(from_t, to_t) for (from_t, to_t) in subtitles]
        #final_clip = editor.concatenate_videoclips(annotated_clips)

        #final_clip.write_videofile(conf['data']['output'])
    except Exception as e:
        print("Exception occured during appending subtitle to video: ", str(e))

if __name__ == '__main__':
    conf_file = "conf/conf.toml"
    conf = read_conf(conf_file)
    subtitles = read_csv(conf['data']['edit'])
    append_subtitle(conf, subtitles)
