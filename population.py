import jsonpickle

import brains
import config


class Population(list):
    def __init__(self,*args,**kwargs):
        super(Population, self).__init__(*args,**kwargs)

    def create_random_pop(self,brain_cls, brain_arguments):
        self.extend(brain_cls(*brain_arguments) for _ in range(config.default_population_size))

    def load(self,file_contents):
        try:
            temp_pop=jsonpickle.decode(file_contents)
        except:
            raise Exception("Couldnt read file, make sure previous save is used for loading (not json pickle)")
        if not all(isinstance(x,brains.Brain) for x in temp_pop):
            raise Exception("Couldnt read file, make sure previous save is used for loading (not Brain models)")
        self.clear()
        self.extend(temp_pop)

    def save(self):
        jsonpickle.set_encoder_options('json', indent=4)
        return jsonpickle.encode(self)

    def display(self):
        for b in self:
            print(repr(b))