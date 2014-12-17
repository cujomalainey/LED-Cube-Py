from threading import Thread
import RPi.GPIO as GPIO
from time import sleep
from time import time
import random
import math

class Cube(object):
	"""docstring for Cube
		mode 0 for continuous running
		mode 1 for callback with time difference
		this driver assumes that each column has its own GPIO and each layer has again its own GPIO
	"""

	def __init__(self, leds, mode):
		super(Cube, self).__init__()
		self.leds = leds
		self._renderer = CubeRender(mode)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		for x in leds["bottom"]:
			for y in x:
				GPIO.setup(y, GPIO.OUT)
				GPIO.output(y, False)
		for z in leds["layers"]:
			GPIO.setup(z, GPIO.OUT)
			GPIO.output(z, False)
		self._renderer.nextFrame = list(list(list()))
		self._renderer.leds = leds
		self._renderer.start();

	def set_callback(self, func):
		pass
		
	def set_cube(self, image):
		self._renderer.nextFrame = image[:]

class CubeRender(Thread):
	"""docstring for CubeRender"""
	def __init__(self, mode):
		super(CubeRender, self).__init__()
		self.mode = mode
		self.on = True

	def run(self):
		while(self.on):
			self.frame = self.nextFrame[:]
			for z, zval in enumerate(self.frame):
				for y, yval in enumerate(zval):
					for x, xval in enumerate(yval):
						if (xval):
							GPIO.output(self.leds["bottom"][x][y], True)
				GPIO.output(self.leds["layers"][z], True)
				GPIO.output(self.leds["layers"][z], False)
				for y, yval in enumerate(zval):
					for x, xval in enumerate(yval):
						if (xval):
							GPIO.output(self.leds["bottom"][x][y], False)

class drop(object):
	"""docstring for drop"""
	def __init__(self, x, y, speed):
		super(drop, self).__init__()
		self.x = x
		self.y = y
		self.z = 3
		self.speed = speed
		self.current_jump = 0

	def inc(self):
		if (self.current_jump + 1 > self.speed):
			self.current_jump = 0
			self.z = self.z - 1
		else:
			self.current_jump = self.current_jump + 1

class point(object):
	"""docstring for point"""
	def __init__(self):
		super(point, self).__init__()
		self.x = random.randint(0,3)
		self.y = random.randint(0,3)
		self.z = random.randint(0,3)

	def attempt(self, coord, direction):
		if direction != 0:
			coord = coord + direction
			if coord > 3 or coord < 0:
				coord = coord - direction
		return coord

	def move(self):
		self.x = self.attempt(self.x, random.randint(-1,1))
		self.y = self.attempt(self.y, random.randint(-1,1))
		self.z = self.attempt(self.z, random.randint(-1,1))
		

class animateCube(object):
	"""docstring for animateCube"""
	def __init__(self, contoller):
		super(animateCube, self).__init__()
		self.contoller = contoller
		random.seed(time())

	def wave(self):
		i = 0;
		while (True):
			sleep(0.1)
			l = list()
			for z in range(0,4):
				l.insert(z, list())
				for y in range(0,4):
					l[z].insert(y, list())
					for x in range(0,4):
						l[z][y].insert(x, False)
			for z in range(0,4):
				for y in range(0,4):
					for x in range(0,4):
						l[round(3 * math.sin((i + x + i * y * 0.1) * 0.3) ** 2)][y][x] = True
			i = i + 1
			self.contoller.set_cube(l)
	
	def rain(self):
		drops = list()
		while (True):
			sleep(0.01)
			l = list()
			for z in range(0,4):
				l.insert(z, list())
				for y in range(0,4):
					l[z].insert(y, list())
					for x in range(0,4):
						l[z][y].insert(x, False)
			if (random.randint(0,10) > 7):
				x = drop(random.randint(0,3),random.randint(0,3), random.randint(0,6))
				drops.append(x)
			for i, obj in enumerate(drops):
				l[obj.z][obj.y][obj.x] = True
				obj.inc()
				if obj.z < 0:
					drops.pop(i)
			self.contoller.set_cube(l)

	def points(self, count):
		points = list()
		for x in range(0, count):
			points.append(point())
		while (True):
			sleep(0.05)
			l = list()
			for z in range(0,4):
				l.insert(z, list())
				for y in range(0,4):
					l[z].insert(y, list())
					for x in range(0,4):
						l[z][y].insert(x, False)
			for obj in points:
				obj.move()
				l[obj.z][obj.y][obj.x] = True
			self.contoller.set_cube(l)

if __name__ == "__main__":
	leds = {
		"bottom":[[15,18,38,32],[31,22,29,35],[21,13,23,36],[19,11,33,16]],
		"layers":[7,40,12,37]
	}
	controller = Cube(leds, 0);
	animations = animateCube(controller)
	animations.points(5)
