###########################################################################
#Import relevant libraries
###########################################################################
import os
import sys
import subprocess
import pkg_resources
import PIL

from PIL import Image, ImageDraw, ImageTk
from ShortestPath import *
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *
from tkinter import ttk

###########################################################################
#Main GUI form - Creating tkinter application and all subsequent forms
###########################################################################
root = tk.Tk()
root.resizable(False, False)
root.title("Find or Build HSSInc.")

#Get file path to set form icon
filePath = os.path.dirname(os.path.abspath(__file__))
root.iconbitmap(filePath+"/Gameico.ico")

#Set geometry so that form appears at the centre of the parent screen
app_width=800
app_height=800

d_screenWidth=root.winfo_screenwidth()
d_screenHeight=root.winfo_screenheight()

x=(d_screenWidth/2) - (app_width/2)
y=(d_screenHeight/2) - (app_height/2)

x=int(x)
y=int(y)

root.geometry(f'{app_width}x{app_height}+{x}+{y}')
root.lift()

#Resize image to parent form size
def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo #avoid garbage collection

image = Image.open(filePath+"/GameStart.png")
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = ttk.Label(root, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill="both",expand = True)

#Game Mode Function - getShortestPath: retrieves a path reuiring the least number of moves from ShortestPath module and returns its length
def getShortestPath(a, start, end):
    path = main(a, start, end)
    if path!="No path":
        return len(path)-1
    else:
        return 0

#Game Mode Function - gameModeWindow: creates and runs the game while handling all game mechanics
def gameModeWindow(level):
    #Create game window
    import turtle
    gameWin = turtle.Screen()
    gameWin.cv._rootwindow.withdraw()
    gameWin.bgcolor("black")
    gameWin.title("Find or Build: Game Mode")
    filePath = os.path.dirname(os.path.abspath(__file__))
    gameWin.cv._rootwindow.iconbitmap(filePath+"/Gameico.ico")
    gameWin.setup(700, 700)
    gameWin.cv._rootwindow.resizable(False,False)

    #Create form to act as load screen while maze is created
    loadScreen=tk.Tk()
    l_width=250
    l_height=75

    l_screenWidth=loadScreen.winfo_screenwidth()
    l_screenHeight=loadScreen.winfo_screenheight()

    x=(l_screenWidth/2) - (l_width/2)
    y=(l_screenHeight/2) - (l_height/2)

    x=int(x)
    y=int(y)

    loadScreen.geometry(f'{l_width}x{l_height}+{x}+{y}')
    loadScreen.resizable(False,False)
    loadScreen.overrideredirect(1)
    loadScreen.lift()
    initial=Label(loadScreen, text="Initializing... \nPlease be patient")
    initial.place(x=25,y=25)

    #Hide the game window
    if level==None:
        loadScreen.quit()
        loadScreen.destroy()
        gameWin.cv._rootwindow.withdraw()
        return

    #Show the game Window
    if level=="*":
        loadScreen.quit()
        loadScreen.destroy()
        gameWin.cv._rootwindow.deiconify()
        return

    #Operate game objects
    class Writer(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("square")
            self.color("white")
            self.penup()
            self.speed(0)

    class End(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("square")
            self.color("gold")
            self.penup()
            self.speed(0)
            self.points = 100

        def complete(self):
            self.hideturtle()

    class Player(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("square")
            self.color("blue")
            self.penup()
            self.speed(0)
            self.points = 0

        def go_up(self):
            moveX = self.xcor()
            moveY = self.ycor()+24
            if (moveX, moveY) not in boundary and (moveX, moveY) in mazeBound:
                PlayerMoves.append((moveX,moveY))
                self.goto(moveX, moveY)

        def go_down(self):
            moveX = self.xcor()
            moveY = self.ycor()-24
            if (moveX, moveY) not in boundary and (moveX, moveY) in mazeBound:
                PlayerMoves.append((moveX,moveY))
                self.goto(moveX, moveY)

        def go_left(self):
            moveX = self.xcor()-24
            moveY = self.ycor()
            if (moveX, moveY) not in boundary and (moveX, moveY) in mazeBound:
                PlayerMoves.append((moveX,moveY))
                self.goto(moveX, moveY)

        def go_right(self):
            moveX = self.xcor()+24
            moveY = self.ycor()
            if (moveX, moveY) not in boundary and (moveX, moveY) in mazeBound:
                PlayerMoves.append((moveX,moveY))
                self.goto(moveX, moveY)

        def is_complete(self, other):
            (x, y) = (self.xcor(), self.ycor())
            if (x, y) == other:
                return True
            else:
                return False

    #Create Maze using the turtle objects
    def create_maze(level):
        for y in range(len(level)):
            temp = []
            for x in range(len(level[y])):
                character = level[y][x]
                screen_x = -288+(x*24)
                screen_y = 288-(y*24)
                mazeBound.append((screen_x, screen_y))

                if character == "X":
                    writer.goto(screen_x, screen_y)
                    writer.stamp()
                    boundary.append((screen_x, screen_y))
                    temp.append(1)

                if character == "P":
                    player.goto(screen_x, screen_y)
                    temp.append(0)
                    S.append((y, x))

                if character == "E":
                    end.goto(screen_x, screen_y)
                    endlst.append((screen_x, screen_y))
                    temp.append(0)
                    E.append((y, x))

                if character == " ":
                    temp.append(0)
            Maze.append(temp)

    writer = Writer()
    player = Player()
    end = End()

    endlst = [] #stores coordinates of end points to run in a loop
    boundary = [] #stores coordinates of walls
    Maze = [] #stores maze area in the form of matrix 
    mazeBound=[] #stores maze area
    S = [] #stores coordinates of the end point
    E = [] # stores coordinates of start point(player)
    
    create_maze(level)
    loadScreen.quit()
    loadScreen.destroy()
    gameWin.cv._rootwindow.deiconify()

    
    global PlayerMoves
    PlayerMoves=[]

    turtle.listen()
    turtle.onkey(player.go_up, "Up")
    turtle.onkey(player.go_down, "Down")
    turtle.onkey(player.go_left, "Left")
    turtle.onkey(player.go_right, "Right")

    gameWin.tracer(0)

    #Run the game
    global cancelled 
    cancelled=False
    running = True
    while running:
        def on_closing():
            #Handle game Window close event
            ans=tk.messagebox.askquestion("Confirm","Are you sure you want to exit Game Mode and return to start screen? Your progress will not be saved.",icon='warning')
            if ans=="yes":
                gameWin.cv._rootwindow.withdraw()
                global cancelled
                cancelled=True
        gameWin.cv._rootwindow.protocol("WM_DELETE_WINDOW",on_closing)
        if cancelled==True:
            return None
        
        #Close game Window after the final level is completed
        if level == []:
            gameWin.bye()
            return
        
        #Check if startpoint is equal to endpoint
        for c in endlst:
            if player.is_complete(c):
                begin = S.pop()
                finish = E.pop()
                end.complete()
                endlst = []
                gameWin.update()
                shortestPath = getShortestPath(Maze, begin, finish) #retrieve the least number of moves required to complete the level
                if len(PlayerMoves) == shortestPath:
                    gameWin.update()
                    gameWin.clear()
                    return end.points
                else:
                    #Handle level retry
                    option=tk.messagebox.askquestion("oops...  you failed!","Looks like you didn't complete the level in the least number of moves. \nRetry this level?",icon='question')
                    if option == "yes":
                        gameWin.update()
                        gameWin.clear()
                        return gameModeWindow(level)
                    else:
                        #Handle level skip
                        gameWin.bye()

                        #Create form to display shortest path animation (path that requires the least number of moves)
                        skip=tk.Tk()
                        skip.title("Animation")
                        skip.iconbitmap(filePath+"/Gameico.ico")
                        txtlabel=Label(skip,text="CLOSE THIS WINDOW TO CONTINUE")
                        txtlabel.pack(side = "top")
                        gifI=tk.PhotoImage(file="maze.gif")
                        skip.resizable(False,False)
                        skip.lift()
                        global gif_index
                        gif_index=0
                        def next_frame():
                            global gif_index
                            try:
                                gifI.configure(format="gif -index {}".format(gif_index))
                                gif_index=gif_index+1
                            except tk.TclError:
                                gif_index=0
                                return next_frame()
                            else:
                                skip.after(100,next_frame)
                        gif_label=tk.Label(skip,image=gifI)
                        gif_label.pack()
                        try:
                            skip.after_idle(next_frame)
                        except:
                            pass
                        skip.mainloop()
                        
                        
        try:
            gameWin.update()
        except:
            running = False
    #return 0 for skipped level
    return 0

#Game Mode Function - gameCommand: Handles the execution of game mode.
def gameCommands(levels):
    root.destroy()
    filePath = os.path.dirname(os.path.abspath(__file__))

    #Form to show instructions
    instructions=tk.Tk()
    instructions.iconbitmap(filePath+"/Gameico.ico")
    instructions.title("Game Mode: Instructions")
    
    instructions_width=700
    instructions_height=700

    i_screenWidth=instructions.winfo_screenwidth()
    i_screenHeight=instructions.winfo_screenheight()

    x=(i_screenWidth/2) - (instructions_width/2)
    y=(i_screenHeight/2) - (instructions_height/2)

    x=int(x)
    y=int(y)

    instructions.geometry(f'{instructions_width}x{instructions_height}+{x}+{y}')
    instructions.resizable(False,False)
    
    #Resize and display form background image
    def resize_image_ins(event):
        new_width = event.width
        new_height = event.height
        load = copy_of_ins.resize((new_width, new_height))
        ins = ImageTk.PhotoImage(load)
        labelIns.config(image = ins)
        labelIns.image = ins #avoid garbage collection


    load=Image.open(filePath+"/Instructions.png")
    copy_of_ins = load.copy()
    ins=ImageTk.PhotoImage(load)
    labelIns=ttk.Label(instructions,image=ins)
    labelIns.bind('<Configure>', resize_image_ins)
    labelIns.pack(fill="both", expand=True)
    instructions.mainloop()
    
    points = 0 #stores the accumulated score
    
    for index,level in enumerate(levels):
        #Call gameModeWindow to run the game and retrieve the score
        gained = gameModeWindow(level)
        if gained == None:
            break
        else:
            points = points+gained
            
        gameModeWindow(None) #Call one last time to close game window

        #Create form to display score
        scores = tk.Tk()
        scores.iconbitmap(filePath+"/Gameico.ico")
        scores.title("Confirm Score")

        form_width=500
        form_height=200

        f_screenWidth=scores.winfo_screenwidth()
        f_screenHeight=scores.winfo_screenheight()

        x=(f_screenWidth/2) - (form_width/2)
        y=(f_screenHeight/2) - (form_height/2)

        x=int(x)
        y=int(y)

        scores.geometry(f'{form_width}x{form_height}+{x}+{y}')

        scores.resizable(False,False)

        score=Label(scores,text="Your score is: "+str(points))
        score.place(x=25,y=50)

        if index!=len(levels)-1:
            msgSco=Label(scores, text="Please Proceed to the next level!")
            msgSco.place(x=25,y=75)
        else:
            if points < 600 and points >= 400:
                msgtxt="Great Work! Polish your skills a bit more to score better next time. \nAnyways, congradulations on completing the game."
            elif points < 400 and points >= 300:
                msgtxt="hmmm! You need to work a little bit more to score well. \nAnyways, congradulations on completing the game."
            elif points < 300:
                msgtxt = "Aaaaa Loser! You must love to fail to score this low. \nAnyways, congradulations on completing the game."
            else:
                msgtxt="Amazing! You must be a genius or something. \nAnyways, congradulations on completing the game."
            msgCong=Label(scores, text=msgtxt)
            msgCong.place(x=25,y=75)

        #Proceed to the next level when the score form is closed.
        def proceed():
            scores.quit()
            gameModeWindow("*")
        button = Button(scores, text="Proceed", command=proceed)
        button.place(x=400, y=150)
        scores.protocol("WM_DELETE_WINDOW",proceed)
        scores.lift()
        scores.mainloop()
        scores.destroy()
    next
    gameModeWindow([]) #Call gameModeWindow to close game window
    os.startfile("makecode.py") #return to main window after game has been played

#Game Mode Function - gameModeLevels: adds individual levels to "levels" array then executes game mode.
def gameModeLevels():
    root.withdraw() 
    levels = []  #stores individual levels
    #'X' = Wall
    #' ' = No Wall
    level_1 = [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XP  XXXXXXXXX       XXXXX",
        "X   XXXXXXXXX  XXXX XXXXX",
        "X               X      XX",
        "XXXX   XXXXXXXX  XXXXXXXX",
        "X     XXXXXXX       XXXXX",
        "X     XXXXXXX       XXXXX",
        "X         XXX          XX",
        "XXXX  XXXXXXXX XXXXXXXX X",
        "X    XXXXXXXX       XXX X",
        "X    XXXXXXXX  XXXX X  XX",
        "X                      XX",
        "XXXX   XX  XXXX  XXXXXXXX",
        "X                    XXXX",
        "X     XXXXXXX        XXXX",
        "X         XXX          XX",
        "X         XXX          XX",
        "XXXXXX XXXXXXXXXX  XXXX X",
        "X   XX XXXXXX       EXX X",
        "X   X          XXXX X  XX",
        "X         XXX  XX      XX",
        "XXXX   XX  XXXX  XXXXXXXX",
        "X       XXXXX       XXXXX",
        "X     XXXXXXX        XXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"]
    levels.append(level_1)

    level_2 = [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXPXXXXX              XXX",
        "XX XXXXX XXXXXXXXXXXX XXX",
        "XX XXXXX XXXXXXXXXXXX XXX",
        "XX                    XXX",
        "XX XXX XXXXXXXXXXXXXX XXX",
        "XX XXX                XXX",
        "XX XXX XXXXXXXXXXXXXX XXX",
        "XX XXX XXXXXXXXXXXXXX XXX",
        "XX    XX              XXX",
        "XX XXXXXXXXXXXXXXXXXX XXX",
        "XX XXXXXXXXXXXXXXXXXX XXX",
        "XX XXXXXXXXXXXXXXXXXX XXX",
        "XX XXXXXXXXXX   XXXXX XXX",
        "XX            X       XXX",
        "XX XXXXXXXXXXXXX XXXX XXX",
        "XX XXXX    XXXXX XXXX XXX",
        "XX XX   XX XXXXX XXXX XXX",
        "XX X  XXXX   E   XXXX XXX",
        "XX   XXXXXXXX XXXXXXX XXX",
        "XXXX XXXXXXXX XXXXXXX XXX",
        "XXXX                  XXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"]
    levels.append(level_2)

    level_3 = [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XX                  XXXXX",
        "XXX  XXXXXXXXX  XXXX XXXX",
        "XXX    XXXXXXXX        XX",
        "XXXX   XXXXXXXXX XXXXXXXX",
        "X     XXXXXXX    X  XXXXX",
        "X     XXXXXXX  XX  XXXXXX",
        "X         XXX  X       XX",
        "XXXXX XXXXXXXX XXX XXXX X",
        "X     XXEXXXX   X   XXX X",
        "X XXXXXX XXXXX XXXX XXXXX",
        "X      X    XX XXXX   XXX",
        "XXXXX  XX  XXX XXXXXX XXX",
        "X     XXXX       XXXX XXX",
        "XXXXX XXXXXXXXXXXXXXX XXX",
        "XXXXX     XXX XXXXXXX  XX",
        "X     XXXXXXX          XX",
        "XXXXX XXXX XXXXXX  XXXXXX",
        "X   X  XXXXXX   X      XX",
        "X XXX  XXX    XXXXXXX  XX",
        "X         XXX   X      XX",
        "XXXX   XX  XXXX  XX XXXXX",
        "X                   XXXXX",
        "XXXXXXXXXXXXXPXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"]
    levels.append(level_3)

    level_4 = [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXPXXXXX              XXX",
        "XX XXXXX XXXXXXXXXXXX XXX",
        "XX XXXXX XXXXXXXXXXXX XXX",
        "XX       XXXXXXX      XXX",
        "XX XXXXXXXXXXXXXXX XXXXXX",
        "XX XXX                XXX",
        "XX XXXXXXXXXXXXXXXXXX XXX",
        "XX XXX XXXXXXXXXXXXXX XXX",
        "XX XXX                XXX",
        "XXXXXX XXXXXXXXXXX XXXXXX",
        "XXXXXX XXXXXXXXXXX XXXXXX",
        "XXXXXX XXXXXXX     XXXXXX",
        "XXXXXX XXXXXX XXXXXXXXXXX",
        "XX            X       XXX",
        "XXXXXXX XXXXXXXX XXXX XXX",
        "XXXXXXX XX       XXXX XXX",
        "XXXXX   XX XXXXX  XXXXXXX",
        "XX X  XXXX   EXXX     XXX",
        "XX   XXXXXXXXXXXXXXXX XXX",
        "XXXX XXXXXXXXXXXXXXXX XXX",
        "XXXX                  XXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"]
    levels.append(level_4)

    level_5 = [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XX                    XXX",
        "XX XXXXXXXXXXXXXXXXXX XXX",
        "XX XXXXX    XXXX XXXX XXX",
        "XX XE    XX XXXX      XXX",
        "XX XXX XXXX XXXXXX XXXXXX",
        "XX XXX    X           XXX",
        "XX XXXXXX XXXXXXXXXXX XXX",
        "XX XXX    XXXX XXXXXX XXX",
        "XX XXX XXX       X    XXX",
        "XX  XX XXXXXXXX XX XXXXXX",
        "XXX   XXXXXXXXX XX XXXXXX",
        "XXXX XXXXXXXXX     XXXXXX",
        "XXXX X XXXXXX XXXX XXXXXX",
        "XX       X            XXX",
        "XXXXXXX XXXXXXXX XXXX XXX",
        "XXXXXXX        X XXXX XXX",
        "XXXXX   XX XXXXX  XXXXXXX",
        "XX X  XXXX    XXX     XXX",
        "XX   XXXXXX XXXXXXXXX XXX",
        "XXXX XXXXXX XXXXXXXXX XXX",
        "XXXXXP                XXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"]
    levels.append(level_5)

    level_6 = [
        "XXXXXXXXXXXEXXXXXXXXXXXXX",
        "X               X       X",
        "X  XXXXXXXXXXXX X XXXX XX",
        "X     XXX   X   X    X  X",
        "XX X    XX  XXX      XX X",
        "XX XXX XXXX XXXXXXXXXXXXX",
        "XXXXXX                XXX",
        "XX XXXXXX XXXX XXXXXX XXX",
        "X  X      XXXX XXXXXX XXX",
        "X  XXX          XXX   XXX",
        "X    XXXXX   XXXXX XXXXXX",
        "XXX    XXX XXXXXXX XXXXXX",
        "XXXX XXX           XXXXXX",
        "XXXX X XXXXXX XXXX XXXXXX",
        "X      XX             XXX",
        "X  XXXX XXXXXXXX XXXX XXX",
        "X  XXXX        XXXX   XXX",
        "X  XX   XX XXXXX  XX XXXX",
        "X  XXXXXXX    XXX      XX",
        "XX    XXXXX XXXXXXXXX  XX",
        "X     XXXXX XXXXXXXXXX   ",
        "XXXXX X                 X",
        "XXXXX XXXXXXXXXXXX XX   X",
        "X                  X    X",
        "XXXXXXXXXXXXXXXXXXPXXXXXX"]
    levels.append(level_6)
    gameCommands(levels)

#Creative Mode Function - creation: allows the user to create the maze and visulaize the shortest path from start to finsih
def creation():
    root.withdraw()
    root.destroy()

    filePath = os.path.dirname(os.path.abspath(__file__))

    #Form to show instructions
    instructions=tk.Tk()
    instructions.iconbitmap(filePath+"/Gameico.ico")
    instructions.title("Creative Mode: Instructions")
    
    instructions_width=700
    instructions_height=700

    i_screenWidth=instructions.winfo_screenwidth()
    i_screenHeight=instructions.winfo_screenheight()

    x=(i_screenWidth/2) - (instructions_width/2)
    y=(i_screenHeight/2) - (instructions_height/2)

    x=int(x)
    y=int(y)

    instructions.geometry(f'{instructions_width}x{instructions_height}+{x}+{y}')
    instructions.resizable(False,False)
    
    #Resize and display form background image
    def resize_image_ins(event):
        new_width = event.width
        new_height = event.height
        load = copy_of_ins.resize((new_width, new_height))
        ins = ImageTk.PhotoImage(load)
        labelIns.config(image = ins)
        labelIns.image = ins #avoid garbage collection


    load=Image.open(filePath+"/creativeIns.png")
    copy_of_ins = load.copy()
    ins=ImageTk.PhotoImage(load)
    labelIns=ttk.Label(instructions,image=ins)
    labelIns.bind('<Configure>', resize_image_ins)
    labelIns.pack(fill="both", expand=True)
    instructions.mainloop()


    #Create 'Creative Mode' window
    import turtle
    creative = turtle.Screen()
    creative.cv._rootwindow.withdraw()
    creative.bgcolor("black")
    creative.title("Find or Build: Creative Mode")
    filePath = os.path.dirname(os.path.abspath(__file__))
    creative.cv._rootwindow.iconbitmap(filePath+"/Gameico.ico")
    creative.setup(700, 700)
    creative.cv._rootwindow.resizable(False,False)

    #create form to act as load screen while maze is being created
    loadScreen=tk.Tk()
    l_width=250
    l_height=75

    l_screenWidth=loadScreen.winfo_screenwidth()
    l_screenHeight=loadScreen.winfo_screenheight()

    x=(l_screenWidth/2) - (l_width/2)
    y=(l_screenHeight/2) - (l_height/2)

    x=int(x)
    y=int(y)

    loadScreen.geometry(f'{l_width}x{l_height}+{x}+{y}')
    loadScreen.resizable(False,False)
    loadScreen.overrideredirect(1)
    loadScreen.lift()
    initial=Label(loadScreen, text="Initializing... \nPlease be patient")
    initial.place(x=25,y=25)


    class Writer(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("square")
            self.color("white")
            self.penup()
            self.speed(0)

    class End(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("square")
            self.color("gold")
            self.penup()
            self.speed(0)

    class Player(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("square")
            self.color("blue")
            self.penup()
            self.speed(0)

    class Empty(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("square")
            self.color("black")
            self.penup()
            self.speed(0)

    class User(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("square")
            self.color("red")
            self.penup()
            self.speed(0)

        def go_up(self):
            moveX = self.xcor()
            moveY = self.ycor()+24
            if (moveX, moveY) in mazeBound:
                self.goto(moveX, moveY)

        def go_down(self):
            moveX = self.xcor()
            moveY = self.ycor()-24
            if (moveX, moveY) in mazeBound:
                self.goto(moveX, moveY)

        def go_left(self):
            moveX = self.xcor()-24
            moveY = self.ycor()
            if (moveX, moveY) in mazeBound:
                self.goto(moveX, moveY)

        def go_right(self):
            moveX = self.xcor()+24
            moveY = self.ycor()
            if (moveX, moveY) in mazeBound:
                self.goto(moveX, moveY)

        def c_player(self):
            x_end=end.xcor()
            y_end=end.ycor()
            x=self.xcor()
            y=self.ycor()
            if x_end!=x or y_end!=y:
                x_play = player.xcor()
                y_play = player.ycor()
                try:
                    cordValue[(x_play,y_play)].pop()
                except:
                    cordValue[(x_play,y_play)].append("X")
                cordValue[(x,y)].append("P")
                player.goto(x,y)
                player.showturtle()

        def c_end(self):
            x_play=player.xcor()
            y_play=player.ycor()
            x=self.xcor()
            y=self.ycor()
            if x_play!=x or y_play!=y:
                x_end=end.xcor()
                y_end=end.ycor()
                try:
                    cordValue[(x_end,y_end)].pop()
                except:
                    cordValue[(x_end,y_end)].append("X")
                cordValue[(x,y)].append("E")
                end.goto(x,y)
                end.showturtle()

        def c_wall(self):
            x=self.xcor()
            y=self.ycor()
            x_play=player.xcor()
            y_play=player.ycor()
            x_end=end.xcor()
            y_end=end.ycor()
            if x!=x_play or y!=y_play:
                if x!=x_end or y!=y_end:
                    cordValue[(x,y)].append("X")
                    writer.goto(x,y)
                    writer.hideturtle()
                    writer.stamp()

        def c_nwall(self):
            x=self.xcor()
            y=self.ycor()
            x_play=player.xcor()
            y_play=player.ycor()
            x_end=end.xcor()
            y_end=end.ycor()
            if x!=x_play or y!=y_play:
                if x!=x_end or y!=y_end:
                    cordValue[(x,y)].append(" ")
                    empty.goto(x,y)
                    empty.stamp()

            
    def create_maze():
        for y in range(25):
            for x in range(25):
                screen_x = -288+(x*24)
                screen_y = 288-(y*24)
                mazeBound.append((screen_x, screen_y))
                cordValue[(screen_x, screen_y)]= ["X"]
                writer.goto(screen_x,screen_y)
                writer.stamp()
                if screen_x==-288 and screen_y==288:
                    user.goto(screen_x,screen_y)
                if screen_x==288 and screen_y==-288:
                    empty.goto(screen_x,screen_y)
                    empty.hideturtle()
                    end.goto(screen_x,screen_y)
                    end.hideturtle()
                    cordValue[(screen_x, screen_y)]= ["X"]
                    player.goto(screen_x,screen_y)
                    player.hideturtle()
                    cordValue[(screen_x, screen_y)]= ["X"]



    mazeBound=[] #stores maze area
    cordValue={} #stores stack for each coordinate to retrieve top object

    empty=Empty()
    player=Player()
    end=End()
    writer=Writer()
    user=User()
    
    create_maze()
    loadScreen.quit()
    loadScreen.destroy()
    creative.cv._rootwindow.deiconify()


    turtle.listen()
    turtle.onkey(user.go_up, "Up")
    turtle.onkey(user.go_down, "Down")
    turtle.onkey(user.go_left, "Left")
    turtle.onkey(user.go_right, "Right")
    turtle.onkey(user.c_player,"p")
    turtle.onkey(user.c_end, "e")
    turtle.onkey(user.c_wall, "w")
    turtle.onkey(user.c_nwall, "space")

    creative.tracer(0)
    global running
    running= True
    while running:
        creative.update()
        def on_closingC():
            #Handle creative Window close event
            ans=tk.messagebox.askquestion("Confirm","Visualize your Maze?",icon='warning')
            if ans=="yes":
                creative.cv._rootwindow.withdraw()
                global Maze
                global begin
                global finish
                Maze=[]
                begin=""
                finish=""
                for y in range(25):
                    temp=[]
                    for x in range(25):
                        screen_x = -288+(x*24)
                        screen_y = 288-(y*24)
                        try:
                            #Top of stack to create maze
                            if cordValue[(screen_x,screen_y)][-1] == "X":
                                temp.append(1)
                            elif cordValue[(screen_x,screen_y)][-1] == " ":
                                temp.append(0)
                            elif cordValue[(screen_x,screen_y)][-1] == "P":
                                temp.append(0)
                                begin= (y,x)
                            elif cordValue[(screen_x,screen_y)][-1] == "E":
                                temp.append(0)
                                finish=(y,x)
                        except:
                            temp.append(1)
                    Maze.append(temp)
            elif ans=="no":
                creative.cv._rootwindow.withdraw()
            global running
            running=False
        creative.cv._rootwindow.protocol("WM_DELETE_WINDOW",on_closingC)
    try:
        #Retrieve length of shortest path
        shortestPath=getShortestPath(Maze,begin,finish)
    except:
        shortestPath="*"
    if shortestPath!=0 and shortestPath!="*":
        #Show Animation
        creative.bye()
        skip=tk.Tk()
        skip.title("Animation")
        skip.iconbitmap(filePath+"/Gameico.ico")
        txtlabel=Label(skip,text="CLOSE THIS WINDOW TO CONTINUE")
        txtlabel.pack(side = "top")
        gifI=tk.PhotoImage(file="maze.gif")
        skip.resizable(False,False)
        skip.lift()
        global gif_index
        gif_index=0
        def next_frame():
            global gif_index
            try:
                gifI.configure(format="gif -index {}".format(gif_index))
                gif_index=gif_index+1
            except tk.TclError:
                gif_index=0
                return next_frame()
            else:
                skip.after(100,next_frame)
        gif_label=tk.Label(skip,image=gifI)
        gif_label.pack()
        skip.after_idle(next_frame)
        skip.mainloop()
        os.startfile("makecode.py") #return to main window after game has been played
    else:
        #Handle created maze with no defined path
        if shortestPath==0:
            getShortestPath([[0,0]],(0,0),(0,1))
            Qans=tk.messagebox.showinfo("Error","Looks like your maze did not have a path. \nReturning to start screen. 'ok' to continue.")
            if Qans == "ok":
                os.startfile("makecode.py")
        else:
            ans=tk.messagebox.showinfo("Quit", "Returning to start screen. \n'ok' to continue.")
            if ans == "ok":
                creative.bye()
                os.startfile("makecode.py") #return to main window after game has been played

#Link buttons to subsequent game methods
gameMode = Button(root, text="Game Mode", command=lambda: gameModeLevels())
gameMode.place(x=280, y=725)
creativeMode = Button(root, text="Creative", command=lambda: creation())
creativeMode.place(x=450, y=725)

#code to handle form close event.
def mainDelete():
    root.quit()
    root.destroy()
root.protocol("WM_DELETE_WINDOW",mainDelete)
root.mainloop()

