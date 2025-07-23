# 3-54
import random as r

class Component:
    index_counter = 0
    def __init__(self,type,enter_time):
        self.index = Component.index_counter
        Component.index_counter+=1
        self.type = type
        self.enter_time = enter_time
        self.return_from_d = 0
        self.leave_time = 0

class simulator():
    def __init__(self):
        self.fel = []
        self.time = 0
        self.start_time = 0

        self.a_queue_length_normal = 0
        self.a_queue_length_emergency = 0
        self.a_status = 0
        self.a_queue_normal = []
        self.a_queue_emergency = []
        self.a_worker_num = 1

        self.b_queue_length_normal = 0
        self.b_queue_length_emergency = 0
        self.b_status = 0
        self.b_queue_normal = []
        self.b_queue_emergency = []
        self.b_worker_num = 3

        self.c_queue_length = 0
        self.c_status = 0
        self.c_queue = []
        self.c_serve_time = 20

        self.d_queue_length_normal = 0
        self.d_queue_length_emergency = 0
        self.d_status = 0
        self.d_queue_normal = []
        self.d_queue_emergency = []
        self.d_worker_num = 4

        self.e_queue_length_normal = 0
        self.e_queue_length_emergency = 0
        self.e_status = 0
        self.e_queue_normal = []
        self.e_queue_emergency = []
        self.e_worker_num = 3

        self.leaved_components = []
        self.entered_components = []
        
        self.queue_length_stat = {
            'a_queue_normal' : [0],
            'a_queue_emergency' : [0],
            'b_queue_normal' : [0],
            'b_queue_emergency' : [0],
            'c_queue' : [0],
            'd_queue_normal' : [0],
            'd_queue_emergency' : [0],
            'e_queue_normal' : [0],
            'e_queue_emergency' : [0],
        }
        
        self.utilization_data = {
            'a': {'last_change_time': 0, 'total_busy_time': 0, 'last_status': 0},
            'b': {'last_change_time': 0, 'total_busy_time': 0, 'last_status': 0},
            'c': {'last_change_time': 0, 'total_busy_time': 0, 'last_status': 0},
            'd': {'last_change_time': 0, 'total_busy_time': 0, 'last_status': 0},
            'e': {'last_change_time': 0, 'total_busy_time': 0, 'last_status': 0},
        }

    def update_utilization(self, station, old_status, new_status):
        """Update utilization tracking when station status changes"""
        station_data = self.utilization_data[station]
        time_interval = self.time - station_data['last_change_time']
        
        if old_status > 0:
            station_data['total_busy_time'] += old_status * time_interval
        
        station_data['last_change_time'] = self.time
        station_data['last_status'] = new_status

    def enter(self,enter_component):
        type = enter_component.type
        self.entered_components.append(enter_component)
        if type==0:
            if self.a_status<self.a_worker_num:
                old_status = self.a_status
                self.a_status += 1
                self.update_utilization('a', old_status, self.a_status)
                serve_time = r.uniform(12-2,12+2)
                self.fel.append(( self.time + serve_time , 'end_a', enter_component))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                self.a_queue_length_normal+=1
                self.queue_length_stat['a_queue_normal'].append(self.a_queue_length_normal)
                self.a_queue_normal.append(enter_component)
            enter_interval = r.uniform(15-13,15+13)
            self.fel.append(( self.time + enter_interval , 'enter', Component(0, self.time + enter_interval)))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if self.a_status<self.a_worker_num:
                old_status = self.a_status
                self.a_status += 1
                self.update_utilization('a', old_status, self.a_status)
                serve_time = r.uniform(12-2,12+2)
                self.fel.append(( self.time + serve_time , 'end_a', enter_component))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                self.a_queue_length_emergency+=1
                self.queue_length_stat['a_queue_emergency'].append(self.a_queue_length_emergency)
                self.a_queue_emergency.append(enter_component)
            enter_interval = r.uniform((4-3)*60,(4+3)*60)
            self.fel.append(( self.time + enter_interval , 'enter', Component(1, self.time + enter_interval)))
            self.fel = sorted(self.fel,key=lambda x : x[0])
    
    def end_a(self,component):
        type = component.type
        if self.b_status<self.b_worker_num:
            old_status = self.b_status
            self.b_status += 1
            self.update_utilization('b', old_status, self.b_status)
            serve_time = r.uniform(40-20,40+20)
            self.fel.append(( self.time + serve_time , 'end_b', component))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if type==0:
                self.b_queue_length_normal+=1
                self.queue_length_stat['b_queue_normal'].append(self.b_queue_length_normal)
                self.b_queue_normal.append(component)
            else:
                self.b_queue_length_emergency+=1
                self.queue_length_stat['b_queue_emergency'].append(self.b_queue_length_emergency)
                self.b_queue_emergency.append(component)
        
        if self.a_queue_length_emergency>0:
            self.a_queue_length_emergency-=1
            self.queue_length_stat['a_queue_emergency'].append(self.a_queue_length_emergency)
            component_poped = self.a_queue_emergency.pop(0)
            serve_time = r.uniform(12-2,12+2)
            self.fel.append(( self.time + serve_time , 'end_a', component_poped))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if self.a_queue_length_normal>0:
                self.a_queue_length_normal-=1
                self.queue_length_stat['a_queue_normal'].append(self.a_queue_length_normal)
                component_poped = self.a_queue_normal.pop(0)
                serve_time = r.uniform(12-2,12+2)
                self.fel.append(( self.time + serve_time , 'end_a', component_poped))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                old_status = self.a_status
                self.a_status -= 1
                self.update_utilization('a', old_status, self.a_status)

    def end_b(self,component):
        type = component.type
        if component.return_from_d==0:
            random_number = r.uniform(0,1)
            if random_number<=0.4:
                if self.d_status<self.d_worker_num:
                    old_status = self.d_status
                    self.d_status+=1
                    self.update_utilization('d', old_status, self.d_status)
                    serve_time = r.uniform(50-40,50+40)
                    self.fel.append(( self.time + serve_time , 'end_d', component))
                    self.fel = sorted(self.fel,key=lambda x : x[0])
                else:
                    if type==0:
                        self.d_queue_length_normal+=1
                        self.queue_length_stat['d_queue_normal'].append(self.d_queue_length_normal)
                        self.d_queue_normal.append(component)
                    else:
                        self.d_queue_length_emergency+=1
                        self.queue_length_stat['d_queue_emergency'].append(self.d_queue_length_emergency)
                        self.d_queue_emergency.append(component)
            else:
                if self.c_status==0:
                    old_status = self.c_status
                    self.c_status=1
                    self.update_utilization('c', old_status, self.c_status)
                    serve_time = self.c_serve_time
                    self.fel.append(( self.time + serve_time , 'end_c', component)) 
                    self.fel = sorted(self.fel,key=lambda x : x[0])
                else:
                    self.c_queue_length+=1
                    self.queue_length_stat['c_queue'].append(self.c_queue_length)
                    self.c_queue.append(component)
        else:
            if self.d_status<self.d_worker_num:
                old_status = self.d_status
                self.d_status+=1
                self.update_utilization('d', old_status, self.d_status)
                serve_time = r.uniform(50-40,50+40)
                self.fel.append(( self.time + serve_time , 'end_d', component))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                if type==0:
                    self.d_queue_length_normal+=1
                    self.queue_length_stat['d_queue_normal'].append(self.d_queue_length_normal)
                    self.d_queue_normal.append(component)
                else:
                    self.d_queue_length_emergency+=1
                    self.queue_length_stat['d_queue_emergency'].append(self.d_queue_length_emergency)
                    self.d_queue_emergency.append(component)
        
        if self.b_queue_length_emergency>0:
            self.b_queue_length_emergency-=1
            self.queue_length_stat['b_queue_emergency'].append(self.b_queue_length_emergency)
            component_pop = self.b_queue_emergency.pop(0)
            serve_time = r.uniform(40-20,40+20)
            self.fel.append(( self.time + serve_time , 'end_b', component_pop))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if self.b_queue_length_normal>0:
                self.b_queue_length_normal-=1
                self.queue_length_stat['b_queue_normal'].append(self.b_queue_length_normal)
                component_pop = self.b_queue_normal.pop(0)
                serve_time = r.uniform(40-20,40+20)
                self.fel.append(( self.time + serve_time , 'end_b', component_pop))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                old_status = self.b_status
                self.b_status-=1
                self.update_utilization('b', old_status, self.b_status)
    
    def end_c(self,component):
        type = component.type
        if self.d_status<self.d_worker_num:
            old_status = self.d_status
            self.d_status+=1
            self.update_utilization('d', old_status, self.d_status)
            serve_time = r.uniform(50-40,50+40)
            self.fel.append(( self.time + serve_time , 'end_d', component))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if type==0:
                self.d_queue_length_normal+=1
                self.queue_length_stat['d_queue_normal'].append(self.d_queue_length_normal)
                self.d_queue_normal.append(component)
            else:
                self.d_queue_length_emergency+=1
                self.queue_length_stat['d_queue_emergency'].append(self.d_queue_length_emergency)
                self.d_queue_emergency.append(component)
        
        if self.c_status==2:
            old_status = self.c_status
            self.c_status=-1
            self.update_utilization('c', old_status, self.c_status)
            end_of_closure_time = r.uniform(10-1,10+1)
            self.fel.append(( self.time + end_of_closure_time , 'end_of_closure'))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        elif self.c_status==1:
            if self.c_queue_length>0:
                self.c_queue_length-=1
                self.queue_length_stat['c_queue'].append(self.c_queue_length)
                component_pop = self.c_queue.pop(0)
                serve_time = self.c_serve_time
                self.fel.append(( self.time + serve_time , 'end_c', component_pop))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                old_status = self.c_status
                self.c_status=0
                self.update_utilization('c', old_status, self.c_status)
    
    def end_of_closure(self):
        if self.c_queue_length>0:
            self.c_queue_length-=1
            self.queue_length_stat['c_queue'].append(self.c_queue_length)
            component_pop = self.c_queue.pop(0)
            old_status = self.c_status
            self.c_status=1
            self.update_utilization('c', old_status, self.c_status)
            serve_time = self.c_serve_time
            self.fel.append(( self.time + serve_time , 'end_c', component_pop))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            old_status = self.c_status
            self.c_status=0
            self.update_utilization('c', old_status, self.c_status)
        
        end_of_open_time = 2*60
        self.fel.append(( self.time + end_of_open_time , 'end_of_open'))
        self.fel = sorted(self.fel,key=lambda x : x[0])
    
    def end_of_open(self):
        if self.c_status==0:
            old_status = self.c_status
            self.c_status=-1
            self.update_utilization('c', old_status, self.c_status)
            end_of_closure_time = r.uniform(10-1,10+1)
            self.fel.append(( self.time + end_of_closure_time , 'end_of_closure'))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            old_status = self.c_status
            self.c_status=2
            self.update_utilization('c', old_status, self.c_status)
    
    def end_d(self,component):
        type = component.type
        random_number = r.uniform(0,1)
        if random_number<=0.1:
            component.return_from_d = 1
            if self.b_status<self.b_worker_num:
                old_status = self.b_status
                self.b_status += 1
                self.update_utilization('b', old_status, self.b_status)
                serve_time = r.uniform(30-10,30+10)
                self.fel.append(( self.time + serve_time , 'end_b', component))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                if type==0:
                    self.b_queue_length_normal+=1
                    self.queue_length_stat['b_queue_normal'].append(self.b_queue_length_normal)
                    self.b_queue_normal.append(component)
                else:
                    self.b_queue_length_emergency+=1
                    self.queue_length_stat['b_queue_emergency'].append(self.b_queue_length_emergency)
                    self.b_queue_emergency.append(component)
        else:
            if self.e_status<self.e_worker_num:
                old_status = self.e_status
                self.e_status+=1
                self.update_utilization('e', old_status, self.e_status)
                serve_time = r.uniform(40-5,40+5)
                self.fel.append(( self.time + serve_time , 'end_e', component))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                if type==0:
                    self.e_queue_length_normal+=1
                    self.queue_length_stat['e_queue_normal'].append(self.e_queue_length_normal)
                    self.e_queue_normal.append(component)
                else:
                    self.e_queue_length_emergency+=1
                    self.queue_length_stat['e_queue_emergency'].append(self.e_queue_length_emergency)
                    self.e_queue_emergency.append(component)
        
        if self.d_queue_length_emergency>0:
            self.d_queue_length_emergency-=1
            self.queue_length_stat['d_queue_emergency'].append(self.d_queue_length_emergency)
            component_pop = self.d_queue_emergency.pop(0)
            serve_time = r.uniform(50-40,50+40)
            self.fel.append(( self.time + serve_time , 'end_d', component_pop))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if self.d_queue_length_normal>0:
                self.d_queue_length_normal-=1
                self.queue_length_stat['d_queue_normal'].append(self.d_queue_length_normal)
                component_pop = self.d_queue_normal.pop(0)
                serve_time = r.uniform(50-40,50+40)
                self.fel.append(( self.time + serve_time , 'end_d', component_pop))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                old_status = self.d_status
                self.d_status-=1
                self.update_utilization('d', old_status, self.d_status)
    
    def end_e(self,component):
        type = component.type

        component.leave_time = self.time
        self.leaved_components.append(component)
        ind = component.index
        for i in self.entered_components:
            if i.index==ind:
                self.entered_components.remove(i)

        if self.e_queue_length_emergency>0:
            self.e_queue_length_emergency-=1
            self.queue_length_stat['e_queue_emergency'].append(self.e_queue_length_emergency)
            component_pop = self.e_queue_emergency.pop(0)
            serve_time = r.uniform(40-5,40+5)
            self.fel.append(( self.time + serve_time , 'end_e', component_pop))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if self.e_queue_length_normal>0:
                self.e_queue_length_normal-=1
                self.queue_length_stat['e_queue_normal'].append(self.e_queue_length_normal)
                component_pop = self.e_queue_normal.pop(0)
                serve_time = r.uniform(40-5,40+5)
                self.fel.append(( self.time + serve_time , 'end_e', component_pop))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                old_status = self.e_status
                self.e_status-=1
                self.update_utilization('e', old_status, self.e_status)

    def run_system(self,final_time):
        if self.start_time == 0:
            self.start_time = self.time
            
        while self.time<final_time:
            action = self.fel.pop(0)
            self.time = action[0]
            if action[1]=='end_a':
                self.end_a(action[2])
            elif action[1]=='end_b':
                self.end_b(action[2])
            elif action[1]=='end_c':
                self.end_c(action[2])
            elif action[1]=='end_d':
                self.end_d(action[2])
            elif action[1]=='end_e':
                self.end_e(action[2])
            elif action[1]=='enter':
                self.enter(action[2])
            elif action[1]=='end_of_closure':
                self.end_of_closure()
            elif action[1]=='end_of_open':
                self.end_of_open()

    def finalize_utilization(self):
        """Finalize utilization calculations at end of simulation"""
        for station in self.utilization_data:
            station_data = self.utilization_data[station]
            time_interval = self.time - station_data['last_change_time']
            if station_data['last_status'] > 0:
                station_data['total_busy_time'] += station_data['last_status'] * time_interval

    def print_results(self):
        print('-----------------------------')
        
        # Average total time in system
        sum_total_time = 0
        for component in self.leaved_components:
            sum_total_time += (component.leave_time - component.enter_time)
        avg_total_time = sum_total_time/len(self.leaved_components)
        self.avg_total_time = avg_total_time
        print(f'avg total time in system : {avg_total_time:.2f} ')
        
        # Number out of system
        print(f'number out of system: {len(self.leaved_components)}')
        
        print('-----------------------------')
        # Station utilization
        self.finalize_utilization()
        total_simulation_time = self.time - self.start_time
        
        worker_counts = {'a': self.a_worker_num, 'b': self.b_worker_num, 'c': 1, 'd': self.d_worker_num, 'e': self.e_worker_num}
        
        for station in ['a', 'b', 'c', 'd', 'e']:
            station_data = self.utilization_data[station]
            total_possible_time = total_simulation_time * worker_counts[station]
            
            if total_possible_time > 0:
                utilization = (station_data['total_busy_time'] / total_possible_time) * 100
            else:
                utilization = 0
                
            print(f'avg utilization of station {station}: {utilization:.2f}%')

def main():
    simulations = []
    avg_total_time_for_10_sim = 0
    
    for i in range(10):
        sim = simulator()
        sim.fel.extend([(0,'enter', Component(0,0)),(0,'enter', Component(1,0)),(60,'end_of_open')])
        
        warm_up_time = 2*60
        sim.run_system(warm_up_time)
        
        sim.leaved_components = []
        sim.start_time = sim.time  # Reset start time for utilization calculation
        for station in sim.utilization_data:
            sim.utilization_data[station]['total_busy_time'] = 0
            sim.utilization_data[station]['last_change_time'] = sim.time
        
        final_time = 8*60
        sim.run_system(final_time)
        
        simulations.append(sim)
        print(f'=====results for simulation {i}=====')
        sim.print_results()
        avg_total_time_for_10_sim += sim.avg_total_time
    
    avg_total_time_for_10_sim = avg_total_time_for_10_sim/10
    print(f'avg total time in system for 10 simulations : {avg_total_time_for_10_sim} ')

if __name__=='__main__':
    main()