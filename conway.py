import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 5px squares
width = 10
height = 10

#1px margin
margin = 1

#50x50 square matrix
rows = 50
screen_width = rows * (width + margin) + 2 * margin
screen_height = screen_width


grid = []
for row in range(rows):
    grid.append([])
    for column in range(rows):
        grid[row].append(0)  

def generate(grid):
    row = len(grid)
    for i in range(1, row-1):
        for j in range(1, row-1):
            alive_neighbours = []
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if not (x == 0 and y == 0): #exclude same cell.
                        if (grid[i+x][j+y] == 1): #only include alive neighbours
                            alive_neighbours.append(grid[i+x][j+y])

            #count neighbours
            if (grid[i][j] == 1):

                #first case: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                if (len(alive_neighbours) < 2):
                    grid[i][j] = 0
                
                #second case: Any live cell with two or three live neighbours lives on to the next generation.
                elif (len(alive_neighbours) <= 3):
                    grid[i][j] = 1
                
                #third case: Any live cell with more than three live neighbours dies, as if by overpopulation.
                elif (len(alive_neighbours) > 3):
                    grid[i][j] = 0
            
            #fourth case: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            elif (grid[i][j] == 0 and len(alive_neighbours) == 3):
                grid[i][j] = 1

    return grid

 




mouse_drag = False
drag_start_point = False
drag_end_point = False
 
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
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)
            # Set that location to one
            grid[row][column] = 1
            print("Click ", pos, "Grid coordinates: ", row, column)

    
    # Set the screen background
    screen.fill(BLACK)

    def update_grid():
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
    
    update_grid()

    grid = generate(grid)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(10)
 
    
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()