import tkinter as tk
import random
import os.path
from PIL import Image, ImageTk

# Variables
CASE = 80
WIDTH = CASE * 10
HEIGHT = CASE * 10
GAME_OVER = False
BORDER = False
BACK = False
SNAKE = [(1, 3), (1, 2), (1, 1)]
BALL = [random.randint(2, 9), random.randint(2, 9)]


# Fonctions
def draw_lines():
    for i in range(10):
        canvas.create_line(CASE * i, 0, CASE * i, 800, width=1, fill='grey94')
        canvas.create_line(0, CASE * i, 800, CASE * i, width=1, fill='grey94')


def draw_snake(snake):
    for i in snake:
        canvas.create_rectangle(i[0] * CASE + 3, i[1] * CASE + 3, i[0] * CASE + CASE - 3, i[1] * CASE + CASE - 3,
                                fill='lightgreen', outline='lightgreen')


def update_snake(TAIL):
    i = SNAKE[0]
    j = TAIL
    k = SNAKE[1]
    canvas.create_rectangle(i[0] * CASE + 3, i[1] * CASE + 3, i[0] * CASE + CASE - 3, i[1] * CASE + CASE - 3, fill='lightgreen', outline='lightgreen')
    canvas.create_rectangle(j[0] * CASE + 3, j[1] * CASE + 3, j[0] * CASE + CASE - 3, j[1] * CASE + CASE - 3, fill='white', outline='white')
    canvas.create_rectangle(k[0] * CASE + 3, k[1] * CASE + 3, k[0] * CASE + CASE - 3, k[1] * CASE + CASE - 3, fill='lightgreen', outline='lightgreen')


def draw_ball():
    rand = []

    for i in range(0, 9):
        for j in range(0, 9):
            rand.append((i, j))

    for i in SNAKE:
        if i in rand:
            rand.remove(i)

    choice = random.choice(rand)
    BALL[0] = choice[0]
    BALL[1] = choice[1]

    canvas.create_image(0, 0, image=tk.PhotoImage(file='apple.png'))
    canvas.create_oval(BALL[0] * CASE + 15, BALL[1] * CASE + 15, BALL[0] * CASE + CASE - 15, BALL[1] * CASE + CASE - 15,
                       fill='firebrick1', outline='firebrick1')


def draw_eyes(color):

    canvas.create_oval(SNAKE[0][0] * CASE + 10, SNAKE[0][1] * CASE + 15, SNAKE[0][0] * CASE + CASE - 50,
                       SNAKE[0][1] * CASE + CASE - 50, fill=color, outline=color)
    canvas.create_oval(SNAKE[0][0] * CASE + 50, SNAKE[0][1] * CASE + 15, SNAKE[0][0] * CASE + CASE - 10,
                       SNAKE[0][1] * CASE + CASE - 50, fill=color, outline=color)


def draw_numbers():
    for i in range(1, len(SNAKE)):
        canvas.create_text(SNAKE[i][0] * CASE + 40, SNAKE[i][1] * CASE + 40, text=i, fill='white', font=('Arial', 15))


def game_over():
    score = len(SNAKE)
    scoreboard = open('scoreboard.txt', 'r').readlines()
    cpt = 0
    with open('scoreboard.txt', 'w') as file:
        for index, line in enumerate(scoreboard):
            if score > int(line):
                file.write(str(score) + '\n')
                print(index)


    canvas.create_rectangle(0, 0, 800, 800, fill='firebrick1')
    canvas.create_text(5 * CASE, 4.9 * CASE, text='GAME OVER', fill='white', font=('Great Vibes bold', 30))
    canvas.create_text(5 * CASE, 5.55 * CASE, text='Press Enter to restart', fill='white', font=('Great Vibes bold', 15))
    canvas.create_text(5 * CASE, 6.2 * CASE, text='SCOREBOARD', fill='white', font=('Great Vibes bold', 16))

    #try:
    #    canvas.create_text(5 * CASE, 6.3 * CASE + 30, text="{} pts".format(scoreboard[0].strip()), fill='white',font=('Great Vibes bold', 15))
    #    canvas.create_text(5 * CASE, 6.3 * CASE + 60, text="{} pts".format(scoreboard[1].strip()), fill='white',font=('Great Vibes bold', 15))
    #    canvas.create_text(5 * CASE, 6.3 * CASE + 90, text="{} pts".format(scoreboard[2].strip()), fill='white',font=('Great Vibes bold', 15))
    #except:
    #    print('Index out of range')


def init():
    canvas.pack()
    draw_lines()
    draw_snake(SNAKE)
    draw_ball()
    draw_eyes('white')

    canvas.bind_all('<Up>', move)
    canvas.bind_all('<Down>', move)
    canvas.bind_all('<Left>', move)
    canvas.bind_all('<Right>', move)
    canvas.bind_all('<Return>', restart)

    if not os.path.exists('./scoreboard.txt'):
        open("scoreboard.txt", "x")


def restart(event):
    global GAME_OVER
    global SNAKE
    global BALL

    if GAME_OVER:
        GAME_OVER = False
        SNAKE = [(1, 3), (1, 2), (1, 1)]
        BALL = [random.randint(3, 8), random.randint(3, 8)]
        canvas.create_rectangle(0, 0, 800, 800, fill='white')
        init()


def move(event):
    global GAME_OVER
    global BORDER
    global BACK

    HEAD = SNAKE[0]
    TAIL = SNAKE[-1]
    OLD_SNAKE_TAIL = SNAKE.copy()[-1]
    LAST_CELL = ()

    for i in range(len(SNAKE)):
        LAST = SNAKE[i]

        match = {'Down': (SNAKE[i][0], SNAKE[i][1] + 1), 'Up': (SNAKE[i][0], SNAKE[i][1] - 1), 'Left': (SNAKE[i][0] - 1, SNAKE[i][1]), 'Right': (SNAKE[i][0] + 1, SNAKE[i][1])}

        if match[event.keysym][0] == -1 or match[event.keysym][0] == 10 or match[event.keysym][1] == -1 or match[event.keysym][1] == 10:
            BORDER = True

        if match[event.keysym] == SNAKE[1]:
            BACK = True

        # if not BORDER:
        # if not BACK:

        if SNAKE[i] == HEAD:
            SNAKE[i] = match[event.keysym]
            if SNAKE[i] in SNAKE[1:]:
                GAME_OVER = True
                game_over()
        else:
            SNAKE[i] = LAST_CELL

        LAST_CELL = LAST

    # if not BORDER:
    # if not BACK:
    if SNAKE[0] == tuple(BALL):
        SNAKE.append(TAIL)
        draw_ball()

    if not GAME_OVER:
        update_snake(OLD_SNAKE_TAIL)
        draw_eyes('white')

    BORDER = False
    BACK = False


# Initialisation du jeu
window = tk.Tk()
window.title('Snake')
window.iconphoto(False, tk.PhotoImage(file='./snake.png'))
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, background='white')
init()

window.mainloop()
