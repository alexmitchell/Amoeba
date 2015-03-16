#! /usr/bin/env python3
import pyglet


window = pyglet.window.Window()
label = pyglet.text.Label("Hello World!", x=window.width//2, y=window.height//2)

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()

