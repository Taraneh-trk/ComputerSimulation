import numpy as np

simulate_number = 0

sandwich_queue_len = 0
main_food_queue_len = 0
cashier_queue_len = 0

sandwich_status = 0
main_food_status = 0
cashier_status = 0

FEL = []
FEL.append((0, 'arrival'))

sandwich_queue_history = []
sandwich_time_history = []
sandwich_time_history.append(0)
sandwich_queue_history.append(0)

main_food_queue_history = []
main_food_time_history = []
main_food_time_history.append(0)
main_food_queue_history.append(0)

cashier_queue_history = []
cashier_time_history = []
cashier_time_history.append(0)
cashier_queue_history.append(0)

sum_busy_sandwich = 0
sum_busy_main_food = 0
sum_busy_cashier = 0

start_time_sandwich = 0
start_time_main_food = 0
start_time_cashier = 0

current_time = 0
service_time = 0
between_arrival_time = 0

customer_id_counter = 0
customers = {}

STATES = {
    'SANDWICH_QUEUE': 'Waiting in sandwich queue',
    'SANDWICH_SERVICE': 'Being served at sandwich station',
    'MAIN_FOOD_QUEUE': 'Waiting in main food queue',
    'MAIN_FOOD_SERVICE': 'Being served at main food station',
    'CASHIER_QUEUE': 'Waiting in cashier queue',
    'CASHIER_SERVICE': 'Being served by cashier',
    'EATING': 'Eating food',
    'DESSERT': 'Having dessert',
    'EXITED': 'Left the cafeteria'
}

LOCATIONS = {
    'SANDWICH_AREA': 'Sandwich area',
    'MAIN_FOOD_AREA': 'Main food area',
    'CASHIER_AREA': 'Cashier area',
    'DINING_AREA': 'Dining area',
    'OUTSIDE': 'Outside cafeteria'
}


def arrival():
    global current_time, sandwich_status, sandwich_queue_len, main_food_status, main_food_queue_len, start_time_sandwich, start_time_main_food, sandwich_time_history, sandwich_queue_history, main_food_time_history, main_food_queue_history, customer_id_counter
    
    customer_id_counter += 1
    cust_id = customer_id_counter
    
    r = np.random.random()
    if r <= 0.4:
        if sandwich_status == 1:
            sandwich_queue_len += 1
            sandwich_time_history.append(current_time)
            sandwich_queue_history.append(sandwich_queue_len)
            customers[cust_id] = {
                'state': STATES['SANDWICH_QUEUE'],
                'location': LOCATIONS['SANDWICH_AREA'],
                'arrival_time': current_time
            }
        else:
            sandwich_status = 1
            start_time_sandwich = current_time
            service_time = np.random.randint(30, 91)
            FEL.append((service_time + current_time, 'sandwich_prepration', cust_id))
            FEL.sort()
            customers[cust_id] = {
                'state': STATES['SANDWICH_SERVICE'],
                'location': LOCATIONS['SANDWICH_AREA'],
                'arrival_time': current_time
            }
    else:
        if main_food_status == 1:
            main_food_queue_len += 1
            main_food_time_history.append(current_time)
            main_food_queue_history.append(main_food_queue_len)
            customers[cust_id] = {
                'state': STATES['MAIN_FOOD_QUEUE'],
                'location': LOCATIONS['MAIN_FOOD_AREA'],
                'arrival_time': current_time
            }
        else:
            main_food_status = 1
            start_time_main_food = current_time
            service_time = np.random.randint(15, 76)
            FEL.append((service_time + current_time, 'main_food_prepration', cust_id))
            FEL.sort()
            customers[cust_id] = {
                'state': STATES['MAIN_FOOD_SERVICE'],
                'location': LOCATIONS['MAIN_FOOD_AREA'],
                'arrival_time': current_time
            }
    
    service_time = np.random.randint(10, 51)
    FEL.append((service_time + current_time, 'arrival'))
    FEL.sort()


def sandwich_prepration(cust_id=None):
    global cashier_status, current_time, sandwich_status, sandwich_queue_len, main_food_status, main_food_queue_len, start_time_sandwich, start_time_main_food, sandwich_time_history, sandwich_queue_history, main_food_time_history, main_food_queue_history, cashier_time_history, cashier_queue_history, start_time_cashier, sum_busy_sandwich, cashier_queue_len
    
    if cust_id is not None:
        if cashier_status == 1:
            cashier_queue_len += 1
            cashier_time_history.append(current_time)
            cashier_queue_history.append(cashier_queue_len)
            customers[cust_id]['state'] = STATES['CASHIER_QUEUE']
            customers[cust_id]['location'] = LOCATIONS['CASHIER_AREA']
        else:
            cashier_status = 1
            start_time_cashier = current_time
            service_time = np.random.randint(20, 41)
            FEL.append((service_time + current_time, 'pay_end', cust_id))
            FEL.sort()
            customers[cust_id]['state'] = STATES['CASHIER_SERVICE']
            customers[cust_id]['location'] = LOCATIONS['CASHIER_AREA']
    
    if sandwich_queue_len > 0:
        next_cust_id = None
        for cid, info in customers.items():
            if info['state'] == STATES['SANDWICH_QUEUE']:
                next_cust_id = cid
                break
        
        if next_cust_id:
            sandwich_queue_len -= 1
            sandwich_time_history.append(current_time)
            sandwich_queue_history.append(sandwich_queue_len)
            service_time = np.random.randint(30, 91)
            FEL.append((service_time + current_time, 'sandwich_prepration', next_cust_id))
            FEL.sort()
            customers[next_cust_id]['state'] = STATES['SANDWICH_SERVICE']
    else:
        sandwich_status = 0
        sum_busy_sandwich += (current_time - start_time_sandwich)


def main_food_prepration(cust_id=None):
    global cashier_queue_len, cashier_status, current_time, sandwich_status, sandwich_queue_len, main_food_status, main_food_queue_len, start_time_sandwich, start_time_main_food, sandwich_time_history, sandwich_queue_history, main_food_time_history, main_food_queue_history, cashier_time_history, cashier_queue_history, start_time_cashier, sum_busy_main_food
    
    if cust_id is not None:
        if cashier_status == 1:
            cashier_queue_len += 1
            cashier_time_history.append(current_time)
            cashier_queue_history.append(cashier_queue_len)
            customers[cust_id]['state'] = STATES['CASHIER_QUEUE']
            customers[cust_id]['location'] = LOCATIONS['CASHIER_AREA']
        else:
            cashier_status = 1
            start_time_cashier = current_time
            service_time = np.random.randint(20, 41)
            FEL.append((service_time + current_time, 'pay_end', cust_id))
            FEL.sort()
            customers[cust_id]['state'] = STATES['CASHIER_SERVICE']
            customers[cust_id]['location'] = LOCATIONS['CASHIER_AREA']
    
    if main_food_queue_len > 0:
        next_cust_id = None
        for cid, info in customers.items():
            if info['state'] == STATES['MAIN_FOOD_QUEUE']:
                next_cust_id = cid
                break
        
        if next_cust_id:
            main_food_queue_len -= 1
            main_food_time_history.append(current_time)
            main_food_queue_history.append(main_food_queue_len)
            service_time = np.random.randint(15, 76)
            FEL.append((service_time + current_time, 'main_food_prepration', next_cust_id))
            FEL.sort()
            customers[next_cust_id]['state'] = STATES['MAIN_FOOD_SERVICE']
    else:
        main_food_status = 0
        sum_busy_main_food += (current_time - start_time_main_food)


def pay_end(cust_id=None):
    global sum_busy_cashier, cashier_status, current_time, sandwich_status, sandwich_queue_len, main_food_status, main_food_queue_len, start_time_sandwich, start_time_main_food, sandwich_time_history, sandwich_queue_history, main_food_time_history, main_food_queue_history, cashier_time_history, cashier_queue_history, start_time_cashier, cashier_queue_len
    
    if cust_id is not None:
        service_time = np.random.randint(10 * 60, 30 * 60 + 1)
        FEL.append((service_time + current_time, 'eat_end', cust_id))
        FEL.sort()
        customers[cust_id]['state'] = STATES['EATING']
        customers[cust_id]['location'] = LOCATIONS['DINING_AREA']
    
    if cashier_queue_len > 0:
        next_cust_id = None
        for cid, info in customers.items():
            if info['state'] == STATES['CASHIER_QUEUE']:
                next_cust_id = cid
                break
        
        if next_cust_id:
            cashier_queue_len -= 1
            cashier_time_history.append(current_time)
            cashier_queue_history.append(cashier_queue_len)
            service_time = np.random.randint(20, 41)
            FEL.append((service_time + current_time, 'pay_end', next_cust_id))
            FEL.sort()
            customers[next_cust_id]['state'] = STATES['CASHIER_SERVICE']
    else:
        cashier_status = 0
        sum_busy_cashier += (current_time - start_time_cashier)


def eat_end(cust_id=None):
    global simulate_number, current_time, sandwich_status, sandwich_queue_len, main_food_status, main_food_queue_len, start_time_sandwich, start_time_main_food, sandwich_time_history, sandwich_queue_history, main_food_time_history, main_food_queue_history
    
    if cust_id is not None:
        r = np.random.random()
        if r <= 0.1:
            service_time = np.random.randint(8 * 60, 12 * 60 + 1)
            FEL.append((service_time + current_time, 'dessert_end', cust_id))
            FEL.sort()
            customers[cust_id]['state'] = STATES['DESSERT']
            customers[cust_id]['location'] = LOCATIONS['DINING_AREA']
        else:
            customers[cust_id]['state'] = STATES['EXITED']
            customers[cust_id]['location'] = LOCATIONS['OUTSIDE']
            simulate_number += 1


def dessert_end(cust_id=None):
    global simulate_number
    
    if cust_id is not None:
        customers[cust_id]['state'] = STATES['EXITED']
        customers[cust_id]['location'] = LOCATIONS['OUTSIDE']
    simulate_number += 1


def report_customer_status():
    """Generate a report of customers currently in the cafeteria and their activities"""
    remaining_customers = 0
    location_counts = {loc: 0 for loc in LOCATIONS.values()}
    activity_counts = {state: 0 for state in STATES.values()}
    
    print("\n===== CUSTOMER STATUS REPORT =====")
    print("ID\tLocation\t\tActivity")
    print("-" * 60)
    
    exited = 0
    for cust_id, info in sorted(customers.items()):
        if info['state'] != STATES['EXITED']:
            remaining_customers += 1
            location_counts[info['location']] += 1
            activity_counts[info['state']] += 1
            print(f"{cust_id}\t{info['location']}\t\t{info['state']}")
        else:
            exited+=1
    
    print("\n===== SUMMARY =====")
    print(f"Total customers remaining in cafeteria: {remaining_customers}, exited customers : {exited}")
    print("\nLocation distribution:")
    for loc, count in location_counts.items():
        if loc != LOCATIONS['OUTSIDE'] and count > 0:
            print(f"- {loc}: {count} customers")
    
    print("\nActivity distribution:")
    for activity, count in activity_counts.items():
        if activity != STATES['EXITED'] and count > 0:
            print(f"- {activity}: {count} customers")
    
    return remaining_customers


def main():
    global sum_busy_main_food, sum_busy_cashier, sum_busy_sandwich, cashier_status, current_time, sandwich_status, sandwich_queue_len, main_food_status, main_food_queue_len, start_time_sandwich, start_time_main_food, sandwich_time_history, sandwich_queue_history, main_food_time_history, main_food_queue_history, cashier_time_history, cashier_queue_history, start_time_cashier

    simulate_max_number = int(input('Enter the Simulation Number: '))
    while (simulate_number < simulate_max_number):
        event = FEL.pop(0)
        
        if len(event) == 3:
            current_time, event_type, cust_id = event
        else:
            current_time, event_type = event
            cust_id = None
        
        if event_type == 'arrival':
            arrival()
        elif event_type == 'sandwich_prepration':
            sandwich_prepration(cust_id)
        elif event_type == 'main_food_prepration':
            main_food_prepration(cust_id)
        elif event_type == 'pay_end':
            pay_end(cust_id)
        elif event_type == 'eat_end':
            eat_end(cust_id)
        elif event_type == 'dessert_end':
            dessert_end(cust_id)
        else:
            continue

    if sandwich_status == 1:
        sum_busy_sandwich += (current_time - start_time_sandwich)
    if main_food_status == 1:
        sum_busy_main_food += (current_time - start_time_main_food)
    if cashier_status == 1:
        sum_busy_cashier += (current_time - start_time_cashier)

    sandwich_time_history.append(current_time)
    sandwich_queue_history.append(sandwich_queue_len)
    main_food_time_history.append(current_time)
    main_food_queue_history.append(main_food_queue_len)
    cashier_time_history.append(current_time)
    cashier_queue_history.append(cashier_queue_len)

    length = len(sandwich_time_history)
    avg_queue_s = 0
    for i in range(length - 1):
        avg_queue_s += (sandwich_time_history[i + 1] - sandwich_time_history[i]) * sandwich_queue_history[i]
    avg_queue_s = avg_queue_s / current_time

    length = len(main_food_time_history)
    avg_queue_mf = 0
    for i in range(length - 1):
        avg_queue_mf += (main_food_time_history[i + 1] - main_food_time_history[i]) * main_food_queue_history[i]
    avg_queue_mf = avg_queue_mf / current_time

    length = len(cashier_time_history)
    avg_queue_c = 0
    for i in range(length - 1):
        avg_queue_c += (cashier_time_history[i + 1] - cashier_time_history[i]) * cashier_queue_history[i]
    avg_queue_c = avg_queue_c / current_time

    busy_percent_sandwich = float(sum_busy_sandwich / current_time)
    busy_percent_main_food = float(sum_busy_main_food / current_time)
    busy_percent_cashier = float(sum_busy_cashier / current_time)

    print('\n===== SIMULATION STATISTICS =====')
    print('Sandwich maker is busy', 100 * busy_percent_sandwich, '%')
    print('Main food maker is busy', 100 * busy_percent_main_food, '%')
    print('Cashier is busy', 100 * busy_percent_cashier, '%')

    print('Average Length of sandwich Queue is', float(avg_queue_s))
    print('Average Length of main food Queue is', float(avg_queue_mf))
    print('Average Length of cashier Queue is', float(avg_queue_c))
    
    report_customer_status()


if __name__ == '__main__':
    main()