import transitions
import places
import resources
import time


    
    




if __name__ == '__main__':
    r1 = places.Road()
    r2 = places.Road()
    r3 = places.Road()
    roads = [r1, r2, r3]
    s1 = places.Storage()
    s2 = places.Storage()
    b1 = places.Barn()
    f1 = transitions.Factory(in_road = r1, out_road = r2, storage = s1)
    farm = transitions.Farm(in_road = r2, out_road = r3, barn = b1 )
    canteen = transitions.Canteen(in_road = r3, out_road = r1, barn = b1)
    f2 = transitions.Factory(in_road = r1, out_road = r2, storage = s1)
    farm2 = transitions.Farm(in_road=r2, out_road=r3, barn = b1)
    hus = transitions.House(in_road = r3, out_road = r1, storage = s1)
    
    
    production_sites = [f1, farm, canteen, f2, farm2]

    # Create all the worker 
    #workers = [resources.Worker() for _ in range(20)]
    # Put all the worker on the road
    
    for _ in range(5):
        r1.put_worker(resources.Worker())
    for _ in range(5):
        r2.put_worker(resources.Worker())
    for _ in range(5):
        r3.put_worker(resources.Worker())
 
    # for worker in workers:
    #     r1.put_worker(worker)
        
    
    # Start simulation
    all_workers_alive = True
    #counts days
    i = 0
    
    while all_workers_alive:
        print("""
current workers on road 1: {}
current workers on road 2: {}
current workers on road 3: {}""".format(r1.get_num_workers(), r2.get_num_workers(), r3.get_num_workers()))
        
        
        total_worker_health = 0.0
        # Drain health of all workers that are on roads
        for road in roads:
            num_workers = road.get_num_workers()
            for _ in range(num_workers):
                worker = road.get_worker()
                if worker != None:          
                    total_worker_health += float(worker._health)
                    is_alive = worker.reduce_health(road.get_num_workers())
                    if is_alive:  
                        road.put_worker(worker)
                        avg_worker_health = total_worker_health/(r1.get_num_workers()+r2.get_num_workers()+r3.get_num_workers())
                    if not is_alive:
                        print('A worker died on the road')
        print('----------------------')
        print('What happend during the day:')
        if avg_worker_health > 40:
            print(f'Resting and producing new workers {[False]}')
            print('-------------------------------------------')
        if avg_worker_health <= 40:
            print(f'Resting and producing new workers {[True]}')
            print('-------------------------------------------')
        for site in production_sites:
            if avg_worker_health > 40: 
                site.produce()
            if avg_worker_health <= 40:
                hus.produce()
                
        print('--------Status---------')
        print(f'Day {i} of hard work')
        print(f'Current food supply {b1.get_num_food()}')
        print(f'Current product supply {s1.get_num_product()}') 
        print(f'Current workers alive {r1.get_num_workers()+r2.get_num_workers()+r3.get_num_workers()}')
        if r2.get_num_workers()+r1.get_num_workers()+r3.get_num_workers() > 0:
            print(f'Average worker health {avg_worker_health}')
        if r2.get_num_workers()+r1.get_num_workers()+r3.get_num_workers() <= 0:
            avg_worker_health = 0
            print(f'Average worker health {avg_worker_health}')
                        
        if not r1._is_empty() and not r2._is_empty() and not r3._is_empty():
            all_workers_alive = False
            print('All workers have died!, there are no workers left on the roads or in the constructions, simulation ending....')
        i += 1
        time.sleep(3)
    print(f'Simulation has ended, the population survived for {i} days')