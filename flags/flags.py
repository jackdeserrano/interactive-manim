from manimlib import *
import random 
import time
import os
import gc 

flags = open("flag_order.txt", "r").read().split("\n")
length = len(flags)

def get_flag():
    random.seed(time.perf_counter())
    r = random.randint(0, length - 1)
    while (r == 826):
        r = random.randint(0, length - 1)
    return r
    
class Flags(Scene):

    def on_mouse_press(self, point, button, mods):
        if (self.active):
            return
        if (self.i == 0):
            self.active = True
            self.play(FadeIn(self.flag), run_time = 1)
            self.i += 1
            self.active = False
        elif (self.i % 2):
            self.active = True
            self.flag.fade(0.8)
            
            self.play(FadeIn(self.ans), run_time = 1)
            self.index = get_flag()
            self.i += 1
            self.active = False
        else: 
            self.active = True
            self.play(FadeOut(self.ans), FadeOut(self.flag), run_time = 1)
            self.flag = ImageMobject(f"./flag_images/{self.index}.png").scale(1.5)
            self.ans = TexText(flags[self.index])
            self.play(FadeIn(self.flag), run_time = 1)
            self.i += 1
            self.active = False
        

    def construct(self):
        self.active = True
        self.i = 0
        self.index = get_flag()
        self.flag = ImageMobject(f"./flag_images/{self.index}.png").scale(1.5)
        self.ans = TexText(flags[self.index])
        self.active = False
        