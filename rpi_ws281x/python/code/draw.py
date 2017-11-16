import gizeh as gz
from numpy import pi # <- 3.14... :)
import moviepy.editor as mpy

W, H = 78,90
surface = gz.Surface(W,H, bg_color=(0,0,0))

duration = 2 # duration of the clip, in seconds

def make_frame(t):
    surface = gizeh.Surface(W,H)
    radius = W*(1+ (t*(duration-t))**2 )/6
    circle = gizeh.circle(radius, xy = (W/2,H/2), fill=(1,0,0))
    circle.draw(surface)
    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif("circle.gif",fps=15, opt="OptimizePlus", fuzz=10)

surface.write_to_png("assets/draw.png")