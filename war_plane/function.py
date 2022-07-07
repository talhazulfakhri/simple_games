from telnetlib import KERMIT
from matplotlib import is_interactive
import numpy as np
import cv2
import os, sys

from object import *
from pynput import keyboard

def check_intersection(array1, array2):
    """
    Check if 2 arrays have common elements

    Args:
        array1 (ndarray): numpy array with tuples as elements 
        array2 (ndarray): numpy array with tuples as elements 

    Returns:
        bool: boolean
    """
    check = np.in1d(array1, array2)
    is_intersect = check.any()
    
    return is_intersect

def create_frame(background, ship, enemy):
    """
    Create one frame from the condition

    Args:
        background (class Background): background of the game
        ship (class Ship): ship that player control
        enemy (class Enemy): enemy that attack player

    Returns:
        ndarray: image of the current condition
    """
    
    hit = False
    
    frame = np.copy(background.background)
    
    # Get the coordinates of every object
    ship_position = np.copy(ship.position)
    copy_of_main_bullets_pos = np.copy(ship.main_bullet)
    copy_of_secondary_bullets_pos = np.copy(ship.secondary_bullet)
    enemies_position = np.copy(enemy.enemies_position_in_t)
    
    # Get enemy texture
    enemy_texture = np.copy(enemy.current_enemy_texture)
    
    # Show bullet
    deleted_bullet = []
    texture = np.copy(ship.bullet_texture["main"])
    for i, position in enumerate(copy_of_main_bullets_pos):
        hit = False    
        try:
            # Checking if main bullet hits the enemy
            try:
                bullet_coords = np.copy(background.coordinate[position[0] : position[0] + texture.shape[0], position[1] : position[1] + texture.shape[1]])
                flatten_bullet_coords = np.concatenate(bullet_coords)
            except:
                pass
            for number, enemies_path in enumerate(enemies_position):
                for j, t_value in enumerate(enemies_path):
                    pos = np.int32(enemy.path[str(enemy.number_path[number])](t_value))
                    
                    if pos[0] < 0 or pos[0] >= 720:
                        continue
                    
                    try:
                        enemy_coords = np.copy(background.coordinate[pos[0] : pos[0] + enemy_texture.shape[0], pos[1] : pos[1] + enemy_texture.shape[1]])
                        flatten_enemy_coords = np.concatenate(enemy_coords)
                        if check_intersection(flatten_bullet_coords, flatten_enemy_coords):
                            deleted_bullet.append(i)
                            print("HIT")
                            hit = True
                            break
                    except:
                        continue
                    
                if hit:
                    break
                
            if hit:
                continue
            
            part_minus_bullet = np.copy(frame[position[0] : position[0] + texture.shape[0], position[1] : position[1] + texture.shape[1]])
            part_minus_bullet[np.where((texture != [0, 0, 0]).all(axis=2))] = [0, 0, 0]
            frame[position[0] : position[0] + texture.shape[0], position[1] : position[1] + texture.shape[1]] = part_minus_bullet + texture
            ship.main_bullet[i] += UP * 6
        except Exception as e:
            print(e)
            deleted_bullet.append(i)
    
    for i in sorted(deleted_bullet, reverse=True):
        ship.main_bullet.pop(i)
    
    deleted_bullet = []
    texture = np.copy(ship.bullet_texture["secondary"])
    for i, position in enumerate(copy_of_secondary_bullets_pos):
        hit = False    
        try:
            # Checking if secondary bullet hits the enemy
            try:
                bullet_coords = np.copy(background.coordinate[position[0] : position[0] + texture.shape[0], position[1] : position[1] + texture.shape[1]])
                flatten_bullet_coords = np.concatenate(bullet_coords)
            except:
                pass
            for number, enemies_path in enumerate(enemies_position):
                for j, t_value in enumerate(enemies_path):
                    pos = np.int32(enemy.path[str(enemy.number_path[number])](t_value))
                    
                    if pos[0] < 0 or pos[0] >= 720:
                        continue
                    
                    try:
                        enemy_coords = np.copy(background.coordinate[pos[0] : pos[0] + enemy_texture.shape[0], pos[1] : pos[1] + enemy_texture.shape[1]])
                        flatten_enemy_coords = np.concatenate(enemy_coords)
                        if check_intersection(flatten_bullet_coords, flatten_enemy_coords):
                            deleted_bullet.append(i)
                            print("HIT")
                            hit = True
                            break
                    except:
                        continue
                    
                if hit:
                    break
                
            if hit:
                continue    
            
            part_minus_bullet = np.copy(frame[position[0] : position[0] + texture.shape[0], position[1] : position[1] + texture.shape[1]])
            part_minus_bullet[np.where((texture != [0, 0, 0]).all(axis=2))] = [0, 0, 0]
            frame[position[0] : position[0] + texture.shape[0], position[1] : position[1] + texture.shape[1]] = part_minus_bullet + texture
            ship.secondary_bullet[i] += UP * 6
        except Exception as e:
            print(e)
            deleted_bullet.append(i)
    
    for i in sorted(deleted_bullet, reverse=True):
        ship.secondary_bullet.pop(i)
    
    # Show ship
    texture = np.copy(ship.ship_texture["lv" + str(ship.current_level)])
    part_minus_ship = np.copy(frame[ship_position[0] : ship_position[0] + 64, ship_position[1] : ship_position[1] + 64])
    part_minus_ship[np.where((texture != [0, 0, 0]).all(axis=2))] = [0, 0, 0]
    frame[ship_position[0] : ship_position[0] + 64, ship_position[1] : ship_position[1] + 64] = part_minus_ship + texture
    
    # Show enemies ship
    enemies_alive = np.sum([len(enemies) for enemies in enemy.enemies_position_in_t])

    if enemies_alive > 0:
        for number, enemies_path in enumerate(enemies_position):
            for i, t_value in enumerate(enemies_path):
                position = np.int32(enemy.path[str(enemy.number_path[number])](t_value))
                
                if position[0] < 0:
                    continue
                
                try:
                    part_minus_enemy = np.copy(frame[position[0] : position[0] + enemy_texture.shape[0], position[1] : position[1] + enemy_texture.shape[1]])
                    part_minus_enemy[np.where((enemy_texture != [0, 0, 0]).all(axis=2))] = [0, 0, 0]
                    frame[position[0] : position[0] + enemy_texture.shape[0], position[1] : position[1] + enemy_texture.shape[1]] = part_minus_enemy + enemy_texture
                except Exception as e:
                    if position[0] >= 700:
                        T = enemy.enemies_position_in_t[number]
                        enemy.enemies_position_in_t[number] = np.delete(T, np.where(T == t_value))
            
    
    return frame

def get_direction_from_keys(keys):
    """
    function that return direction for ship from key pressed

    Args:
        keys (set): keys that got from Listener

    Returns:
        array: direction 
    """
    
    direction = np.copy(NO_MOVE)
    
    if keyboard.KeyCode.from_char("w") in keys:
        direction += UP
    if keyboard.KeyCode.from_char("s") in keys:
        direction += DOWN
    if keyboard.KeyCode.from_char("a") in keys:
        direction += LEFT
    if keyboard.KeyCode.from_char("d") in keys:
        direction += RIGHT
        
    return direction

def is_shooting(keys):
    """
    Checking if player was shooting by pressing space button

    Args:
        keys (set): keys that got from Listener

    Returns:
        bool: shooting status 
    """
    if keyboard.Key.space in keys:
        return True
    
    return False

def get_exit_status(key):
    """
    function that return exit status from key pressed

    Args:
        key (int): key that got from cv2.waitKey()

    Returns:
        bool: exit status
    """
    
    if key == 27:
        return True
    
    return False