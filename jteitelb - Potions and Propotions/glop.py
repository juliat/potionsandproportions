# known issues

#setting up canvas

from Tkinter import *
import random
import copy
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
    if canvas.currentBottles != None:
        for currentBottle in currentBottles:
            (left, top, right, bottom) = currentBottle.bounds
            if (x >= left) and (x<= right) and (y >= top) and (y<= bottom):
                cupOnCounter = canvas.cupOnCounter
                ingredientColorRGB = canvas.ingredientInfo[str(currentBottle.ingredientName)]["bottleColor"]
                if (cupOnCounter != None):
                    cupOnCounter.isFull = True
                    ingredientColor = RGBtoHex(ingredientColorRGB[0], ingredientColorRGB[1], ingredientColorRGB[2])
                    cupOnCounter.drawCupFill(ingredientColor)
                    cupOnCounter.filledWithColor = ingredientColorRGB
                    cupOnCounter.filledWith=(currentBottle.ingredientName) # add the ingredient information to the information for the cup
    for currentCup in currentCups:
        (left, top, right, bottom) = currentCup.bounds
        if (x >= left) and (x<= right) and (y >= top) and (y<= bottom):
            currentCup.isSelected = True

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
    print currentBottles
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
                canvas.myCauldron.addToCauldron(cup.filledWith, cup.floatSize)
                canvas.myCauldron.drawCauldronLiquid(cup.filledWithColor)
                canvas.recipe.checkRecipe(canvas.myCauldron.inCauldron)
                cup.isFull = False
                redraw(canvas)
                canvas.cupOnCounter = None
    recipe = canvas.recipe
    recipe.checkRecipe(canvas.myCauldron.inCauldron)
    

def keyPressed(event):
    canvas = event.widget.canvas
    if event.char == "r":
        canvas.ingredientColor = None
        canvas.cupOnCounter = None
        canvas.onCounterCount = 0
        myCauldron = cauldron.Cauldron(canvas)
        canvas.myCauldron = myCauldron
        drawScene(canvas)
    if (event.char == "n") and (canvas.recipe.complete == True):
        getNewRecipe(canvas)
        init(canvas)

   
def init(canvas):
    getNewRecipe(canvas)
    canvas.ingredientColor = None
    canvas.cupOnCounter = None
    canvas.onCounterCount = 0
    myCauldron = cauldron.Cauldron(canvas)
    canvas.myCauldron = myCauldron
    canvas.backgroundImage = PhotoImage(file = "apothecaryBackground.gif")
    canvas.backgroundImage = canvas.backgroundImage.zoom(2,2)
    canvas.ingredientsShelfImage = PhotoImage(file = "ingredientsShelf.gif")
    canvas.measuresShelfImage = PhotoImage(file = "measuresShelf.gif")
    canvas.personImage = PhotoImage(file = "mcgontransp.gif")
    canvas.personImage = canvas.personImage.subsample(2, 2)
    canvas.woodCounter = PhotoImage(file = "woodCounter.gif")
    drawScene(canvas)
    # this will set up the canvas at the beginning of each new game
    # it will have to draw the background and all the objects in the scene

def getNewRecipe(canvas):
    allRecipes = recipes.recipeList
    randomIndex = random.randint(0, len(allRecipes)-1) # shouldn't be random, should be progressively more difficult
    randomRecipe = allRecipes[randomIndex]
    if randomRecipe != canvas.recipeName:
        canvas.recipeName = randomRecipe

def find(canvas, anObject): # cup, would also work if moveBottle were enabled
    location = None
    (objLeft, objTop, objRight, objBottom) = anObject.bounds
    counterBounds= ("counter", canvas.counterBounds)
    cauldronBounds = ("cauldron", canvas.myCauldron.cauldronBounds)
    areaBounds = [  counterBounds, cauldronBounds]
    for area in areaBounds:
        (aLeft, aTop, aRight, aBottom) = area[1]
        if ((objLeft >= aLeft) and (objRight <= aRight)) and ((objTop >= aTop) and (objBottom <= aBottom)):
            location = area[0]
    anObject.location = location
    return location

def drawScene(canvas):
    canvas.create_image(canvas.width/2, canvas.height, image = canvas.backgroundImage, anchor = S)
    canvas.create_image(canvas.width, 0, image = canvas.ingredientsShelfImage, anchor = NE)
    canvas.create_image(canvas.width/4, 0, image = canvas.measuresShelfImage, anchor = NW)
    canvas.create_image((canvas.width*2)/5, canvas.height/2, image = canvas.personImage)
    canvas.create_image(0, ((canvas.height*3)/4 )+ (canvas.height/100), image = canvas.woodCounter, anchor = NW)
    drawIngredientsShelf(canvas)
    drawMeasuresShelf(canvas)
    drawCounter(canvas)
    drawRecipeBook(canvas)
    drawRecipe(canvas, canvas.recipeName)
    canvas.recipe.checkRecipe(canvas.myCauldron.inCauldron)
    canvas.myCauldron.drawCauldron()
    drawBottles(canvas)
    createMeasuringCups(canvas)
    drawMeasuringCups(canvas)
    

def redraw(canvas): # called after ingredient is put in cauldron
    drawMeasuresShelf(canvas)
    drawMeasuringCups(canvas)
    canvas.myCauldron.drawCauldron()
    canvas.myCauldron.drawCauldronLiquid()
    canvas.recipe.checkRecipe(canvas.myCauldron.inCauldron)
    drawBottles(canvas)
    drawCounter(canvas)
        
def drawIngredientsShelf(canvas):
    # draw background of shelf
    shelfColor = RGBtoHex(106, 45, 4)
    canvas.shelfColor = shelfColor
    left = (canvas.width*4)/5
    top = 4
    right = canvas.width
    bottom =  canvas.height
    canvas.ingredientsShelfBounds = (left, top, right, bottom)
    shelfLinesColor = RGBtoHex(150, 63, 5)
    canvas.shelfLinesColor = shelfLinesColor
    shelves = 3 #store in canvas later?
    shelfCoords = [ ]
    for shelf in xrange(shelves):
        left = (canvas.width*4)/5
        top = (canvas.height*shelf)/4 + 5 # 5 is for window border
        right = canvas.width
        bottom = top + (canvas.height)/4
        shelfWidth = canvas.width/100
        shelfCoords.append((left, right, top, bottom))
    canvas.ingredientsShelves = shelfCoords      
 
def drawMeasuresShelf(canvas):
    top = 35
    left = canvas.width/4 + 5 #relative to recipe book
    right = ((canvas.width*4)/5)  -20# relative to ingredients shelf
    bottom = top +(canvas.height/7) -5
    shelfWidth = canvas.width/100
    canvas.measuresShelf1 = (left, top, right, bottom)

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
    canvas.counterBounds = (left, top - (canvas.height/16), right, bottom)
    
def createMeasuringCups(canvas):
    oneCup = measures.MeasuringCup(canvas, "1")
    halfCup = measures.MeasuringCup(canvas, "1/2")
    thirdCup = measures.MeasuringCup(canvas, "1/3")
    quarterCup = measures.MeasuringCup(canvas, "1/4")
    sixthCup = measures.MeasuringCup(canvas, "1/6")
    currentCups = [oneCup, halfCup, thirdCup, quarterCup, sixthCup]
    
    if canvas.difficulty != -1:
        for index in xrange(min(2,canvas.difficulty)):
            currentCups.pop(index)

    random.shuffle(currentCups)
    canvas.currentCups = currentCups

def drawMeasuringCups(canvas):
    
    currentCups = canvas.currentCups
    for cupIndex in xrange(len(currentCups)):
        cup = currentCups[cupIndex]
        cup.placeCup(cupIndex)
    
    for cup in currentCups:
        cup.drawCup()
        cup.drawCupFill(None)
        

    
def drawBottles(canvas):
    allIngredients = [ ]
    pineSap = bottles.LiquidIngredients(canvas, "pine sap")
    allIngredients.append(pineSap)
    roseDew = bottles.LiquidIngredients(canvas, "rose dew")
    allIngredients.append(roseDew)
    lilyVenom = bottles.LiquidIngredients(canvas, "lily venom")
    allIngredients.append(lilyVenom)
    fluxweedJuice = bottles.LiquidIngredients(canvas, "fluxweed juice")
    allIngredients.append(fluxweedJuice)
    pamplemousse = bottles.LiquidIngredients(canvas, "pamplemousse")
    allIngredients.append(pamplemousse)
    armadilloBile = bottles.LiquidIngredients(canvas, "armadillo bile")
    allIngredients.append(armadilloBile)
    gillywater = bottles.LiquidIngredients(canvas, "gillywater")
    allIngredients.append(gillywater)
    leechJuice = bottles.LiquidIngredients(canvas, "leech juice")
    allIngredients.append(leechJuice)

    recipe = canvas.recipe
    recipeIngredients = recipe.ingredients

    currentBottles = [ ]
    otherIngredients = [ ]
    for Bottle in allIngredients:
        if Bottle.ingredientName in recipe.ingredients:
            currentBottles.append(Bottle)
        else:
            otherIngredients.append(Bottle)

    random.shuffle(otherIngredients)
    while len(currentBottles) != 6:
        currentBottles.append(otherIngredients[0])
        otherIngredients.pop(0)

    BottleCount = 0
    place = "left"
    for Bottle in currentBottles:
        Bottle.placeBottle(BottleCount/2, place)
        BottleCount +=1
        if place == "left": place = "right"
        else: place = "left"
        
    for Bottle in currentBottles:
        Bottle.drawBottle()

    canvas.currentBottles = currentBottles
    

def drawRecipe(canvas, potionName):
    recipe = recipes.Recipe(canvas, potionName)
    recipe.displayRecipe()
    canvas.recipe = recipe # store instance of recipe class in canvas


def RGBtoHex(red, green, blue):
    color = "#%02x%02x%02x" % (red, green, blue) # to hexadecimal string
    return color


def run():
    # create the root and the canvas
    root = Tk()
    canvasWidth = 1120
    canvasHeight = 814
    canvas = Canvas(root, width= canvasWidth, height = canvasHeight)
    canvas.pack(fill = BOTH, expand = YES) # this makes the canvas resizable
    root.resizable(width=FALSE, height=FALSE) # and this makes it not resizable
    # store canvas in root and canvas in itself for callbacks
    root.canvas = canvas.canvas = canvas
    # set up canvas data and call init
    canvas.data = Struct()
    canvas.width = canvasWidth
    canvas.height = canvasHeight
    canvas.difficulty = -1
    canvas.recipeName = None
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
