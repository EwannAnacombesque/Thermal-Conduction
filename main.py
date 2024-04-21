import pygame
import colorsys
from unidecode import unidecode
import math
from PIL import Image
import argparse 

def parse_arguments():
    parser = argparse.ArgumentParser(description='Program with -type -file -color -dt')
    
    parser.add_argument('-t', '--type', type=str, help='Type of canva',choices=["blank","image","text"],nargs='?',const="blank",default="blank")
    parser.add_argument('-f', '--file', type=str, help='In case type is either image or text, specify the file path',nargs="?",const="",default="")
    parser.add_argument('-c', '--color', type=int, help='Color accuracy of the canva',nargs="?",const=256,default=256)
    parser.add_argument('-dt', '--dt', type=float, help='Time modifier',nargs="?",const=0.1,default=0.1)
    args = parser.parse_args()
    return [args.type,args.file,args.color,args.dt]

def load_text(file_name):
    text =""

    with open(file_name,"rt",encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        text += line 

    text = unidecode(text.lower()).replace("\n"," ")
    
    # Transform the char, into its ASCII code, and back in binary, to finally be cast in string
    global transcripted_text
    transcripted_text = "".join([str(bin(ord(char)))[2:] for char in text])

    # Determine the grid_size so it is  big enough to contain the whole text
    global grid_size
    grid_size = math.floor(math.sqrt(len(transcripted_text))+1)

def load_image(file_name):
    global image
    image = Image.open(file_name)

    # Convert image in right mode
    if image.mode != "RGB":
        image = image.convert("RGB")

    global grid_size 
    grid_size = image.size[0]

def create_context(loading_type_var,file_name_var,color_accuracy_var,initial_dt_var):
    global screen, clock, dt, initial_dt, running
    global cell_length, loading_type, grid_size, text_length, color_accuracy, heat_radius
    

    # Manage each type of user input #
    loading_type = loading_type_var
    assert loading_type in ["blank","image","text"], "type should be either blank, image or text"    
    file_name = file_name_var if file_name_var else "cahun.png" if loading_type=="image" else "cocteau.txt"

    if loading_type == "text": load_text(file_name); text_length=len(transcripted_text)
    if loading_type == "image": load_image(file_name)
    if loading_type == "blank": grid_size = 50

    # Lattice context
    ideal_screen_size = 500
    cell_length = int(ideal_screen_size/grid_size)
    color_accuracy = int(color_accuracy_var)
    heat_radius = 1    

    # Pygame context #
    screen = pygame.display.set_mode((cell_length*grid_size,cell_length*grid_size))
    clock = pygame.time.Clock()
    running = True 
    dt = 0
    initial_dt = float(initial_dt_var)

def create_grid():
    global grid
    global temp_grid 
    temp_grid = [ [0]*grid_size for i in range(grid_size) ]

    # Case one : fill the grid with 0s
    if loading_type == "blank":
        grid = [[0]*grid_size for i in range(grid_size)]
        return

    # Case two : fill the grid with the bits of the transcripted text, loop over it
    if loading_type == "text":
        grid = [[200*int(transcripted_text[(i+grid_size*j) % text_length]) for j in range(grid_size)] for i in range(grid_size)]
        return 
    
    # Case three : fill the grid with the red component of the image
    if loading_type == "image":
        grid = [[image.getpixel((i,j))[0] for j in range(grid_size)] for i in range(grid_size)]

def create_colors():
    global colors
    colors = []
    
    hue_base = 0 
    hue_gap = (360-hue_base )/color_accuracy  
    
    for i in range(color_accuracy):
        # Make a rainbow, from hue_base to 360°, add i*hue_gap
        colors.append(list(colorsys.hsv_to_rgb((hue_base+i*hue_gap)/360,
                                               0.7,
                                               0.6+0.4*i/color_accuracy)))
        # Save RGB components of the color, translate it from 0-1 to 0-255
        for component in range(3):
            colors[i][component] = int(colors[i][component]*255)

def get_event():
    global running
    global dt 
    
    # Keyboard and quit handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE:
                dt = not dt if dt else initial_dt
    
    # Make sure to not heat or cool the lattice if no mouse button is pressed
    if pygame.mouse.get_pressed() == (False,False,False):
        return 

    # Get the nature of the heating (positive = heat, negative = cool)
    is_heated = pygame.mouse.get_pressed()[0]
    
    cell_x = pygame.mouse.get_pos()[0]//cell_length
    cell_y = pygame.mouse.get_pos()[1]//cell_length
    
    # Heat / Cool the cells around the mouse, in a radius (default 1)
    for i in range(cell_x-heat_radius,cell_x+heat_radius+1):
        for j in range(cell_y-heat_radius,cell_y+heat_radius+1):
            grid[i%grid_size][j%grid_size] = 256 if is_heated else 3
    
def update():
    global grid 
    
    # Apply a discrete second derivate all over the lattice
    # Heat diffusion is ruled by the law : k*∇^2T = dT/dt, aggregating all the factors 
    # Which could be translated by k * ∇^2T = dT/dt and T = T + dT = T + dt*dT/dt
    #                           so  T = T + dt * k * ∇^2T
    # k can be unheeded, indeed, k only impacts on speed of the conduction, which dt already determine
    # So T only depends on T and its second derivatives, which can be discretized
    # I use a linear approximation of the second derivative (first-order Taylor-polynomial)
    # Could be done with a convolution all over the canva
    # In fact, thermal conduction is the same as gaussian blurring, 
    # Not sure but maybe the gaussian blur kernel is bound to heat kernel
    
    # ----
    # Thermal conduction, convolution, gaussians, periodicity, blurring, is all connected to Fourier Transformations
    # ----    

    for x in range(grid_size):
        for y in range(grid_size):
            temp_grid[x][y] = grid[x][y] + dt*(grid[x][(y+1)%grid_size]+grid[x][(y-1)%grid_size]+grid[(x+1)%grid_size][y]+grid[(x-1)%grid_size][y]-4*grid[x][y])

    grid = temp_grid

def draw():
    screen.fill((0,0,0))
    
    # Draw each cell, as a square
    for x in range(grid_size):
        for y in range(grid_size):
            screen.fill(colors[int(grid[x][y]%color_accuracy)],
                        (x*cell_length,y*cell_length,cell_length,cell_length))
    

    pygame.display.flip()

create_context(*parse_arguments())
create_colors()
create_grid()

while running:
    get_event()
    update()
    draw()
