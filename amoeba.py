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


pyglet.app.run()
