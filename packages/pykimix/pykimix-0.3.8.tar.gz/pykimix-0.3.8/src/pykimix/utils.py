import math
import random
import time

def clamp(value, min_val, max_val):
    return max(min(value, max_val), min_val)

def lerp(a, b, t):
    """Linear interpolation between a and b with factor t (0-1)"""
    return a + (b - a) * t

def distance(x1, y1, x2, y2):
    """Calculate Euclidean distance"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)