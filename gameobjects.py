from turtle import Turtle
from utils import *


class Paddle(Turtle):
    def __init__(self, init_x, init_y):
        super().__init__()
        self.hideturtle()
        self.shape("square")
        self.color("white")
        self.penup()
        self.shapesize(stretch_len=STRETCH_LENGTH, stretch_wid=STRETCH_HEIGHT)
        self.setx(init_x)
        self.sety(init_y)
        self.showturtle()
        self.score = 0

    def upward(self):
        if self.ycor() + PADDLE_HEIGHT / 2 <= UPPER_BOUND:
            self.sety(self.ycor() + STEP_BLOCK)

    def downward(self):
        if self.ycor() - PADDLE_HEIGHT / 2 >= LOWER_BOUND:
            self.sety(self.ycor() - STEP_BLOCK)


class Ball(Turtle):
    def __init__(self, heading):
        super().__init__()
        # self.speed("normal")
        self.shape("circle")
        self.color("yellow")
        self.penup()
        self.shapesize(stretch_len=BALL_STRETCH, stretch_wid=BALL_STRETCH)
        self.setx((RIGHT_BOUND - LEFT_BOUND) / 2)
        self.sety(LOWER_BOUND + PIXEL_BLOCK)
        self.setheading(heading)

    def wall_collision(self):
        if self.ycor() >= UPPER_BOUND or self.ycor() <= LOWER_BOUND:
            self.setheading(360 - self.heading())

    def wall_through(self):
        if self.xcor() > RIGHT_BOUND + 2 * PIXEL_BLOCK:
            print(self.xcor())
            # player left has scored
            return True
        elif self.xcor() < LEFT_BOUND - 2 * PIXEL_BLOCK:
            print(self.xcor())
            # player right has scored
            return True
        return False

    def paddle_collision(self, left_player, right_player):
        if self.distance(right_player) <= PADDLE_HEIGHT / 2 + BALL_RADIUS and self.xcor() > RIGHT_BOUND - PIXEL_BLOCK:
            current_heading = self.heading()
            if current_heading > 180:
                current_heading -= 180
            self.setx(RIGHT_BOUND - PIXEL_BLOCK)
            self.setheading(180 - current_heading)
            return True
        elif self.distance(left_player) <= PADDLE_HEIGHT / 2 + BALL_RADIUS and self.xcor() < LEFT_BOUND + PADDLE_WIDTH:
            self.setx(LEFT_BOUND + PADDLE_WIDTH)
            self.setheading(180 - self.heading())
            return True
        return False
