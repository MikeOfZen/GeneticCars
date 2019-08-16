import json
import pathlib

import pyglet


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

pyglet.resource.path = ["@resources"]
pyglet.resource.reindex()

basic_car_name="yellow_car.png"
car_img = pyglet.resource.image(basic_car_name)
center_image(car_img)

dead_car_name="dead_car.png"
dead_img = pyglet.resource.image(dead_car_name)
center_image(dead_img)

user_car_name="user_car.png"
user_img = pyglet.resource.image(user_car_name)
center_image(user_img)



tracks=[]
resources=pyglet.resource.location("__init__.py").path
for f in pathlib.Path(resources).glob('track_*.json'):
    track_json = pyglet.resource.file(f.name)
    tracks.append(json.load(track_json))
