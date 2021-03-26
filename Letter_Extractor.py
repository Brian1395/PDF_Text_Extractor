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
import os
from os import listdir
from os.path import isfile, join

## Gets files in the training data folder so names don't overlap
path_to_training_data = "C:\\Users\\brian\\Documents\\GitHub\\PDF_Text_Extractor\\TrainingData"

zoom_img = None
zoom = False
letter = ''
top_gap = 50
letter_written = None
cur_page = 1

## Turns PDF into image to display
images = convert_from_path('Source.pdf',poppler_path = r"C:\Users\brian\Documents\GitHub\PDF_Text_Extractor\poppler-21.02.0\Library\bin", first_page=1, last_page=2, fmt='JPEG')

img = images[1]
img = img.resize((int(img.width/2),int(img.height/2)))





## Display current letter to collect training data on
def inc_letter(eventorigin = None):
    global letter, letter_written
    if(letter == ''):
        letter = 'A'
    elif(letter == 'Z'):
        letter = 'a'
    elif(letter == 'z'):
        print("DONE!!!")
        #TODO: DEFINE FINISHING PROG
    else:
        letter = chr(ord(letter)+1)
    canvas.delete(letter_written)
    letter_written = canvas.create_text(int(canvas['width'])/2,top_gap/2,fill="darkblue",font="Times 20 bold",text=letter)
    canvas.update


## Creates a Tkinter instance where you can choose the corners of the letter
root = Tk()
zoom_scale = Scale(root, from_=2, to=4, tickinterval=0.5)
zoom_scale.pack(side = LEFT)
canvas = Canvas(root, width = 950, height = 800)      
canvas.pack()
tkimg = ImageTk.PhotoImage(img)
canv_img = canvas.create_image(0,top_gap, anchor=NW, image=tkimg) 
inc_letter()


# Determine the origin by clicking
def first_corner(eventorigin):
    global x0,y0, first_marker
    x0 = eventorigin.x
    y0 = eventorigin.y
    if(y0<top_gap):
        print("Cannot select within this area")
        return
    first_marker = canvas.create_oval(x0-1, y0-1, x0+1, y0+1)
    root.bind("<Button 1>",second_corner)

# Determine the origin by clicking
def second_corner(eventorigin):
    global x1,y1,selection_box
    x1 = eventorigin.x
    y1 = eventorigin.y
    if(y1<top_gap):
        print("Cannot select within this area")
        return
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
        section = zoom_img.crop((left, upper - top_gap, right, lower - top_gap))
    else:
        section = img.crop((left, upper - top_gap, right, lower - top_gap)) #Should add something for if they click outside the image but inside the window
    #section.show()
    cur_num = 0
    only_files = [f for f in listdir(path_to_training_data) if isfile(join(path_to_training_data, f))] #Doing all this every time is wildly inefficient, but makes sure you don't overwrite anything
    for x in only_files: 
        if(x[0] == letter and int(x[1:x.index('.')]) == cur_num):
            cur_num = int(x[1:x.index('.')]) + 1
    name = letter + str(cur_num)
    section.save(path_to_training_data + "\\" + name + ".jpg")

    root.bind("<Button 1>",first_corner)
    clear_selection()



def clear_selection(eventorigin = None):
    try:
        canvas.delete(first_marker)
        canvas.delete(selection_box)
    except:
        print("Nothing to clear")
    root.bind("<Button 1>",first_corner)



def zoom_in(eventorigin):
    global tkimg, canv_img, zoom, zoom_img
    scale = zoom_scale.get()
    x_click = eventorigin.x
    y_click = eventorigin.y
    x_offset = int(canvas['width'])/scale - x_click*scale
    y_offset = int(canvas['height'])/scale - y_click*scale
    print("called", x_click, y_click)
    zoom_img = img.resize((int(img.width*scale),int(img.height*scale)))
    zoom_img = zoom_img.crop((-x_offset, -y_offset, -x_offset + img.width, -y_offset + img.height))
    tkimg = ImageTk.PhotoImage(zoom_img)
    canvas.delete(canv_img)
    canv_img = canvas.create_image(0,top_gap, anchor=NW, image=tkimg)
    root.bind("<Button 3>",zoom_out)
    zoom = True
    clear_selection()

def zoom_out(eventorigin):
    global tkimg, canv_img, zoom
    tkimg = ImageTk.PhotoImage(img)
    canvas.delete(canv_img)
    canv_img = canvas.create_image(0,top_gap, anchor=NW, image=tkimg)
    root.bind("<Button 3>",zoom_in)
    zoom = False
    clear_selection()



##Switch to the next page
def turn_page(eventorigin):
    global cur_page, canv_img, img, letter, tkimg
    cur_page = cur_page + 1
    images = convert_from_path('Source.pdf',poppler_path = r"C:\Users\brian\Documents\GitHub\PDF_Text_Extractor\poppler-21.02.0\Library\bin", first_page=cur_page, last_page=cur_page+1, fmt='JPEG')
    img = images[1]
    img = img.resize((int(img.width/2),int(img.height/2)))
    tkimg = ImageTk.PhotoImage(img)
    canvas.delete(canv_img)
    canv_img = canvas.create_image(0,top_gap, anchor=NW, image=tkimg) 
    letter = 'A'



#mouseclick events
root.bind("<Button 1>",first_corner)
root.bind("<Button 3>",zoom_in)
root.bind("q",clear_selection)
root.bind("n",inc_letter)
root.bind("p",turn_page)

root.mainloop() 
