import pyglet
import json
import pathlib
import track
def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

pyglet.resource.path = ["@resources"]
pyglet.resource.reindex()

car_img = pyglet.resource.image("yellow_car.png")
center_image(car_img)

dead_img = pyglet.resource.image("dead_car.png")
center_image(dead_img)
user_img = pyglet.resource.image("user_car.png")
center_image(user_img)

tracks=[]
resources=pyglet.resource.location("__init__.py").path
for f in pathlib.Path(resources).glob('track_*.json'):
    track_json = pyglet.resource.file(f.name)
    tracks.append(json.load(track_json))
