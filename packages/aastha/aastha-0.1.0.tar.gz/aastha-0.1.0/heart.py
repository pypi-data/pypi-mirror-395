import turtle as t

# --- Setup screen ---
t.setup(width=800, height=600)   # Optional: window size
t.bgcolor("black")               # Background black
t.title("Arrow Drawing a Heart")

# --- Setup turtle (arrow) ---
t.shape("arrow")                 # Make the turtle look like an arrow
t.color("red")                   # Pen color (and fill color)
t.speed(3)                       # 1 (slow) - 10 (fast), or "fastest"
t.pensize(3)

# Move to a nicer starting position
t.penup()
t.goto(0, -100)                  # Start a bit lower so heart is centered
t.pendown()

# --- Draw and fill heart ---
t.begin_fill()

t.left(140)                      # Tilt to start heart curve
t.forward(180)                   # Left side of heart

# Top left curve
t.circle(-90, 200)               # radius, extent in degrees

# Go to the other side
t.left(120)

# Top right curve
t.circle(-90, 200)

t.forward(180)                   # Right side of heart back to bottom point

t.end_fill()

# Hide the turtle (arrow) at the end (optional)
t.hideturtle()

# Keep window open until clicked
t.done()
