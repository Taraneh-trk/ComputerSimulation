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

        self.a_queue_length_normal = 0
        self.a_queue_length_emergency = 0
        self.a_status = 0
        self.a_queue_normal = []
        self.a_queue_emergency = []
        self.a_worker_num = 1
        # self.a_worker_num = 2

        self.b_queue_length_normal = 0
        self.b_queue_length_emergency = 0
        self.b_status = 0
        self.b_queue_normal = []
        self.b_queue_emergency = []
        self.b_worker_num = 3
        # self.b_worker_num = 4

        self.c_queue_length = 0
        self.c_status = 0
        self.c_queue = []
        self.c_serve_time = 20
        # self.c_serve_time = 16

        self.d_queue_length_normal = 0
        self.d_queue_length_emergency = 0
        self.d_status = 0
        self.d_queue_normal = []
        self.d_queue_emergency = []
        self.d_worker_num = 4
        # self.d_worker_num = 5

        self.e_queue_length_normal = 0
        self.e_queue_length_emergency = 0
        self.e_status = 0
        self.e_queue_normal = []
        self.e_queue_emergency = []
        self.e_worker_num = 3
        # self.e_worker_num = 4

        self.leaved_components = []
        self.entered_components = []

    def enter(self,enter_component):
        type = enter_component.type
        self.entered_components.append(enter_component)
        if type==0:
            if self.a_status<self.a_worker_num:
                self.a_status += 1
                serve_time = r.uniform(12-2,12+2)
                self.fel.append(( self.time + serve_time , 'end_a', enter_component))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                self.a_queue_length_normal+=1
                self.a_queue_normal.append(enter_component)
            enter_interval = r.uniform(15-13,15+13)
            self.fel.append(( self.time + enter_interval , 'enter', Component(0, self.time + enter_interval)))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if self.a_status<self.a_worker_num:
                self.a_status += 1
                serve_time = r.uniform(12-2,12+2)
                self.fel.append(( self.time + serve_time , 'end_a', enter_component))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                self.a_queue_length_emergency+=1
                self.a_queue_emergency.append(enter_component)
            enter_interval = r.uniform((4-3)*60,(4+3)*60)
            self.fel.append(( self.time + enter_interval , 'enter', Component(1, self.time + enter_interval)))
            self.fel = sorted(self.fel,key=lambda x : x[0])
    
    def end_a(self,component):
        type = component.type
        if self.b_status<self.b_worker_num:
            self.b_status += 1
            serve_time = r.uniform(40-20,40+20)
            self.fel.append(( self.time + serve_time , 'end_b', component))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if type==0:
                self.b_queue_length_normal+=1
                self.b_queue_normal.append(component)
            else:
                self.b_queue_length_emergency+=1
                self.b_queue_emergency.append(component)
        
        if self.a_queue_length_emergency>0:
            self.a_queue_length_emergency-=1
            component_poped = self.a_queue_emergency.pop(0)
            serve_time = r.uniform(12-2,12+2)
            self.fel.append(( self.time + serve_time , 'end_a', component_poped))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if self.a_queue_length_normal>0:
                self.a_queue_length_normal-=1
                component_poped = self.a_queue_normal.pop(0)
                serve_time = r.uniform(12-2,12+2)
                self.fel.append(( self.time + serve_time , 'end_a', component_poped))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                self.a_status -= 1

    def end_b(self,component):
        type = component.type
        if component.return_from_d==0:
            random_number = r.uniform(0,1)
            if random_number<=0.4:
                if self.d_status<self.d_worker_num:
                    self.d_status+=1
                    serve_time = r.uniform(50-40,50+40)
                    self.fel.append(( self.time + serve_time , 'end_d', component))
                    self.fel = sorted(self.fel,key=lambda x : x[0])
                else:
                    if type==0:
                        self.d_queue_length_normal+=1
                        self.d_queue_normal.append(component)
                    else:
                        self.d_queue_length_emergency+=1
                        self.d_queue_emergency.append(component)
            else:
                if self.c_status==0:
                    self.c_status=1
                    serve_time = self.c_serve_time
                    self.fel.append(( self.time + serve_time , 'end_c', component)) 
                    self.fel = sorted(self.fel,key=lambda x : x[0])
                else:
                    self.c_queue_length+=1
                    self.c_queue.append(component)
        else:
            if self.d_status<self.d_worker_num:
                self.d_status+=1
                serve_time = r.uniform(50-40,50+40)
                self.fel.append(( self.time + serve_time , 'end_d', component))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                if type==0:
                    self.d_queue_length_normal+=1
                    self.d_queue_normal.append(component)
                else:
                    self.d_queue_length_emergency+=1
                    self.d_queue_emergency.append(component)
        
        if self.b_queue_length_emergency>0:
            self.b_queue_length_emergency-=1
            component_pop = self.b_queue_emergency.pop(0)
            serve_time = r.uniform(40-20,40+20)
            self.fel.append(( self.time + serve_time , 'end_b', component_pop))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if self.b_queue_length_normal>0:
                self.b_queue_length_normal-=1
                component_pop = self.b_queue_normal.pop(0)
                serve_time = r.uniform(40-20,40+20)
                self.fel.append(( self.time + serve_time , 'end_b', component_pop))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                self.b_status-=1
    
    def end_c(self,component):
        type = component.type
        if self.d_status<self.d_worker_num:
            self.d_status+=1
            serve_time = r.uniform(50-40,50+40)
            self.fel.append(( self.time + serve_time , 'end_d', component))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if type==0:
                self.d_queue_length_normal+=1
                self.d_queue_normal.append(component)
            else:
                self.d_queue_length_emergency+=1
                self.d_queue_emergency.append(component)
        
        if self.c_status==2:
            self.c_status=-1
            end_of_closure_time = r.uniform(10-1,10+1)
            self.fel.append(( self.time + end_of_closure_time , 'end_of_closure'))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        elif self.c_status==1:  #or just else they are equal
            if self.c_queue_length>0:
                self.c_queue_length-=1
                component_pop = self.c_queue.pop(0)
                serve_time = self.c_serve_time
                self.fel.append(( self.time + serve_time , 'end_c', component_pop))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                self.c_status=0
    
    def end_of_closure(self):
        if self.c_queue_length>0:
            self.c_queue_length-=1
            component_pop = self.c_queue.pop(0)
            self.c_status=1
            serve_time = self.c_serve_time
            self.fel.append(( self.time + serve_time , 'end_c', component_pop))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            self.c_status=0
        
        end_of_open_time = 2*60
        self.fel.append(( self.time + end_of_open_time , 'end_of_open'))
        self.fel = sorted(self.fel,key=lambda x : x[0])
    
    def end_of_open(self):
        if self.c_status==0:
            self.c_status=-1
            end_of_closure_time = r.uniform(10-1,10+1)
            self.fel.append(( self.time + end_of_closure_time , 'end_of_closure'))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            self.c_status=2
    
    def end_d(self,component):
        type = component.type
        random_number = r.uniform(0,1)
        if random_number<=0.1:
            component.return_from_d = 1
            if self.b_status<self.b_worker_num:
                self.b_status += 1
                serve_time = r.uniform(30-10,30+10)
                self.fel.append(( self.time + serve_time , 'end_b', component))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                if type==0:
                    self.b_queue_length_normal+=1
                    self.b_queue_normal.append(component)
                else:
                    self.b_queue_length_emergency+=1
                    self.b_queue_emergency.append(component)
        else:
            if self.e_status<self.e_worker_num:
                self.e_status+=1
                serve_time = r.uniform(40-5,40+5)
                self.fel.append(( self.time + serve_time , 'end_e', component))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                if type==0:
                    self.e_queue_length_normal+=1
                    self.e_queue_normal.append(component)
                else:
                    self.e_queue_length_emergency+=1
                    self.e_queue_emergency.append(component)
        
        if self.d_queue_length_emergency>0:
            self.d_queue_length_emergency-=1
            component_pop = self.d_queue_emergency.pop(0)
            serve_time = r.uniform(50-40,50+40)
            self.fel.append(( self.time + serve_time , 'end_d', component_pop))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if self.d_queue_length_normal>0:
                self.d_queue_length_normal-=1
                component_pop = self.d_queue_normal.pop(0)
                serve_time = r.uniform(50-40,50+40)
                self.fel.append(( self.time + serve_time , 'end_d', component_pop))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                self.d_status-=1
    
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
            component_pop = self.e_queue_emergency.pop(0)
            serve_time = r.uniform(40-5,40+5)
            self.fel.append(( self.time + serve_time , 'end_e', component_pop))
            self.fel = sorted(self.fel,key=lambda x : x[0])
        else:
            if self.e_queue_length_normal>0:
                self.e_queue_length_normal-=1
                component_pop = self.e_queue_normal.pop(0)
                serve_time = r.uniform(40-5,40+5)
                self.fel.append(( self.time + serve_time , 'end_e', component_pop))
                self.fel = sorted(self.fel,key=lambda x : x[0])
            else:
                self.e_status-=1

    def run_system(self,final_time):
        # print('start simulation....')
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
        # print('end simulation.')

    def print_results(self):
        sum_total_time = 0
        for component in self.leaved_components:
            sum_total_time += (component.leave_time - component.enter_time)
        avg_total_time = sum_total_time/len(self.leaved_components)
        self.avg_total_time = avg_total_time
        print(f'avg total time in system : {avg_total_time} ')

def main():
    simulations = []
    avg_total_time_for_10_sim = 0
    for i in range(10):
        sim = simulator()
        sim.fel.extend([(0,'enter', Component(0,0)),(0,'enter', Component(1,0)),(60,'end_of_open')])
        
        warm_up_time = 2*60
        sim.run_system(warm_up_time)
        
        sim.leaved_components = []
        
        final_time = 8*60
        sim.run_system(final_time)
        
        simulations.append(sim)
        print(f'results for simulation {i}')
        sim.print_results()
        avg_total_time_for_10_sim += sim.avg_total_time
    
    avg_total_time_for_10_sim = avg_total_time_for_10_sim/10
    print(f'avg total time in system for 10 simulations : {avg_total_time_for_10_sim} ')

if __name__=='__main__':
    main()