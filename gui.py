import math
import numpy as np
import pyglet
from pyglet.window import key

import car
import config
import image_funcs
import load
from track import Track


class GameWindow(pyglet.window.Window):

    def __init__(self,close_on_finish=True,*args,**kwargs):
        super(GameWindow,self).__init__(*args,**kwargs)
        self.close_on_finish=close_on_finish
        self.set_caption("Genetic Cars")

        self.fixed_batch=pyglet.graphics.Batch()
        self.activity_batch=None
        self.batches=[]

        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

        self.activity = None

    def check_exit(self):
        return self.keys[key.ESCAPE]

    def step(self, dt):
        running=self.activity()
        if running or self.check_exit():
            self.clear()
            self.fixed_batch.draw()
            if self.activity_batch:
                self.activity_batch.draw()
        else:
            self.activity_batch=None
            if self.close_on_finish:
                self.close()
            self.halt()

    def on_close(self):
        self.close()
        self.halt()

    def halt(self):
        pyglet.clock.unschedule(self.step)
        #maybe unneeded
        pyglet.app.exit()

    def start(self):
        pyglet.clock.schedule_interval(self.step, 1 / config.fps)
        pyglet.app.run()

    def new_activity_batch(self):
        self.activity_batch=pyglet.graphics.Batch()
        return self.activity_batch


class DrawingTrack(Track):
    def __init__(self,window,batch,*args,**kwargs):
        super(DrawingTrack, self).__init__(*args,**kwargs)
        self.window=window
        self.batch=batch

        #transform track and start to gui coords
        self.borders_t = self.borders + np.array([self.transform_x(0), self.transform_y(0)], dtype=np.float)
        self.gates_t = self.gates + np.array([self.transform_x(0), self.transform_y(0)], dtype=np.float)
        self.start_t = (self.transform_x(self.start[0]), self.transform_y(self.start[1]))

        self._setup_borders()
        self._setup_gats()

    def _setup_borders(self):
        self.tri_strip=[]
        for border in self.borders_t:
            vertices=thickness_vertices(border,config.border_thickness)
            self.batch.add_indexed(4,pyglet.gl.GL_TRIANGLES,
                                         None,[0, 1, 2, 1, 2, 3],
                                         ('v2f', (vertices.flatten())))

    def _setup_gats(self):
        self.tri_strip=[]
        for border in self.gates_t:
            vertices=thickness_vertices(border,config.gate_thickness)
            self.batch.add_indexed(4,pyglet.gl.GL_TRIANGLES,
                                         None,[0, 1, 2, 1, 2, 3],
                                         ('v2f', tuple(vertices.flatten())),
                                          ('c3B', config.gate_color*4) )

    def transform_x(self,x):
        """transform x from track coordinate system to grpahic coordinate system, relative to center of window"""
        return x+self.window.width/2.0
    def transform_y(self,y):
        """transform y from track coordinate system to grpahic coordinate system, relative to center of window"""
        return y+self.window.height/2.0


class DrawingCar(car.ScoringCar):
    def __init__(self, window, batch,*args, **kwargs):
        super(DrawingCar, self).__init__(*args, **kwargs)
        self.window=window
        self.batch=batch


        # img=load.car_img
        self.graphics=[]

        pyg_image=image_funcs.write_on_image(load.basic_car_name,self.name,config.basic_name_colors)
        self.sprite=pyglet.sprite.Sprite(img=pyg_image,x=self.track.transform_x(self.x),y=self.track.transform_y(self.y),batch=self.batch)

        # self.label=pyglet.text.Label(self.name,
        #                           font_name='Arial',
        #                           font_size=10,
        #                           x=self.track.transform_x(self.x),
        #                           y=self.track.transform_y(self.y),
        #                           anchor_x='center',
        #                           anchor_y='center',batch=self.batch,color=(255,0,0,255))

        self.graphics+=[self.sprite]



    def step(self):
        r=super(DrawingCar, self).step()
        if not self.dead:
            for graphic in self.graphics:
                graphic.x = int(self.track.transform_x(self.x))
                graphic.y = int(self.track.transform_y(self.y))
                graphic.rotation=-math.degrees(self.dir)
        else:
            #self.label.text="X"+self.name
            pyg_image = image_funcs.write_on_image(load.dead_car_name, self.name, config.basic_name_colors)
            self.sprite.image = pyg_image
        return r


def thickness_vertices(line, thickness):
    """line is a numpy array (2,2) of start and and positions in x,y
    returns 4 vertices of triangles to draw thick line"""
    n=find_normal(line)
    v1=line[0]+n*thickness
    v2 = line[0] - n * thickness
    v3= line[1]+n*thickness
    v4 =line[1]-n*thickness
    return np.array([v1,v2,v3,v4],dtype=np.float)


def find_normal(line):
    n=np.zeros(2)
    v=line[1]-line[0]
    n[0]=v[1]
    n[1]=-v[0]
    n=n/np.linalg.norm(n)
    return n