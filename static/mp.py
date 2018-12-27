#!/usr/bin/env python2
#-*- coding:utf-8 -*-

from moviepy.editor import *
from moviepy.audio.fx import all
 
# 字体名字不能含有中文
FONT_URL = './heimi.TTF'
 
 
def render(input_video, output_video="new_video.mp4"):
    # 剪个10s的720x1280px的视频
    background_clip = VideoFileClip(input_video, target_resolution=(720, 1280)).subclip(0, 10)
    # 音乐只要前10s
    audio_clip = AudioFileClip('./song/yi_bai_wan_ge_ke_neng.mp3').subclip(40, 50)
    background_clip = background_clip.set_audio(audio_clip)
    # 左下角加文字, 持续10s
    #text_clip1 = TextClip('你', fontsize=30, color='white', font=FONT_URL)
    #text_clip1 = text_clip1.set_position(('left', 'bottom'))
    #text_clip1 = text_clip1.set_duration(10)
    # 右下角加文字, 持续3s
    #text_clip2 = TextClip('woshi', fontsize=30, color='white', font=FONT_URL)
    #text_clip2 = text_clip2.subclip(0, 3).set_position(('right', 'bottom'))
    image_clip = ImageClip('../img/iconfont-logo.png')
    # 图片放中间, 从第2s开始播持续6s
    image_clip = image_clip.set_duration(6).set_position('center').set_start(2)
    video = CompositeVideoClip([background_clip, image_clip])
    # 调节音量
    video = all.volumex(video, 0.8)
    video.write_videofile(output_video)
 
 
if __name__ == '__main__':
    print('start!!!')
    render(input_video="./movie/tangtang.mp4", output_video="new_tangtang.mp4")