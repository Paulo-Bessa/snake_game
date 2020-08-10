from tkinter import *
import random
import time
from threading import Thread
import numpy as np

SIZE = 20
# DIRECTIONS = {Up:[0,-20],Down:[0,20],Left:[-20,0],Right:[20,0]}

root = Tk()


C = Canvas(root,height=500,width=500,bg='white')

frame1 = Frame(root)
frame1.pack(side='left')

label1 = Label(frame1,font = ('Times',42),text = "You:")
label1.pack(side="top")
label2 = Label(frame1,font = ('Times',42),text = "1")
label2.pack(side="bottom")

frame2 = Frame(root)
frame2.pack(side='right')

label3 = Label(frame2,font = ('Times',42),text = "Enemy:")
label3.pack(side="top")
label4 = Label(frame2,font = ('Times',42),text = "1")
label4.pack(side="bottom")

class Food:

    def __init__(self):
        self.pos = [random.randint(0,24)*20,random.randint(0,24)*20]
    
    def represent(self):
        C.delete('foody')
        self.pos = [random.randint(0,24)*20,random.randint(0,24)*20]
        C.create_oval(self.pos[0],self.pos[1],self.pos[0]+SIZE,self.pos[1]+SIZE,fill='grey',tags='foody')


class Player:

    def __init__(self,food,pos=[100,100]):
        self.pos = pos
        self.lenght = 1
        self.body = []
        self.direction = 0
        self.food = food

    def represent(self):
        C.delete('handle')                                                                              # Erase the old snake
        self.colision()                                                                                 # Verify if the snake ate some food
        while len(self.body) > self.lenght:                                                             # Fix the lenght of the snake
            del self.body[-1]
        for elem in self.body:
            C.create_oval(elem[0],elem[1],elem[0]+SIZE,elem[1]+SIZE,fill='black',tags='handle')

    def colision(self):
        if self.pos[0] == self.food.pos[0] and self.pos[1] == self.food.pos[1]:                         # If the snake hits the food, the lenght is 
            self.lenght += 1                                                                            # increased and a new random food is created
            label2.configure(text = str(self.lenght))
            self.food.represent()
    
    def mov_up(self,e):
        self.direction = 0
        if self.pos[1] < 0:                                                                             # Verify the borders
            self.pos[1] = 500
        else:
            self.pos[1] -= SIZE
        self.body.insert(0,[self.pos[0],self.pos[1]])
        self.represent()
        

    def mov_down(self,e):
        self.direction = 1
        if self.pos[1] > 500:
            self.pos[1] = 0
        else:
            self.pos[1] += SIZE
        self.body.insert(0,[self.pos[0],self.pos[1]])
        self.represent()

    def mov_right(self,e):
        self.direction = 2
        if self.pos[0] > 500:
            self.pos[0] = 0
        else:
            self.pos[0] += SIZE
        self.body.insert(0,[self.pos[0],self.pos[1]])
        self.represent()

    def mov_left(self,e):
        self.direction = 3
        if self.pos[0] < 0:
            self.pos[0] = 500
        else:
            self.pos[0] -= SIZE
        self.body.insert(0,[self.pos[0],self.pos[1]])
        self.represent()
    
    def step(self):
        if self.direction == 0:
            self.pos[1] -= SIZE
        elif self.direction == 1:
            self.pos[1] += SIZE
        elif self.direction == 2:
            self.pos[0] += SIZE
        elif self.direction == 3:
            self.pos[0] -= SIZE
        time.sleep(1.0)
        self.step()
    
class Enemy:

    def __init__(self, clock,food,player):
        self.clock = clock
        self.pos = [random.randint(0,24)*20,random.randint(0,24)*20]
        self.body = []
        self.lenght = 1
        self.food = food
        self.player = player
        self.dist = []
        self.value = []
        self.near = []

    def movement(self):
        self.closest()
        a = random.randint(0,1)
        if self.near == []:
            self.pos[a] -= SIZE
        else:
            if self.near[a] > 0:
                self.pos[a] -= SIZE
            elif self.near[a] < 0:
                self.pos[a] += SIZE
            else:
                if self.near[1-a] > 0:
                    self.pos[1-a] -= SIZE
                elif self.near[1-a] < 0:
                    self.pos[1-a] += SIZE
        self.body.insert(0,[self.pos[0],self.pos[1]])
        self.represent()
    
    def represent(self):
        if self.pos[1] < 0:                                                                             # Verify the borders
            self.pos[1] = 500
        elif self.pos[1] > 500:
            self.pos[1] = 0
        elif self.pos[0] > 500:
            self.pos[0] = 0
        elif self.pos[0] < 0:
            self.pos[0] = 500
        C.delete('redy')                                                                              # Erase the old snake
        self.colision_food()
        self.colision_player()  
        self.closest()                                                                                # Verify if the snake ate some food
        while len(self.body) > self.lenght:                                                             # Fix the lenght of the snake
            del self.body[-1]
        for elem in self.body:
            C.create_oval(elem[0],elem[1],elem[0]+SIZE,elem[1]+SIZE,fill='red',tags='redy')

    def distance(self,elem):
        self.dist.append([self.pos[0] - elem[0], self.pos[1] - elem[1]])
        self.value.append(abs(self.pos[0] - elem[0]) + abs(self.pos[1] - elem[1]))

    def closest(self):
        for elem in self.player.body:
            self.distance(elem)
        if self.value != []:
            self.near = self.dist[self.value.index(min(self.value))]
        self.value, self.dist = [], []
        
    def colision_food(self):
        if self.pos[0] == self.food.pos[0] and self.pos[1] == self.food.pos[1]:                         # If the snake hits the food, the lenght is 
            self.lenght += 1 
            label4.configure(text = str(self.lenght))
            self.food.represent()
        
    def colision_player(self):
        if [self.pos[0],self.pos[1]] in self.player.body:
            self.player.lenght = 1
            label2.configure(text = str(self.player.lenght))
    
    def tick(self):
        self.represent()
        self.movement()
        self.clock.after(300, self.tick)

F = Food()
P = Player(F)
P.represent()
E1 = Enemy(root,F,P)

F.represent()

first = Thread(E1.tick())
first.start()

play = Thread(P.represent())
play.start()

arrow_up = root.bind("<Up>",P.mov_up)
arrow_down = root.bind("<Down>",P.mov_down)
arrow_right = root.bind("<Right>",P.mov_right)
arrow_left = root.bind("<Left>",P.mov_left)

C.pack()


root.mainloop()