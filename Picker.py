from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import threading
from math import pi, sin, cos

from direct.task import Task

import Ship

# Stuff related to mouse picking is collected in this class
class Picker ():
	def __init__(self, base, render):
		# Stash ivars
		self._base = base
		self._render = render

		# Similar to what you do for other (object to object) collision detection
		self._picker = CollisionTraverser()
		self._pickerQueue = CollisionHandlerQueue()

		# Node for the ray we're going to use, attached to camera
		pickerNode = CollisionNode ("mouseRay")
		pickerNP = camera.attachNewNode (pickerNode)

		# The ray that we'll extend from the mouse,
		# it will be relative to the camera cause we attached it to camera above
		self._pickerRay = CollisionRay()
		pickerNode.addSolid (self._pickerRay)

		# We don't need the mask feature
		pickerNode.setFromCollideMask (GeomNode.getDefaultCollideMask())

		# Register our new ray so it can trigger collisions
		self._picker.addCollider (pickerNP, self._pickerQueue)

		# Turn off the normal mouse camera control, use our mouse stuff instead
		base.disableMouse()
		base.accept("mouse1", self._mouseClick)

	def _mouseClick(self):
		if self._base.mouseWatcherNode.hasMouse():
			# Move the picker ray to current mouse position
			self._pickerRay.setFromLens (self._base.camNode, self._base.mouseWatcherNode.getMouseX(), self._base.mouseWatcherNode.getMouseY())

			# Run the picker
			self._picker.traverse(self._render)

			# Process the list returned by the picker
			if self._pickerQueue.getNumEntries() > 0:
					# Sort, so first entry = the closest object.
					self._pickerQueue.sortEntries()
					node = self._pickerQueue.getEntry(0).getIntoNodePath()

					# Climb up the graph until we find a node we had tagged
					# and fade() it, else quietly do nothing and return
					while node != self._render: 
						if node.hasPythonTag("myfade"):
							#node.ls()
							temp = node.getPythonTag ("myfade").fade()
							print temp.__class__.__name__
							self._base.accept( "arrow_up", temp.arrowUp )
							self._base.accept( "arrow_up-repeat", temp.arrowUp )
							self._base.accept( "arrow_up-up", temp.arrowUp )
							self._base.accept( "arrow_down", temp.arrowDown )
							self._base.accept( "arrow_down-repeat", temp.arrowDown )
							self._base.accept( "arrow_down-up", temp.arrowDown )
							self._base.accept( "arrow_left", temp.arrowLeft )
							self._base.accept( "arrow_left-repeat", temp.arrowLeft )
							self._base.accept( "arrow_left-up", temp.arrowLeft )
							self._base.accept( "arrow_right", temp.arrowRight )
							self._base.accept( "arrow_right-repeat", temp.arrowRight )
							self._base.accept( "arrow_right-up", temp.arrowRight )
							break
						else: 
							node = node.getParent()
							
	