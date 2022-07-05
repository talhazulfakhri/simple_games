from turtle import position
import numpy as np
import cv2
import sys
import os

UP = np.array([0, -1])
DOWN = np.array([0, 1])
LEFT = np.array([-1, 0])
RIGHT = np.array([1, 0])

class Background:
    """Create area to play the game"""
    def __init__(self, width = 5, height = 5, style = 'grass'):
        """Set width, height, and style"""
        if width <= 3 or height <= 3:
            raise AssertionError("The board is too small") # Cant play with small board
        self.width = width
        self.height = height
        self.style = style
    
    def create_background(self):
        """Set backround style"""
        self.pixel = cv2.imread(os.path.join(".", "texture", self.style + ".png")) # importing 16 by 16 square image
        if self.pixel is None:
            raise AssertionError("Invalid style option") # if the style isn't available

        """Create background from 16 by 16 image"""
        self.background = np.vstack([np.hstack([self.pixel for i in range(self.width)]) for j in range(self.height)])
        
        """Create coordinates"""
        self.coordinate = {}
        x_coords = np.arange(7, 16 * self.width, 16)
        y_coords = np.arange(7, 16 * self.height, 16)
        for j,y in enumerate(y_coords):
            for i,x in enumerate(x_coords):
                self.coordinate[(i,j)] = (x,y)

class Snake:
    """Create Snake Object"""
    def __init__(self, width = 5, height = 5, style = 'grass'):
        """Initial position and direction"""
        self.width = width
        self.height = height
        
        self.initial_direction = RIGHT
        self.initial_position = np.array([np.array([self.width//2 - 2, self.height//2 - 2]),
                                          np.array([self.width//2 - 2, self.height//2 - 1]),
                                          np.array([self.width//2 - 1, self.height//2 - 1])])
        
        self.position = self.initial_position
        self.direction = self.initial_direction  
        self.style = style
        
    def create_snake_texture(self):
        self.texture = {}
        self.texture["body_1"] = cv2.imread(os.path.join(".", "snake_texture", self.style,  "body_1.png"))
        self.texture["body_2"] = cv2.imread(os.path.join(".", "snake_texture", self.style,  "body_2.png"))
        self.texture["head"] = cv2.imread(os.path.join(".", "snake_texture", self.style,  "head.png"))
    
    def move(self, direction):
        """Update the position of the snake"""
        self.direction = direction
        self.position = np.concatenate((self.position[1:], [self.position[-1] + self.direction]))
        
    def grow(self, direction):
        """grow the snake adapting the snake direction"""
        self.direction = direction
        self.position = np.concatenate((self.position, [self.position[-1] + self.direction]))

class Food:
    """Create Food Object"""
    def __init__(self, width = 5, height = 5, style = 'grass'):
        """Initial food condition"""
        self.width = width
        self.height = height
        self.style = style
        self.food_coords = np.array([(np.random.randint(0, self.width),
                                      np.random.randint(0, self.height))])
        
    def create_food_texture(self):
        self.texture = cv2.imread(os.path.join(".", "food_texture", self.style + ".png"))
        
    def spawn_food(self):
        x = np.random.randint(0,self.width)
        y = np.random.randint(0,self.height)
        self.food_coords = np.concatenate((self.food_coords, np.array([(x,y),])))
        
    def remove_food(self):
        if len(self.food_coords) > 5:
            self.food_coords = np.delete(self.food_coords, np.random.randint(0,2), axis=0)
            
    def remove_food_from_coords(self, coord):
        i = np.where((self.food_coords == coord).all(axis=1))
        self.food_coords = np.delete(self.food_coords, i, axis=0)

def get_direction(current_direction):
    """
    Update direction from user input
    w => UP
    a => DOWN
    d => RIGHT
    a => LEFT
    """
    press = cv2.waitKey(500) & 0xff
    direction = current_direction
    """
    Note : Snake can't go backward
    ex : if the current snake direction is UP, player can't input DOWN ("s")
    """
    if current_direction[0] == 1 and current_direction[1] == 0:
        if press == ord("w"):
            direction = UP
        elif press == ord("s"):
            direction = DOWN
    elif current_direction[0] == -1 and current_direction[1] == 0:
        if press == ord("w"):
            direction = UP
        elif press == ord("s"):
            direction = DOWN
    elif current_direction[0] == 0 and current_direction[1] == 1:
        if press == ord("a"):
            direction = LEFT
        elif press == ord("d"):
            direction = RIGHT
    elif current_direction[0] == 0 and current_direction[1] == -1:
        if press == ord("a"):
            direction = LEFT
        elif press == ord("d"):
            direction = RIGHT
        
    if press == 27:
        exit = True
    else:
        exit = False
        
    return direction, exit 

def get_frame(background, snake, food):
    """
    Create frame from current condition of snake

    Args:
        background (Background): Background class
        snake (Snake): Snake class
        food (Food): Food class

    Returns:
        ndarray: frame of condition
    """
    frame = np.copy(background.background)
    coordinate = background.coordinate
    food_coords = food.food_coords
    for coord in food_coords:
        position = coordinate[tuple(coord)]
        for i, row in enumerate(food.texture):
            for j, x in enumerate(row):
                if x[0] == 255 and x[1] == 255 and x[2] == 255:
                    continue
                frame[position[1] - 7 + i][position[0] - 7 + j] = x
    
    head = snake.position[-1]
    body = snake.position[:-1]
    n = 1
    for N, coord in enumerate(body):
        position = coordinate[tuple(coord)]
        for sub in np.arange(0, 15, 2):
            sub_position = position + (snake.position[N+1] - coord) * sub
            for i, row in enumerate(snake.texture["body_" + str(n % 2 + 1)]):
                for j, x in enumerate(row):
                    if x[0] == 255 and x[1] == 255 and x[2] == 255:
                        continue
                    frame[sub_position[1] - 7 + i][sub_position[0] - 7 + j] = x
                    n += 1
                    
    position = coordinate[tuple(head)]
    for i, row in enumerate(snake.texture["head"]):
        for j, x in enumerate(row):
            if x[0] == 255 and x[1] == 255 and x[2] == 255:
                continue
            frame[position[1] - 7 + i][position[0] - 7 + j] = x 
        
    return frame

def check(array_list, tupl):
    """
    Checking if tuple (1 x 2) is in array_list (n x 2)

    Args:
        array_list (ndarray): list of array (n x 2)
        tupl (tuple): tuple for check if it was in array list (1 x 2)

    Returns:
        boolean : True or False
    """
    for i,j in array_list:
        if i == tupl[0] and j == tupl[1]:
            return True
        
    return False

def main():
    try:
        background = Background(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
        snake = Snake(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
        food = Food(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
    except IndexError:
        raise AssertionError("Need exactly 3 input (width, height, style)")
    
    background.create_background()
    snake.create_snake_texture()
    food.create_food_texture()
    
    i = 0
    exit = False
    
    while not exit:
        frame = get_frame(background, snake, food)
        cv2.imshow("Snake Game", frame)
        direction, exit = get_direction(snake.direction)
        snake.move(direction)
        
        i += 1
        if i % 10 == 9:
            food.spawn_food()
        elif i % 10 == 5:
            food.remove_food()
            
        head = snake.position[-1]
        if check(food.food_coords,head):
            snake.grow(direction)
            food.remove_food_from_coords(head)
        
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()