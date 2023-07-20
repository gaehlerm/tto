from tto import *

mirror1 = Mirror(R=0.9)
laser = LightSource(P=1e-3, wavelength=532e-9)
sensor = PowerMeter()
dichroic_beam_splitter = DichroicBeamSplitter(cut_off_wavelength=800e-9, pass_mode=PassMode.LowPass)
beamsplitter = BeamSplitter(T=0.8)

light_beam = laser.emit()
light_beam.traverse(mirror1)
light_beam2 = light_beam.traverse(dichroic_beam_splitter)
light_beam2.traverse(sensor)
print(sensor.get_result())
light_beam.traverse(sensor)
print(sensor.get_result())