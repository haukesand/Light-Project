import gizeh as gz
import moviepy.editor as mpy
from math import sqrt
W,H = 78,90 # width, height, in pixels
duration = 2 # duration of the clip, in seconds

def make_frame(t):
    surface = gz.Surface(W, H, bg_color=(0, 0, 0))
    speed = H * ((t * (duration - t))**3) / 4

    gradient = gz.ColorGradient(type="radial",
                                stops_colors=[(0, (1, .8, 0)), (1, (0, 0, 0))], xy1=[0, 0], xy2=[0, 0], xy3=[0, W / 2])
    circle = gz.circle(r=W / 2, fill=gradient).translate(xy=(0, speed - 15))
    circle.draw(surface)
    circle = gz.ellipse(W, H, xy = (W/2,H/2),stroke_width=1, stroke=(1,1,1))
    circle.draw(surface)
    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif("circle.gif",fps=15, opt="OptimizePlus", fuzz=10)
