import resources
import random
class Transition():
    def __init__(self, in_road, out_road):
        self._in_road = in_road
        self._out_road = out_road
        self._max_items = 0

class Farm(Transition):
    def __init__(self, in_road, out_road, barn):
        super(Farm, self).__init__(in_road, out_road)
        self._barn = barn
    
    def produce(self):
        # Get a worker
        worker = self._in_road.get_worker()
        # If no worker exists, return
        if worker is None:
            print('Could not find a worker that can be used in farm!')
            return
    
        worker_alive = worker.do_work(health_drain=0)
        if worker_alive:
            print('Worker found, the worker is now making food in the farm')
            food = resources.Food()
            poison = food.bad_food()
            print('A worker made a food!')
            self._barn.put_food(poison)
            print('Food sent to barn!')
            self._out_road.put_worker(worker)
        if not worker_alive:
            print('A worker died in the farm!')
        return

class Factory(Transition):
    def __init__(self, in_road, out_road, storage):
        super(Factory, self).__init__(in_road, out_road)
        self._storage = storage
        
    def produce(self):
        # Get a worker
        worker = self._in_road.get_worker()
        # If no worker exists, return
        if worker is None:
            print('Could not find a worker that can be used in the factory!')
            return
    
        # Make worker produce a product
        worker_alive = worker.do_work(health_drain=2, accident_rate=0.01)
        if worker_alive:
            print('Worker found, the worker is now making products in factory')
            product = resources.Product()
            print('A worker made a product!')
            self._storage.put_product(product)
            print('Product sent to storage!')
            self._out_road.put_worker(worker)
        if not worker_alive:
            print('A worker died in the factory!!')
        return

class Canteen(Transition):
    def __init__(self, in_road, out_road, barn):
        super(Canteen, self).__init__(in_road, out_road)
        self._barn = barn
      
    def produce(self):
        worker = self._in_road.get_worker()
        
        if worker is None:
            print('Could not find a worker that wanted to eat!')
            return

        if self._barn.has_food() and worker != None:
            print('Worker found, the worker is now eating food')
            food = self._barn.get_food()
            if food < 25:
                worker.reduce_health(15)
                print('A worker ate bad food and got sick!')
            if food >= 25 :
                worker.gain_health(35)
                print('A worker ate and gained 5 hp!')
                
        self._out_road.put_worker(worker)
        return
class House(Transition):
    def __init__(self, in_road, out_road, storage):
        super(House, self).__init__(in_road, out_road)
        self._storage = storage
     
    def produce(self):
        worker = self._in_road.get_worker()
        worker2 = self._out_road.get_worker()
          
        if worker is None and worker2 is None:
            print('Could not find a worker in the house')
            return
        
        if worker is None and worker2 is not None:
            if self._storage.has_product():
                worker2.gain_health(50)
                print('A worker gained 50 hp by resting')
            
        if worker is not None and worker2 is None:
            if self._storage.has_product():
                worker.gain_health(50)
                print('A worker gained 50 hp by resting')
        
        if worker is not None and worker2 is not None:
            kid_chance = random.random()
            if kid_chance < 0.4:
                if 0 <= kid_chance < 0.05:
                    self._storage.get_product()
                    new_worker = resources.Worker()
                    new_worker2 = resources.Worker()
                    new_worker3 = resources.Worker()
                    self._out_road.put_worker(new_worker)
                    self._out_road.put_worker(new_worker2)
                    self._out_road.put_worker(new_worker3)
                    print('3 new worker(s) spawned!')
                if 0.05 <= kid_chance < 0.15:
                    self._storage.get_product()
                    new_worker = resources.Worker()
                    new_worker2 = resources.Worker()
                    self._out_road.put_worker(new_worker)
                    self._out_road.put_worker(new_worker2)
                    print('2 new worker(s) spawned!')
                if 0.15 <= kid_chance < 0.4:
                    new_worker = resources.Worker()
                    self._out_road.put_worker(new_worker)
                    print('1 new worker(s) spawned!')
        self._in_road.put_worker(worker2)
        self._out_road.put_worker(worker)
        return