import turtle

# ---------- Setup ----------
screen = turtle.Screen()
screen.title("Three Layer Birthday Cake")
screen.bgcolor("light pink")

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(3)
pen.pensize(3)


# ---------- Helper: Draw rectangle ----------
def draw_rect(x, y, width, height, color):
    pen.up()
    pen.goto(x, y)
    pen.down()
    pen.fillcolor(color)
    pen.begin_fill()
    for _ in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)
    pen.end_fill()


# ---------- Draw cake layers ----------
def draw_three_layer_cake():

    # Bottom layer
    draw_rect(-180, -120, 360, 80, "chocolate")

    # Middle layer
    draw_rect(-150, -40, 300, 70, "light blue")

    # Top layer
    draw_rect(-120, 30, 240, 60, "hot pink")

    # Frosting on the top layer
    pen.up()
    pen.goto(-110, 90)
    pen.down()
    pen.fillcolor("white")
    pen.begin_fill()
    for _ in range(2):
        pen.forward(220)
        pen.left(90)
        pen.forward(15)
        pen.left(90)
    pen.end_fill()


# ---------- Candle ----------
def draw_candle():
    # Candle body
    draw_rect(-10, 90, 20, 60, "yellow")

    # Flame
    pen.up()
    pen.goto(0, 150)
    pen.down()
    pen.fillcolor("orange")
    pen.begin_fill()
    pen.circle(10)
    pen.end_fill()

    # Wick
    pen.pensize(4)
    pen.pencolor("black")
    pen.up()
    pen.goto(0, 150)
    pen.down()
    pen.setheading(90)
    pen.forward(10)
    pen.pensize(3)
    pen.pencolor("black")


# ---------- Main ----------
draw_three_layer_cake()
draw_candle()

pen.up()
pen.goto(0, 200)
pen.color("purple")
pen.write("Happy Birthday! 🎉🎂", align="center", font=("Arial", 24, "bold"))

screen.mainloop()
