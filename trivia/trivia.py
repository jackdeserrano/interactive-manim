from manimlib import *
import random 
import time
import os
import gc 

questions = open("tex_trivia.txt", "r").read().split("\n\n")
length = len(questions)

def get_question():
    random.seed(time.perf_counter())
    index = random.randint(0, length - 1)
    if ("Greek root" in questions[index]):
        return get_question()
    return questions[index].split("\n")
    
class Trivia(Scene):

    def on_mouse_press(self, point, button, mods):
        if (self.active):
            return
        if (self.i == 0):
            self.active = True
            self.play(FadeIn(self.prompt), run_time = 0.5)
            self.i += 1
            self.active = False
        elif (self.i % 2):
            self.active = True
            self.play(FadeOut(self.prompt), run_time = 0.5)
            self.ans = TexText(self.question[1], color = BLUE).scale(0.8)
            self.length = len(self.question[1])
            self.play(FadeIn(self.ans), run_time = 0.5)
            self.length = len(self.question[1])
            self.question = get_question()
            self.i += 1
            self.active = False
        else: 
            self.active = True
            self.play(FadeOut(self.ans), FadeOut(self.guess_obj), run_time = 0.5)
            self.guess_obj = Text("", color = RED).scale(0.8)
            self.length = len(self.question[0])
            self.prompt = TexText(self.question[0]).scale(0.8)
            self.play(FadeIn(self.prompt), run_time = 0.5)
            self.i += 1
            self.active = False

    def on_key_press(self, symbol, modifiers):
        if (symbol == 65505): # shift
            self.shift = True

    def on_key_release(self, symbol, modifiers):
        if (self.active):
            return
        
        if (self.guess_on):
            if (symbol == 65293): # enter
                self.guess_on = False
                self.guess = ""
                self.active = True
                self.play(FadeOut(self.prompt), run_time = 0.5)
                self.ans = TexText(self.question[1], color = BLUE).scale(0.8)
                self.length = len(self.question[1])
                self.play(self.guess_obj.animate.next_to(self.ans, DOWN))
                self.play(FadeIn(self.ans))
                self.length = len(self.question[1])
                self.question = get_question()
                self.i += 1
                self.active = False
                return

            if (symbol == 65288): # backspace
                self.guess = self.guess[:-1]
                self.guess_obj.become(Text(self.guess, color = RED).scale(0.8).next_to(self.prompt, DOWN))
                return

            if (symbol == 65505): # shift
                self.shift = False
                return

            if (self.shift and symbol >= ord('a') and symbol <= ord('z')):
                self.guess += chr(symbol - ord('a') + ord('A'))
            else:
                self.guess += chr(symbol)

            self.guess_obj.become(Text(self.guess, color = RED).scale(0.8).next_to(self.prompt, DOWN))
            return
        
        if (symbol == 113): # 'q'
            global questions
            del questions
            gc.collect()
            os._exit(1)
        
        if (symbol == 103): # 'g'
            if (self.i % 2 and not self.active):
                self.guess_on = True
                self.guess_obj = Text("", color = RED).scale(0.8)
                self.guess_obj.next_to(self.prompt, DOWN)
                self.add(self.guess_obj)
        

        

    def construct(self):

        self.shift = False

        self.question = get_question()
        self.length = len(self.question[0])
        self.guess_on = False

        self.guess = ""
        self.guess_obj = Text("")
        self.prompt = TexText(self.question[0]).scale(0.8)
        self.ans = TexText("")
        self.i = 0
        self.active = False