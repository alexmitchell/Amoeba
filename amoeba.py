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
    gui.handle_mouse_press(x, y, button, modifiers)

@window.event
def on_mouse_release(x, y, button, modifiers):
    gui.handle_mouse_release(x, y, button, modifiers)

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
    gui.handle_mouse_drag(x, y, dx, dy, button, modifiers)


pyglet.app.run()
