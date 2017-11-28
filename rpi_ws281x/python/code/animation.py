import animationhelper as ah
import time
import threading
import gizeh as gz

import weakref

W, H = 78, 90  # width, height, in pixels
halfW, halfH = W / 2, H / 2
leftX, rightX = 0, W
topY, bottomY = 0, H
duration = 2  # duration of the clip, in seconds
fps = 15
surface = gz.Surface(W, H, bg_color=(0, 0, 0))

animation_list = []


class animation:
    instances = []
    def __init__(self, light_type=None, always_loop=None, loop_time=None, loop_amount=None, strength=None, angle=None):
        self.__class__.instances.append(weakref.proxy(self))
        self.type = light_type
        # Received values
        self.loop_amount = loop_amount
        self.loop_time = loop_time
        self.always_loop = always_loop
        self.strength = strength
        self.angle = angle

        # self.start_time = start_time
        # self.last_loop_time = last_loop_time

        # self.animation_duration = animation_duration
        if self.type == "turn_left":
            self.color = ah.rgb_color_alpha(253, 215, 15, .5)
            self.position = (15, 30)
            self.size = 140
            # self.function = point_light_grow_shrink()



class Draw(object):
    def __init__(self):
        self._is_running = True
        thread = threading.Thread(target=self.draw, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def draw(self):
        while (self._is_running):
            try:
                # make_frame(t)


                toDelete = None
                for index, cur_animation in enumerate(animation_list, start=0):
                    if cur_animation.type == "turn_left":
                        ah.point_light_grow_shrink(1, cur_animation.size, cur_animation.position, cur_animation.color)



                    # Here stuff is going to happen
                    # TODO create light patterns each make_frame
                    # TODO iterate through light patterns until death
                    # TODO fade light patterns in & out

                    if cur_animation.always_loop == False:
                        # TODO Implement Fadout
                        toDelete = index
                        print cur_animation.type +  "is deleted"

                if toDelete is not None: # turn off one animation each iteration
                    del animation_list[toDelete]
                    # print len(animation_list)

                time.sleep(1)
            except KeyboardInterrupt:
                stop()
                print "\nInterrupted from Keyboard interrupt in draw loop"
                pass

    def new_animation(self, light_type=None, always_loop=False, loop_amount=None, loop_time=None, strength=None, angle=None):
        animation_list.append(animation(light_type=light_type, always_loop=always_loop, loop_time=loop_time,
                                        loop_amount=loop_amount, strength = strength, angle=angle))
        print light_type + ": Is new"

    def update_animation(self, light_type=None, always_loop=False, loop_amount=None, loop_time=None, strength=None, angle=None): # not yet implemented from sending side (changing strength and angle)
        for one_animation in animation_list:
            if one_animation.type == light_type:
                one_animation.always_loop = always_loop
                one_animation.angle = angle
                one_animation.strength = strength
                print one_animation.type + ": Updated"


    def off_animation(self, light_type=None):
        for one_animation in animation_list:
            if one_animation.type == light_type:
                one_animation.always_loop = False
                print one_animation.type + ": Turned off"

    def stop(self):
        self._is_running = False
        print "\nStopped drawing"

    def make_frame(t):
        # reset background
        background = gz.rectangle(xy=(halfW, halfH), lx=W,
                                  ly=H, fill=rgb_color_alpha(1, 0, 0, 1))
        background.draw(surface)

        # point_light_through(t, leftX, rgb_color_alpha(253, 215, 15, .5))
        # point_light_through(t, rightX, rgb_color_alpha(253, 215, 15, .5))

        # point_light_grow_shrink(t, (15, 15), rgb_color_alpha(253, 215, 15, .5))
        # point_light_grow_shrink(t, (W-15, 15), rgb_color_alpha(253, 215, 15, .5))

        # flank_light_pulse(t, xy1=(0,halfH), xy2=(0,-bottomY), color= rgb_color_alpha(231, 37, 66, .5))
        # flank_light_pulse(t, xy1=(0, -halfH), xy2=(0, bottomY), color=rgb_color_alpha(231, 37, 66, .5))
        # flank_light_pulse(t, xy1=(-halfW, 0), xy2=(rightX, 0), color=rgb_color_alpha(231, 37, 66, .5))
        # flank_light_pulse(t, xy1=(halfW, 0), xy2=(-rightX, 0),color=rgb_color_alpha(231, 37, 66, .5))

        # animation.multi_strip_light_through(t, angle=math.radians(
        #     0), thickness=H / 3, color=rgb_color_alpha(17, 155, 255, .5))
        # light_rotate_around(t, angle = math.radians(0), thickness = H, direction = 1, color = rgb_color_alpha(17, 155, 255, .5))

        # debugging ellipse
        # ellipse = gz.ellipse(W, H, xy=(halfW, halfH),
        #                      stroke_width=1, stroke=(1, 1, 1))
        # ellipse.draw(surface)
        return surface.get_npimage()
