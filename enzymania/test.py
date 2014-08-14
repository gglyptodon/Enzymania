import pygame
import elementtree.ElementTree as etree
import random
from EnzymaniaClasses import Drawable, Enzyme, Metabolite, Reaction, Source, Sink, Wall, PreviewPanel


RUNNING = True
FLOW = False


def makeEnzymesMetabolites(reaction):
    prod = [Metabolite(name=p, y=random.randint(0, HEIGHT-100), x=random.randint(0, WIDTH-100))
            for p in reaction.listOfProducts]
    react = [Metabolite(name=r, y=random.randint(0, HEIGHT-100), x=random.randint(0, WIDTH-100))
             for r in reaction.listOfReactants]
    reactnames = [r.name for r in react]
    prodnames = [p.name for p in prod]
    e = Enzyme(x=random.randint(0, WIDTH-100),
               y=random.randint(0, HEIGHT-100),
               name=reaction.enzymeName,
               products=prodnames,
               reactants=reactnames)
    return e, prod, react


def addReactionSet(entityList, e, r, x=0, y=20):
    entityList.append(e)
    for rr in r:
        rr.y = 20
        rr.x = 0
        rr.xvel = 1
        rr.yvel = 1
        entityList.append(rr)

def checkEvents(entityList):
    global RUNNING
    global FLOW
    reactionCounter = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            #print(event)
            if event.key == pygame.K_ESCAPE:
                print("escape")
                RUNNING = False
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.key == pygame.K_s:
                mouseX, mouseY = pygame.mouse.get_pos()
                pygame.display.toggle_fullscreen()
            elif event.key == pygame.K_e:
                mouseX, mouseY = pygame.mouse.get_pos()
                spawnEnzyme(entityList=entityList, x=mouseX, y=mouseY)
                #entityList.append(Enzyme(x=mouseX, y=mouseY))
            elif event.key == pygame.K_m:
                mouseX, mouseY = pygame.mouse.get_pos()
                entityList.append(Metabolite(x=mouseX, y=mouseY))
            elif event.key == pygame.K_r:                   #0th element as source metabolite
                e, p, r = makeEnzymesMetabolites(REACTIONSET[0])
                #todo
                dummy = Source()
                addReactionSet(entityList, e, r, dummy.x+dummy.xsize, dummy.y+dummy.ysize)
                reactionCounter += 1
            elif event.key == pygame.K_f:
                if not FLOW:
                    FLOW = True
                else:
                    FLOW = False

        if event.type == pygame.QUIT:
            RUNNING = False

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                # clicked and moving
                rel = event.rel
                enzymeList = [e for e in entityList if isinstance(e, Enzyme)]
                for entity in enzymeList:
                    if entity.shape.collidepoint(pygame.mouse.get_pos()):
                        entity.x += rel[0]
                        entity.y += rel[1]


WIDTH = 800
HEIGHT = 600
REACTIONSET = None
SCORE = ""


def texts(screen, font):
   #font=pygame.font.Font(None,42)
   scoretext=font.render(""+str(SCORE), 1,(99,99,88))
   screen.blit(scoretext, (500, 457))


def appendSource(entityList=None):
    if entityList is not None:
        entityList.append(Source())


def appendSink(entityList):
    if entityList is not None:
        entityList.append(Sink())


def spawnSourceMetabolite(entityList):
    e, p, r = makeEnzymesMetabolites(REACTIONSET[0])
    dummy = Source()
    #todo multiple
    r = r[0]
    r.x = dummy.x+dummy.xsize
    r.y = dummy.y+dummy.ysize
    entityList.append(r)

def spawnEnzyme(entityList,x=random.randint(50,WIDTH-50),y=random.randint(50,HEIGHT-50)):
    #grab random REACTIONSET
    rand = random.choice(REACTIONSET)
    e, p, r = makeEnzymesMetabolites(rand)
    e.x=x
    e.y=y
    entityList.append(e)


def main():
    pygame.init()
    #todo
    enzyme_font=pygame.font.Font("Arcade.ttf",24)
    metabolite_font=pygame.font.SysFont("monospace",18)
    metabolite_font=pygame.font.Font("SFSquareHead.ttf", 18)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Enzymania")
    pygame.mouse.set_visible(1)
    clock = pygame.time.Clock()
    #init reactionlist
    global REACTIONSET
    REACTIONSET = makeReactionSet()
    global RUNNING
    global SCORE
    RUNNING = True
    entityList = []
    print(REACTIONSET)
    appendSource(entityList)
    appendSink(entityList)
    entityList.append(Wall())
    entityList.append(PreviewPanel())
    spawningTime = 0
    while RUNNING:
        dt = clock.tick(60)
        spawningTime += dt # new source metab every 0.8sec
        checkEvents(entityList)
        screen.fill((0, 0, 0))
        if FLOW and spawningTime > 800:
            spawnSourceMetabolite(entityList)
            spawningTime = 0

        screen.blit(screen, (0, 0))
        for i, e in enumerate(entityList):
            if isinstance(e,Enzyme):
                e.addText(screen=screen, font=enzyme_font)

            elif isinstance(e,Metabolite):
                e.addText(screen=screen, font=metabolite_font)
                #print(e.name)
            #if not e.textDrawn:
            #    e.addText(screen=screen, font=font)

            e.checkCollisionList(entityList[:i])
            bounceOff(e)
            if isOutOfSight(e):
                entityList.remove(e)
                screen.blit(screen, (0, 0))
            e.move()
            e.draw(screen)
            if isinstance(e,Sink):
                pygame.draw.rect(screen, e.color, e.boundingbox, 2)

        pygame.display.flip()


def bounceOff(entity):
    if entity.x+entity.xsize > WIDTH or entity.x <0:
        if entity.xvel > 0:
            entity.xvel += 0
        else:
            entity.xvel -=0
        entity.xvel *=-1
        entity.move()

    if entity.y+entity.ysize > HEIGHT or entity.y < 0:
        if entity.yvel > 0:
            entity.yvel += 0
        else:
            entity.yvel -= 0
        entity.yvel *= -1
        entity.move()


def isOutOfSight(entity):
    out = False
    if entity.x > WIDTH or entity.x < 0 or entity.y > HEIGHT or entity.y < 0:
        out = True
    return out


def makeReactionSet (xml='enzymes_out.xml'):
    pathwaytree = etree.parse(xml)
    pathwaytree = pathwaytree.getroot()
    """prepare new Reaction objects from XML"""
    res = []

    for reaction in pathwaytree.getiterator(tag='reaction'):
        newReactionName = ""
        newReactantList = []
        newProductList = []
        try:
            newReactionName = reaction.attrib['name']
            for reactantlist in reaction.getiterator(tag='listOfReactants'):
                for reactant in reactantlist:
                    newReactantList.append(reactant.attrib['species'])

            for productlist in reaction.getiterator(tag='listOfProducts'):
                for product in productlist:
                    newProductList.append(product.attrib['species'])
            r = Reaction(name=newReactionName, enzymeName=newReactionName, listOfProducts=newProductList, listOfReactants=newReactantList)
            res.append(r)
        except Exception as e:
            print(e)
    # makes set of all enzymes in the source file and positions at bottom of screen
    # for iteration & tag == reaction
    #   newEnzyme(name, metabolites_in, metabolites_out)
    # Drawable(name='my name')
    for i in res:
        print(i)
    return res

if __name__ == "__main__":
    main()
