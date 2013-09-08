# scene

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
        canvas.measuresShelf = (left, top, right, bottom)
        shelfWidth = canvas.width/100
        canvas.create_rectangle(left, top, right, bottom, fill = None, width = shelfWidth)

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
    canvas.create_rectangle(left, top, right, bottom, fill = counterColor)

def drawCauldron(canvas):
    cauldronColor = RGBtoHex(34, 35, 24)
    # outer oval
    left = canvas.width/5
    top = (canvas.height*3)/5
    right = left + canvas.width/4
    bottom = top + canvas.height/3
    canvas.create_oval(left, top, right, bottom, fill = cauldronColor)
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
    
def drawMeasuringCups(canvas):
    oneCup = measures.MeasuringCup(canvas, "1")
    halfCup = measures.MeasuringCup(canvas, "1/2")
    thirdCup = measures.MeasuringCup(canvas, "1/3")
    quarterCup = measures.MeasuringCup(canvas, "1/4")
    canvas.currentCups = [oneCup, halfCup, thirdCup, quarterCup]
    
# * should be if canvas.thingsMoved == False:
    oneCup.placeCup(0)
    halfCup.placeCup(1)
    thirdCup.placeCup(2)
    quarterCup.placeCup(3)
    
    oneCup.drawCup(canvas)   
    halfCup.drawCup(canvas)
    thirdCup.drawCup(canvas)
    quarterCup.drawCup(canvas)

    
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
