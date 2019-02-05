
from pprint import pprint
from threading import Timer
import sys, termios, tty, os, time







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
	if gameover == False:
		timer = Timer(0.2, refresh)
		timer.start()




def refresh():
	move()
	#sys.stdout.write("\r"*20)
	#sys.stdout.flush()
	string = ""
	for row in board:
		
		for item in row:
			#print(item)
			if item >= 1:
				string +="O" 
			else:
				string += " "
		string += "\n\r"
	
	os.system("clear")
	sys.stdout.write(string + "\r")	
	sys.stdout.flush()
	starttimer()

		
def move():
	global headloc
	global gameover
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
	if board[newloc[0]][newloc[1]] == 0:
		# Set value of current loc (in s)
		board[newloc[0]][newloc[1]] = (board[currentloc[0]][currentloc[1]])+1
		headloc = newloc
	else:
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



board = createboard(10, 20)

startloc_h = int(len(board[0])/2)
startloc_v = int(len(board)/2)


# set head value
board[startloc_v][startloc_h] = 1
headloc = [startloc_v, startloc_h]


direction = "RIGHT"
gameover = False


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