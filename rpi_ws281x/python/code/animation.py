import animationhelper as ah
import time
import threading
import gizeh as gz
import numpy as np
import weakref
import send
animation_list = []


class animation:
    instances = []
    surface = None
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
            self.time = 0
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

                ah.background()
                for index, cur_animation in enumerate(animation_list, start=0):
                    if cur_animation.type == "turn_left":
                        ah.point_light_grow_shrink(
                            cur_animation.time, cur_animation.size, cur_animation.position, cur_animation.color)

                    # Here stuff is going to happen
                    # TODO create light patterns each make_frame
                    # TODO iterate through light patterns until death
                    # TODO fade light patterns in & out

                    if cur_animation.always_loop == False:
                        # TODO Implement Fadout
                        toDelete = index
                        print cur_animation.type + ": is deleted"

                    cur_animation.time += 0.06
                    if cur_animation.time > duration:
                        cur_animation.time = 0

                if toDelete is not None:  # turn off one animation each iteration
                    del animation_list[toDelete]
                    # print len(animation_list)

                surface = ah.getSurface()
                print np.amax(surface)

                time.sleep(1)
            except KeyboardInterrupt:
                stop()
                print "\nInterrupted from Keyboard interrupt in draw loop"
                pass

    def new_animation(self, light_type=None, always_loop=False, loop_amount=None, loop_time=None, strength=None, angle=None):
        animation_list.append(animation(light_type=light_type, always_loop=always_loop, loop_time=loop_time,
                                        loop_amount=loop_amount, strength=strength, angle=angle))
        print light_type + ": Is new"

    # not yet implemented from sending side (changing strength and angle)
    def update_animation(self, light_type=None, always_loop=False, loop_amount=None, loop_time=None, strength=None, angle=None):
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
                print one_animation.type + ": Turning off"

    def stop(self):
        self._is_running = False
        print "\nStopped drawing"
