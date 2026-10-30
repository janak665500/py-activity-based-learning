"""
Case Study 45: Weekly Electricity Consumption Matrix
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Description:
Processes appliance-wise electrical consumption readings across 7 days of the week.
Computes daily and appliance-wise totals, identifies quota threshold violations,
detects peak consumption surges, and estimates weekly billing costs.
Concepts Used: 2D Nested Lists, Row & Column Iterations, Min/Max Detection,
               Conditional Statements, Tuples, and Tabular Formatting.
"""

def print_banner(title):
    border = "=" * 88
    print(border)
    print(title.center(88))
    print(border)

def calculate_electricity_bill(total_units):
    """
    Tiered slab tariff:
    - First 50 units  @ INR 3.50 / unit
    - Next 50 units   @ INR 5.00 / unit
    - Above 100 units @ INR 7.50 / unit
    Fixed charges     : INR 65.00
    """
    fixed_charge = 65.0
    energy_charge = 0.0
    remaining = total_units
    
    if remaining > 100:
        energy_charge += (remaining - 100) * 7.50
        remaining = 100
    if remaining > 50:
        energy_charge += (remaining - 50) * 5.00
        remaining = 50
    energy_charge += remaining * 3.50
    
    total_bill = energy_charge + fixed_charge
    return round(energy_charge, 2), fixed_charge, round(total_bill, 2)

def analyze_electricity_matrix(appliances, days, consumption_matrix, daily_limit=24.0, appliance_limit=35.0):
    num_appliances = len(appliances)
    num_days = len(days)
    
    print_banner("HOUSEHOLD WEEKLY ELECTRICITY CONSUMPTION AUDIT")
    print(f"Audit Horizon           : 7 Full Operating Days ({days[0]} to {days[-1]})")
    print(f"Daily Safety Limit      : {daily_limit:.1f} kWh / day")
    print(f"Weekly Appliance Quota  : {appliance_limit:.1f} kWh / week\n")
    
    # 1. Print Consumption Matrix with Row Totals
    col_w = 8
    day_headers = "".join([f"{d:>{col_w}}" for d in days])
    header_line = f"{'#':<3} {'Appliance':<26}{day_headers} {'Total':>9} {'Avg/Day':>9}  {'Audit Status'}"
    print(header_line)
    print("-" * len(header_line))
    
    appliance_totals = []
    over_limit_appliances = []
    
    peak_val = -1.0
    peak_appliance = ""
    peak_day = ""
    
    for r in range(num_appliances):
        app_name = appliances[r]
        readings = consumption_matrix[r]
        row_tot = round(sum(readings), 2)
        row_avg = round(row_tot / num_days, 2)
        appliance_totals.append(row_tot)
        
        # Check peak event
        for c in range(num_days):
            val = readings[c]
            if val > peak_val:
                peak_val = val
                peak_appliance = app_name
                peak_day = days[c]
                
        # Check weekly appliance threshold
        if row_tot > appliance_limit:
            status = "QUOTA EXCEEDED [ALERT]"
            over_limit_appliances.append((app_name, row_tot, row_tot - appliance_limit))
        else:
            status = "Within Quota"
            
        row_cells = "".join([f"{val:>{col_w}.1f}" for val in readings])
        print(f"{r+1:<3} {app_name:<26}{row_cells} {row_tot:>9.1f} {row_avg:>9.1f}  {status}")
        
    print("-" * len(header_line))
    
    # 2. Day-Wise Column Totals
    daily_totals = []
    over_limit_days = []
    
    for c in range(num_days):
        day_sum = 0.0
        for r in range(num_appliances):
            day_sum += consumption_matrix[r][c]
        day_sum = round(day_sum, 2)
        daily_totals.append(day_sum)
        if day_sum > daily_limit:
            over_limit_days.append((days[c], day_sum, round(day_sum - daily_limit, 2)))
            
    grand_total = round(sum(daily_totals), 2)
    daily_avg_overall = round(grand_total / num_days, 2)
    
    # Print Day Totals row
    day_tot_cells = "".join([f"{dt:>{col_w}.1f}" for dt in daily_totals])
    print(f"{'':<3} {'DAILY TOTAL (kWh)':<26}{day_tot_cells} {grand_total:>9.1f} {daily_avg_overall:>9.1f}")
    print("-" * len(header_line))
    
    # 3. Peak Event & Threshold Breach Analysis
    print("\nSURGE & PEAK LOAD ANALYSIS:")
    print(f"[*] Peak Single Consumption Event : {peak_val:.2f} kWh by '{peak_appliance}' on {peak_day}.")
    
    print("\nDAILY HOUSEHOLD LIMIT AUDIT (> 24.0 kWh):")
    if len(over_limit_days) == 0:
        print("[OK] Daily consumption remained strictly within safety limit across all 7 days.")
    else:
        for d_name, d_tot, breach in over_limit_days:
            print(f"[!] {d_name}: Total {d_tot:.1f} kWh exceeded safety threshold by +{breach:.1f} kWh.")
            
    print("\nAPPLIANCE QUOTA BREACH AUDIT (> 35.0 kWh/week):")
    if len(over_limit_appliances) == 0:
        print("[OK] All appliances operated within weekly assigned energy budget.")
    else:
        for a_name, a_tot, excess in over_limit_appliances:
            print(f"[!] '{a_name}': Used {a_tot:.1f} kWh, exceeding assigned quota by +{excess:.1f} kWh.")
            
    # 4. Weekly Cost Estimation
    energy_chg, fix_chg, net_bill = calculate_electricity_bill(grand_total)
    print("\nESTIMATED TARIFF & BILLING BREAKDOWN:")
    print(f"- Cumulative Energy Consumed : {grand_total:.2f} kWh")
    print(f"- Energy Charges (Slab rate) : INR {energy_chg:,.2f}")
    print(f"- Grid Fixed Maintenance Fee : INR {fix_chg:,.2f}")
    print(f"- Estimated Net Weekly Bill  : INR {net_bill:,.2f}")

if __name__ == "__main__":
    appliance_names = [
        "Air Conditioner (2.0 TR)",
        "Refrigerator (Double Door)",
        "Geyser / Water Heater",
        "Washing Machine",
        "Lighting & Ceiling Fans",
        "Microwave & Induction"
    ]
    
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    # 6 Appliances x 7 Days Consumption (kWh)
    weekly_matrix = [
        [7.5, 8.0, 7.8, 8.2, 9.0, 11.5, 12.0],  # AC (Heavy weekend usage)
        [2.2, 2.1, 2.3, 2.2, 2.4,  2.5,  2.4],  # Fridge (Steady)
        [4.0, 3.8, 4.2, 3.9, 4.1,  4.5,  4.8],  # Geyser
        [0.0, 1.5, 0.0, 1.6, 0.0,  2.2,  2.0],  # Washing machine (alternate days)
        [3.0, 3.2, 3.1, 3.0, 3.5,  4.0,  4.2],  # Lights & Fans
        [1.8, 1.5, 1.9, 1.6, 2.0,  2.8,  3.0]   # Kitchen Appliances
    ]
    
    analyze_electricity_matrix(appliance_names, days_of_week, weekly_matrix, daily_limit=24.0, appliance_limit=35.0)

