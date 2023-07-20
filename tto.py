from enum import Enum
import math
from graphics import *

class SpectralLine:
	def __init__(self, power, wavelength):
		self.power = power
		self.wavelength = wavelength


class Lightbeam:
	def __init__(self, P, wavelength=0, diameter=1e-3, focal_length=math.inf):
		self.P = P
		self.wavelength = wavelength
		self.diameter = diameter
		self.focal_length = focal_length
		self.objects_traversed = []

	def traverse(self, object):
		self.objects_traversed.append(object)
		return object.traverse(self)

def create_graphics(light_beam, window):
	coordinates = [0,0]
	angle = 0
	for object in light_beam.objects_traversed:
		[coordinates, angle] = object.graphical_representation(window, coordinates, angle)

def run_experiment(light_beam):
	for object in light_beam.objects_traversed:
		object.initialize()


class LightSource:
	def __init__(self, P, wavelength=0, diameter=1e-3, focal_length=math.inf):
		self.P = P
		self.wavelength = wavelength
		self.diameter = diameter
		self.focal_length = focal_length

	def emit(self):
		# TODO should we just use the traverse notation as well?
		lightbeam = Lightbeam(self.P, self.wavelength, self.diameter)
		lightbeam.objects_traversed.append(self)
		return lightbeam

	def graphical_representation(self, window, coordinates, angle):
		new_coordinates = [50,50]
		top_left = Point(new_coordinates[0]-25*math.sin(angle), new_coordinates[1]-10*math.cos(angle))
		bottom_right = Point(new_coordinates[0]+25*math.sin(angle), new_coordinates[1]+10*math.cos(angle))
		rect = Rectangle(top_left, bottom_right)

		rect.draw(window)
		return [new_coordinates, angle]

	def initialize(self):
		pass

class Mirror:
	def __init__(self, R, angle_to_beam=0):
		self.R = R
		self.angle_to_beam = angle_to_beam

	def traverse(self, beam):
		beam.P *= self.R

	def graphical_representation(self, window, coordinates, angle):
		# TODO change the rotation of the mirror
		shape = [[-10, 20],[10,20],[10,-20],[-10,-20]]
		shape = rotate(shape, angle - self.angle_to_beam/2)
		shape = translate(shape, coordinates)
		points = [Point(x,y) for [x,y] in shape]
		polygon = Polygon(points)
		polygon.draw(window)

		return [coordinates, (angle + 2*self.angle_to_beam) % (2*math.pi)]

	def initialize(self):
		pass

class BeamSplitter:
	def __init__(self, T):
		self.T = T

	def traverse(self, beam):
		beam.P *= self.T
		return Lightbeam(beam.P * (1-self.T))

	def initialize(self):
		pass

class PassMode(Enum):
	LowPass = 0
	HighPass = 1

class DichroicBeamSplitter:
	def __init__(self, cut_off_wavelength, pass_mode):
		self.cut_off_wavelength = cut_off_wavelength
		self.pass_mode = pass_mode

	def traverse(self, beam):
		# TODO how to implement this efficiently?
		if beam.wavelength > self.cut_off_wavelength and self.passmode == PassMode.LowPass:
			beam.P = 0
		return beam

	def graphical_representation(self, window, coordinates, angle):
		# TODO change the rotation of the mirror
		top_left = Point(coordinates[0], coordinates[1]-20)
		bottom_right = Point(coordinates[0]+10, coordinates[1]+20)
		rect = Rectangle(top_left, bottom_right)
		rect.draw(window)
		return [coordinates, angle]

	def initialize(self):
		pass

class PowerMeter:
	def traverse(self, beam):
		self.measured_power = beam.P
		beam.P = 0

	def get_result(self):
		return self.measured_power

class Lens:
	def __init__(self, f):
		self.f = f

	def traverse(self, beam):
		# TODO needs distance for serious implementation
		if beam.focal_length == math.inf:
			beam.focal_length = self.f
		else:
			beam.focal_length += self.f
		
	def graphical_representation(self, window, coordinates, angle):
		shape = [[10,20],[0,30],[-10,20],[-10,-20],[0,-30],[10,-20]]
		shape = rotate(shape, angle)
		shape = translate(shape, coordinates)
		points = [Point(x,y) for [x,y] in shape]
		polygon = Polygon(points)
		polygon.draw(window)

		return [coordinates, angle]

	def initialize(self):
		pass

class FreeSpace:
	def __init__(self, l):
		self.l = l

	def traverse(self, beam):
		beam.diameter = abs(beam.diameter * (1 - self.l/beam.focal_length))
		beam.focal_length -= self.l

	def graphical_representation(self, window, coordinates, angle):
		pt = Point(coordinates[0], coordinates[1])
		dx = self.l*math.cos(angle)
		dy = self.l*math.sin(angle)
		new_coordinates = [coordinates[0] + dx, coordinates[1] + dy]
		line = Line(pt, Point(new_coordinates[0], new_coordinates[1]))
		line.draw(window)

		pt2 = Point(coordinates[0], coordinates[1] + 5)
		new_coordinates2 = [coordinates[0] + dx, coordinates[1] + dy + 5]
		line2 = Line(pt2, Point(new_coordinates2[0], new_coordinates2[1]))
		line2.draw(window)

		return [new_coordinates, angle]

	def initialize(self):
		pass

def rotate(points, angle):
	new_points = []
	for point in points:
		new_point = [point[0]*math.cos(-angle) + point[1]*math.sin(-angle), -point[0]*math.sin(-angle) + point[1]*math.cos(-angle)]
		new_points.append(new_point)
	return new_points

def translate(points, translation):
	new_points = []
	for point in points:
		new_point = [point[0]+translation[0], point[1]+translation[1]]
		new_points.append(new_point)
	return new_points


