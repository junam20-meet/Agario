import turtle
import time
import random
import math
import timeit
from ball import Ball 
from turtle import Screen
turtle.tracer(0)
turtle.hideturtle()
turtle.colormode(1) 

turtle.bgpic("bgpic.png")

you_won = turtle.Turtle()
turtle.register_shape('youwon.gif')
you_won.goto(0,0)

game_over = turtle.Turtle()
turtle.register_shape("GameOver.gif")
game_over.goto(0,0)

powerupS = turtle.Turtle()
turtle.register_shape("powerup2.gif")
powerupS.penup()
powerupS.shape('powerup2.gif')
powerupS.goto(10000,10000)



expu = False # (powerup exists meaning appears on screen)
durpu = False # (during powerup meaning during 3 seconds of pause)
running = True 

screen_width = turtle.getcanvas().winfo_width()/2
screen_height = turtle.getcanvas().winfo_height()/2
clr = input('choose a  color!!')


my_ball = Ball(0,0,5,5,70,clr)
number_of_balls = 5
minimum_ball_radius = 10
maximum_ball_radius = 100
minimum_ball_dx = -5
maximum_ball_dx = 5
minimum_ball_dy = -5
maximum_ball_dy = 5

BALLS = []

for i in range (number_of_balls):
	x = random.randint(-screen_width+ maximum_ball_radius, screen_width -maximum_ball_radius)
	y = random.randint(-screen_height + maximum_ball_radius, screen_height -maximum_ball_radius)
	dx = random.randint(minimum_ball_dx, maximum_ball_dx)
	dy = random.randint(minimum_ball_dy , maximum_ball_dy)
	r = random.randint(minimum_ball_radius,maximum_ball_radius)
	color = (random.random(), random.random(), random.random())
	new_balls = Ball(x,y,dx,dy,r,color)
	BALLS.append(new_balls)


def move_all_balls():
	for i in BALLS:
		i.move(screen_width,screen_height)



def collide(ball_a,ball_b):
	if ball_a == ball_b:
		return False
	distance = math.sqrt(math.pow((ball_b.xcor()-ball_a.xcor()), 2) + math.pow((ball_b.ycor()-ball_a.ycor()), 2))
	radii = ball_a.r + ball_b.r
	if distance <= radii:
		if ball_a==my_ball or ball_b==ball_b:
			print("you killed " + str(my_ball.count) + " balls")
			turtle.penup()
			turtle.goto(200,300)
			turtle.pendown()
			turtle.pencolor('deep pink')
			turtle.clear()
			turtle.write("you killed " + str(my_ball.count) + " balls" , align = "left" , font = ("suruma" , 30 , "normal"))
		return True
	else:
		return False






def check_all_balls_collisions():

	all_balls = []
	all_balls.append(my_ball)
	for ball in BALLS:
		all_balls.append(ball)

	for ball_a in all_balls :
		for ball_b in all_balls:
			global running
			if collide(ball_a,ball_b):
				r1 = ball_a.r
				r2 = ball_b.r
				x = random.randint(-screen_width+ maximum_ball_radius, screen_width -maximum_ball_radius)
				y = random.randint(-screen_height + maximum_ball_radius, screen_height -maximum_ball_radius)
				dx = random.randint(minimum_ball_dx, maximum_ball_dx)
				while (dx == 0):
					dx = random.randint(minimum_ball_dx, maximum_ball_dx)
				dy = random.randint(minimum_ball_dy , maximum_ball_dy)
				while (dy == 0):
					dy = random.randint(minimum_ball_dy , maximum_ball_dy)

				r = random.randint(minimum_ball_radius,maximum_ball_radius)
				color = (random.random(), random.random(), random.random())
				if r1 >= r2:
					ball_a.count+=1
					if ball_b == my_ball:
						print("game over!")
						running = False 
						game_over.shape("GameOver.gif")
					else:
						ball_b.new_ball(x,y,dx,dy,r,color)
						ball_a.r = ball_a.r + 5
						ball_a.shapesize(ball_a.r/10)
				'''else:
					if ball_a == my_ball:
						print ("game over!")
						running = False
						game_over.shape("GameOver.gif")
					else:
						ball_a.new_ball(x,y,dx,dy,r,color)
						ball_b.r = ball_b.r + 5
						ball_b.shapesize(ball_b.r/10)'''



def win():
	if my_ball.shapesize()[1] >= 110:
		global running
		running = False
		you_won.shape("youwon.gif")





def movearound():
	cursor_x = turtle.getcanvas().winfo_pointerx() - screen_width
	cursor_y = screen_height - turtle.getcanvas().winfo_pointery()
	my_ball.goto(cursor_x,cursor_y)





def create_powerup():
	global durpu
	global expu
	if not durpu and not expu:
		n = random.randint(0,5)
		if n == 1:
			x = random.randint(-screen_width+ maximum_ball_radius, screen_width -maximum_ball_radius)
			y = random.randint(-screen_height + maximum_ball_radius, screen_height -maximum_ball_radius)			
			powerupS.goto(x,y)
			expu = True


def powerup(): # checks if my_ball is in collision with powerup
	global expu
	if expu:
		my_ball_pos_max = (my_ball.pos()[0]+my_ball.r, my_ball.pos()[1]+my_ball.r)
		my_ball_pos_min = (my_ball.pos()[0]-my_ball.r, my_ball.pos()[1]-my_ball.r)
		if my_ball_pos_min[0] < powerupS.pos()[0] < my_ball_pos_max[0] and my_ball_pos_min[1] < powerupS.pos()[1] < my_ball_pos_max[1]:
			powerupS.goto(10000,10000)
			slowdown()
			expu = False



def slowdown():
	pu_pen = turtle.Turtle()
	pu_pen.hideturtle()
	global durpu
	durpu = True
	start = timeit.default_timer()
	for ball in BALLS:
		ball.dx = ball.dx/10
		ball.dy = ball.dy/10
	while timeit.default_timer() - 3 < start and running:
		print(start,"START!!!")
		run()
		if 0 < timeit.default_timer() - start < 1:
			sec = 3
		if 1 < timeit.default_timer() - start < 2:
			sec = 2
		if 2 < timeit.default_timer() - start < 3:
			sec = 1
		pu_pen.penup()
		pu_pen.goto(-550,190)
		pu_pen.pendown()
		pu_pen.pencolor('red')
		pu_pen.clear()
		pu_pen.write(sec , align = "right" , font = ("suruma" , 90 , "bold"))
	pu_pen.clear()
	for ball in BALLS:
		dx = random.randint(minimum_ball_dx, maximum_ball_dx)
		while (dx == 0):
			dx = random.randint(minimum_ball_dx, maximum_ball_dx)
		dy = random.randint(minimum_ball_dy , maximum_ball_dy)
		while (dy == 0):
			dy = random.randint(minimum_ball_dy , maximum_ball_dy)
		ball.dx = dx
		ball.dy = dy
	durpu = False


def run():
	screen_width = turtle.getcanvas().winfo_width()/2
	screen_height = turtle.getcanvas().winfo_height()/2
	movearound() 
	move_all_balls()
	check_all_balls_collisions()
	win()
	create_powerup()
	if durpu == False :
		powerup()
	turtle.update() 
	time.sleep(0.1)

while running == True:
	run()


for ball in BALLS:
	ball.r = 0
	ball.hideturtle()


my_ball.r = 0
my_ball.hideturtle()



turtle.update()
time.sleep(0.1)
print("end")


turtle.mainloop() 
