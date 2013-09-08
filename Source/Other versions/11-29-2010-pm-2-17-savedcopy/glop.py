# known issues
# 1. when canvas size changes, everything resets-- bad
# 2. when clicking and dragging bottles, the top part of the bottle disappears even though the moveBottle
#       function should be changing it's coordinates
# 3. measuring spoons are not yet implemented and should probably be a subclass of measuring tools, reusing
#     code written for measuring cups, which also should become a subclass rather than a class





#setting up canvas

from Tkinter import *
import bottles
import recipes
import measures

# to make the canvas a struct instead of a dictionary
class Struct:
    pass

def leftMousePressed(event):
    canvas = event.widget.canvas
    (x, y) = event.x, event.y
    currentBottles = canvas.currentBottles
    location = None # default
    for currentBottle in currentBottles:
        (left, top, right, bottom) = currentBottle.bounds
        if (x >= left) and (x<= right) and (y >= top) and (y<= bottom):
            canvas.potionColor = canvas.ingredientContainers[str(currentBottle.ingredientName)]["bottleColor"] # should depend on ingredient
##            print "cupOnCounter", canvas.cupOnCounter
            cupOnCounter = canvas.cupOnCounter
            if (cupOnCounter != None): # possibly check cupOnCounter.isFull
##                print "in leftMousePressed, cup bounds for", cupOnCounter.info, "are", cupOnCounter.bounds
                cupOnCounter.isFull = True
                cupOnCounter.drawCupFill(canvas.potionColor)
                cupOnCounter.info.append(currentBottle.info) # add the ingredient information to the information for the cup
                
##            location =  find(canvas, currentBottle) # currently unnecessary since bottles aren't moving (at least right now)
##    currentCups = canvas.currentCups
    
## currently, don't think there's anything in the final game that will happen if you click on a measuring cup
##
##    for currentCup in currentCups:
##            (left, top, right, bottom) = currentCup.bounds
##            if (x >= left) and (x<= right) and (y >= top) and (y<= bottom): #and (currentCup.isFull == False):
##                location =  find(canvas, currentCup)
##                if location == "cauldron":
##                    canvas.addedToCauldron.append(currentCup.info)
##                if location == "counter":
##                    currentCup.onCounter = True
##                    canvas.cupOnCounter = currentCup
##                    print "cupOnCounter = ", canvas.cupOnCounter
    
##    print location
    print canvas.addedToCauldron
    # in the future, this will call one of several functions depending on where the mouse is pressed such as
    # moveBottle, moveMeasuringCup, moveMeasuringSpoon, fillCup, fillSpoon, fillCauldron, or ignore(pass)

def leftMouseClickAndDrag(event):
    canvas = event.widget.canvas
    # make list of bounds for each potion, loop over the list and check if it was in any of those?
    currentBottles = canvas.currentBottles # list of potion bottles objects on the canvas
    currentCups = canvas.currentCups
    (x, y) = event.x, event.y
    if (x>= 0) and (x <= canvas.width) and (y>= 0) and (y <= canvas.height):
##        for currentBottle in currentBottles:
##            (left, top, right, bottom) = currentBottle.bounds
##            if (x >= left) and (x<= right) and (y >= top) and (y<= bottom):
##                currentBottle.moveBottle(event.x, event.y)
##                canvas.thingsMoved = True
        for currentCup in currentCups:
                (left, top, right, bottom) = currentCup.bounds
##                print "in leftMouseClickAndDrag, cupBounds are", currentCup.bounds
                if (x >= left) and (x<= right) and (y >= top) and (y<= bottom):
                    currentCup.moveCup(event.x, event.y)
                    currentCup.isMoving = True
       

def leftMouseReleased(event):
    canvas = event.widget.canvas
    x, y = event.x, event.y
##    print "leftMouseReleased x and y", x, y
    currentBottles = canvas.currentBottles # list of potion bottles objects on the canvas
    currentCups = canvas.currentCups
    for cup in currentCups:
##        print "in leftMouseReleased, cup bounds are", cup.info, cup.bounds
        (left, top, right, bottom) = cup.bounds
        if (x >= left) and (x<= right) and (y >= top) and (y<= bottom): #and (currentCup.isFull == False):
            cup.isMoving = False
            location =  find(canvas, cup)
            cup.location = location
            if location == "counter":
                cup.onCounter = True
                canvas.cupOnCounter = cup
## currently unnecessary since bottles aren't moving
##    for bottle in currentBottles:
##        (left, top, right, bottom) = bottle.bounds
##        bottle.isMoving = False
##        location = find(canvas, bottle)
##        bottle.location = location

       

def keyPressed(event):
    pass
    #this is not really a keyboard based game, but pressing p would pause the game (as much as it can be)
    # pressing h should present a help screen with instructions
    # pressing r should restart the level/the game

def timerFired(canvas):
    pass
    #not a twitch game, so this may not be necessary, but probably will be anyway, especially if there's
    # ongoing animation in the background

def redraw(canvas):
    canvas.delete(ALL) # effectively redraw all, but * get rid of this later
    drawBackground(canvas)
    drawStaticScene(canvas)
    drawDynamicScene(canvas)
    # temporary function to be replaced with delta graphics

    
def init(canvas):
    canvas.width = canvas.winfo_reqwidth()
    canvas.height = canvas.winfo_reqheight()
    canvas.potionColor = None
    redraw(canvas)
    # this will set up the canvas at the beginning of each new game
    # it will have to draw the background and all the objects in the scene
    # it will display the recipe on the book in the corner

def find(canvas, anObject): # cup, bottle
    location = None
    (objLeft, objTop, objRight, objBottom) = anObject.bounds
    counterBounds = ("counter", canvas.counterBounds)
    cauldronBounds = ("cauldron",canvas.cauldronBounds)
    ingredientShelfBounds = ("ingredients shelf",canvas.ingredientsShelfBounds)
    eachIngredientShelfBounds = canvas.ingredientsShelves # list of bounds for each shelf (there are 3)
    topMeasuresShelfBounds = ("top measures shelf", canvas.measuresShelf1)
    bottomMeasuresShelfBounds = ("bottom measures shelf", canvas.measuresShelf2)
    areaBounds = [ counterBounds, cauldronBounds, ingredientShelfBounds,
                   topMeasuresShelfBounds, bottomMeasuresShelfBounds]
    for area in areaBounds:
        (aLeft, aTop, aRight, aBottom) = area[1]
        if ((objLeft >= aLeft) and (objRight <= aRight)) and ((objTop >= aTop) and (objBottom <= aBottom)):
            location = area[0]
##            if location == "cauldron":
##                canvas.addedToCauldron.append(anObject.info)
    anObject.location = location
    return location

def drawStaticScene(canvas):
    drawBackground(canvas)
    drawIngredientsShelf(canvas)
    drawMeasuresShelf(canvas)
    drawCounter(canvas)
    drawRecipeBook(canvas)
    drawRecipe(canvas, "Good Luck Potion")
    
def drawBackground(canvas):
    backgroundColor = RGBtoHex(174,147,134)
    canvas.create_rectangle(0, 0, canvas.width, canvas.height, fill = backgroundColor)

def drawIngredientsShelf(canvas):
    # draw background of shelf
    shelfColor = RGBtoHex(106, 45, 4)
    canvas.shelfColor = shelfColor
    left = (canvas.width*4)/5
    top = 4
    right = canvas.width
    bottom =  canvas.height
    canvas.ingredientsShelfBounds = (left, top, right, bottom)
    canvas.create_rectangle(left, top, right, bottom, fill = shelfColor)
    # draw shelf lines-- four rectangles/shelves
    shelfLinesColor = RGBtoHex(150, 63, 5)
    canvas.shelfLinesColor = shelfLinesColor
    shelves = 3 #store in canvas later?
    shelfCoords = [ ]
    for shelf in xrange(shelves):
        # shelfName created for debugging and possibly use as a key to access info about shelf from canvas dictionary
        left = (canvas.width*4)/5
        top = (canvas.height*shelf)/4 + 5 # 5 is for window border
        right = canvas.width
        bottom = top + (canvas.height)/4
        shelfWidth = canvas.width/100
        canvas.create_rectangle(left, top, right, bottom, fill = None, width = shelfWidth)
        shelfCoords.append((left, right, top, bottom))
    canvas.ingredientsShelves = shelfCoords      
 
def drawMeasuresShelf(canvas):
    for shelf in xrange(2):
        left = canvas.width/4 #relative to recipe book
        top = 5 + (canvas.height*shelf)/8
        right = (canvas.width*4)/5 # relative to ingredients shelf
        bottom = top +canvas.height/8
        canvas.create_rectangle(left, top, right, bottom, fill = canvas.shelfColor)
        shelfWidth = canvas.width/100
        canvas.create_rectangle(left, top, right, bottom, fill = None, width = shelfWidth)
    canvas.measuresShelf1 = (left, 5, right, (canvas.height/8)+5)
    canvas.measuresShelf2 = (left, top, right, bottom)

def drawRecipeBook(canvas):
    # draw "cover"
    coverColor = RGBtoHex(150, 63, 5)
    left = 0
    top = 0
    right = canvas.width/4
    bottom = canvas.height/2
    canvas.create_rectangle(left, top, right, bottom, fill = coverColor)
    # draw blank page
    for page in xrange(7):
        border = canvas.width/80
        pageBorder = 1 # to give the effect of multiple pages
        right = right - page*pageBorder
        pageColor = RGBtoHex(250, 248, 239)
        canvas.create_rectangle(left, top + border, right - border, bottom-border, fill= pageColor)
        pageBounds = (left, top+border, right - border, bottom-border)
    canvas.pageBounds = pageBounds
        
def drawCounter(canvas):
    counterColor = RGBtoHex(48,33, 18)
    left = 0
    top = (canvas.height*3)/4 + canvas.height/100
    right = canvas.width
    bottom = canvas.height
    counter = canvas.create_rectangle(left, top, right, bottom, fill = counterColor)
    canvas.counterBounds = (left, top, right, bottom)

def drawCauldron(canvas):
    cauldronColor = RGBtoHex(34, 35, 24)
    # outer oval
    left = canvas.width/5
    top = (canvas.height*3)/5
    right = left + canvas.width/4
    bottom = top + canvas.height/3
    canvas.create_oval(left, top, right, bottom, fill = cauldronColor)
    canvas.cauldronBounds = (left, top, right, bottom)
    # top oval
    bottom = top + canvas.height/8
    canvas.create_oval(left, top, right, bottom, fill = cauldronColor, width = 2)
    # rim
    space = canvas.width/90
    left = left + space
    top =  top + space
    right = right - space
    bottom = bottom - space
    canvas.create_oval(left, top, right, bottom, fill = cauldronColor, width = 2)
    canvas.cauldronRimBounds = (left, top, right, bottom)

def drawCauldronLiquid(canvas):
    potionColor = canvas.potionColor
    rimBounds = canvas.cauldronRimBounds
    border = (rimBounds[2] - rimBounds[0])/12
    left = rimBounds[0] + border
    top = rimBounds[1] + 1.6*border
    right = rimBounds[2] - border
    bottom = rimBounds[3] 
    canvas.create_oval(left, top, right, bottom, fill = potionColor, width = 0)

    
    
def drawDynamicScene(canvas): # probably a whole different module
    drawCauldron(canvas)
    drawBottles(canvas)
    drawMeasuringCups(canvas)  

def drawMeasuringCups(canvas):
    oneCup = measures.MeasuringCup(canvas, "1")
    halfCup = measures.MeasuringCup(canvas, "1/2")
    thirdCup = measures.MeasuringCup(canvas, "1/3")
    quarterCup = measures.MeasuringCup(canvas, "1/4")
    currentCups = [oneCup, halfCup, thirdCup, quarterCup]
    
### * should be if canvas.thingsMoved == False:
    for cupIndex in range(len(currentCups)):
        cup = currentCups[cupIndex]
        cup.placeCup(cupIndex)
        cup.drawCup(canvas)
        cup.drawCupFill()
        
    canvas.currentCups = currentCups

    
def drawBottles(canvas):
    currentBottles = [ ]

    gillywater = bottles.LiquidIngredients(canvas, "gillywater")
    leechJuice = bottles.LiquidIngredients(canvas, "leech juice")
    lilyVenom = bottles.LiquidIngredients(canvas, "lily venom")

    # bottles should only be placed in their original spots if they haven't been moved: if canvas.thingsMoved == False:
    # this is a problem when sizeChanged calls redraw
    gillywater.placeBottle(0, "left")
    leechJuice.placeBottle(0, "right")
    lilyVenom.placeBottle(1, "left")

    gillywater.drawBottle()
    leechJuice.drawBottle()
    lilyVenom.drawBottle()

    canvas.gillywater = gillywater
    canvas.leechJuice = leechJuice
    canvas.lilyVenom = lilyVenom

    currentBottles.append(gillywater)
    currentBottles.append(leechJuice)
    currentBottles.append(lilyVenom)
    canvas.currentBottles = currentBottles
    

def drawRecipe(canvas, potionName):
    recipe = recipes.Recipe(canvas, potionName)
    recipe.displayRecipe()
                                              
def RGBtoHex(red, green, blue):
    color = "#%02x%02x%02x" % (red, green, blue) # to hexadecimal string
    return color

# from resizeableDemo from class, resizes window
def sizeChanged(event):
    canvas = event.widget.canvas
    canvas.width = event.width - 4 
    canvas.height = event.height - 4
    redraw(canvas)

def run():
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width= 1100, height = 800)
    canvas.pack(fill = BOTH, expand = YES) # this makes the canvas resizable
    # store canvas in root and canvas in itself for callbacks
    root.canvas = canvas.canvas = canvas
    # set up canvas data and call init
    canvas.data = Struct()
    init(canvas)
    canvas.addedToCauldron = [ ]
    canvas.cupOnCounter = None
    # set up events
    root.bind("<Button-1>", leftMousePressed) # for the left mouse button
    root.bind("<B1 - Motion>", leftMouseClickAndDrag)
    root.bind("<B1 - ButtonRelease>", leftMouseReleased)
    root.bind("<KeyPress>", keyPressed)
    root.bind("<Configure>", sizeChanged)
    root.minsize( 550 +4, 390 +4) # 4 extra pixels for frame boundaries
    # and launch the application
    root.mainloop() # this calls BLOCKS (so your program waits until you close the window)


# Actually calling something!
run()
