# Put the robot class in a separate file
# This one also responds to tick() from timer
# and to mouse picking

from math import pi, sin, cos

from direct.actor.Actor import Actor
 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import *
from direct.gui.DirectGui import *
from Ship import *

#
# Robot class
#
class RowBoat (Ship):
	def __init__(self, loader):
		Ship.__init__(self, loader)

		# Base
		boat = loader.loadModel ("Rowboat/Rowboat")
		boat.setScale (1, 1, 1)
		boat.setPos (0, 0, 0)
		boat.reparentTo (self)
		

		
		rightOar = boat.find("**/rpaddle")
		rightOar.setHpr (0, 0, -33)
		#rightOar.setPythonTag ("myfade", Fader(rightOar))
		self._rightMove = rightOar
		self._rightDirection = 1.
		

		
		leftOar = boat.find("**/leftpaddle")
		leftOar.setHpr (0, 0, 33)
		#leftOar.setPythonTag ("myfade", Fader(leftOar))
		self._leftMove = leftOar
		self._leftDirection = -1.


	# Received whenever timer tick()'s,
	# we should update everything we need in scene graph,
	# redraw is automatic.
	def tick (self):
		Ship.tick(self)
		
		roll = self._rightMove.getHpr() [2]
		feather = self._rightMove.getHpr() [1]
		angle = self._rightMove.getHpr() [0]
		angle += self._rightDirection * 150. / 50.
		if abs(angle) > 40:
			self._rightDirection *= -1.
			#feather = 0.
		if angle > 30:
			feather += 600. / 50.
		if angle < -30:
			feather -= 600. / 50.
		self._rightMove.setHpr (angle, feather, roll)

		# Left armhand:
		# oscillates -30 to +30 degrees in 1 second
		roll = self._leftMove.getHpr() [2]
		feather = self._leftMove.getHpr() [1]
		angle = self._leftMove.getHpr() [0]
		angle += self._leftDirection * 150. / 50.
		if abs(angle) > 40:
			self._leftDirection *= -1.
		if angle > 30:
			feather -= 600. / 50.
		if angle < -30:
			feather += 600. / 50.
		self._leftMove.setHpr (angle, feather, roll)
		#print angle

