class Queue():
    def __init__(self):
        self._queue = []
        self._max_len = 0
    
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
