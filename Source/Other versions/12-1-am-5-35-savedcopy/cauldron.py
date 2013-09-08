# cauldron

class Cauldron():
    def __init__(self, canvas):
        self.canvas = canvas
        self.inCauldron = { }
        self.potionColor = None
        
    def drawCauldron(self):
        canvas = self.canvas
        cauldronColor = RGBtoHex(34, 35, 24)
        # outer oval
        left = canvas.width/13
        top = (canvas.height*3)/5
        right = left + canvas.width/4
        bottom = top + canvas.height/3
        canvas.create_oval(left, top, right, bottom, fill = cauldronColor)
        self.cauldronBounds = (left, top - (canvas.height/12), (right + (canvas.height/20)), bottom) # adding space cushions to accept input near cauldron
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
        self.cauldronRimBounds = (left, top, right, bottom)

    def drawCauldronLiquid(self, ingredientColor=None): # ingredient color is currently an RGB
        if ingredientColor == None:
            ingredientColor = self.potionColor
        canvas = self.canvas
        rimBounds = self.cauldronRimBounds
        border = (rimBounds[2] - rimBounds[0])/12
        left = rimBounds[0] + border
        top = rimBounds[1] + 1.6*border
        right = rimBounds[2] - border
        bottom = rimBounds[3]
        if self.potionColor == None:
            potionColor = (ingredientColor[0], ingredientColor[1], ingredientColor[2])
            self.potionColor= potionColor
            potionColor = RGBtoHex(ingredientColor[0], ingredientColor[1], ingredientColor[2])
        else:
            (oldR, oldG, oldB) = self.potionColor[0], self.potionColor[1], self.potionColor[2]
            (addR, addG, addB) = ingredientColor
            (newR, newG, newB) = ((oldR+addR)/2, (oldG+addG)/2, (oldB+addB)/2)
            self.potionColor = (newR, newG, newB)
            potionColor =  RGBtoHex(newR, newG, newB)
        canvas.create_oval(left, top, right, bottom, fill = potionColor, width = 0)

    def addToCauldron(self, ingredient, amount): # cup.filledWith and cup.floatSize
    # assuming only measuring cups are implemented
        inCauldron = self.inCauldron
        if inCauldron.get(ingredient)== None:
            inCauldron[ingredient]  = amount
        else: inCauldron[ingredient] += amount
        inCauldron = self.inCauldron
    

def RGBtoHex(red, green, blue):
    color = "#%02x%02x%02x" % (red, green, blue) # to hexadecimal string
    return color
