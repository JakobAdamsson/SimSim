import random
import time
import json

class Food():
    def __init__(self):
        super(Food, self).__init__()
        self._is_type = 'Food'
        self._quality = 100
    
    def bad_food(self):
        bad = random.randint(1, 1000)
        if bad < 25:
            self._quality -= 75
        return self._quality
    

class Product():
    def __init__(self):
        super(Product, self).__init__()
        self._is_type = 'Product'

class Worker():
    def __init__(self, health = 100):
        self._health = health
        self._is_alive = True
        self._death_cause = ['Head smashed', 'Heart attack', 
                             'Got shot by a college', 'Drowned', 'ate too much'
                             ,'simply collapsed']

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
    
    def reduce_health(self, amount):
        self._health -= amount
        if self._health < 0:
             self._is_alive = False
        return self._is_alive

    @property
    def is_alive(self):
        return self._is_alive

class Queue():
  
    def __init__(self):
        self._queue = []
    
    def _get_first_item(self):
        if self._queue:
            return self._queue.pop(0)
        else: 
            return None
  
    def _put_item_last(self, item):
        self._queue.append(item)
    
    def _get_queue_len(self):
        return len(self._queue)
    
    def _is_empty(self):
        if len(self._queue) > 0:
              return True
        return False

class Transition():
    def __init__(self, in_road, out_road):
        self._in_road = in_road
        self._out_road = out_road
 
class Road(Queue):
    def __init__(self):
        super(Road, self).__init__()
    
    def get_worker(self):
        return self._get_first_item()
  
    def put_worker(self, worker):
        self._put_item_last(worker)

    def get_num_workers(self):
        return self._get_queue_len()
  
    def has_worker(self):
        return self._is_empty()



class Barn(Queue):
    def __init__(self):
        super(Barn, self).__init__()
    
    def get_food(self):
        return self._get_first_item()
  
    def put_food(self, food):
        self._put_item_last(food)

    def has_food(self):
        return self._is_empty()
    
    def get_num_food(self):
        return self._get_queue_len()
    
class Storage(Queue):
    def __init__(self):
        super(Storage, self).__init__()
    
    def get_product(self):
        return self._get_first_item()
  
    def put_product(self, product):
        self._put_item_last(product)

    def has_product(self):
        return self._is_empty()

    def get_num_product(self):
        return self._get_queue_len()

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
    
        worker_alive = worker.do_work(health_drain=2)
        if worker_alive:
            print('Worker found, the worker is now making food in the farm')
            food = Food()
            poison = food.bad_food()
            print('A worker made a food!')
            self._barn.put_food(poison)
            print('Food sent to barn!')
            self._out_road.put_worker(worker)
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
        worker_alive = worker.do_work(health_drain=5, accident_rate=0.05)
        if worker_alive:
            print('Worker found, the worker is now making products in factory')
            product = Product()
            print('A worker made a product!')
            self._storage.put_product(product)
            print('Product sent to storage!')
            self._out_road.put_worker(worker)
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
                worker.reduce_health(25)
                print('A worker ate bad food and got sick!')
            if food >= 25 :
                worker.gain_health(25)
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
                    new_worker = Worker()
                    new_worker2 = Worker()
                    new_worker3 = Worker()
                    self._out_road.put_worker(new_worker)
                    self._out_road.put_worker(new_worker2)
                    self._out_road.put_worker(new_worker3)
                    print('3 new worker(s) spawned!')
                if 0.05 <= kid_chance < 0.15:
                    new_worker = Worker()
                    new_worker2 = Worker()
                    self._out_road.put_worker(new_worker)
                    self._out_road.put_worker(new_worker2)
                    print('2 new worker(s) spawned!')
                if 0.15 <= kid_chance < 0.4:
                    new_worker = Worker()
                    self._out_road.put_worker(new_worker)
                    print('1 new worker(s) spawned!')
        self._out_road.put_worker(worker2)
        self._out_road.put_worker(worker)
        return
        
if __name__ == '__main__':
    r1 = Road()
    r2 = Road()
    roads = [r1, r2]
    s1 = Storage()
    s2 = Storage()
    b1 = Barn()
    f1 = Factory(in_road = r1, out_road = r2, storage = s1)
    farm = Farm(in_road = r2, out_road = r1, barn = b1 )
    canteen = Canteen(in_road = r1, out_road = r2, barn = b1)
    f2 = Factory(in_road = r2, out_road = r1, storage = s1)
    farm2 = Farm(in_road=r1, out_road=r2, barn = b1)
    hus = House(in_road = r2, out_road = r1, storage = s1)
    
    
    production_sites = [f1, farm, canteen, f2, farm2]

    # Create all the worker 
    workers = [Worker() for _ in range(30)]
    # Put all the worker on the road
    
    
    for worker in workers:
        r1.put_worker(worker)
    
    # Start simulation
    all_workers_alive = True
    #counts days
    i = 0
    
    while all_workers_alive:
        total_worker_health = 0.0
        # Drain health of all workers that are on roads
        for road in roads:
            num_workers = road.get_num_workers()
            for _ in range(num_workers):
                worker = road.get_worker()
                if worker != None:
                    is_alive = worker.reduce_health(road.get_num_workers())
                    if is_alive:  
                        road.put_worker(worker)
                        total_worker_health += float(worker._health)
                        avg_worker_health = total_worker_health/(len(workers))
        print('----------------------')
        print('What happend during the day:')
        if avg_worker_health > 20:
            print(f'Resting and producing new workers {[False]}')
            print('-------------------------------------------')
        if avg_worker_health <= 20:
            print(f'Resting and producing new workers {[True]}')
            print('-------------------------------------------')
        for site in production_sites:
            if avg_worker_health > 20: 
                site.produce()
            if avg_worker_health <= 20:
                hus.produce()
                
        print('--------Status---------')
        print(f'Day {i} of hard work')
        print(f'Current food supply {b1.get_num_food()}')
        print(f'Current product supply {s1.get_num_product()}') 
        print(f'Current workers alive {r1.get_num_workers()+r2.get_num_workers()}')
        if r2.get_num_workers()+r1.get_num_workers() > 0:
            print(f'Average worker health {avg_worker_health}')
        if r2.get_num_workers()+r1.get_num_workers() <= 0:
            avg_worker_health = 0
            print(f'Average worker health {avg_worker_health}')
                        
        if not r1._is_empty() and not r2._is_empty():
            all_workers_alive = False
            print('All workers have died!, there are no workers left on the roads or in the constructions, simulation ending....')
        i += 1
        time.sleep(0)
    print(f'Simulation has ended, the population survived for {i} days')

        # num_workers_alive = 0
        #         for worker in workers:
        #             if worker.is_alive:
        #                 num_workers_alive += 1 
        #             if not worker.is_alive:
        #                 num_workers_alive -= 1
        # if num_workers_alive == 0:
        #     all_workers_alive = False
        #     print('All workers have died!, there are no workers left on the roads or the constructions, simulation ending....')
        # else:
