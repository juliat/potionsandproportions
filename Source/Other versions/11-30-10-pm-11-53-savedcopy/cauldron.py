# cauldron

class Cauldron():
    def __init__(self, canvas):
        canvas = self.canvas
    def drawCauldron(self):
        canvas = self.canvas
        cauldronColor = RGBtoHex(34, 35, 24)
        # outer oval
        left = canvas.width/13
        top = (canvas.height*3)/5
        right = left + canvas.width/4
        bottom = top + canvas.height/3
        canvas.create_oval(left, top, right, bottom, fill = cauldronColor)
        canvas.cauldronBounds = (left, top - (canvas.height/12), (right + (canvas.height/20)), bottom) # adding space cushions to accept input near cauldron
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

    def drawCauldronLiquid(canvas, ingredientColor): # ingredient color is currently an RGB
        rimBounds = canvas.cauldronRimBounds
        border = (rimBounds[2] - rimBounds[0])/12
        left = rimBounds[0] + border
        top = rimBounds[1] + 1.6*border
        right = rimBounds[2] - border
        bottom = rimBounds[3]
        cupSize = canvas.mCupSize
        if canvas.potionColor == None:
            potionColor = (ingredientColor[0], ingredientColor[1], ingredientColor[2])
            canvas.potionColor= potionColor
            potionColor = RGBtoHex(ingredientColor[0], ingredientColor[1], ingredientColor[2])
        else:
            (oldR, oldG, oldB) = canvas.potionColor[0], canvas.potionColor[1], canvas.potionColor[2]
            (addR, addG, addB) = ingredientColor
            (newR, newG, newB) = ((oldR+addR)/2, (oldG+addG)/2, (oldB+addB)/2)
            canvas.potionColor = (newR, newG, newB)
            potionColor =  RGBtoHex(newR, newG, newB)
        canvas.create_oval(left, top, right, bottom, fill = potionColor, width = 0)
