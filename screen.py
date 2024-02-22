import time
import turtle
from turtle import Screen
from gameobjects import *
from utils import *


def draw_divider():
    tempo = turtle.Turtle()
    tempo.hideturtle()  # hide the drawer
    tempo.sety(LOWER_BOUND)
    tempo.setx((RIGHT_BOUND - LEFT_BOUND) / 2)
    tempo.speed("fastest")
    tempo.setheading(90)
    tempo.pencolor("white")
    for i in range(round((UPPER_BOUND - LOWER_BOUND) / 10)):
        tempo.pendown()
        tempo.forward(PIXEL_BLOCK)

        tempo.penup()
        tempo.forward(PIXEL_BLOCK)
        pass


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.pencolor("white")
        self.l_score = 0
        self.r_score = 0
        self.write_scores()

    def write_scores(self):
        self.clear()
        self.goto((RIGHT_BOUND - LEFT_BOUND) / 2 - PIXEL_BLOCK, UPPER_BOUND - SCORE_FONT - PIXEL_BLOCK)
        self.write(arg=self.l_score, font=("Comic Sans", SCORE_FONT, "normal"), align="right")
        self.goto((RIGHT_BOUND - LEFT_BOUND) / 2 + PIXEL_BLOCK, UPPER_BOUND - SCORE_FONT - PIXEL_BLOCK)
        self.write(arg=self.r_score, font=("Comic Sans", SCORE_FONT, "normal"), align="left")


class Pong:
    def __init__(self):
        self.leftPlayer = None
        self.rightPlayer = None
        self.gameScreen = None
        self.isOver = False
        self.ball = None
        self.scoreboard = None

        self.setup_screen()
        self.setup_players()
        self.setup_ball()
        self.scoreboard = ScoreBoard()

    def setup_ball(self):
        self.ball = Ball(BALL_ANGLE)
        pass

    def setup_screen(self):
        self.gameScreen = Screen()
        self.gameScreen.title("LET'S PLAY PONG!")
        self.gameScreen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.gameScreen.setworldcoordinates(llx=0, lly=0,
                                            urx=SCREEN_WIDTH, ury=SCREEN_HEIGHT)
        self.gameScreen.bgcolor("black")
        self.gameScreen.tracer(0)
        self.gameScreen.onclick(self.stop_game)
        self.gameScreen.listen()
        draw_divider()

    def setup_players(self):
        self.leftPlayer = Paddle(init_x=INIT_COR['left']['x'], init_y=INIT_COR['left']['y'])
        self.rightPlayer = Paddle(init_x=INIT_COR['right']['x'], init_y=INIT_COR['right']['y'])

    def reset_screen(self):
        self.leftPlayer.goto(INIT_COR['left']['x'], INIT_COR['left']['y'])
        self.rightPlayer.goto(INIT_COR['right']['x'], INIT_COR['right']['y'])
        self.ball.goto(INIT_COR['ball']['x'], INIT_COR['ball']['y'])
        self.ball.setheading(BALL_ANGLE)
        self.scoreboard.l_score = self.leftPlayer.score
        self.scoreboard.r_score = self.rightPlayer.score
        self.scoreboard.write_scores()

    def stop_game(self, x, y):
        print(f"Clicked at: ({x}, {y})")
        self.isOver = True

    def bind_events(self):
        self.gameScreen.onkeypress(key='w', fun=self.leftPlayer.upward)
        self.gameScreen.onkeypress(key='s', fun=self.leftPlayer.downward)
        self.gameScreen.onkeypress(key='Up', fun=self.rightPlayer.upward)
        self.gameScreen.onkeypress(key='Down', fun=self.rightPlayer.downward)
        self.gameScreen.listen()


pong = Pong()
pong.bind_events()

while not pong.isOver:
    time.sleep(SLEEP_TIME)
    if not pong.ball.paddle_collision(pong.leftPlayer, pong.rightPlayer):
        pong.ball.wall_collision()
    pong.ball.forward(STEP_BLOCK)
    pong.gameScreen.update()
    if pong.ball.wall_through():
        if pong.ball.xcor() > RIGHT_BOUND + 2 * PIXEL_BLOCK:
            pong.leftPlayer.score += 1
        elif pong.ball.xcor() < LEFT_BOUND - 2 * PIXEL_BLOCK:
            pong.rightPlayer.score += 1
        pong.reset_screen()

pong.gameScreen.exitonclick()
