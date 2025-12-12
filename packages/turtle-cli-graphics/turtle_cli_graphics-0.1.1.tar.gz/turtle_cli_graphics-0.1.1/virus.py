import turtle as t

# -----------------------------
# Setup Screen
# -----------------------------
t.setup(800, 600)
t.bgcolor("black")
t.title("Virus Danger Alert")

# Turtle settings
t.speed(2)
t.pensize(4)
t.color("red")
t.hideturtle()

# -----------------------------
# Draw Outer Warning Circle
# -----------------------------
t.penup()
t.goto(0, -200)
t.pendown()

t.begin_fill()
t.circle(200)
t.end_fill()

# Draw inner black circle (to create a ring)
t.color("black")
t.penup()
t.goto(0, -170)
t.pendown()
t.begin_fill()
t.circle(170)
t.end_fill()

# -----------------------------
# Draw Biohazard / Virus Arms
# -----------------------------
t.color("red")
t.pensize(8)

def arc():
    t.circle(100, 60)   # draw curved arm

# 3 virus hazard arms
for angle in [0, 120, 240]:
    t.penup()
    t.goto(0, 0)
    t.setheading(angle)
    t.forward(80)
    t.pendown()
    arc()

# -----------------------------
# Draw Center Virus Dot
# -----------------------------
t.penup()
t.goto(0, -30)
t.pendown()
t.begin_fill()
t.circle(30)
t.end_fill()

# -----------------------------
# Danger Text
# -----------------------------
t.penup()
t.goto(0, 240)
t.color("red")
t.write("⚠ VIRUS ALERT ⚠", align="center", font=("Arial", 30, "bold"))

t.done()
