#! /usr/bin/env python3
import pyglet
import pyglet.gl as pgl

import gui as GUI


window = pyglet.window.Window()
pgl.glClearColor(1,1,1,1)

gui = GUI.Gui(window)

@window.event
def on_draw():
    window.clear()
    gui.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    gui.handle_mouse_press(float(x), float(y), button, modifiers)

@window.event
def on_mouse_release(x, y, button, modifiers):
    gui.handle_mouse_release(x, y, button, modifiers)

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    # Note: x, y, dx, and dy are all integers. Events can exist where 
    # both dx and dy are zero! I do not understand why they decided to 
    # use integers rather than floats for dx and dy....
    gui.handle_mouse_drag(float(x), float(y), float(dx), float(dy), button, modifiers)


pyglet.app.run()
