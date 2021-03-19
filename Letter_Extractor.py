# The end goal is for it to show you a letter and you select some examples of it on the page.
# Then those are added to a folder with other training material for the eventual neural net

from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from PIL import Image, ImageTk
from tkinter import *  

## Turns PDF into image to display
images = convert_from_path('Source.pdf',poppler_path = r"C:\Users\brian\Documents\GitHub\PDF_Text_Extractor\poppler-21.02.0\Library\bin", first_page=1, last_page=2, fmt='JPEG')
#images = convert_from_bytes(open('Source.pdf', 'rb').read())

img = images[1]
img = img.resize((int(img.width/2),int(img.height/2)))
zoom_img = None
zoom = False
#img.show()

## Creates a Tkinter instance where you can choose the corners of the letter
root = Tk()      
canvas = Canvas(root, width = 950, height = 800)      
canvas.pack()
tkimg = ImageTk.PhotoImage(img)
canv_img = canvas.create_image(0,0, anchor=NW, image=tkimg) #if you want to edit the image offset you need to add something later when you crop the image. 

# Determine the origin by clicking
def first_corner(eventorigin):
    global x0,y0, first_marker
    x0 = eventorigin.x
    y0 = eventorigin.y
    print(x0,y0)
    first_marker = canvas.create_oval(x0, y0, x0+2, y0+2)
    root.bind("<Button 1>",second_corner)

# Determine the origin by clicking
def second_corner(eventorigin):
    global x1,y1,selection_box
    x1 = eventorigin.x
    y1 = eventorigin.y
    print("second", x1,y1)
    selection_box = canvas.create_rectangle(x0, y0, x1, y1,fill='')
    root.bind("<Button 1>",cut_image)

#Cuts the selected section of the image
def cut_image(eventorigin): #remove eventorigin if you want to call the funct directly
    if(x0 < x1):
        left = x0
        right = x1
    else:
        left = x1
        right = x0

    if(y0<y1):
        upper = y0
        lower = y1
    else:
        upper = y1
        lower = y0

        
    if zoom:
        section = zoom_img.crop((left, upper, right, lower))
    else:
        section = img.crop((left, upper, right, lower)) #Should add something for if they click outside the image but inside the window
    section.show()

    root.bind("<Button 1>",first_corner)

def clear_selection(eventorigin = None):
    try:
        canvas.delete(first_marker)
        canvas.delete(selection_box)
    except:
        print("Nothing to clear")
    root.bind("<Button 1>",first_corner)

def zoom_in(eventorigin):
    global tkimg, canv_img, zoom, zoom_img
    x_click = eventorigin.x
    y_click = eventorigin.y
    x_offset = int(canvas['width'])/2 - x_click*2
    y_offset = int(canvas['height'])/2 - y_click*2
    print("called", x_click, y_click)
    zoom_img = img.resize((int(img.width*2),int(img.height*2)))
    zoom_img = zoom_img.crop((-x_offset, -y_offset, -x_offset + img.width, -y_offset + img.height))
    tkimg = ImageTk.PhotoImage(zoom_img)
    canvas.delete(canv_img)
    canv_img = canvas.create_image(0,0, anchor=NW, image=tkimg)
    root.bind("<Button 3>",zoom_out)
    zoom = True
    clear_selection()

def zoom_out(eventorigin):
    global tkimg, canv_img, zoom
    tkimg = ImageTk.PhotoImage(img)
    canvas.delete(canv_img)
    canv_img = canvas.create_image(0,0, anchor=NW, image=tkimg)
    root.bind("<Button 3>",zoom_in)
    zoom = False
    clear_selection()

#mouseclick events
root.bind("<Button 1>",first_corner)
root.bind("<Button 3>",zoom_in)
root.bind("q",clear_selection)

root.mainloop() 
