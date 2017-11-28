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
    def __init__(self, light_type=None, always_loop=None, loop_time=None, loop_amount=None, strength=None, angle=None):
        self.__class__.instances.append(weakref.proxy(self))
        self.type = light_type
        # Received values
        self.loop_amount = loop_amount
        self.loop_time = loop_time
        self.always_loop = always_loop
        self.strength = strength
        self.angle = angle

        self.duration = 2  # duration of the clip, in seconds

        # self.animation_duration = animation_duration
        if self.type == "turn_left":
            self.color = ah.rgb_color_alpha(253, 215, 15, .5)
            self.position = (15, 30)
            self.size = 140
            self.time = 0.0
            self.duration = 2.0  # duration of the clip, in seconds

            # self.function = point_light_grow_shrink()


class Draw(object):
    def __init__(self):
        self._is_running = True
        self.last_frame = None # numpy array of animations

        thread = threading.Thread(target=self.draw, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def draw(self):
        last_loop_time = time.time()  
        while (self._is_running):
           
            # make_frame(t)

            start_loop_time = time.time()
            loop_delta = start_loop_time - last_loop_time
            print loop_delta
            toDelete = None # mark which object should be deleted
            ah.background() # clear background

            for index, cur_animation in enumerate(animation_list, start=0):
                if cur_animation.type == "turn_left":
                    ah.point_light_grow_shrink(
                        cur_animation.time, cur_animation.size, cur_animation.position, cur_animation.color)


                if cur_animation.always_loop == False:
                    # TODO Implement Fadout
                    toDelete = index
                    print cur_animation.type + ": is deleted"

                cur_animation.time += loop_delta
                if cur_animation.time >= cur_animation.duration:
                    cur_animation.time = 0.0

            if toDelete is not None:  # turn off one animation each iteration
                del animation_list[toDelete]
                # print len(animation_list)

            self.last_frame = ah.getSurface()
            # print np.amax(self.last_frame)


            last_loop_time = time.time() 
            time.sleep(0.001)
            


        

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

    def get_last_frame(self):
        return self.last_frame
