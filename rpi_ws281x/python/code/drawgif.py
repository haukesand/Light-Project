import gizeh as gz
import moviepy.editor as mpy
import math
import easing
import time

W, H = 78, 90  # width, height, in pixels
halfW, halfH = W / 2, H / 2
leftX, rightX = 0, W
topY, bottomY = 0, H
duration = 2  # duration of the clip, in seconds
fps = 15
surface = gz.Surface(W, H, bg_color=(0, 0, 0))
_is_running = True
message = "nomessage"

def stop():
  _is_running = False

def make_frame(t):
    # reset background
    background = gz.rectangle(xy=(halfW, halfH), lx=W,
                              ly=H, fill=rgb_color_alpha(1, 0, 0, 1))
    background.draw(surface)

    # point_light_through(t, leftX, rgb_color_alpha(253, 215, 15, .5))
    # point_light_through(t, rightX, rgb_color_alpha(253, 215, 15, .5))

    # point_light_grow_shrink(t, 140, (15, 30), rgb_color_alpha(253, 215, 15, .5))
    # point_light_grow_shrink(t, (W-15, 15), rgb_color_alpha(253, 215, 15, .5))

    # flank_light_pulse(t, xy1=(0,halfH), xy2=(0,-bottomY), color= rgb_color_alpha(231, 37, 66, .5))
    # flank_light_pulse(t, xy1=(0, -halfH), xy2=(0, bottomY), color=rgb_color_alpha(231, 37, 66, .5))
    # flank_light_pulse(t, xy1=(-halfW, 0), xy2=(rightX, 0), color=rgb_color_alpha(231, 37, 66, .5))
    # flank_light_pulse(t, xy1=(halfW, 0), xy2=(-rightX, 0),color=rgb_color_alpha(231, 37, 66, .5))

    multi_strip_light_through(t, angle=math.radians(180), thickness=H / 3, color=rgb_color_alpha(17, 155, 255, .5))
    # light_rotate_around(t, angle = math.radians(0), thickness = H, direction = 1, color = rgb_color_alpha(17, 155, 255, .5))

    # debugging ellipse
    ellipse = gz.ellipse(W, H, xy=(halfW, halfH),
                         stroke_width=1, stroke=(1, 1, 1))
    ellipse.draw(surface)
    return surface.get_npimage()


def multi_strip_light_through(t, angle, thickness, color):
    angle += math.radians(90)  # to start animation from front

    gradient = gz.ColorGradient("linear", ((0, rgb_color_alpha(0.0)), (.5, color), (1, rgb_color_alpha(0.0))),
                                xy1=(-thickness / 2, 0), xy2=(thickness / 2, 0))

    for x in range(1, 6):
        center = (gz.polar2cart(
            (thickness * x + thickness * t / duration) - thickness * 4, angle))
        rect = gz.rectangle(xy=(halfW, halfH), lx=thickness,
                            ly=H, fill=gradient).rotate(angle, center=(halfW, halfH)).translate(center)
        rect.draw(surface)


def strip_light_through(t, angle, thickness, color):
    angle += math.radians(90)  # to start animation from front
    center = (gz.polar2cart((H * 2 * t / duration) - H, angle))

    gradient = gz.ColorGradient("linear", ((0, rgb_color_alpha(0)), (.5, color), (1, rgb_color_alpha(0))),
                                xy1=(-thickness / 2, 0), xy2=(thickness / 2, 0))

    rect = gz.rectangle(xy=(halfW, halfH), lx=thickness,
                        ly=H, fill=gradient).rotate(angle, center=(halfW, halfH)).translate(center)
    rect.draw(surface)


def light_rotate_around(t, angle, thickness, direction, color):

    strength = easing.easeOutQuart(t, 0.0, 1.0, duration / 2)
    angle = angle + 2 * math.pi * (t / duration) * direction

    gradient = gz.ColorGradient("linear", ((0, rgb_color_alpha(0)), (.5, tuple(i * strength for i in color)), (1, rgb_color_alpha(0))),
                                xy1=(-thickness / 2, 0), xy2=(thickness / 2, 0))

    rect = gz.rectangle(xy=(halfW, 0), lx=H,
                        ly=thickness, fill=gradient).rotate(angle, center=(halfW, halfH))
    rect.draw(surface)


def flank_light_pulse(t, xy1, xy2, color):
    # this is not sharing friendly yet
    if t < .5:
        strength = easing.easeOutQuart(t, 0.0, 1.0, duration / 2)
    else:
        strength = 1.0 - easing.easeInQuart(t, 0.0, 1.0, duration / 2)

    gradient = gz.ColorGradient("linear", ((0, tuple(i * strength for i in color)), (1, (0, 0, 0, 0))),
                                xy1=xy1, xy2=xy2)

    rect = gz.rectangle(xy=(halfW, halfH), lx=W, ly=H, fill=gradient)
    rect.draw(surface)


def point_light_grow_shrink(t, size, xy, color):
    # radius = W * (1 + (t * (duration - t)) ** 2) / 6
    size = size
    if t < .5:
        radius = easing.easeOutQuart(t, 0, size, duration / 2)
    else:
        radius = size - easing.easeInQuart(t, 0, size, duration / 2)

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
                                xy3=[0, halfW])
    circle = gz.circle(r=halfW, fill=gradient).translate(xy=(side, y))
    circle.draw(surface)


# def rgb_color_alpha(red, green, blue, alpha):
#     return red / 255.0, green / 255.0, blue / 255.0, alpha

def rgb_color_alpha(*colors):
    if len(colors) == 1:
        r, g, b, a = colors[0], colors[0], colors[0], colors[0]
    else:
        r, g, b, a = colors[0] / 255.0, colors[1] / \
            255.0, colors[2] / 255.0, colors[3]
    return r, g, b, a


clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif("circle.gif", fps=fps, opt="OptimizePlus", fuzz=10)
