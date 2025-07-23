import numpy as np
import random
from collections import deque

def can_form_exact_load(queue, target_weight):
    """Determine if items in the queue can form an exact load of target_weight.
    Returns (can_form, selected_indices)"""
    
    items = [(i, item[1]) for i, item in enumerate(queue)]
    n = len(items)
    
    items.sort(key=lambda x: x[1], reverse=True)
    
    def find_subset_sum(items, target, start_idx=0, current_sum=0, current_indices=None):
        if current_indices is None:
            current_indices = []
            
        if current_sum == target:
            return True, current_indices
            
        if start_idx >= len(items) or current_sum > target:
            return False, []
            
        include_result, include_indices = find_subset_sum(
            items, target, start_idx + 1, 
            current_sum + items[start_idx][1], 
            current_indices + [items[start_idx][0]]
        )
        
        if include_result:
            return True, include_indices
            
        return find_subset_sum(items, target, start_idx + 1, current_sum, current_indices)
    
    can_form, selected_indices = find_subset_sum(items, target_weight)
    
    return can_form, selected_indices

def run_elevator_simulation(duration=60, num_runs=100):
    MATERIAL_A_WEIGHT = 200
    MATERIAL_B_WEIGHT = 100
    MATERIAL_C_WEIGHT = 50
    ELEVATOR_CAPACITY = 400
    UP_TIME = 1
    UNLOAD_TIME = 2
    DOWN_TIME = 1
    
    all_a_wait_times = []
    all_b_wait_times = []
    all_c_transferred = []
    
    for _ in range(num_runs):
        def generate_a_interval():
            return random.uniform(3, 7) 
            
        def generate_c_interval():
            return 2 if random.random() <= 0.33 else 3  # P(2)=0.33, P(3)=0.67
        
        current_time = 0
        queue = deque() 
        
        next_a_arrival = generate_a_interval()
        next_b_arrival = 6  
        next_c_arrival = generate_c_interval()
        
        elevator_status = "ready"  
        elevator_next_ready_time = 0
        
        a_wait_times = []
        b_wait_times = []
        c_transferred = 0
        
        while current_time < duration:
            next_event_times = [next_a_arrival, next_b_arrival, next_c_arrival]
            
            elevator_departure = float('inf')
            if elevator_status == "ready" and current_time >= elevator_next_ready_time:
                total_queue_weight = sum(item[1] for item in queue)
                
                if total_queue_weight >= ELEVATOR_CAPACITY:
                    can_form, selected_indices = can_form_exact_load(queue, ELEVATOR_CAPACITY)
                    if can_form:
                        elevator_departure = current_time
                        next_event_times.append(elevator_departure)
            
            next_time = min(next_event_times)
            current_time = next_time
            
            if current_time == next_a_arrival:
                queue.append(('A', MATERIAL_A_WEIGHT, current_time))
                next_a_arrival = current_time + generate_a_interval()
                
            if current_time == next_b_arrival:
                queue.append(('B', MATERIAL_B_WEIGHT, current_time))
                next_b_arrival = current_time + 6
                
            if current_time == next_c_arrival:
                queue.append(('C', MATERIAL_C_WEIGHT, current_time))
                next_c_arrival = current_time + generate_c_interval()
                
            if current_time == elevator_departure:
                can_form_load, selected_indices = can_form_exact_load(queue, ELEVATOR_CAPACITY)
                
                if can_form_load:
                    elevator_status = "moving_up"
                    moved_materials = []
                    new_queue = deque()
                    
                    for i, item in enumerate(queue):
                        if i in selected_indices:
                            moved_materials.append(item)
                            
                            if item[0] == 'A':
                                a_wait_times.append(current_time - item[2])
                            elif item[0] == 'B':
                                b_wait_times.append(current_time - item[2])
                            elif item[0] == 'C':
                                c_transferred += 1
                        else:
                            new_queue.append(item)
                    
                    queue = new_queue
                    
                    elevator_next_ready_time = current_time + UP_TIME + UNLOAD_TIME + DOWN_TIME
                    elevator_status = "ready"  
        
        all_a_wait_times.extend(a_wait_times)
        all_b_wait_times.extend(b_wait_times)
        all_c_transferred.append(c_transferred)
    
    avg_a_transfer_time = sum(all_a_wait_times) / len(all_a_wait_times) if all_a_wait_times else 0
    avg_b_wait_time = sum(all_b_wait_times) / len(all_b_wait_times) if all_b_wait_times else 0
    avg_c_count = sum(all_c_transferred) / num_runs
    
    avg_a_transfer_time += (UP_TIME + UNLOAD_TIME)
    
    return avg_a_transfer_time, avg_b_wait_time, avg_c_count


avg_a_transfer_time, avg_b_wait_time, avg_c_count = run_elevator_simulation(duration=60, num_runs=50)

print(f"1. Average transfer time for material A: {avg_a_transfer_time:.2f} minutes")
print(f"2. Average waiting time for material B: {avg_b_wait_time:.2f} minutes")
print(f"3. Number of material C boxes transferred in one hour: {int(round(avg_c_count))}")