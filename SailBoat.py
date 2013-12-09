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
class SailBoat (Ship):
	def __init__(self, loader):
		Ship.__init__(self, loader)

		# Base
		boat = loader.loadModel ("Sailboat/Sailboat")
		boat.setScale (1, 1, 1)
		boat.setPos (0, 0, 0)
		boat.reparentTo (self)

		self._listDirection = -1.
		self._bobDirection = 1.

