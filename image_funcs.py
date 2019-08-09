from PIL import Image, ImageDraw, ImageFont
import load
import pyglet

base = load.car_img

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', (200,200), (0,0,0,0))
base = Image.new('RGBA', (200,200), (0,0,0,255))
# get a font
fnt = ImageFont.load_default()
# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((10,10), "Hello", font=fnt, fill=(255,255,255,128))
# draw text, full opacity
d.text((10,60), "World", font=fnt, fill=(255,255,255,255))

out = Image.alpha_composite(base, txt)

out.show()