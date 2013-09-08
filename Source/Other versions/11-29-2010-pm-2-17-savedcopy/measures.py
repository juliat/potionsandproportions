# measures

class MeasuringCup:
    def __init__(self, canvas, size): # size should be a proportion of a cup: 1/2, 1/4, 1/5, 1
        self.canvas = canvas
        self.type = "Measuring Cup"
        self.size = size
        self.onShelf = True # default, when it's on counter, can be filled, when over cauldron, can pour
        self.onCounter = False
        self.isMoving = False
        self.isFull = False
        self.info = [self.type, self.size]
        self.location = "top measures shelf"

    def placeCup(self, shelfPlace):
        # this function also sizes the cups based on how they're placed on the shelf-- assumes they're in order from largest to smallest
        canvas= self.canvas
        shelfBounds = canvas.measuresShelf1
        border = canvas.width/80
        left = shelfBounds[0] + border
        top = shelfBounds[1] + border
        right = left + canvas.width/10
        bottom = shelfBounds[3] - 5
        placeWidth = right - left + border
        left += (shelfPlace*placeWidth)
        right += (shelfPlace*placeWidth)
        top += border*shelfPlace
        cupBounds = (left, top, right, bottom)
        self.bounds = cupBounds

    def drawCup(self, canvas):
        cupBounds = self.bounds
        (x0, y0, x1, y1) = cupBounds
        cupWidth = x1 - x0
        cupHeight = y1 - y0
        self.cupWidth, self.cupHeight = cupWidth, cupHeight
        # draw round base
        left = x0
        top = y0 + ((cupHeight*3)/5)
        right = x0 + ((cupWidth*2)/3)
        bottom = y1
        baseOvalHeight = bottom - top
        cupColor =RGBtoHex(219, 219, 219)
        self.cupBase = canvas.create_oval(left, top, right, bottom, fill = cupColor , width = 0)
        # middle rectangle
        top = y0 + (cupHeight/3)
        bottom = bottom - (cupHeight/7)
        self.middleRectangle = canvas.create_rectangle(left, top, right, bottom, fill = cupColor, width = 0)
        # label
        scaledFontSize =  canvas.height*canvas.width/(300**2) 
        fontStyle = ("Times New Roman", scaledFontSize, "bold")
        label = self.size + " cup"
        centerX = (right + left)/2
        centerY = (bottom + top)/2 + scaledFontSize
        self.cupLabel = canvas.create_text(centerX, centerY, text = label, font = fontStyle)
        # top rim
        top = top -  (cupHeight/4)
        bottom = top + baseOvalHeight
        self.cupRim= canvas.create_oval(left, top, right, bottom, fill = cupColor)
        self.rimBounds = (left, top, right, bottom)
        # handle
        left = right
        top = top + (baseOvalHeight/2)
        right = x1
        self.cupHandle = canvas.create_rectangle(left, top, right, bottom, fill = cupColor)

    def drawCupFill(self, fill=None):
        canvas = self.canvas
        rimBounds =  self.rimBounds
        left = rimBounds[0]
        top = rimBounds[1] + ((rimBounds[3]-rimBounds[1])/3)
        right = rimBounds[2]
        bottom = rimBounds[3]
        fillWidth = 0
        if (self.isFull == True):
            fillWidth = 1
        self.cupFill = canvas.create_oval(left, top, right, bottom, fill = fill, width = fillWidth)
        
    def moveCup(self, x, y):
        canvas = self.canvas
        newCoords = [ ]
        cupWidth, cupHeight = self.cupWidth, self.cupHeight
        x0 = x - (cupWidth/2)
        y0 = y - (cupHeight/2)
        x1 = x + (cupWidth/2)
        y1 = y + (cupHeight/2)
        self.bounds = (x0, y0, x1, y1)
        # draw round base
        left = x0
        top = y0 + ((cupHeight*3)/5)
        right = x0 + ((cupWidth*2)/3)
        bottom = y1
        newCoords.append((left, top, right, bottom))
        baseOvalHeight = bottom - top
        # middle rectangle
        top = y0 + (cupHeight/3)
        bottom = bottom - (cupHeight/7)
        newCoords.append((left, top, right, bottom))
        # label
        scaledFontSize =  canvas.height*canvas.width/(300**2) 
        centerX = (right + left)/2
        centerY = (bottom + top)/2 + scaledFontSize
        newCoords.append((centerX, centerY))
        # top rim
        top = top -  (cupHeight/4)
        bottom = top + baseOvalHeight
        rimBounds = (left, top, right, bottom)
        self.rimBounds =  (left, top, right, bottom)
        newCoords.append((left, top, right, bottom))
        # handle
        left = right
        top = top + (baseOvalHeight/2)
        right = x1
        newCoords.append((left, top, right, bottom))
        # fill
        left = rimBounds[0]
        top = rimBounds[1] + ((rimBounds[3]-rimBounds[1])/3)
        right = rimBounds[2]
        bottom = rimBounds[3]
        newCoords.append((left, top, right, bottom))
        
        canvas = self.canvas
        cupBase = self.cupBase
        middleRectangle = self.middleRectangle
        cupLabel = self.cupLabel
        cupRim = self.cupRim
        cupHandle = self.cupHandle
        cupFill = self.cupFill
        canvas.coords(cupBase, newCoords[0])
        canvas.coords(middleRectangle, newCoords[1])
        canvas.coords(cupLabel, newCoords[2])
        canvas.coords(cupRim, newCoords[3])
        canvas.coords(cupHandle, newCoords[4])
        canvas.coords(cupFill, newCoords[5])

##    class MeasuringSpoon: 
##        def __init__(self, canvas, size): #
##            self.canvas = canvas
##            self.type = "Measuring Spoon"
##            self.size = size
##            self.onShelf = True # default, when it's on counter, can be filled, when over cauldron, can pour
##            self.isMoving = False
##            self.isFull = False
##            self.info = [self.type, self.size]




def RGBtoHex(red, green, blue):
    color = "#%02x%02x%02x" % (red, green, blue) # to hexadecimal string
    return color
        
