import animationhelper as ah
import time
import threading
import gizeh as gz
import numpy as np
import weakref
import send
import i2c_display as display


animation_list = []
W, H = 78, 90  # width, height, in pixels

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
        if angle is not None:
            self.angle = angle - 180
        self.duration = 2  # default duration of the clip, in seconds
        self.time = 0.0
        # individual variables
        if self.type == "turn_left":
            # would be better to use a custom type here
            self.function = "point_light_grow_shrink"
            self.color = ah.rgb_color_alpha(253, 215, 15, .5)
            self.position = (15, 30)
            self.size = 140
        elif self.type == "turn_right":
            self.function = "point_light_grow_shrink"
            self.color = ah.rgb_color_alpha(253, 215, 15, .5)
            self.position = (W - 15, 30)
            self.size = 140

        elif self.type == "start_moving":
            self.function = "strip_light_through"
            self.color = ah.rgb_color_alpha(0, 191, 255, .5)
            self.thickness = H / 3
        elif self.type == "move_backwards":
            self.function = "strip_light_through"
            self.color = ah.rgb_color_alpha(135, 206, 235, .5)
            self.thickness = H / 4
            self.angle = self.angle - 180

        elif self.type == "lane_left":
            self.function = "point_light_through"
            self.posx = 0
            self.size = ah.halfW
            self.color = ah.rgb_color_alpha(200, 255, 200, .5)
        elif self.type == "lane_right":
            self.function = "point_light_through"
            self.posx = ah.W
            self.size = ah.halfW
            self.color = ah.rgb_color_alpha(200, 255, 200, .5)

        elif self.type == "depart_todestination":
            self.angle = 0
            self.function = "light_rotate_around"
            self.color = ah.rgb_color_alpha(127, 255, 212, .5)
            self.thickness = H
            self.direction = 1
        elif self.type == "arrive_destination":
            self.angle = 0
            self.function = "light_rotate_around"
            self.color = ah.rgb_color_alpha(127, 255, 212, .5)
            self.thickness = H
            self.direction = -1

        elif self.type == "highway_enter":
            self.angle = -45
            self.function = "strip_light_through"
            self.color = ah.rgb_color_alpha(255, 215, 0, .5)
            self.thickness = H / 3
        elif self.type == "highway_leave":
            self.angle = 45
            self.function = "strip_light_through"
            self.color = ah.rgb_color_alpha(255, 215, 0, .5)
            self.thickness = H / 3

        elif self.type == "wait_trafficlight":
            self.function = "light_pulsate"
            self.color = ah.rgb_color_alpha(144, 255, 0, .5)
            self.duration = 3.0

        elif self.type == "wait_pedestrian":
            self.function = "light_pulsate"
            self.color = ah.rgb_color_alpha(255, 165, 0, .5)
            self.duration = 3.0

        elif self.type == "uneven_road":  # Needs a special animation type to "rattle"
            self.function = "multi_strip_light_through"
            self.angle = 0
            self.color = ah.rgb_color_alpha(184, 134, 11, .5)
            self.thickness = H / 3
        elif self.type == "swerve_left":
            self.function = "flank_light_pulse"
            self.xy1 = (ah.halfW, 0)
            self.xy2 = (-ah.rightX, 0)
            self.color = ah.rgb_color_alpha(220, 20, 60, .8)

        elif self.type == "brake_now":
            self.function = "flank_light_pulse"
            self.xy1 = (0, -ah.halfH)
            self.xy2 = (0, ah.bottomY)
            self.color = ah.rgb_color_alpha(255, 30, 70, .1 * strength)

        elif self.type == "slow_down":
            self.angle = -180
            self.function = "multi_strip_light_through"
            self.color = ah.rgb_color_alpha(135, 206, 250, .5)
            self.thickness = H / 2
        elif self.type == "speed_up":  # TODO use strength for either speed of animation or visibility
            self.function = "multi_strip_light_through"
            self.color = ah.rgb_color_alpha(135, 206, 250, .1 * strength)
            self.duration = 1
            # self.duration = (101 - strength) * 0.02
            self.thickness = H / 3
        elif self.type == "speed_keep":  # TODO use strength for either speed of animation or visibility
            self.function = "multi_strip_light_through"
            self.duration = (86 - strength) * 0.02
            self.color = ah.rgb_color_alpha(255, 248, 220, .2)
            self.thickness = H / 3.

        if self.always_loop == True:
            self.fadeout = True
            self.fadespeed = 0.03
            self.fadein = self.color[3]
            self.color = list(self.color)
            self.color[3] = 0.0
            self.color[3]
        else:
            self.fadeout = False
            self.fadein = False




class Draw(object):
    def __init__(self):
        self._is_running = True
        self.last_frame = None  # numpy array of animations
        self.light_on = False
        self.augmentation_on = True
        thread = threading.Thread(target=self.draw, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

        print "Start animation thread"

    def draw(self):
        last_loop_time = time.time()
        while (self._is_running):

            # make_frame(t)

            start_loop_time = time.time()
            loop_delta = start_loop_time - last_loop_time

            toDelete = None  # mark which object should be deleted
            ah.background()  # clear background

            for index, cur_animation in enumerate(animation_list, start=0):
                # render individual animations here

                if cur_animation.fadein:
                    cur_animation.color[3] += cur_animation.fadespeed
                    if cur_animation.color[3] >= cur_animation.fadein:
                        cur_animation.fadein = False

                if cur_animation.function == "point_light_grow_shrink":
                    ah.point_light_grow_shrink(
                        cur_animation.time, cur_animation.size, cur_animation.position, cur_animation.color)
                elif cur_animation.function == "point_light_through":
                    ah.point_light_through(
                        cur_animation.time, cur_animation.size, cur_animation.posx, cur_animation.color)
                elif cur_animation.function == "strip_light_through":
                    ah.strip_light_through(
                        cur_animation.time, cur_animation.angle, cur_animation.thickness, cur_animation.color)
                elif cur_animation.function == "multi_strip_light_through":
                    ah.multi_strip_light_through(
                        cur_animation.time, cur_animation.angle, cur_animation.thickness, cur_animation.color, cur_animation.duration)
                elif cur_animation.function == "light_rotate_around":
                    ah.light_rotate_around(cur_animation.time, cur_animation.angle,
                                           cur_animation.thickness, cur_animation.direction, cur_animation.color)
                elif cur_animation.function == "flank_light_pulse":
                    ah.flank_light_pulse(
                        cur_animation.time, cur_animation.xy1, cur_animation.xy2, cur_animation.color)
                elif cur_animation.function == "light_pulsate":
                    ah.light_pulsate(cur_animation.time, cur_animation.color, cur_animation.duration)


                if cur_animation.always_loop is not None and cur_animation.always_loop == False \
                        or cur_animation.loop_time is not None and cur_animation.loop_time <= 0.0 \
                        or cur_animation.loop_amount is not None and cur_animation.loop_amount <= 0:
                    # TODO Implement Fadout
                    # print np.average(cur_animation.color)
                    if cur_animation.fadeout and np.average(cur_animation.color) >= cur_animation.fadespeed:
                        cur_animation.color = np.subtract(cur_animation.color , cur_animation.fadespeed) # this is framerate dependent
                    else:
                        toDelete = index
                        print cur_animation.type + ": is deleted"

                cur_animation.time += loop_delta  # increase framerate independently
                if cur_animation.time >= cur_animation.duration:
                    cur_animation.time = 0.0
                    if cur_animation.loop_amount is not None:
                        cur_animation.loop_amount -= 1
                if cur_animation.loop_time is not None:  # checl if loop number needs to be reduced
                    cur_animation.loop_time -= loop_delta

            if toDelete is not None:  # turn off one animation each iteration
                del animation_list[toDelete]
                display.write_line(1, "Autopilot")
                display.write_line(2, "is active")
                # print len(animation_list)

            self.last_frame = ah.getSurface()
            # print np.amax(self.last_frame)

            last_loop_time = time.time()
            time.sleep(0.008)

    def new_animation(self, light_type=None, always_loop=False, loop_amount=None, loop_time=None, strength=None, angle=None):
        if self.augmentation_on:
            animation_list.append(animation(light_type=light_type, always_loop=always_loop, loop_time=loop_time,
                                            loop_amount=loop_amount, strength=strength, angle=angle))
        print light_type + ": Is new"
        display.create_message(light_type)


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

    def set_light(self, onoff):
        if onoff == True:
            display.write_line(1, "Hello!")
            display.write_line(2, "")
        else:
            display.write_line(1, "Bye!")
            display.write_line(2, "")
        self.light_on = onoff

    def toggle_user_light(self):
        self.light_on = not self.light_on
        if self.light_on:
            display.write_line(1, "Light:")
            display.write_line(2, "On")
        else:
            display.write_line(1, "Light:")
            display.write_line(2, "Off")

    def toggle_augmentation_on(self):
        self.augmentation_on = not self.augmentation_on
        if self.augmentation_on:
            display.write_line(1, "Augmentation:")
            display.write_line(2, "On")
        else:
            display.write_line(1, "Augmentation:")
            display.write_line(2, "Off")

    def user_starts_ride(self):
        if self.augmentation_on:
            animation_list.append(animation(light_type="depart_todestination", always_loop=False, loop_time=None, loop_amount=1, strength=None, angle=None))
        display.write_line(1, "Have a ")
        display.write_line(2, "good ride!")

    def stop(self):
        self._is_running = False
        print "\nStopped drawing"

    def get_last_frame(self):
        return self.last_frame
    def get_light_on(self):
        return self.light_on
