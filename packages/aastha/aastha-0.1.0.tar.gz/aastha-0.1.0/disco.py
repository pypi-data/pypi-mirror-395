import turtle 
import colorsys

t = turtle.Turtle()
s = turtle.Screen().bgcolor('black')
t.speed(0)
n=70
h=0
for i in range(360):
    c = colorsys.hsv_to_rgb(h, 1, 0.5)
    h+=1/n 
    t.color(c)
    t.left(1)
    t.fd(1)
    for i in range (2):
        t.left(2)
        t.circle(100)import turtle as t
# import colorsys
# import turtle as t

# # Safe screen setup
# screen = t.Screen()
# screen.setup(800, 800)
# screen.bgcolor("black")
# screen.title("DJ Disco Disc - Spiral Gradient")

# t.speed(0)
# t.hideturtle()
# t.penup()
# t.goto(0, 0)
# t.pendown()

# t.tracer(0)   # reduce crashes by drawing in batches

# # Spiral Disc
# radius = 200
# steps = 1200

# for i in range(steps):
#     try:
#         # Gradient color
#         h = i / steps
#         r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
#         t.pencolor(r, g, b)

#         # Draw spiral arc
#         t.circle(radius, 2)

#         # Slowly reduce radius
#         radius -= 0.05
#         if radius <= 0:
#             break

#         if i % 5 == 0:
#             t.update()   # update every few frames to prevent crash

#     except:
#         # SAFETY: if window closes during drawing, exit gracefully
#         break

# t.update()
# t.done()
