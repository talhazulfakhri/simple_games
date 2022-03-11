from logging import raiseExceptions
import numpy as np
import cv2

UP = [-1, 0]
DOWN = [1, 0]
LEFT = [0, -1]
RIGHT = [0, 1]

class Playground:
  """Create area to play the game"""
  def __init__(self, width, height, style):
    """Set width, height, and style"""
    if width <= 3 or height <= 3:
      raise AssertionError("The board is too small") # Cant play with small board
    self.width = width
    self.height = height
    self.style = style
    
  def background_style(self):
    """Set backround style"""
    pixel_background = cv2.imread("texture/" + self.style + ".png") # importing 16 by 16 square image
    if pixel_background is None:
      raise AssertionError("Invalid style option") # if the style isn't available
    """"Create background from 16 by 16 image"""
    row_background = []
    for i in range(self.width):
      for col in pixel_background:
        row_background.append(col)
    row_background = cv2.transpose(np.array(row_background))
    background = []
    for i in range(self.height):
      for col in row_background:
        background.append(col)
    self.background = np.array(background)
  
  def coordinates(self):
    """Create coordinates to every square"""
    self.background_style()
    self.coords = {}
    self.inv_coords = {}
    x_coords = np.arange(7, 16 * self.width, 16)
    y_coords = np.arange(7, 16 * self.height, 16)
    for y, y_coord in enumerate(y_coords):
      for x, x_coord in enumerate(x_coords):
        self.coords[(x,y)] = (x_coord, y_coord)
        self.inv_coords[(x_coord,y_coord)] = (x, y)
  
class Snake(Playground):
  """Create snake and snake's movement"""
  def __init__(self):
    """Initialize snake position and direction of snake"""
    self.list_pos = [(self.width//2 - 1, self.height//2 - 1),(self.width//2 - 2, self.height//2 - 1)]
    self.coordinates()
    self.direction_vector = [0,1]
  
  def snake_texture(self):
    """Import snake texture from directory to dictionary"""
    self.snake = {}
    self.snake["body_1"] = cv2.imread("snake_texture/" + self.style + "/body_1.png")
    self.snake["body_2"] = cv2.imread("snake_texture/" + self.style + "/body_2.png")
    self.snake["head"] = cv2.imread("snake_texture/" + self.style + "/head.png")

  def update_direction(self):
    """
    Update direction of the snake with user input
    w => UP
    a => DOWN
    d => RIGHT
    a => LEFT
    """
    press = cv2.waitKey(10) & 0xff
    """
    Note : Snake can't go backward
    ex : if the current snake direction is UP, player can't input DOWN ("s")
    """
    if self.direction_vector[0] == 0 and self.direction_vector[1] == 1:
      if press == ord("w"):
        self.direction_vector = UP
      elif press == ord("s"):
        self.direction_vector = DOWN
    elif self.direction_vector[0] == 0 and self.direction_vector[1] == -1:
      if press == ord("w"):
        self.direction_vector = UP
      elif press == ord("s"):
        self.direction_vector = DOWN
    elif self.direction_vector[0] == 1 and self.direction_vector[1] == 0:
      if press == ord("a"):
        self.direction_vector = LEFT
      elif press == ord("d"):
        self.direction_vector = RIGHT
    elif self.direction_vector[0] == -1 and self.direction_vector[1] == 0:
      if press == ord("a"):
        self.direction_vector = LEFT
      elif press == ord("d"):
        self.direction_vector = RIGHT
    
class Food(Playground):
  """Create food for snake to grow""" 
  pass

     
def main():
  pass

main()