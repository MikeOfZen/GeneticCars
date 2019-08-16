import io

import pyglet
from PIL import Image, ImageDraw, ImageFont

fnt = ImageFont.load_default()
def write_on_image(resource_name,text,text_colors=(255, 255, 255, 255)):
    p_res_fp = pyglet.resource.file(resource_name)
    base = Image.open(p_res_fp, mode='r')

    txt_im = Image.new('RGBA', base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(txt_im)
    d.text((5, 5), text, font=fnt, fill=text_colors)

    out = Image.alpha_composite(base, txt_im)

    temp_buf = io.BytesIO()
    out.save(temp_buf, "PNG")
    pyg_img=pyglet.image.load("a.png", file=temp_buf)
    center_image(pyg_img)
    return pyg_img

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2