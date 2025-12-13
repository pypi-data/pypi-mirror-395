from turtle import Shape
from turtle import Turtle

shape = Shape("compound")
shape.addcomponent(((0,0),(10,-5),(0,10),(-10,-5)), "white")
t = Turtle()

t.screen.title("Object-oriented turtle demo")
t.screen.bgcolor("orange")
print(f"{t.screen.getshapes()=}")

print(f"{t.pos()=}")
t.screen.mainloop()
