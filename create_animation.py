import os
from moviepy.editor import *

DIR = "anim/"
FPS = 30

imgs = [DIR + x for x in os.listdir(DIR) if x != "main.png"]
imgs = sorted(imgs, key=lambda x: int(x.split(".")[0].split("/")[-1]))

clips = [ImageClip(m).set_duration(1/FPS) for m in imgs]

clips = [ ImageClip(DIR + "main.png").set_duration(1) ] + clips

concat_clip = concatenate_videoclips(clips, method="compose")
concat_clip.write_videofile("test.mp4", fps=FPS)