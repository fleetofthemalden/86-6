from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import threading
from math import pi, sin, cos

from direct.task import Task

import Ship
import RowBoat
import SailBoat
import BigBoat
import Picker

#
# Root of our scene
#
class Scene (NodePath):
	def __init__(self, parent):
		NodePath.__init__(self, "myscene")
		
		# Load the environment model.
		self.environ = parent.loader.loadModel("BeachTerrain/BeachTerrain")
        # Reparent the model to render.
		self.environ.reparentTo(self)
        # Apply scale and position transforms on the model.
		self.environ.setScale(1,1,1)
		self.environ.setPos(-8, -60, -4)
		
		# Load the environment model.
		self.sky = parent.loader.loadModel("happysky/happysky")
        # Reparent the model to render.
		self.sky.reparentTo(self)
        # Apply scale and position transforms on the model.
		self.sky.setScale(1,1,1)
		self.sky.setPos(0,0,-7)
		
		# Add the spinCameraTask procedure to the task manager.
		parent.taskMgr.add(parent.spinCameraTask, "SpinCameraTask")

		# We save list of ships so tick() can access
		self._ships = []
		

		# First ship, location is from WC origin to ship local origin
		r = RowBoat.RowBoat (parent.loader)
		r.setPos (0, 15, -5)
		r.reparentTo (self)
		self._ships.append (r)

		# Second ship, different local origin
		r = SailBoat.SailBoat (parent.loader)
		r.setPos (-25, 45, -5)
		r.setHpr (20, 0, 0)
		r.reparentTo (self)
		self._ships.append (r)
		
		# Second ship, different local origin
		r = BigBoat.BigBoat (parent.loader)
		r.setPos (200, 200, -7)
		r.setHpr (20, 0, 0)
		r.reparentTo (self)
		self._ships.append (r)

		#
		# Set up some lights, just inline here, not in separate object
		#
		# Main light
		l = DirectionalLight("main light")
		lnode = parent.render.attachNewNode (l)
		lnode.setHpr (45, -45, -3)
		parent.render.setLight (lnode)

		# Fill light, ditto
		l = DirectionalLight ("fill light")
		l.setColor (VBase4 (.5, .5, .5, 1.))
		lnode = parent.render.attachNewNode (l)
		lnode.setHpr (-45, 0, 0)
		parent.render.setLight (lnode)

		# Ambient light, to reduce shadows
		l = AmbientLight ("ambient light")
		l.setColor (VBase4 (.1, .1, .1, 1.))
		lnode = parent.render.attachNewNode (l)
		parent.render.setLight (lnode)

		# Set up timer, 0.1 seconds
		threading.Timer (0.1, self._tick).start()

	# Receive timer tick, pass it to objects that need it,
	# then set up another timer for next tick
	def _tick (self):
		for r in self._ships:
			r.tick()
		threading.Timer (0.1, self._tick).start()


#
# Main program
#
class MyApp (ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		Picker.Picker (self, self.render)
		scene = Scene (self)
		scene.reparentTo (self.render)
		self._zoomRad = 100.0
		self._zoomHt = 3
		self._orginX = 0.
		self._orginY = 0.
		self._pitch = 0.
		self._roll = 0.
		self.accept( "shift-arrow_up", self.arrowUp )
		self.accept( "shift-arrow_up-repeat", self.arrowUp )
		self.accept( "shift-arrow_up-up", self.arrowUp )
		self.accept( "shift-arrow_down", self.arrowDown )
		self.accept( "shift-arrow_down-repeat", self.arrowDown )
		self.accept( "shift-arrow_down-up", self.arrowDown )
		self.accept( "shift-arrow_left", self.arrowLeft )
		self.accept( "shift-arrow_left-repeat", self.arrowLeft )
		self.accept( "shift-arrow_left-up", self.arrowLeft )
		self.accept( "shift-arrow_right", self.arrowRight )
		self.accept( "shift-arrow_right-repeat", self.arrowRight )
		self.accept( "shift-arrow_right-up", self.arrowRight )
		self.accept( "alt-arrow_up", self.arrowUpCtrl )
		self.accept( "alt-arrow_up-repeat", self.arrowUpCtrl )
		self.accept( "alt-arrow_up-up", self.arrowUpCtrl )
		self.accept( "alt-arrow_down", self.arrowDownCtrl )
		self.accept( "alt-arrow_down-repeat", self.arrowDownCtrl )
		self.accept( "alt-arrow_down-up", self.arrowDownCtrl )
		self.accept( "alt-arrow_left", self.arrowLeftCtrl )
		self.accept( "alt-arrow_left-repeat", self.arrowLeftCtrl )
		self.accept( "alt-arrow_left-up", self.arrowLeftCtrl )
		self.accept( "alt-arrow_right", self.arrowRightCtrl )
		self.accept( "alt-arrow_right-repeat", self.arrowRightCtrl )
		self.accept( "alt-arrow_right-up", self.arrowRightCtrl )
	
	def spinCameraTask(self, task):
		angleDegrees = task.time * 6.0
		angleRadians = angleDegrees * (pi / 180.0)
		zoom = self._zoomRad
		self.camera.setPos(zoom * sin(angleRadians), -1 * zoom * cos(angleRadians), self._zoomHt)
		self.camera.setHpr(angleDegrees, self._pitch, self._roll)
		return Task.cont
		
	def arrowUp(self):
		self._zoomHt += 1.
	def arrowDown(self):
		self._zoomHt -= 1.
	def arrowLeft(self):
 		self._zoomRad -= 5.
 	def arrowRight(self):
 		self._zoomRad += 5.
	def arrowUpCtrl(self):
		self._pitch += 1.
	def arrowDownCtrl(self):
		self._pitch -= 1.
	def arrowLeftCtrl(self):
		self._roll -= 1.
	def arrowRightCtrl(self):
		self._roll += 1.

MyApp().run()