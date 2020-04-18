import pygame
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps
from PIL import ImageEnhance


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)

# 5px squares
width = 5
height = 5

#1px margin
margin = 1

#90x90 square matrix
rows = 100

#button height
btn_height = 50

screen_width = rows * (width + margin) + 2 * margin 
screen_height = screen_width + btn_height

btn_width = screen_width // 3

start_build = False

class button:
    def __init__(self, x, y, width, height, title):
        self.height = height
        self.width = width
        self.title = title
        self.x = x
        self.y = y


    def isOver(self, pos):
        if ((pos[0] > self.x and pos[0] < self.x + self.width) and (pos[1] > self.y and pos[1] < self.y + self.height)):
            return True
        else:
            return False

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        if self.title != '':
            font = pygame.font.SysFont('arial', 20)
            title = font.render(self.title, 1, (0,0,0))
            screen.blit(title, (self.x + int(self.width/2 - title.get_width()/2), self.y + int(self.height/2 - title.get_height()/2)))


        

def create_grid(size):
    grid = []
    for i in range(size):
        grid.append([])
        for j in range(size):
            grid[i].append(0)  
    return grid



main_grid = create_grid(rows)    # our main grid


def generate(grid):     # generation of next iteration grid
    row = len(grid)


    aux = create_grid(row)     # create a separate grid

    
    # do not update the current main grid until all the cells are updated

    for i in range(row):    # include boundaries, we use modulus arithmetic
        for j in range(row):
            alive_neighbours = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if not (x == 0 and y == 0): #exclude same cell.
                        r = (i + x + row) % row
                        c = (j + y + row) % row
                        if (grid[r][c] == 1): #only include alive neighbours
                            alive_neighbours += 1

            #count neighbours
            if (grid[i][j] == 1):

                #first case: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                if (alive_neighbours < 2):
                    aux[i][j] = 0
                
                #second case: Any live cell with two or three live neighbours lives on to the next generation.
                elif (alive_neighbours <= 3):
                    aux[i][j] = 1
                
                #third case: Any live cell with more than three live neighbours dies, as if by overpopulation.
                elif (alive_neighbours > 3):
                    aux[i][j] = 0
            
            #fourth case: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            elif (grid[i][j] == 0 and alive_neighbours == 3):
                aux[i][j] = 1

    return aux

 

start_button = button(0, screen_width, btn_width, btn_height, "start")
clear_button = button(btn_width + margin, screen_width, btn_width, btn_height, "clear")
upload_button = button((btn_width + margin) * 2, screen_width, btn_width, btn_height, "upload")


def update_grid(grid, start_build):

    if start_build  == True:
        grid = generate(grid)
    # Draw the grid
    for row in range(rows):
            for column in range(rows):
                color = WHITE
                if (grid[row][column] == 1):
                    color = BLACK
                pygame.draw.rect(
                    screen,
                    color,
                    [
                    (margin + width) * column + margin,
                    (margin + height) * row + margin,
                    width,
                    height
                    ]
                    )

    start_button.draw(screen, WHITE)
    clear_button.draw(screen, WHITE)
    upload_button.draw(screen, WHITE)
    return grid


# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
screen = pygame.display.set_mode((screen_width, screen_height))
 
# Set title of screen
pygame.display.set_caption("Conway")
 
# Loop until the user clicks the close button.
done = False


# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:

    for event in pygame.event.get():  # User did something

        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            if (pos[1] <= screen_width-1):
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (width + margin)
                row = pos[1] // (height + margin)
                # Set that location to one
           
                main_grid[row][column] = 1 if main_grid[row][column] == 0 else 0

                print("Click ", pos, "Grid coordinates: ", row, column)

            elif (start_button.isOver(pos)):   
                start_build = not start_build
                start_button.title = "stop" if start_button.title == "start" else "start" 

            elif (clear_button.isOver(pos)):
                main_grid = create_grid(rows)

                start_build = False
                start_button.title = "start"
                
            elif (upload_button.isOver(pos)):
                # this part is gonna be a pain in the ass

                root = tk.Tk()
                root.withdraw()
                root.attributes("-topmost", True)
                file_path = filedialog.askopenfilename(parent = root)
                if file_path:

                    img = Image.open(file_path)
                    
                    ######################################################################################################
                    # Kudos to this guy for the simple tutorial on converting images to pixel grid                       #
                    #                                                                                                    #                         
                    # https://linux.ime.usp.br/~robotenique//computer%20science/python/2017/09/17/image-grid-python.html #
                    ######################################################################################################
                    
                    size = (rows, rows)

                    img = ImageOps.fit(img, size, Image.ANTIALIAS)
                    img = ImageEnhance.Contrast(img).enhance(2.0).convert('1')
                    pixel_arr = np.asarray(img)
                    
                    print(pixel_arr.shape)
                    for i in range(rows):
                        for j in range(rows):
                            main_grid[i][j] = not pixel_arr[i][j]
                else:
                    pass
    # Set the screen background
    screen.fill(BLACK)


    main_grid = update_grid(main_grid, start_build)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.update()
    clock.tick()

    # Limit to 60 frames per second

 
    
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()