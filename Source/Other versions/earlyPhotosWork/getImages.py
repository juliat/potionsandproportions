# proportion potions
# this module will draw the background for the game, eventually
# getting images

from Tkinter import *


def getPhotos(canvas):
    canvas.create_rectangle(0, 0, canvas.width, canvas.height, fill="black")
    # Draw a background rectangle to highlight the transparency
    # of the images
    backgroundImage = PhotoImage(file = "apothecaryBackground.gif")
    backgroundImage = backgroundImage.zoom(2,2)
    canvas.create_image(canvas.width/2, canvas.height/2, image = backgroundImage)
    canvas.data["backgroundImage"] = backgroundImage

    # ingredients shelf
    ingredientsShelfImage = PhotoImage(file = "ingredientsShelf.gif")
    canvas.create_image(canvas.width, canvas.height/2.5, image = ingredientsShelfImage)
    canvas.data["ingredientsShelfImage"]= ingredientsShelfImage

    # wood Counter
    woodCounterImage = PhotoImage(file ="woodCounter.gif")
    woodCounterImage = woodCounterImage.zoom(2, 1) #stretch horizontally
    woodCounterImage = woodCounterImage.subsample(1,2) #shrink vertically
    #canvas.create_image(canvas.width/2, canvas.height, anchor=S, image=woodCounterImage) # coordinates give upper left corner
    woodCounter = canvas.create_image(canvas.width, canvas.height, anchor=SE, image=woodCounterImage)
    canvas.data["woodCounterImage"] = woodCounterImage

    #test bottole
    bottleImage = PhotoImage(file= "blue potion bottle.gif")
    bottle = canvas.create_image(canvas.width, canvas.height, anchor = NW, image = bottleImage)
    canvas.data["bottleImage"] = bottleImage



def init(canvas):
    canvas.width = canvas.winfo_reqwidth()-4
    canvas.height = canvas.winfo_reqheight()-4
    getPhotos(canvas)

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    canvas = Canvas(root, width=1000, height=800)
    canvas.pack(fill=BOTH, expand=YES)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    init(canvas)
    # set up events
    # root.bind("<Button-1>", leftMousePressed)
    # root.bind("<KeyPress>", keyPressed)
    # timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()

