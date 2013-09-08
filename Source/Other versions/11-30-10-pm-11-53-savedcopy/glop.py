# known issues
# 1. when canvas size changes, everything resets-- bad
# resolved mostly by disabling resize
# 2. when clicking and dragging bottles, the top part of the bottle disappears even though the moveBottle
#       function should be changing it's coordinates
# more or less resolved by disabling move bottles
# 3. measuring spoons are not yet implemented and should probably be a subclass of measuring tools, reusing
#     code written for measuring cups, which also should become a subclass rather than a class
# not yet resolved
# 4. Better user feedback with text box (and possibly person) needs to be implemented.
# 5. INSTRUCTIONS
# good progress on 4 and 5
# 6. alternate solutions to recipes



#setting up canvas

from Tkinter import *
import random
import bottles
import recipes
import measures
import cauldron

# to make the canvas a struct instead of a dictionary
class Struct:
    pass

def leftMousePressed(event):
    canvas = event.widget.canvas
    (x, y) = event.x, event.y
    currentBottles = canvas.currentBottles
    currentCups = canvas.currentCups
    location = None # default
    for currentBottle in currentBottles:
        (left, top, right, bottom) = currentBottle.bounds
        if (x >= left) and (x<= right) and (y >= top) and (y<= bottom):
            cupOnCounter = canvas.cupOnCounter
            ingredientColorRGB = canvas.ingredientContainers[str(currentBottle.ingredientName)]["bottleColor"]
            if (cupOnCounter != None):
                cupOnCounter.isFull = True
                ingredientColor = RGBtoHex(ingredientColorRGB[0], ingredientColorRGB[1], ingredientColorRGB[2])
                cupOnCounter.drawCupFill(ingredientColor)
                cupOnCounter.filledWith = ingredientColorRGB
                cupOnCounter.info.append(currentBottle.info) # add the ingredient information to the information for the cup
    for currentCup in currentCups:
        (left, top, right, bottom) = currentCup.bounds
        if (x >= left) and (x<= right) and (y >= top) and (y<= bottom):
            currentCup.isSelected = True
            canvas.mCupSize = currentCup.floatSize

def leftMouseClickAndDrag(event):
    canvas = event.widget.canvas
    # make list of bounds for each potion, loop over the list and check if it was in any of those?
    currentBottles = canvas.currentBottles # list of potion bottles objects on the canvas
    currentCups = canvas.currentCups
    (x, y) = event.x, event.y
    if (x>= 0) and (x <= canvas.width) and (y>= 0) and (y <= canvas.height):
        for currentCup in currentCups:
            if (currentCup.isSelected == True):
                    currentCup.moveCup(event.x, event.y)
       

def leftMouseReleased(event):
    canvas = event.widget.canvas
    x, y = event.x, event.y
    currentBottles = canvas.currentBottles # list of potion bottles objects on the canvas
    currentCups = canvas.currentCups
    for cup in currentCups:
        (left, top, right, bottom) = cup.bounds
        if (x >= left) and (x<= right) and (y >= top) and (y<= bottom): 
            cup.isSelected = False
            location =  find(canvas, cup)
            cup.location = location
            if (location == "counter"): 
                cup.onCounter = True
                canvas.cupOnCounter = cup
                canvas.onCounterCount +=1
            elif (location == "cauldron") and (cup.isFull ==True):
                cauldron.addToCauldron(cup.info)
                cauldron.drawCauldronLiquid(cup.filledWith)
                redraw(canvas)
                canvas.cupOnCounter = None
    recipe = canvas.recipe
    recipe.checkRecipe(canvas, cauldron.inCauldron)
    recipe.displayProgress(canvas)

def keyPressed(event):
    canvas = event.widget.canvas
    if event.char == "r":
        init(canvas)
    recipe = canvas.recipe
    if (recipe.complete == True) and (event.char == "n"):
        getNewRecipe(canvas)
    #this is not really a keyboard based game, but
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
    canvas.ingredientColor = None
    canvas.potionColor = None
    canvas.cupOnCounter = None
    canvas.onCounterCount = 0
    redraw(canvas)
    # this will set up the canvas at the beginning of each new game
    # it will have to draw the background and all the objects in the scene

def getNewRecipe(canvas):
    allRecipes = recipes.recipeList
    randomIndex = random.randint(0, len(allRecipes)-1) # shouldn't be random, should be progressively more difficult
    canvas.recipeName = allRecipes[randomIndex]

def find(canvas, anObject): # cup, would also work if moveBottle were enabled
    location = None
    (objLeft, objTop, objRight, objBottom) = anObject.bounds
    counterBounds= ("counter", canvas.counterBounds)
    cauldronBounds = ("cauldron", cauldron.cauldronBounds)
    areaBounds = [  counterBounds, cauldronBounds]
    for area in areaBounds:
        (aLeft, aTop, aRight, aBottom) = area[1]
        if ((objLeft >= aLeft) and (objRight <= aRight)) and ((objTop >= aTop) and (objBottom <= aBottom)):
            location = area[0]
    anObject.location = location
    return location

def drawStaticScene(canvas):
    drawBackground(canvas)
    drawIngredientsShelf(canvas)
    drawMeasuresShelf(canvas)
    drawCounter(canvas)
    drawRecipeBook(canvas)
    drawRecipe(canvas, canvas.recipeName)
        
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
    canvas.counterBounds = (left, top - (canvas.height/16), right, bottom)
    
def drawDynamicScene(canvas): # probably a whole different module
    cauldron = cauldron.Cauldron()
    cauldron.drawCauldron()
    if canvas.potionColor != None:
        cauldron.drawCauldronLiquid(canvas, canvas.potionColor)
    drawBottles(canvas)
    drawMeasuringCups(canvas)
    recipe = canvas.recipe
    recipe.checkRecipe(canvas, cauldron.inCauldron)
    recipe.displayProgress(canvas)

def drawMeasuringCups(canvas):
    oneCup = measures.MeasuringCup(canvas, "1")
    halfCup = measures.MeasuringCup(canvas, "1/2")
    thirdCup = measures.MeasuringCup(canvas, "1/3")
    quarterCup = measures.MeasuringCup(canvas, "1/4")
    currentCups = [oneCup, halfCup, thirdCup, quarterCup]
    
    for cupIndex in range(len(currentCups)):
        cup = currentCups[cupIndex]
        cup.placeCup(cupIndex)
        cup.cupIndex = cupIndex
        cup.drawCup(canvas)
        cup.drawCupFill(None)
        
    canvas.currentCups = currentCups

    
def drawBottles(canvas):
    currentBottles = [ ]
    # these ingredients should be retrieved from the recipes dictionary in the recipe module for the current recipe
    pineSap = bottles.LiquidIngredients(canvas, "pine sap")
    roseDew = bottles.LiquidIngredients(canvas, "rose dew")
    lilyVenom = bottles.LiquidIngredients(canvas, "lily venom")
    fluxweedJuice = bottles.LiquidIngredients(canvas, "fluxweed juice")
    pamplemousse = bottles.LiquidIngredients(canvas, "pamplemousse")
    armadilloBile = bottles.LiquidIngredients(canvas, "armadillo bile")

    # bottles should only be placed in their original spots if they haven't been moved: if canvas.thingsMoved == False:
    # this is a problem when sizeChanged calls redraw
    pineSap.placeBottle(0, "left")
    roseDew.placeBottle(0, "right")
    lilyVenom.placeBottle(1, "left")
    fluxweedJuice.placeBottle(1, "right")
    pamplemousse.placeBottle(2, "left")
    armadilloBile.placeBottle(2, "right")

    pineSap.drawBottle()
    roseDew.drawBottle()
    lilyVenom.drawBottle()
    fluxweedJuice.drawBottle()
    pamplemousse.drawBottle()
    armadilloBile.drawBottle()

    canvas.pineSap = pineSap
    canvas.roseDew = roseDew
    canvas.lilyVenom = lilyVenom
    canvas.fluxweedJuice = fluxweedJuice
    canvas.pamplemousse= pamplemousse
    canvas.armadilloBile = armadilloBile

    currentBottles.append(pineSap)
    currentBottles.append(roseDew)
    currentBottles.append(lilyVenom)
    currentBottles.append(fluxweedJuice)
    currentBottles.append(pamplemousse)
    currentBottles.append(armadilloBile)
    canvas.currentBottles = currentBottles
    

def drawRecipe(canvas, potionName):
    recipe = recipes.Recipe(canvas, potionName)
    recipe.displayRecipe()
    canvas.recipe = recipe # store instance of recipe class in canvas


def RGBtoHex(red, green, blue):
    color = "#%02x%02x%02x" % (red, green, blue) # to hexadecimal string
    return color

# from resizeableDemo from class, resizes window, now unused
def sizeChanged(event):
    print "sizeChanged called"
    canvas = event.widget.canvas
    canvas.width = event.width - 4 
    canvas.height = event.height - 4
    redraw(canvas)

def run():
    # create the root and the canvas
    root = Tk()
    canvasWidth = 1100
    canvasHeight = 800
    canvas = Canvas(root, width= canvasWidth, height = canvasHeight)
    canvas.pack(fill = BOTH, expand = YES) # this makes the canvas resizable
    root.resizable(width=FALSE, height=FALSE) # and this makes it not resizable
    # store canvas in root and canvas in itself for callbacks
    root.canvas = canvas.canvas = canvas
    # set up canvas data and call init
    canvas.data = Struct()
    canvas.width = canvasWidth
    canvas.height = canvasHeight
    canvas.recipeName = "Slug Repellent" # default starting recipe
    init(canvas)
    # set up events
    root.bind("<Button-1>", leftMousePressed) # for the left mouse button
    root.bind("<B1 - Motion>", leftMouseClickAndDrag)
    root.bind("<B1 - ButtonRelease>", leftMouseReleased)
    root.bind("<KeyPress>", keyPressed)
##    root.bind("<Configure>", sizeChanged)
    root.minsize( 550 +4, 390 +4) # 4 extra pixels for frame boundaries
    # and launch the application
    root.mainloop() # this calls BLOCKS (so your program waits until you close the window)


# Actually calling something!
run()
