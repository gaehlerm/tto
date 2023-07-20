from graphics import *
import time

from tto import *



laser = LightSource(P=1e-3, wavelength=532e-9)
lens = Lens(f=3e-1)
one_meter = FreeSpace(l=100)

light_beam = laser.emit()
light_beam.traverse(lens)
# light_beam.traverse(lens)
light_beam.traverse(one_meter)
light_beam.traverse(lens)
print(light_beam.focal_length)
print(light_beam.diameter)

window = GraphWin('what goes here?', 150, 150)
create_graphics(light_beam, window)

message = Text(Point(window.getWidth()/2, 20), 'test test test')
message.draw(window)

window.postscript(file="image.eps", colormode='color')


x = input()
