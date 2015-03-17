#! /usr/bin/env python3
import pyglet
from pyglet.window import mouse
import pyglet.gl as pgl

from vecrec import Vector
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
    def draw_node(node):
        position = node.position
        x, y = position.tuple
        state = node.state
        right_node = node.right_node

        # Draw the right side link
        if right_node is not None:
            rx, ry = right_node.position.tuple
            rstate = right_node.state
            color_map = {
                    'inactive' : (0,0,0),
                    'active' : (255,0,0),
                    }
            r, g, b = color_map[state]
            rr, rg, rb = color_map[rstate]
            link_points = x, y, rx, ry
            link_colors = r, g, b, rr, rg, rb
            pyglet.graphics.draw(2, pgl.GL_LINES,
                    ('v2f', link_points),
                    ('c3B', link_colors))

        # Draw the dot
        Gui.dot_images[state].blit(x,y,0)

    def draw_dot(x, y, state):
        Gui.dot_images[state].blit(x,y,0)


    # Member functions
    def __init__(self, window):
        self.window = window
        self.length_scale = Gui.dot_images['inactive'].width

        midx = self.window.width/2
        midy = self.window.height/2

        self.shape = shape.Shape(midx, midy, Gui.draw_node, self.length_scale)
        self.shape.generate_init_box(10, 5)
        self.click_location = None

    def draw(self):
        # draw some test dots
        midx = self.window.width/2
        midy = self.window.height/2
        
        Gui.draw_dot(midx   , midy   , 'inactive')
        Gui.draw_dot(midx+12, midy-12, 'active')
        Gui.draw_dot(midx-12, midy-12, 'green')
        Gui.draw_dot(midx-12, midy+12, 'blue')
        # end test dots

        # Draw the shape
        self.shape.draw()

        # Draw the mouse click
        if self.click_location is not None:
            click_x, click_y = self.click_location.tuple
            Gui.draw_dot(click_x, click_y, 'green')

    def handle_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.click_location = Vector(x, y)
            self.shape.activate_closest_nodes(self.click_location)

    def handle_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.click_location = None
            self.shape.deactivate_nodes()

    def handle_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if button == mouse.LEFT:
            delta =  Vector(dx, dy)
            self.click_location += delta
            self.shape.move_active_nodes(delta)


