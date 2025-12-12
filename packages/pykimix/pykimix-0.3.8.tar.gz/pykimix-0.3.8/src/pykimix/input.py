import pygame

class InputManager:
    def __init__(self):
        self.key_down_callbacks = []
        self.touch_callbacks = []

    def register_key_down(self, callback):
        self.key_down_callbacks.append(callback)

    def register_touch(self, callback):
        self.touch_callbacks.append(callback)