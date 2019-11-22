# What comes after the # is not seen by python. These are comments. :)

from turtle import * # imports the module turtle,
                    #* stands for all, which makes things easier

speed(0) # sets the speed of drawing to 0, which is the fastest
pencolor('white') # sets the color of the pen/lines to white
bgcolor('black') # sets the color of the background/canvas to black

x = 0 # creates a variable x with value 0
up() # lifts up the pen, so no lines are drawn

#note fd() means move forward, bk() means move back
# rt() or lt() means tilt right by a certain angle

rt(45) 
fd(90) 
rt(135) 

down() # sets down the pen, so that turtle can draw
while x < 120: 
    fd(200)     
    rt(61)
    fd(200)
    rt(61)
    fd(200)
    rt(61)
    fd(200)
    rt(61)
    fd(200)
    rt(61)
    fd(200)
    rt(61)
    rt(11.1111) 
    x = x+1

exitonclick() # When you click, turtle exits.