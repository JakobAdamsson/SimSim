import random

class Food():
    def __init__(self):
        self._is_type = 'Food'
        self._quality = 100
    
    def bad_food(self):
        bad = random.randint(1, 1000)
        if bad < 25:
            self._quality -= 75
        return self._quality
    

class Product():
    def __init__(self):
        self._is_type = 'Product'

class Worker():
    def __init__(self, health = 100):
        self._health = health
        self._is_alive = True
        self._death_cause = ['Head smashed']

    #worker works and might get hurt
    def do_work(self, health_drain, accident_rate = None):
        death_cause = random.randint(1, len(self._death_cause))
        self._health -= health_drain
        if self._health < 0:
              self._is_alive = False
              print('A worker lost all its health and died!')
              return self.is_alive
        
        # An accident can happen
        if accident_rate is not None:
            if random.random() < accident_rate:
                print(f'A worker died in the factory, cause of death: {self._death_cause[death_cause-1]}')
                self._is_alive = False
        return self._is_alive

    def gain_health(self, amount):
        self._health += amount
        if self._health > 100:
            self._health = 100
    
    def reduce_health(self, amount):
        self._health -= amount
        if self._health < 0:
             self._is_alive = False
        return self._is_alive

    @property
    def is_alive(self):
        return self._is_alive
