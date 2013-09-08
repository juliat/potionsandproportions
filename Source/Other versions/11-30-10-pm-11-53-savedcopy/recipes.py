# recipes

class Recipe:
    def __init__(self, canvas, potionName):
        self.canvas = canvas
        self.potionName = potionName
        canvas.potionName = potionName
        self.complete = False # initially, recipe has not been completed.
        self.progressMessage =  " Try putting a cup on the counter, \n then click to fill the cup with \n an ingredient from the shelf."


    def displayRecipe(self):
        canvas = self.canvas
        potionName = self.potionName
        pageBounds = canvas.pageBounds # left, top, right, bottom
        pageWidth = pageBounds[2] - pageBounds[0]
        pageHeight = pageBounds[3] - pageBounds[1]
        pageCenterX = pageBounds[0] + pageWidth/2
        pageCenterY = pageBounds[1] + pageHeight/2
        scaledFontSize =  pageHeight*pageWidth/(70**2) # should be based on how many lines
        fontStyle = ("Times New Roman", scaledFontSize, "bold")
        # display recipe title
        canvas.create_text(pageCenterX, pageBounds[1]+ scaledFontSize, text = potionName, font= fontStyle)
        # display actual recipe retreived from dictionary
        steps = recipes[self.potionName]["steps"]
        scaledFontSize = pageHeight*pageWidth/(85**2)
        fontStyle = ("Times New Roman", scaledFontSize)
        canvas.create_text((pageCenterX), (pageCenterY), text = steps, font = fontStyle)


    def checkRecipe(self, canvas, addedToCauldron):
        progressMessage = None
        potionName = self.potionName
        recipe = recipes[potionName]["steps checklist"]
        if addedToCauldron != [ ]:
            movesMadeCount = len(addedToCauldron)-1
            if movesMadeCount >= len(recipe):
                progressMessage ="Uh oh... That doesn't look right.\n Try pressing \"r\" to start over."
            else:
                mostRecentUserMove = addedToCauldron[movesMadeCount]
                if mostRecentUserMove == recipe[movesMadeCount]:
                    progressMessage= "Good! You're on the right track."
                else:
                    progressMessage = "Are you sure that  you're \n following the recipe? " # should be refined based on what they did wrong, wrong cup, wrong ingredient, possible "antidote" 
                if  addedToCauldron == recipe:
                    self.complete = True
                    progressMessage ="Perfect! It's done! \n Press \"n\" to get a new recipe."
        elif (canvas.cupOnCounter != None):
            progressMessage = " Once you've filled the cup \n with an ingredient, try pouring \n what's in the cup into the cauldron."
        if progressMessage != None:
            self.progressMessage = progressMessage

    def displayProgress(self, canvas):
        # draw "paper"/speech bubble
        left = (canvas.width/2)
        top = canvas.height/3
        right = left + (canvas.width/4)
        bottom = top + (canvas.height/5)
        canvas.create_rectangle(left, top, right, bottom, fill = RGBtoHex(251, 242, 221))
        centerX = (left + right)/2
        centerY = (top + bottom)/2
        scaledFontSize =  canvas.height/60
        fontStyle = ("Times New Roman", scaledFontSize, "bold")
        canvas.create_text(centerX, centerY, text = self.progressMessage, font = fontStyle)


def RGBtoHex(red, green, blue):
    color = "#%02x%02x%02x" % (red, green, blue) # to hexadecimal string
    return color

    #defines a dictionary of possible recipes to be displayed, keys are recipe names
recipes = {}
recipes["Good Luck Potion"] = {}
recipes["Good Luck Potion"] ["steps"] = \
              "1. Add 1 cup of gillywater. \n 2. Add 1/2 cup leech juice. \n 3. Add 1/3 cup of lily venom."
recipes["Good Luck Potion"]["steps checklist"] = [['Measuring Cup', '1', 'gillywater'],\
                                                  ['Measuring Cup', '1/2', 'leech juice'],['Measuring Cup', '1/3', 'lily venom']]
recipes["Good Luck Potion"]["ingredients"] = ['gillywater', 'leech juice', 'lily venom']

recipes["Confusing Concoction"] = {}
recipes["Confusing Concoction"]["steps"]="1. Add 1 cup of pine sap. \n 2. Add 1 1/2 cups of rose dew."
recipes["Confusing Concoction"]["steps checklist"] = [['Measuring Cup', '1', 'pine sap'], \
                                                      ['Measuring Cup', '1/2', 'rose dew'], \
                                                      ['Measuring Cup', '1/2', 'rose dew'], \
                                                      ['Measuring Cup', '1/2', 'rose dew']]
recipes["Confusing Concoction"]["ingredients"] = ['pine sap', 'rose dew']


recipes["Slug Repellent"] = {}
recipes["Slug Repellent"]["steps"] =\
              "1.  Add 1 cup pamplemousse. \n 2. Add 1/3 cup fluxweed juice. \n 3. Add 1/4 cup pamplemousse. \n \
4. Add 1/4 cup armadillo bile. \n 5. Add 1/3 cup lily venom."
recipes["Slug Repellent"]["steps checklist"] = [['Measuring Cup', '1', 'pamplemousse'], \
                                                ['Measuring Cup', '1/3', 'fluxweed juice'], \
                                                ['Measuring Cup', '1/4', 'armadillo bile'], \
                                                ['Measuring Cup', '1/3', 'lily venom']]
recipes["Slug Repellent"]["ingredients"] = ['pamplemousse', 'fluxweed juice', 'armadillo bile', 'lily venom']


recipes["Ageing Potion"] = {}
recipes["Ageing Potion"]["steps"] = \
                "1. Add 1 cup lily venom. \n 2. Add 1 cup armadillo bile. \n 3. Add 1/3 cup leech juice. \n 4. Add 1/4 cup pamplemousse."
recipes["Ageing Potion"]["steps checklist"]=[['Measuring Cup', '1', 'lily venom'], \
                                            ['Measuring Cup', '1', 'armadillo bile'],\
                                            ['Measuring Cup', '1/3', 'leech juice'], \
                                            ['Measuring Cup', '1/4', 'pamplemousse']]

recipes["Dizziness Draught"] = {}
# no one cup measure for this recipe
recipes["Dizziness Draught"]["steps"] =\
                   "1. Add 1/3 cup gillywater. \n 2. Add 1 cup fluxweed juice."
recipes["Dizziness Draught"]["steps checklist"] = [['Measuring Cup', '1/3', 'gillywater'], \
                                                   ['Measuring Cup', '1/2', 'fluxweed juice'], \
                                                   ['Measuring Cup', '1/2', 'fluxweed juice']]


recipes["Purple Fire Potion"] = {}
# this potion only uses the 1 cup measure
recipes["Purple Fire Potion"]["steps"] =\
                 "This potion only makes \n a little Purple Fire Potion, \n but we want to make a lot\n \
\n \n so we can have a big \n purple bonfire. To make more, \n multiply everything by 3.  \
1. Add 2 cups pamplemousse. \n 2, Add 1 cup lily venom. \n 3. Add 1/2 cup rose dew. \n 4. Add 1/2 cup fluxweed juice"
recipes["Purple Fire Potion"]["steps checklist"] = [['Measuring Cup', '1', 'pamplemousse'], \
                                                    ['Measuring Cup', '1', 'pamplemousse'], \
                                                    ['Measuring Cup', '1', 'pamplemousse'], \
                                                    ['Measuring Cup', '1', 'pamplemousse'], \
                                                    ['Measuring Cup', '1', 'pamplemousse'], \
                                                    ['Measuring Cup', '1', 'pamplemousse'], \
                                                    ['Measuring Cup', '1', 'lily venom'], \
                                                    ['Measuring Cup', '1', 'lily venom'], \
                                                    ['Measuring Cup', '1', 'rose dew'], \
                                                    ['Measuring Cup', '1', 'fluxweed juice']]


        
recipeList = recipes.keys()
        
