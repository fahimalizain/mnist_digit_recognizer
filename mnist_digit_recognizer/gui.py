
from PIL import ImageTk, Image, ImageDraw
import PIL.ImageOps
import PIL
import numpy
import tkinter
from tkinter import *
from keras.models import load_model

width = 600
height = 200
center = height//2
white = (255, 255, 255)
green = (0,128,0)

def save():
    filename = "image.png"
    image1.save(filename)

def paint(event):
    # python_green = "#476042"
    x1, y1 = (event.x - 2), (event.y - 2)
    x2, y2 = (event.x + 2), (event.y + 2)
    cv.create_oval(x1, y1, x2, y2, fill="black",width=5)
    # draw.line([x1, y1, x2, y2],fill="black",width=5)
    draw.ellipse([x1, y1, x2, y2],fill="black",outline="black")

root = Tk()

# Tkinter create a canvas to draw on
cv = Canvas(root, width=width, height=height, bg='white')
cv.pack()

# PIL create an empty image and draw object to draw on
# memory only, not visible
def makeNewDrawImage():
  global draw, image1
  image1 = PIL.Image.new("RGB", (width, height), white)
  draw = ImageDraw.Draw(image1)

# do the Tkinter canvas drawings (visible)
# cv.create_line([0, center, width, center], fill='green')

cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)

# do the PIL image/draw (in memory) drawings
# draw.line([0, center, width, center], green)

# PIL image can be saved as .png .jpg .gif or .bmp file (among others)
# filename = "my_drawing.png"
# image1.save(filename)
button=Button(text="save",command=save)
# button.pack()

def debugTest():
  test(debug=True)

def test(debug=False):
  if debug:
    print('--------------------------')
  resetText()
  im = image1.copy().convert('L')
  im = PIL.ImageOps.invert(im)
  digits = segment(im)
  r = ""
  t = ""
  for d in digits:
    if debug:
      d.show()
    r += str(predict_digit(d.copy(), debug))
    t += str(predict_digit_conv(d.copy(), debug))
  setText(r)
  setText2(t)
  if debug:
    print('--------------------------')

nn_model = load_model('mnist.h5')
def predict_digit(im, debug=False):
  im.thumbnail((28,28))
  # WIDTH=28
  # HEIGHT=28
  # pixels = [pixels[offset:offset+WIDTH] for offset in range(0, WIDTH*HEIGHT, WIDTH)]

  # im.show()
  model = nn_model

  d = numpy.array([list(im.getdata())]) / 255
  # print(d)
  # print(d.shape)
  predicted = model.predict(d)[0].tolist()
  predicted = predicted.index(max(predicted))
  if debug:
    print(predicted)
  # print(predicted)
  return predicted

conv_model = load_model('mnist-conv.h5')
def predict_digit_conv(im, debug=False):
  model = conv_model
  im.thumbnail((28,28))

  d = numpy.array([list(im.getdata())]) / 255
  d = d.reshape(1, 28, 28, 1)
  predicted = model.predict(d)[0].tolist()
  predicted = predicted.index(max(predicted))
  return predicted

def segment(im):
  """
    im of size 600x200
  """
  pixels = numpy.asarray(list(im.getdata()))
  vertical_hits = []
  segments = []
  last_black = False
  for i in range(0, width):
    vertical = pixels[i:width*height:width]
    # if numpy.any(vertical > 0):
    #   print(vertical)
    #   print(vertical.shape)
    if last_black and not numpy.any(vertical > 0):
      vertical_hits.append(i)
      last_black = False
      digit = im.copy().crop((vertical_hits.pop(-2), 0, vertical_hits.pop(-1), height))
      digit_prop = PIL.Image.new('L', (height, height))
      digit_prop.paste(digit, (int((height/2) - (digit.width/2)), 0))
      # digit_prop.show()
      segments.append(digit_prop)
    elif not last_black and numpy.any(vertical > 0):
      vertical_hits.append(i)
      last_black = True

  return segments

def reset():
  cv.delete("all")
  makeNewDrawImage()
  resetText()

def resetText():
  setText("--")
  setText2("--")

def setText(txt):
  lbl["text"] = "NN: " + txt

def setText2(txt):
  lbl2["text"] = "CNN: " + txt

neuralButton = Button(text="Detect", command=test)
neuralButton.pack(side=LEFT)

debugButton = Button(text="Detect (DEBUG)", command=debugTest)
debugButton.pack(side=LEFT)

resetButton = Button(text="Reset", command=reset)
resetButton.pack(side=LEFT)

lbl = Label(text='T')
lbl.pack()

lbl2 = Label(text='T')
lbl2.pack()

makeNewDrawImage()
root.mainloop()
