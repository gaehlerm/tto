from tto import *

laser = LightSource(P=1e-3, wavelength=532e-9)
one_meter = FreeSpace(l=100)
dichroic = DichroicBeamSplitter(cut_off_wavelength=800e-9, pass_mode=PassMode.LowPass)

light_beam = laser.emit()
light_beam.traverse(one_meter)
light_beam2 = light_beam.traverse(dichroic)
light_beam2.traverse(one_meter)
light_beam.traverse(one_meter)

run_experiment(light_beam)


window = GraphWin('what goes here?', 300, 150)
create_graphics(light_beam, window)

window.postscript(file="image.eps", colormode='color')

x = input()