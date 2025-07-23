import numpy as np

def simulate_single_day():
    day_types = ['good', 'medium', 'bad']
    day_probs = [0.35, 0.45, 0.20]
    
    demand_dist = {
        'good': {40: 0.03, 50: 0.05, 60: 0.15, 70: 0.20, 80: 0.35, 90: 0.15, 100: 0.07},
        'medium': {40: 0.10, 50: 0.18, 60: 0.40, 70: 0.20, 80: 0.08, 90: 0.04, 100: 0.00},
        'bad': {40: 0.44, 50: 0.22, 60: 0.16, 70: 0.12, 80: 0.06, 90: 0.00, 100: 0.00}
    }
    
    day_type = np.random.choice(day_types, p=day_probs)
    
    curr_dist = demand_dist[day_type]
    demands = list(curr_dist.keys())
    probabilities = list(curr_dist.values())
    
    demand = np.random.choice(demands, p=probabilities)
    
    return demand

def calculate_profit(order_quantity, demand):
    purchase_price = 13
    selling_price = 20
    salvage_value = 2
    
    sales = min(demand, order_quantity)
    leftover = max(0, order_quantity - demand)
    lost_sales = max(0, demand - order_quantity)
    
    revenue = sales * selling_price
    salvage_revenue = leftover * salvage_value
    cost = order_quantity * purchase_price
    
    profit = revenue + salvage_revenue - cost
    return profit

def run_simulation(order_quantity, num_simulations=1000):
    profits = []
    for _ in range(num_simulations):
        demand = simulate_single_day()
        profit = calculate_profit(order_quantity, demand)
        profits.append(profit)
    
    return np.mean(profits)

order_quantities = range(40, 101, 10)
average_profits = []

for qty in order_quantities:
    avg_profit = run_simulation(qty)
    average_profits.append(avg_profit)
    print(f"Order Quantity: {qty}, Average Profit: {avg_profit:.2f}")

optimal_qty = order_quantities[np.argmax(average_profits)]
max_profit = max(average_profits)
print(f"\nOptimal order quantity: {optimal_qty}")
print(f"Expected daily profit: {max_profit:.2f}")