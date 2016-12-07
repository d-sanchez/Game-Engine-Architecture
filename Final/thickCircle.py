import ogre.renderer.OGRE as ogre

import math
class ThickCircle (object):
    ''' An object that draws a circle centered at c, with radius r, and thickness t
    '''
    def __init__(self, name, sm, parentNode = None, circleType = ogre.RenderOperation.OT_TRIANGLE_LIST):
        self.name = name
        self.sceneManager = sm
        self.circleType = circleType
        self.parentNode = parentNode or self.sceneManager.getRootSceneNode()
        self.mm = ogre.MaterialManager.getSingleton()
        self.accuracy = 10
        self.yup = 5

    def setup(self, color = "RedCircle", center = (0, 5, 0), radius = 500, thickness = 40):
        self.color = color
        self.center = center
        self.radius = radius
        self.thickness = thickness
        self.circle = self.sceneManager.createManualObject(self.name)
        self.materialName = self.color
        self.circle.begin(self.materialName, self.circleType)
        self.index = 0
        twopi = 2.0 * math.pi
        inc   = math.pi/self.accuracy
        theta = 0
        for i  in range(0, self.accuracy*2):
            self.circle.position(self.radius * math.cos(theta), self.yup, self.radius * math.sin(theta))
            self.circle.position(self.radius * math.cos(theta - inc), self.yup, self.radius * math.sin(theta - inc))
            self.circle.position((self.radius - self.thickness) * math.cos(theta - inc), self.yup, (self.radius - self.thickness) * math.sin(theta - inc))
            self.circle.position((self.radius - self.thickness) * math.cos(theta), self.yup, (self.radius - self.thickness) * math.sin(theta))
            self.circle.quad(self.index, self.index+1, self.index+2, self.index+3)
            self.index += 4
            theta += inc
        self.circle.end()

        self.circleNode = self.parentNode.createChildSceneNode()
        self.circleNode.attachObject(self.circle)

    def clear(self):
        self.circleNode.setVisible(False)
    
    def show(self):
        self.circleNode.setVisible(True)

    def hide(self):
        self.circleNode.setVisible(False)

    def flipVisibility(self):
        self.circleNode.flipVisibility()

    def draw(self):
        self.circleNode.show()


