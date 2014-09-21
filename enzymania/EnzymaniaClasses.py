import pygame
import math


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
        self.textxOffset = 0
        # create an actual rect, polygon etc; easier for collision handling
#        self.hasCollided = False

    def addText(self, screen, font):
        tmpfont = font.render(self.name, True, (0,255,0))
        rect = tuple(tmpfont.get_rect())
        #print(rect)
        tmpwidth = rect[2]
        tmpheight = rect[3]
        #if self.x-tmpwidth/2+self.textxOffset  < self.x-tmpwidth/2:
        fontx = self.x-tmpwidth/2+math.sin(self.textxOffset)*60
        #else:
        #    fontx = self.x-tmpwidth/2-self.textxOffset
        self.textxOffset += 0.02
        #self.textxOffset%tmpwidth
        screen.blit(tmpfont, (fontx, self.y-tmpheight))
        #pygame.display.update()

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
                pygame.draw.rect(display, self._color, self._shape, 0)
        else:
            #TODO
            pass

    def move(self, x=None, y=None, boundx=800, boundy=500):
        if x is None:
            x = self.xvel
        if y is None:
            y = self.yvel

        if not self.x + self.xvel > boundx:
            self.x += self.xvel
        else:
            self.xvel *=-1
        if not (self.y + self.yvel) > boundy:
            self.y += self.yvel
        else:
            self.yvel *= -1

    def checkCollision(self, other):
        try:
            if self.shape.colliderect(other.shape):
                #self._color = (255, 0, 0)
                self.collide()
                other.collide()
        except TypeError as e:
            print(e)

    def checkCollisionList(self, otherList, entityList):
        others = [o.shape for o in otherList]
        try:
            collided = (self.shape.collidelistall(others))
            if len(collided) > 0:
                for i in collided:
                    #otherList[i].collide()
                    if isinstance(otherList[i],Enzyme):
                        otherList[i].bounceOff(self,entityList=entityList)
                        self.bounceOff(otherList[i])
                    elif isinstance(self,Enzyme):
                        self.bounceOff(otherList[i],entityList=entityList)
                        otherList[i].bounceOff(self)
                    else:
                        self.bounceOff(otherList[i])
                        otherList[i].bounceOff(self)
                self._color = (255, 0, 0)
        except TypeError as e:
            print(e)

#    def bounceOffOld(self, other):
#        if self.x+self.xsize > other.x or self.x < other.x+other.xsize:
#            if self.xvel > 0:
#                self.xvel += 0
#            else:
#                self.xvel -= 0
#            self.xvel *= -1
#            #self.move()
#
#        elif self.y+self.ysize > other.y or self.y < other.ysize:
#            if self.yvel > 0:
#                self.yvel += 0
#            else:
#                self.yvel -= 0
#            self.yvel *=-1
#        self.move()

    def bounceOff(self, other, entityList = None):
        res = self.name+" collided with "+other.name
        #velocity
        vx = self.xvel
        vy = self.yvel
        #print(str(vx)+','+str(vy))
        #coordinates y
        #take colliding sides of each box
        if vy > 0:
            ys = self.y + self.ysize
            yo = other.y
        # take the complementary sides of boxes if collision is in other direction, but inverse for future simplicity
        else:
            ys = self.y * (-1)
            yo = (other.y + other.ysize) * (-1)
        # coordinates x
        if vx > 0:
            xs = self.x + self.xsize
            xo = other.x
        else:
            xs = self.x * (-1)
            xo = (other.x + other.xsize) * (-1)

        #check for last frame pass through y
        test = []
        if (ys >= yo) and ((ys - 2.2*abs(vy)) <= yo):
            self.yvel *= -1
            test.append('y')
        else:
            #print (ys,yo,abs(vy))
            other.yvel *= -1
        #check for last frame pass through x
        if (xs >= xo) and ((xs - 2.2*abs(vx)) <= xo):
            self.xvel *= -1
            test.append('x')
        else:
            other.xvel *= -1
        if len(test) == 0:
            pass

        self.move()
        other.move()

class Enzyme(Drawable):

    def __init__(self, *args, **kwargs):
        Drawable.__init__(self) # *args, **kwargs)
        self.xsize=50
        self.ysize=30
        self.xvel=0
        self.yvel=0
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
        self.name = kwargs.get('name', "")
        """products and reactants are strings"""
        self.products = kwargs.get('products', [])
        self.reactants = kwargs.get('reactants', [])

    def explode(self, other):
        #let the metabolite disappear
        other.x = -100
        other.y = -100


    def bounceOff(self, other, entityList = None):
        new = other
        if isinstance(other, Enzyme) or isinstance(other, Wall) or isinstance(other, PreviewPanel):
            pass
        else:
            #print(other.name, self.reactants)
            #todo handle two reactants
            if other.name in self.reactants:
                self.color=(20,200,22)
                tmp = other
                #print(tmp.name,"NAME")
                new = Metabolite(name=self.products[0])
                #todo spawn 2nd, 3rd, 4th, etc... products as well as first... maybe x,y, and vel from other???
                #print(other.name, "NAMEn", self.products[0])
                other.name = self.products[0]
                        #spawn metabolit
                #print(other.name+" NAME3")
                if other.xvel >0:
                    other.x = tmp.x+self.xsize
                else:
                    other.x = tmp.x-self.xsize
                if other.yvel > 0:
                    other.y = tmp.y+self.ysize
                else:
                    other.y = tmp.y-self.ysize

                if len(self.products) > 1:
                    for i in range(1,len(self.products),1):
                        angle = math.pi / 4 * i
                        deltax = 1 - math.cos(angle)
                        deltay = math.sin(angle)
                        r = Metabolite(name=self.products[i],x=other.x,y=other.y,xvel=other.xvel + deltax,yvel=other.yvel + deltay)
                        entityList.append(r)
            else:
                self.color = (0, 90, 200)
#                self.explode(other)
       #todo
        if isinstance(other, Metabolite):
            other.bounceOff(self)
        return new


class Metabolite(Drawable):
    def __init__(self, *args, **kwargs):
        Drawable.__init__(self, *args, **kwargs)
        self.xsize = 15
        self.ysize = 15

    def bounceOff(self, other, entityList = None):
        res = self.name+" collided with "+other.name
        #velocity
        vx = self.xvel
        vy = self.yvel
        #print(str(vx)+','+str(vy))
        #coordinates y
        #take colliding sides of each box
        if vy > 0:
            ys = self.y + self.ysize
            yo = other.y
        # take the complementary sides of boxes if collision is in other direction, but inverse for future simplicity
        else:
            ys = self.y * (-1)
            yo = (other.y + other.ysize) * (-1)
        # coordinates x
        if vx > 0:
            xs = self.x + self.xsize
            xo = other.x
        else:
            xs = self.x * (-1)
            xo = (other.x + other.xsize) * (-1)

        #check for last frame pass through y
        test = []
        if (ys >= yo) and ((ys - 2.2*abs(vy)) <= yo):
            self.yvel *= -1
            test.append('y')
        else:
            #print (ys,yo,abs(vy))
            other.yvel *= -1
        #check for last frame pass through x
        if (xs >= xo) and ((xs - 2.2*abs(vx)) <= xo):
            self.xvel *= -1
            test.append('x')
        else:
            other.xvel *= -1
        if len(test) == 0:
            pass

        self.move()
        other.move()
        return(None)


class Source(Drawable):
    def __init__(self, sourceMetab=None,*args, **kwargs):
        #if "sourceMetab" in kwargs:
        self.sourceMetab = sourceMetab
#        else:
 #               self.sourceMetab = None
        Drawable.__init__(self, *args, **kwargs)
        self.xsize = 50
        self.ysize = 20
        self.xvel = 0
        self.yvel = 0
        self.color = (255, 255, 255)



class Sink(Drawable):
    def __init__(self, *args, **kwargs):

        if "sinkMetab" in kwargs:
            self.sinkMetab = kwargs["sinkMetab"]
        else:
            self.sinkMetab = None
        del kwargs

        Drawable.__init__(self, *args)
        self.xsize = 50
        self.ysize = 10
        self.color = (255, 255, 0)
        self.x = 750
        self.y = 50-10
        self.xvel = 0
        self.yvel = 0
        self.boundingbox = pygame.Rect(self.x, 0, self.xsize, 50)
        self.score = 0

    def bounceOff(self, other, entityList = None):
        if self.sinkMetab == other.name:
            self.y -= 5
            self.ysize += 5
            self.score += 1
            other.x = -100
            other.y = -100
    def addText(self, screen, font):
        tmpfont = font.render(str(self.score), True, (0,255,0))
        rect = tuple(tmpfont.get_rect())
        #print(rect)
        #tmpwidth = rect[2]
        tmpheight = rect[3]
        self.textxOffset+=0.02
        screen.blit(tmpfont, (self.x+self.xsize/3, self.y+tmpheight))


class Wall(Drawable):
    def __init__(self, *args, **kwargs):
        Drawable.__init__(self, *args, **kwargs)
        self.x = 0
        self.y = 500
        self.xsize = 800
        self.ysize = 5
        self.xvel = 0
        self.yvel = 0
        self.color = (0, 0, 255)
        #self.shape.width = 2
        #self.boundingbox = pygame.Rect(self.x,1 , self.xsize, 50)

        #if "sourceMetab" in kwargs:
        #self.sourceMetab = kwargs["sourceMetab"]
        #else:
        #   self.sourceMetab = None
    def bounceOff(self, other, entityList = None):
        pass


class PreviewPanel(Drawable):
    def __init__(self, *args, **kwargs):
        Drawable.__init__(self,*args, **kwargs)
        self.x = 500
        self.y = 505
        self.xsize = 10
        self.ysize = 100
        self.xvel = 0
        self.yvel = 0
        self.color = (0, 0, 255)
        self.nextEnzyme = None
        if "nextEnzyme" in kwargs:
            self.nextEnzyme = kwargs["nextEnzyme"]

    def addText(self, screen, font, x=660, y=550):
        if self.nextEnzyme:
            #self.nextEnzyme.x = x
            #self.nextEnzyme.y = y
            self.nextEnzyme.addText(screen=screen, font=font)

    def bounceOff(self, other, entityList = None):
        pass


    #def addText(self, screen, font):
    #    self.nextMetab.addText(screen=screen, font=font)


class Reaction(object):
    def __init__(self, name=None, enzymeName=None, listOfReactants=None, listOfProducts=None, pathway=None):
        self._name = name
        self._enzymeName = enzymeName.split("-RXN")[0]
        self._listOfReactants = [r.replace("__", "_") for r in listOfReactants]
        self._listOfProducts = [p.replace("__", "_") for p in listOfProducts]
        self._pathway = pathway

    @property
    def name(self):
        return self._name

    @property
    def enzymeName(self):
        return self._enzymeName

    @property
    def listOfProducts(self):
        return self._listOfProducts

    @property
    def listOfReactants(self):
        return self._listOfReactants

    @property
    def pathway(self):
        return self._pathway

    def __repr__(self):
        return self.enzymeName+"\nProd: "+",".join(self._listOfProducts)+"\nReact: "+",".join(self.listOfReactants)


class Score(Drawable):
    def __init__(self, *args, **kwargs):
        Drawable.__init__(self,*args, **kwargs)
        self.x = 500
        self.y = 505
        self.xsize = 10
        self.ysize = 100
        self.xvel = 0
        self.yvel = 0
        self.color = (0, 0, 255)
        self.nextEnzyme = None
        if "nextEnzyme" in kwargs:
            self.nextEnzyme = kwargs["nextEnzyme"]

    def addText(self, screen, font, x=660, y=550):
        if self.nextEnzyme:
            #self.nextEnzyme.x = x
            #self.nextEnzyme.y = y
            self.nextEnzyme.addText(screen=screen, font=font)

    def bounceOff(self, other, entityList = None):
        pass


        #def addText(self, screen, font):
        #    self.nextMetab.addText(screen=screen, font=font)
