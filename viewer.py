'''Tools for displaying patterns.'''
from tkinter import *
import lifetree
window = Tk()
window.geometry('800x600')
canvas = Canvas(window)
canvas.pack()
lt = lifetree.lifetree('b3s23')
pt = lt.pattern('2ob$obo$bo!')
print(pt.apgcode)
def display(pt):
    pt.cleanup()
    coords = pt.coords
    for c in coords:
        print(c)
        x = c[0] * 50
        y = -c[1] * 50
        dx = 50
        dy = -50
        canvas.create_rectangle(x, y, x + dx, y + dy, fill = '#000000')
    window.update()
display(pt)
