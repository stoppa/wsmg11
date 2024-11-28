import urequests
import ujson
import check_daytime as cd
from time import localtime, mktime, time

#Smart controle API url
API_URL = "https://apis.smartenergy.at/market/v1/price"

def get_cheapest_hours(hours=3, prt=False):
    
    try:
        # API request
        response = urequests.get(API_URL)
        
        if response.status_code == 200:
            
            data = ujson.loads(response.text)
            
            if "data" in data and isinstance(data["data"], list):
                
                prices = data["data"]
                
                current_time = cd.get_time(raw=True)
                price_list = []
                
                for price_entry in prices:
                    
                    try:
                        
                        date = tuple(map(int, [
                            price_entry["date"][:4],      # Year
                            price_entry["date"][5:7],    # Month
                            price_entry["date"][8:10],   # Day
                            price_entry["date"][11:13],  # Hour
                            price_entry["date"][14:16],  # Minute
                            price_entry["date"][17:19]   # Second
                        ]))
                        
                        full_date = date + (0, 0, -1)  # Add weekday, yearday, and DST
                        timestamp = mktime(full_date)
                        
                        if timestamp > current_time:
                            
                            price_list.append((timestamp, price_entry["value"]))
                            
                    except Exception as e:
                        print(f"Error parsing date: {e}")
                
                # Sort prices by timestamp
                price_list.sort(key=lambda x: x[0])
                
                def find_best_start(start_time=None, end_time=None):
                    
                    """Helper function to find the best start time within a specific range."""
                    min_cost = float('inf')
                    best_start = None
                    best_prices = []
                    
                    for i in range(len(price_list) - hours * 4 + 1):
                        
                        block_start_time = price_list[i][0]
                        
                        if start_time and block_start_time < start_time:
                            continue
                        if end_time and block_start_time + hours * 3600 > end_time:
                            break
                        
                        current_cost = sum(price_list[j][1] for j in range(i, i + hours * 4))
                        
                        if current_cost < min_cost:
                            
                            min_cost = current_cost
                            best_start = block_start_time
                            best_prices = [price_list[j][1] for j in range(i, i + hours * 4)]
                    
                    return best_start, best_prices
                
                # 1. Best start within the next 10 hours
                next_10h_end = current_time + 10 * 3600
                next_10h_start, next_10h_prices = find_best_start(current_time, next_10h_end)
                
                # 2. Best start in the entire timeframe
                full_period_start, full_period_prices = find_best_start()
                
                # 3. Best start between 0 and 6 AM of the next day if boiler=True
                boiler_start = boiler_end = boiler_prices = None
                    
                tomorrow = localtime(current_time + 24 * 3600)
                next_day_start = mktime((tomorrow[0], tomorrow[1], tomorrow[2], 0, 0, 0, -1, -1, -1))
                next_day_end = next_day_start + 6 * 3600
                boiler_start, boiler_prices = find_best_start(next_day_start, next_day_end)
                boiler_end = boiler_start + hours * 3600 if boiler_start else None
            
                # Time difference helper
                def time_diff(target_time):
                    
                    if target_time:
                        diff_seconds = target_time - current_time
                        hours = diff_seconds // 3600
                        minutes = (diff_seconds % 3600) // 60
                        return hours, minutes
                    return None, None
                
                # Calculate time differences
                next_10h_hours, next_10h_minutes = time_diff(next_10h_start)
                full_period_hours, full_period_minutes = time_diff(full_period_start)
                
                # LED activation check
                led = False
                if next_10h_start < current_time and (next_10h_start + 1800) > current_time:  # Within 1 minute
                    led = True
                
                # Formatting and output
                def format_time(timestamp):
                    if timestamp:
                        time = localtime(timestamp)
                        return f"{time[3]:02d}:{time[4]:02d}"
                    return "N/A"
                
                if prt:
                    print(f"Best start in next 10 hours: {format_time(next_10h_start)}")
                    print(f"Time until next start: {next_10h_hours}h {next_10h_minutes}m")
                    print(f"Best start overall: {format_time(full_period_start)}")
                    print(f"Time until overall start: {full_period_hours}h {full_period_minutes}m")
                    print(f"Best boiler start: {format_time(boiler_start)}")
                
                return {
                    "next_10h": {
                        "start": next_10h_start,
                        "end": next_10h_start + hours * 3600 if next_10h_start else None,
                        "time_until_start": (next_10h_hours, next_10h_minutes),
                        "led_on": led
                    },
                    "full_period": {
                        "start": full_period_start,
                        "end": full_period_start + hours * 3600 if full_period_start else None,
                        "time_until_start": (full_period_hours, full_period_minutes)
                    },
                    "boiler": {
                        "start": boiler_start,
                        "end": boiler_end
                    }
                }
            else:
                print("Unexpected data format from API.")
        else:
            print(f"Error retrieving API data: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")







