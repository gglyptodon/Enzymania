###############################################################################################
### initiate instances of Enzyme and Metabolite classes based upon the enzymes_out.xml data ###
###############################################################################################
# copy pasta classes to avoid issues of simultaneous changes.
import pygame
import math
import elementtree.ElementTree as etree

class Drawable(object):
    ID = 0

    def __init__(self, name="",
                 x=0, y=0, xvel=1.0, yvel=1.0,
                 angle= math.pi/2, xsize=10, ysize=10,
                 color=(0, 255, 0), shapeStr="rectangle"):

        Drawable.ID += 1
        self.id = Drawable.ID
        self._name = name
        self._x = x
        self._y = y
        self._xvel = xvel
        self._yvel = yvel
        self._angle = angle
        self._xsize = xsize
        self._ysize = ysize
        self._shape = self.initShape(shapeStr)
        self._shapeStr = shapeStr
        self.xsurface = self.x+self.xsize
        self.ysurface = self.y+self.ysize
        self._color = color
        # create an actual rect, polygon etc; easier for collision handling
        self.hasCollided = False

    def __repr__(self):
        s = ""
        s += ",".join([str(i) for i in [self.id, self.x, self.y, self.xsize, self.ysize, self.shape, self.color]])
        return s

    def initShape(self, shapeStr):
        if isinstance(shapeStr, str):
            if shapeStr.lower() == "rectangle":
                return pygame.Rect(self._x, self._y, self._xsize, self._ysize)
            else:
                return None
        else:
            raise Exception("initShape needs str")

    @property
    def x(self):
        return self._shape.x

    @x.setter
    def x(self, val):
        try:
            self._shape.x = float(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def y(self):
        return self._shape.y

    @y.setter
    def y(self, val):
        try:
            self._shape.y = float(val)
            self._y = float(val)
            # print(self._shape.y)
        except TypeError as e:
            print(e, self.id)

    @property
    def yvel(self):
        return self._yvel

    @yvel.setter
    def yvel(self, val):
        try:
            self._yvel = float(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def xvel(self):
        return self._xvel

    @xvel.setter
    def xvel(self, val):
        try:
            self._xvel = float(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, val):
        try:
            self._angle = float(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        if isinstance(val, tuple):
            try:
                self._color = val
            except TypeError as e:
                print(e, self.id)
        else:
            raise Exception("Sth wrong with color setter")

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, val):
        try:
            self._color = int(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def xsize(self):
        return self._xsize

    @xsize.setter
    def xsize(self, val):
        try:
            self._shape.width = int(val)
            self._xsize = int(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def ysize(self):
        return self._ysize

    @ysize.setter
    def ysize(self, val):
        try:
            self._ysize = int(val)
            self._shape.height = int(val)
        except TypeError as e:
            print(e, self.id)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        if isinstance(val, str):
            self._name = val

    def draw(self, display):
        if self._shapeStr == "rectangle":
            if isinstance(self._shape, pygame.Rect):
                pygame.draw.rect(display, self._color, self._shape, 2)
        else:
            #TODO
            pass

    def move(self, x=None, y=None):
        if x is None:
            x = self.xvel
        if y is None:
            y = self.yvel
        #self.x += math.sin(self._angle) * self.xvel
        #self.y -= math.cos(self._angle) * self.yvel
        self.x += self.xvel
        self.y += self.yvel

    def checkCollision(self, other):
        try:
            if self.shape.colliderect(other.shape):
                #self._color = (255, 0, 0)
                self.collide()
                other.collide()
        except TypeError as e:
            print(e)

    def checkCollisionList(self, otherList):
        others = [o.shape for o in otherList]
        try:
            collided = (self.shape.collidelistall(others))
            if len(collided) > 0:
                for i in collided:
                    #otherList[i].collide()
                    self.bounceOff(otherList[i])
                self._color = (255, 0, 0)
        except TypeError as e:
            print(e)

    def bounceOff(self, other):
        if self.x+self.xsize > other.x or self.x < other.x+other.xsize:
            if self.xvel > 0:
                self.xvel += 0.2
            else:
                self.xvel -= 0.2
            self.xvel *= -1
            #self.move()

        elif self.y+self.ysize > other.y or self.y < other.ysize:
            if self.yvel > 0:
                self.yvel += 0.2
            else:
                self.yvel -=0.2
            self.yvel *=-1
        self.move()


class Enzyme(Drawable):
    def __init__(self, *args, **kwargs):
        Drawable.__init__(self, *args, **kwargs)
        self.xsize=30
        self.ysize=10
        self.xvel=0
        self.yvel=0
    def bounceOff(self, other):
        #pass
        other.bounceOff(self)

class Metabolite(Drawable):
    def __init__(self, *args, **kwargs):
        Drawable.__init__(self, *args, **kwargs)
        self.xsize = 5
        self.ysize = 5

    def bounceOff(self, other):
        x1s = self.x
        x2s = self.x+self.xsize
        y1s = self.y
        y2s = self.y+self.ysize

        x1o = other.x
        x2o = other.x+other.xsize
        y1o = other.y
        y2o = other.y+other.ysize

        if (y1s < y1o and y2s > y1o) or (y1s < y2o and y2s > y2o):
            self.yvel *= -1
            print("rev y", self._yvel)
        if (x1s < x1o and x2s > x1o) or (x1s < x2o and x2s > x2o):
            self.xvel *= -1
            print("rev x", self._xvel)
        self.move()
        #overlapX = max([abs(other.x-(self.x+self.xsize)), abs(self.x -(other.x+other.xsize))])

        #overlapY = max([abs(other.y-(self.y+self.ysize)), abs(self.y-(other.y+other.ysize))])
        #print(overlapX, overlapY)
        #print("x",abs(other.x-(self.x+self.xsize)))
        #print("y",abs(self.x -(other.x+other.xsize)))
        #if overlapX > overlapY:
        #if self.x+self.xsize > other.x or self.x < other.x+other.xsize:
        #    if self.xvel > 0:
        #        self.xvel += 0.0
        #    else:
        #        self.xvel -= 0.0
        #    self.xvel *= -1
        #    self.move()

        #    print("bouncex",self.x, other.x, self.xsize, self.ysize)
        #else:
        #if self.y+self.ysize > other.y or self.y < other.ysize:
        #    if self.yvel > 0:
        #        self.yvel += 0
        #    else:
        #        self.yvel -= 0
        #    self.yvel *= -1
        #    self.move()
        #    print("bouncey")


# create random enzyme
pathwaytree = etree.parse('enzymes_out.xml')
pathwaytree = pathwaytree.getroot()

def newEnzymeSet (pathwaytree)
    # makes set of all enzymes in the source file and positions at bottom of screen
    # for iteration & tag == reaction
    #   newEnzyme(name, metabolites_in, metabolites_out)
    # Drawable(name='my name')
    pass
def newEnzyme (name, metabolites_in, metabolites_out)
    # given
    pass
print pathwaytree
# create random metabolite