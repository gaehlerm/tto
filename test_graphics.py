from tto import *

laser = LightSource(P=1e-3, wavelength=532e-9)
lens = Lens(f=3e-1)
one_meter = FreeSpace(l=100)
mirror = Mirror(R=0.9, angle_to_beam = 1)

light_beam = laser.emit()
light_beam.traverse(one_meter)
light_beam.traverse(lens)
light_beam.traverse(one_meter)
light_beam.traverse(mirror)
light_beam.traverse(one_meter)
light_beam.traverse(lens)


window = GraphWin('what goes here?', 500, 500)
create_graphics(light_beam, window)

window.postscript(file="image.eps", colormode='color')

x = input()