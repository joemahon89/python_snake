
from pprint import pprint
from threading import Timer
import sys, termios, tty, os, time
from random import randint






def createboard(height, width):
	board = []
	for i in range(0,height):
		row = []
		char0 = 0
		for j in range(0,width):
			row.append(char0)
		board.append(row)
	return board


def starttimer():
	#if gameover == False:
	timer = Timer(0.1, refresh)
	timer.start()


def pick_food_spot():
	global width
	global height
	verti_spot = randint(0, height-1)
	horiz_spot = randint(0, width-1)
	return verti_spot, horiz_spot

def place_food():
	global board
	global debugstring
	placedfood = False
	while placedfood == False:
		verti_spot, horiz_spot = pick_food_spot()
		#debugstring = str(verti_spot)+" "+str(horiz_spot)
		if board[verti_spot][horiz_spot] == 0:
			board[verti_spot][horiz_spot] = -1
			placedfood = True

debugstring = ""



def refresh():
	move()
	#sys.stdout.write("\r"*20)
	#sys.stdout.flush()
	string = ""
	global timerdown
	for index, row in enumerate(board):
		for index2,item in enumerate(row):
			if timerdown == True:
				if item > 0:
				#print(board[index][index2])
					board[index][index2] = board[index][index2]-1

	for row in board:
		for item in row:

			#print(item)
			if item >= 1:
				if item % 2 == 0:
					string +="\033[91m"+"██"+'\x1b[0m'
				else:
					string +="\033[92m"+"██"+'\x1b[0m'
			elif item == -1:
				string +="\033[93m"+"██"+'\x1b[0m'
			else:
				string += "\x1b[102m"+"██"+'\x1b[0m'
		string += "\n\r"
	
	os.system("clear")
	sys.stdout.write(string + "\r"+ '\x1b[0m'+"SCORE: "+score+debugstring)	
	sys.stdout.flush()
	timerdown = True
	if gameover == False:
		starttimer()

		
def move():
	global headloc
	global gameover
	global timerdown
	global score
	global vector
	global new_direction
	global current_direction
	newdir = False
	if new_direction == "UP":
		if current_direction != "DOWN":
			vector = (-1,0)
			newdir = True
	elif new_direction == "DOWN":
		if current_direction != "UP":
			vector = (1,0)
			newdir = True
	elif new_direction == "LEFT":
		if current_direction != "RIGHT":
			vector = (0,-1)
			newdir = True
	elif new_direction == "RIGHT":
		if current_direction != "LEFT":
			vector = (0,1)
			newdir = True
	currentloc = headloc
	if newdir == True:
		current_direction = new_direction

	# Apply vector to get new location
	newloc = [currentloc[0]+vector[0],currentloc[1]+vector[1]]
	
	# Going past V min/max
	if newloc[0] == -1:
		newloc[0] = height-1
	elif newloc[0] == height:
		newloc[0] = 0

	# Goin past H min/max
	if newloc[1] == -1:
		newloc[1] = width-1
	elif newloc[1] == width:
		newloc[1] = 0	

	# Check whether it is safe to move there
	if board[newloc[0]][newloc[1]] <= 0:
		
		# if its food, eat it and set it to 0
		if board[newloc[0]][newloc[1]] == -1:
			timerdown = False
			board[newloc[0]][newloc[1]] = 0
			# add to score, int/str conv done here so not done evry frame
			score = str(int(score)+1)

			#generate new food spot
			place_food()

		# Set value of current loc (in s)
		board[newloc[0]][newloc[1]] = (board[currentloc[0]][currentloc[1]])+1
		headloc = newloc


	else:
		debugstring = "GAME OVER"
		gameover = True
		print_game_over()




def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)

	finally:
		pass
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch


def print_game_over():
	string = ""
	string +="\n\r"
	string +="\n\r"
	string +=("\033[91m"+"   ███ ███ ██ ██ ███ ███ █ █ ███ ███"+'\x1b[0m'*width)+"\n\r"
	string +=("\033[91m"+"   █   █ █ █ █ █ █   █ █ █ █ █   █ █"+'\x1b[0m'*width)+"\n\r"
	string +=("\033[91m"+"   █ █ ███ █ █ █ ██  █ █ █ █ ██  ██"+'\x1b[0m'*width)+"\n\r"
	string +=("\033[91m"+"   █ █ █ █ █   █ █   █ █ █ █ █   █ █"+'\x1b[0m'*width)+"\n\r"
	string +=("\033[91m"+"   ███ █ █ █   █ ███ ███  █  ███ █ █"+'\x1b[0m'*width)+"\n\r"
	string +="\n\r"
	string +="\n\r"
	string +="\n\r"


	# for row in board:
	# 	for item in row:
	# 		string +="\033[91m"+"██"+'\x1b[0m'
	# 	string += "\n\r"
	os.system("clear")
	sys.stdout.write(string + "\r"+ '\x1b[0m'+"FINAL SCORE: "+score+"\r\n")	
	sys.stdout.flush()
	print("")
	exit()

height = 10
width = 20


board = createboard(height, width)

startloc_h = int(len(board[0])/2)
startloc_v = int(len(board)/2)

# set first food item
board[3][3] = -1


# set head value
board[startloc_v][startloc_h] = 5
headloc = [startloc_v, startloc_h]


current_direction = "RIGHT"
new_direction = "RIGHT"
gameover = False

# makes snake not be infinite length
timerdown = True

score = "0"
starttimer()

while gameover == False:
	
	char = getch()
	#print("char is", char)
	
	if char == "q":
		gameover = True
	
	if char == "w":
		new_direction = "UP"
	if char == "a":
		new_direction = "LEFT"
	if char == "d":
		new_direction = "RIGHT"
	if char == "s":
		new_direction = "DOWN"

sys.exit()


# todo
# swap wasd with arrow keys
# rather than reprint, use this to go the start of prev line "\033[F"

"""

   ██████ ██████ ██████ ██  ██ ██████
   ██     ██  ██ ██  ██ ██  ██ ██
   ██████ ██  ██ ██████ ████   █████
       ██ ██  ██ ██  ██ ██  ██ ██
   ██████ ██  ██ ██  ██ ██  ██ ██████

████████████████████████████████████████

"""