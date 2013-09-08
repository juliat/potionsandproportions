# recipes

class Recipe:
    def __init__(self, canvas, potionName):
        self.canvas = canvas
        self.potionName = potionName
        canvas.potionName = potionName
        self.complete = False # initially, recipe has not been completed.
        self.readableSteps = recipes[potionName]["steps"]
        self.ingredients = recipes[potionName]["ingredients amounts"].keys()
        self.ingredientsAmounts = recipes[potionName]["ingredients amounts"]


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
        # display actual recipe
        scaledFontSize = pageHeight*pageWidth/(85**2)
        fontStyle = ("Times New Roman", scaledFontSize)
        canvas.create_text((pageCenterX), (pageCenterY), text = self.readableSteps, font = fontStyle)


    def checkRecipe(self, inCauldron):
        canvas = self.canvas
        progressMessage = "Hello there!"
        allCorrect = False
        ingredient = canvas.myCauldron.currentIngredient
        potionName = self.potionName
        correctAmounts = recipes[potionName]["ingredients amounts"]
        if (ingredient == None):
            progressMessage =  " Try putting a cup on the counter, \n then click to fill the cup with \n an ingredient from the shelf."
            if (canvas.cupOnCounter != None):
                progressMessage = " Once you've filled the cup \n with an ingredient, try pouring \n what's in the cup into the cauldron."
        else:
            cauldronAmount =inCauldron.get(ingredient)
            correctAmount = correctAmounts.get(ingredient)

            if ingredient not in correctAmounts.keys():
                progressMessage = "\t\tUh oh. \n Is that really the right ingredient?\n  Try pressing \"u\" to undo."
##                print progressMessage
                
            elif  cauldronAmount== correctAmount:
                
                progressMessage= "\t\tGood! \n That's enough of that ingredient."
##                print progressMessage
                 
            elif cauldronAmount > correctAmount:
                progressMessage = "Uh oh... That's too much.\n Try pressing \"u\" to fix it."
##                print progressMessage
                 
            elif cauldronAmount < correctAmount:
                progressMessage = "Keep going, the recipe \n calls for more of that."
##                print progressMessage

        
        for ingr in correctAmounts:
            cauldronAmount =inCauldron.get(ingr)
            correctAmount = correctAmounts.get(ingr)
##            print "perfect?"
##            print ingr, "in cauldron", inCauldron.get(ingr), "recipe needs", correctAmounts.get(ingr)
            if cauldronAmount == correctAmount:
                allCorrect = True
            else:
                allCorrect = False
                
        if allCorrect == True:
            progressMessage = "Perfect! It's done! \n Press \"n\" to get a new recipe."
##            print progressMessage
            canvas.difficulty +=1
                 
             
                    
    

        # and display progress  
        # draw "paper"/speech bubble
        left = (canvas.width/2)
        top = canvas.height/3
        right = left + (canvas.width/4)
        bottom = top + (canvas.height/6)
        canvas.create_rectangle(left, top, right, bottom, fill = RGBtoHex(251, 242, 221))
        centerX = (left + right)/2
        centerY = (top + bottom)/2
        scaledFontSize =  canvas.height/60
        fontStyle = ("Times New Roman", scaledFontSize, "bold")
        canvas.create_text(centerX, centerY, text = progressMessage, font = fontStyle)


def RGBtoHex(red, green, blue):
    color = "#%02x%02x%02x" % (red, green, blue) # to hexadecimal string
    return color

    #defines a dictionary of possible recipes to be displayed, keys are recipe names
recipes = {}
recipes["Good Luck Potion"] = {}
recipes["Good Luck Potion"] ["steps"] = \
              "1. Add 1 cup of gillywater. \n 2. Add 1/2 cup leech juice. \n 3. Add 1/3 cup of lily venom."
recipes["Good Luck Potion"]["ingredients"] = ['gillywater', 'leech juice', 'lily venom']
recipes["Good Luck Potion"]["ingredients amounts"]=\
dict([("gillywater",1.0), ("leech juice", (1/2.0)), ("lily venom", (1/3.0))]) # amount of ingredient to be added


recipes["Confusing Concoction"] = {}
recipes["Confusing Concoction"]["steps"]="1. Add 1 cup of pine sap. \n 2. Add 1 1/2 cups of rose dew."
recipes["Confusing Concoction"]["ingredients"] = ['pine sap', 'rose dew']
recipes["Confusing Concoction"]["ingredients amounts"] = {'pine sap':1.0, 'rose dew':1.5}


recipes["Slug Repellent"] = {}
recipes["Slug Repellent"]["steps"] =\
              "1.  Add 1 cup pamplemousse. \n 2. Add 1/3 cup fluxweed juice. \n 3. Add 1/4 cup leech juice. \n \
4. Add 1/4 cup armadillo bile. \n 5. Add 1/3 cup lily venom."
recipes["Slug Repellent"]["ingredients amounts"] ={'pamplemousse':1.0, 'fluxweed juice':(1/3.0), 'leech juice':(1/4.0),'armadillo bile':(1/4.0), 'lily venom':(1/3.0)}
recipes["Slug Repellent"]["ingredients"] = ['pamplemousse', 'fluxweed juice', 'armadillo bile', 'lily venom', ' leech juice']


recipes["Aging Potion"] = {}
recipes["Aging Potion"]["steps"] = \
                "1. Add 1 cup lily venom. \n 2. Add 1 cup armadillo bile. \n 3. Add 1/3 cup leech juice. \n 4. Add 1/4 cup pamplemousse."
recipes["Aging Potion"]["ingredients amounts"] = {'lily venom':1.0, 'armadillo bile':1.0, 'leech juice':(1/3.0), 'pamplemousse':(1/4.0)}

recipes["Dizziness Draught"] = {}
# no one cup measure for this recipe
recipes["Dizziness Draught"]["steps"] =\
                   "1. Add 1/3 cup gillywater. \n 2. Add 1 cup fluxweed juice."
recipes["Dizziness Draught"]["ingredients amounts"] = {'gillywater':(1/3.0), 'fluxweed juice': (1/2.0)}


recipes["Purple Fire Potion"] = {}
# this potion only uses the 1 cup measure
recipes["Purple Fire Potion"]["steps"] =\
                 "This potion only makes \n a little Purple Fire Potion, \n but we want to make a lot\n so we can have a big \n purple bonfire. \
To make more, \n multiply everything by three. \n \n 1. Add 2 cups pamplemousse. \n 2. \
Add 1 cup lily venom. \n 3. Add 1/2 cup rose dew. \n 4. Add 1/2 cup fluxweed juice"
recipes["Purple Fire Potion"]["ingredients amounts"] = {'pamplemousse': 6.0, 'lily venom': 3.0, 'rose dew':(3/2.0), 'fluxweed juice':(3/2.0)}

recipeList = recipes.keys()

