
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
	timer = Timer(0.2, refresh)
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
		debugstring = str(verti_spot)+" "+str(horiz_spot)
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
				#if item % 2 == 0:
				string +="\033[91m"+"#"+'\x1b[0m'
				#else:
				#	string +="\x1b[41m"+str(item)
			elif item == -1:
				string +="\033[91m"+"O"+'\x1b[0m'
			else:
				string += "\x1b[102m"+" "+'\x1b[0m'
		string += "\n\r"
	
	os.system("clear")
	sys.stdout.write(string + "\r"+ '\x1b[0m'+debugstring)	
	sys.stdout.flush()
	timerdown = True
	starttimer()

		
def move():
	global headloc
	global gameover
	global timerdown
	movedir = direction
	if movedir == "UP":
		vector = (-1,0)
	elif movedir == "DOWN":
		vector = (1,0)
	elif movedir == "LEFT":
		vector = (0,-1)
	elif movedir == "RIGHT":
		vector = (0,1)
	currentloc = headloc
	# Apply vector to get new location
	newloc = [currentloc[0]+vector[0],currentloc[1]+vector[1]]
	
	# Check whether it is safe to move there
	if board[newloc[0]][newloc[1]] <= 0:
		
		# if its food, eat it and set it to 0
		if board[newloc[0]][newloc[1]] == -1:
			timerdown = False
			board[newloc[0]][newloc[1]] = 0
			#generate new food spot
			place_food()

		# Set value of current loc (in s)
		board[newloc[0]][newloc[1]] = (board[currentloc[0]][currentloc[1]])+1
		headloc = newloc


	else:
		debugstring = "GAME OVER"
		gameover = True




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


direction = "RIGHT"
gameover = False

# makes snake not be infinite length
timerdown = True


starttimer()

while gameover == False:
	
	char = getch()
	#print("char is", char)
	
	if char == "q":
		gameover = True
	
	if char == "w":
		direction = "UP"
	if char == "a":
		direction = "LEFT"
	if char == "d":
		direction = "RIGHT"
	if char == "s":
		direction = "DOWN"

sys.exit()