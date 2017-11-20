import gizeh as gz
import moviepy.editor as mpy
import easing

W, H = 78, 90  # width, height, in pixels
left, right = W, 0
duration = 2  # duration of the clip, in seconds
fps = 15
surface = gz.Surface(W, H, bg_color=(0, 0, 0))


def make_frame(t):
    # reset background
    background = gz.rectangle(xy=(W / 2, H / 2), lx=W, ly=H, fill=rgb_color_alpha(1, 0, 0, 1))
    background.draw(surface)

    point_light_through(t, left, rgb_color_alpha(253, 215, 15, .5))
    point_light_through(t, right, rgb_color_alpha(253, 215, 15, .5))

    point_light_grow_shrink(t, (15, 15), rgb_color_alpha(253, 215, 15, .5))
    point_light_grow_shrink(t, (W-15, 15), rgb_color_alpha(253, 215, 15, .5))

    # debugging ellipse
    ellipse = gz.ellipse(W, H, xy=(W / 2, H / 2), stroke_width=1, stroke=(1, 1, 1))
    ellipse.draw(surface)
    return surface.get_npimage()


def point_light_grow_shrink(t, xy, color):
    # radius = W * (1 + (t * (duration - t)) ** 2) / 6
    size = 90
    if t < .5:
        radius = easing.easeOutQuart(t, 0, size, duration-.5)
    else:
        radius = size - easing.easeInQuart(t, 0, size, duration)

    gradient = gz.ColorGradient(type="radial",
                                stops_colors=[(0, color), (1, (0, 0, 0, 0))],
                                xy1=[0, 0],
                                xy2=[0, 0],
                                xy3=[0, radius / 2])
    circle = gz.circle(r=radius / 2, fill=gradient).translate(xy=xy)
    circle.draw(surface)


def point_light_through(t, side, color):
    y = (-H / 5) + (5 * H / 3) * (t / duration)
    gradient = gz.ColorGradient(type="radial",
                                stops_colors=[(0, color), (1, (0, 0, 0, 0))],
                                xy1=[0, 0],
                                xy2=[0, 0],
                                xy3=[0, W / 2])
    circle = gz.circle(r=W / 2, fill=gradient).translate(xy=(side, y))
    circle.draw(surface)


def rgb_color_alpha(red, green, blue, alpha):
    return red / 255.0, green / 255.0, blue / 255.0, alpha


clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif("circle.gif", fps=fps, opt="OptimizePlus", fuzz=10)
