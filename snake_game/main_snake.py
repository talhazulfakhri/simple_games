from logging import raiseExceptions
import numpy as np
import cv2

class Playground:
  """Create area to play the game"""
  def __init__(self, width, height, style):
    """Set width, height, and style"""
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
    background = np.array(background)

class Snake(Playground):
  """Create snake and snake's movement"""
  pass

class Food(Playground):
  """Create food for snake to grow""" 
  pass

     
def main():
  pass

main()