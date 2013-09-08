# bottles with classes

from Tkinter import *

ingredientContainers = {}
ingredientContainers["gillywater"] = {}
ingredientContainers["gillywater"]["bottleType"] = "stout"
ingredientContainers["gillywater"]["bottleColor"] = (0, 255, 0)
ingredientContainers["leech juice"] = {}
ingredientContainers["leech juice"]["bottleType"] = "stout"
ingredientContainers["leech juice"]["bottleColor"] = (255, 0, 0)
ingredientContainers["lily venom"] = {}
ingredientContainers["lily venom"]["bottleType"] = "stout"
ingredientContainers["lily venom"]["bottleColor"] = (255, 255, 0)
ingredientContainers["fluxweed juice"] ={}
ingredientContainers["fluxweed juice"]["bottleType"] = "stout"
ingredientContainers["fluxweed juice"]["bottleColor"] = (0, 0, 255)
ingredientContainers["pamplemousse"] ={}
ingredientContainers["pamplemousse"]["bottleType"] = "stout"
ingredientContainers["pamplemousse"]["bottleColor"] = (163, 73, 164)
ingredientContainers["armadillo bile"] ={}
ingredientContainers["armadillo bile"]["bottleType"] = "stout"
ingredientContainers["armadillo bile"]["bottleColor"] = (201, 235, 67)
ingredientContainers["pine sap"] = {}
ingredientContainers["pine sap"]["bottleType"] = "stout"
ingredientContainers["pine sap"]["bottleColor"] = (47, 47, 0)
ingredientContainers["rose dew"] = {}
ingredientContainers["rose dew"]["bottleType"] = "stout"
ingredientContainers["rose dew"]["bottleColor"] = (255, 174, 215)


class LiquidIngredients:
    # makeBottle becomes __init__:
    def __init__(self, canvas, ingredientName): # bottleType is the shape of the bottle
        self.canvas = canvas
        self.type = "Liquid Ingredient"
        self.ingredientName = ingredientName
        self.bottleType = ingredientContainers[ingredientName]["bottleType"]
        bottleColor = ingredientContainers[ingredientName]["bottleColor"]
        self.bottleColor = RGBtoHex(bottleColor[0], bottleColor[1], bottleColor[2])
        self.isMoving = False
        self.info = self.ingredientName
        self.location = "ingredients shelf"
        # doesn't belong here
        canvas.ingredientContainers = ingredientContainers

    def placeBottle(self, shelfNumber, shelfSide):
        canvas = self.canvas
        bottleWidth = canvas.width/12
        bottleHeight = canvas.height/7
        border = canvas.width/80
        # adjust coordinates for shelf location (have factors in calculations?)*
        left = (canvas.width*13)/16
        if shelfSide == "right":
            left += bottleWidth + border
        top = ((canvas.height/8) - border)+(shelfNumber*(canvas.height/4))
        right = left + bottleWidth
        bottom = top + bottleHeight
        (self.left, self.top, self.right, self.bottom)=(left, top, right, bottom) 
        self.bounds = (left, top, right, bottom)

    def drawBottle(self): 
        canvas = self.canvas
        bottleType = self.bottleType
        bottleColor = self.bottleColor
        x0 = self.left
        y0 = self.top
        x1 = self.right
        y1 = self.bottom
        corkColor = RGBtoHex(190, 145, 82)
        if bottleType == "stout":
            bottleWidth = x1 - x0
            bottleHeight = y1 - y0
            self.bottleWidth, self.bottleHeight = bottleWidth, bottleHeight
            # cork
            left = x0 + bottleWidth/8
            top = y0
            right = x1 - bottleWidth/8
            bottom = y0 + bottleWidth/12
            self.bottleCork = canvas.create_rectangle(left, top, right, bottom, fill =corkColor)
            # top part
            left = x0 + bottleWidth/12
            top = bottom
            right = x1 - bottleWidth/12
            bottom = y0 + bottleWidth/6
            self.bottleTop = canvas.create_rectangle(left, top, right, bottom, fill = bottleColor)
            # main part of bottle
            left = x0
            top = bottom
            right = x1
            bottom = y1
            self.bottleMain = canvas.create_rectangle(left, top, right, bottom, fill = bottleColor)
        # insert elifs and adjust dimensions to change appearance of bottle

        # label
        centerX = (left + right)/2
        centerY = (top + bottom)/2
        scaledFontSize =  canvas.height*canvas.width/(300**2) 
        fontStyle = ("Times New Roman", scaledFontSize, "bold")
        labelText = self.ingredientName
        self.bottleLabel = canvas.create_text(centerX, centerY, text = labelText, font = fontStyle)


    def moveBottle(self, x, y): # * FIX THIS
        canvas = self.canvas
        bottleType = self.bottleType
        canvas.isBottleMoving = True
        newCoords = [ ]
        bottleWidth = self.bottleWidth
        bottleHeight = self.bottleHeight
        left = x - (bottleWidth/2)
        top = y - (bottleHeight/2)
        right = x + (bottleWidth/2)
        bottom = y + (bottleHeight/2)
        (x0, y0, x1, y1) = (left, top, right, bottom)
        (self.left, self.top, self.right, self.bottom) = (left, top, right, bottom) # update values for coordinates of bottle
        self.bounds = (left, top, right, bottom) # update values for bounds of bottle
        if bottleType == "stout":
            # top part
            left = x0 + bottleWidth/12
            top = bottom
            right = x1 - bottleWidth/12
            bottom = y0 + bottleWidth/6
            newCoords.append((left, top, right, bottom))
            # main part of bottle
            left = x0 
            top = bottom
            right = x1
            bottom = y1
            newCoords.append((left, top, right, bottom))
            # label
            centerX = (left + right)/2
            centerY = (top + bottom)/2
            newCoords.append((centerX, centerY))
        bottleTop = self.bottleTop
        bottleMain = self.bottleMain
        bottleLabel = self.bottleLabel
        bottleCork = self.bottleTop
        canvas.coords(bottleTop, newCoords[0])
        canvas.coords(bottleMain, newCoords[1])
        canvas.coords(bottleLabel, newCoords[2])
        canvas.delete(bottleCork)
        self.hasBeenMoved = True
        
        
    
        # this should change the coordinates of the bottle (all component parts as described above)
        # it should also check to see if moving the bottle is legal
        
    
def RGBtoHex(red, green, blue):
    color = "#%02x%02x%02x" % (red, green, blue) # to hexadecimal string
    return color
