# recipes

class Recipe:
    def __init__(self, canvas, potionName):
        self.canvas = canvas
        self.potionName = potionName

    def displayRecipe(self):
        canvas = self.canvas
        potionName = self.potionName
        pageBounds = canvas.pageBounds # left, top, right, bottom
        pageWidth = pageBounds[2] - pageBounds[0]
        pageHeight = pageBounds[3] - pageBounds[1]
        pageCenterX = pageBounds[0] + pageWidth/2
        pageCenterY = pageBounds[1] + pageHeight/2
        scaledFontSize =  pageHeight*pageWidth/(65**2) # should be based on how many lines
        fontStyle = ("Times New Roman", scaledFontSize, "bold")
        # display recipe title
        canvas.create_text(pageCenterX, pageBounds[1]+ scaledFontSize, text = potionName, font= fontStyle)
        # display actual recipe retreived from dictionary
        steps = recipes["Good Luck Potion"]["steps"]
        scaledFontSize = pageHeight*pageWidth/(80**2)
        fontStyle = ("Times New Roman", scaledFontSize)
        canvas.create_text(pageCenterX, pageCenterY, text = steps, font = fontStyle)

    def checkRecipe(self):
        canvas = self.canvas
        addedToCauldron = canvas.addedToCauldron

#defines a dictionary of possible recipes to be displayed
recipes = {}
recipes["Good Luck Potion"] = {}
recipes["Good Luck Potion"] ["steps"] = " 1. Add 1 cup of gillywater. \n 2. Add 1/2 cup leech juice."
recipes["Good Luck Potion"]["step1"] = False # True if completed
recipes["Good Luck Potion"]["step2"] = False
recipes["Good Luck Potion"]["steps checklist"] = None # should be list of stuff that will appear in
                                                                                                                    # addedToCauldron list if steps of recipe are done

        
        
        
        
