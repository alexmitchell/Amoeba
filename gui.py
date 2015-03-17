#! /usr/bin/env python3
import pyglet
import pyglet.gl as pgl

import shape

# Helper functions
def load_centered_image(filename):
    img = pyglet.image.load(filename)
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
    return img


class Gui:
    dot_images = {
            'inactive' : load_centered_image("images/black_dot.png"),
            'active'   : load_centered_image("images/red_dot.png"),
            'green' : load_centered_image("images/green_dot.png"),
            'blue' : load_centered_image("images/blue_dot.png")
            }

    # Class functions
    def draw_dot(x, y, state):
        Gui.dot_images[state].blit(x,y,0)


    # Member functions
    def __init__(self, window):
        self.window = window
        self.length_scale = Gui.dot_images['inactive'].width

        midx = self.window.width/2
        midy = self.window.height/2

        self.shape = shape.Shape(midx, midy, Gui.draw_dot, self.length_scale)
        self.shape.generate_init_box(10, 5)

    def draw(self):

        midx = self.window.width/2
        midy = self.window.height/2

        Gui.draw_dot(midx   , midy   , 'inactive')
        Gui.draw_dot(midx+12, midy-12, 'active')
        Gui.draw_dot(midx-12, midy-12, 'green')
        Gui.draw_dot(midx-12, midy+12, 'blue')

        self.shape.draw()


