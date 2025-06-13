import pygame
import time
import random

# set up pygame window
WIDTH = 525
HEIGHT = 550
FPS = 30

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)

#maxX=int(input("Enter maze size"))
#maxY=maxX

maxX=maxY=20

# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Maze Generator and Solver")
clock = pygame.time.Clock()

# setup maze variables
x = 0                    # x axis
y = 0                    # y axis
w = 10                   # width of cell
grid = []
visited = []
stack = []
solution = {}

# build the grid
def build_grid(x, y, w):
    for i in range(1,21):
        x = w                                                            # set x coordinate to start position
        y = y + w                                                        # start a new row
        for j in range(1, 21):
            pygame.draw.line(screen, WHITE, [x, y], [x + w, y])           # top of cell
            pygame.draw.line(screen, WHITE, [x + w, y], [x + w, y + w])   # right of cell
            pygame.draw.line(screen, WHITE, [x + w, y + w], [x, y + w])   # bottom of cell
            pygame.draw.line(screen, WHITE, [x, y + w], [x, y])           # left of cell
            grid.append((x,y))                                            # add cell to grid list
            x = x + w                                                    # move cell to new position


def push_up(x, y):
    pygame.draw.rect(screen, BLUE, (x + 1, y - w + 1, w-1, 2*w-1), 0)         # draw a rectangle twice the width of the cell
    pygame.display.update()                                              # to animate the wall being removed


def push_down(x, y):
    pygame.draw.rect(screen, BLUE, (x +  1, y + 1, w-1, 2*w-1), 0)
    pygame.display.update()


def push_left(x, y):
    pygame.draw.rect(screen, BLUE, (x - w +1, y +1, 2*w-1, w-1), 0)
    pygame.display.update()


def push_right(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, 2*w-1, w-1), 0)
    pygame.display.update()


def single_cell( x, y):
    pygame.draw.rect(screen, GREEN, (x +1, y +1, w-2, w-2), 0)          # draw a single width cell
    pygame.display.update()


def backtracking_cell(x, y):
    pygame.draw.rect(screen, BLUE, (x +1, y +1, w-2, w-2), 0)        # used to re-colour the path after single_cell
    pygame.display.update()                                        # has visited cell


def solution_cell(x,y):
    pygame.draw.circle(screen, YELLOW, (x+(w/2), y+(w/2)), w/4, 0)             # used to show the solution
    pygame.display.update()                                                    # has visited cell


def carve_out_maze(x,y):
    single_cell(x, y)                                              # starting positing of maze
    stack.append((x,y))                                            # place starting cell into stack
    visited.append((x,y))                                          # add starting cell to visited list
    while len(stack) > 0:                                          # loop until stack is empty
        time.sleep(0.01)                                            # slow program now a bit
        cell = []                                                  # define cell list
        if (x + w, y) not in visited and (x + w, y) in grid:       # right cell available?
            cell.append("right")                                   # if yes add to cell list

        if (x - w, y) not in visited and (x - w, y) in grid:       # left cell available?
            cell.append("left")

        if (x , y + w) not in visited and (x , y + w) in grid:     # down cell available?
            cell.append("down")

        if (x, y - w) not in visited and (x , y - w) in grid:      # up cell available?
            cell.append("up")

        if len(cell) > 0:                                          # check to see if cell list is empty
            cell_chosen = (random.choice(cell))                    # select one of the cell randomly

            if cell_chosen == "right":                             # if this cell has been chosen
                push_right(x, y)                                   # call push_right function
                solution[(x + w, y)] = x, y                        # solution = dictionary key = new cell, other = current cell
                x = x + w                                          # make this cell the current cell
                visited.append((x, y))                              # add to visited list
                stack.append((x, y))                                # place current cell on to stack

            elif cell_chosen == "left":
                push_left(x, y)
                solution[(x - w, y)] = x, y
                x = x - w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "down":
                push_down(x, y)
                solution[(x , y + w)] = x, y
                y = y + w
                visited.append((x, y))
                stack.append((x, y))

            elif cell_chosen == "up":
                push_up(x, y)
                solution[(x , y - w)] = x, y
                y = y - w
                visited.append((x, y))
                stack.append((x, y))
        else:
            x, y = stack.pop()                                    # if no cells are available pop one from the stack
            single_cell(x, y)                                     # use single_cell function to show backtracking image
            time.sleep(0.01)                                       # slow program down a bit
            backtracking_cell(x, y)                               # change colour to green to identify backtracking path


def plot_route_back(x,y):
    solution_cell(x, y)                                          # solution list contains all the coordinates to route back to start
    while (x, y) != (w,w):                                     # loop until cell position == start position
        x, y = solution[x, y]                                    # "key value" now becomes the new key
        solution_cell(x, y)                                      # animate route back
        time.sleep(0.01)


x, y = 20, 20                     # starting position of grid
build_grid(40, 0, 20)             # 1st argument = x value, 2nd argument = y value, 3rd argument = width of cell
carve_out_maze(x,y)               # call build the maze  function
plot_route_back(400, 400)         # call the plot solution function


# ##### pygame loop #######
running = True
while running:
    # keep running at the at the right speed
    clock.tick(FPS)
    # process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False