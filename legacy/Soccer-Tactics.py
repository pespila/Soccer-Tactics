#!/usr/local/bin

import csv
from turtle import *
from random import *
from time import *

class TacticBoard(object):
        addshape("../img/ball.gif")
        addshape("../img/feld2.gif")
        addshape("../img/spieler.gif")

        def __init__(self):
                self.screen = getscreen()
                self.ball = Turtle("../img/ball.gif")
                self.player = []

        @staticmethod
        def InitScreen(self):
                self.screen.setup(width=0.6, height=1.0)
                self.screen.title("Soccer Tactics")
                self.screen.bgcolor("white")
                self.screen.bgpic("../img/feld2.gif")

        @staticmethod
        def InitBall(self):
                self.ball.penup()
                self.ball.speed(3)
                self.ball.setpos((0, -250))
                self.ball.speed(0)
                self.ball.ondrag(self.ball.goto)

        @staticmethod
        def InitPlayer(self):
                system = []
                with open('../data/coords.csv', 'rb') as f:
                        reader = csv.reader(f)
                        for row in reader:
                                system.append(tuple([int(row[0]), int(row[1])]))
                for i in range(0,11):
                        k = Turtle("../img/spieler.gif")
                        k.penup()
                        k.speed(3)
                        k.setpos(system[i])
                        k.speed(0)
                        k.ondrag(k.goto)
                        self.player.append(k)

        @staticmethod
        def Start(self):
                InitBall(self)
                InitPlayer(self)
		
        @staticmethod
        def Restart(self):
                self.screen.clear()
                self.screen.title("Soccer Tactics")
                self.screen.bgcolor("white")
                self.screen.bgpic("../img/feld2.gif")
                Start(self)

board = TacticBoard()
board.InitScreen(board)
board.InitBall(board)
board.InitPlayer(board)

listen()
mainloop()