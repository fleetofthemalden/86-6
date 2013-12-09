from math import pi, sin, cos

from direct.actor.Actor import Actor
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import *
from direct.gui.DirectGui import *
import sys

#
# Robot class
#
class Ship (NodePath):
	def __init__(self, loader):
		NodePath.__init__(self, "myscene")
		
		self.setPythonTag ("myfade", Fader(self))
		self._listDirection = 1.
		self._bobDirection = -1.
		self._listMax = 8.
		self._bobMax = 4.
		self._boatSpeed = 0.
		
	def chart(self, headingChange):
		heading = self.getHpr() [0]
		self.setH(heading + headingChange)

	
	def incrementSpeed(self, num):
		self._boatSpeed += num
		
		
	# Received whenever timer tick()'s,
	# we should update everything we need in scene graph,
	# redraw is automatic.
	def tick (self):
		roll = self.getHpr() [2]
		pitch = self.getHpr() [1]
		heading = self.getHpr() [0]
		roll += self._listDirection * 100. / 800.
		pitch += self._bobDirection * 100. / 800.
		if abs(roll) > self._listMax:
			self._listDirection *= -1.
		if abs(pitch) > self._bobMax:
			self._bobDirection *= -1.
		
		self.setHpr (heading, pitch, roll)
		self.setPos (self, 0, self._boatSpeed, 0)
		
	def arrowUp(self):
		self.incrementSpeed(1.)
		#print "up"
	def arrowDown (self):
		self.incrementSpeed(-1.)
		#print "down"
	def arrowLeft (self):
		self.chart(4.)
		#print "left"
	def arrowRight (self):
		self.chart(-4.)
		#print "right"

# A little class to handle a node's fading
# points to the node it controls
class Fader ():
	def __init__(self, node):
		#sprint node.__class__.__name__
		self._node = node
		self._factor = 1

	def fade (self):
		#print self._node.__class__.__name__
		self._factor *= 0.9
		self._node.setColorScale (VBase4 (self._factor, self._factor, self._factor, 1))
		return self._node
	
	


	