"""
Case Study 63: Multi-Product Price Fluctuation Analysis
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Description:
Tracks historical price trajectories of multiple retail and wholesale commodities over time.
Computes period-over-period percentage changes, peak-to-trough price variance,
identifies maximum single-period price fluctuations, and flags volatile products
breaching acceptable risk thresholds.
Concepts Used: Lists of Prices, Nested Loops, Min/Max Algorithms, Arithmetic Formulas,
               Conditional Statements, Tuples, Sorting via Algorithmic Swapping, and Tabular Reporting.
"""

def print_banner(title):
    border = "=" * 88
    print(border)
    print(title.center(88))
    print(border)

def calculate_fluctuations(price_series):
    """
    Computes period-over-period percentage shifts, maximum absolute shift,
    peak-to-trough range, and net change.
    """
    n = len(price_series)
    if n < 2:
        return [], 0.0, 0.0, 0.0
        
    shifts = []
    max_abs_shift = 0.0
    
    for i in range(1, n):
        prev = price_series[i - 1]
        curr = price_series[i]
        pct = round(((curr - prev) / prev) * 100.0, 2)
        shifts.append(pct)
        if abs(pct) > max_abs_shift:
            max_abs_shift = abs(pct)
            
    min_p = min(price_series)
    max_p = max(price_series)
    peak_trough_volatility = round(((max_p - min_p) / min_p) * 100.0, 2) if min_p > 0 else 0.0
    net_change = round(((price_series[-1] - price_series[0]) / price_series[0]) * 100.0, 2)
    
    return shifts, max_abs_shift, peak_trough_volatility, net_change

def analyze_market_fluctuations(products_dataset, periods, threshold_pct=15.0):
    num_products = len(products_dataset)
    num_periods = len(periods)
    
    print_banner("COMMODITY PRICE TRAJECTORY & VOLATILITY RISK AUDIT")
    print(f"Observation Horizon : {num_periods} Time Intervals ({periods[0]} to {periods[-1]})")
    print(f"Volatility Alert Threshold: Max Period Fluctuation > {threshold_pct:.1f}%\n")
    
    # 1. Period Prices Ledger
    col_w = 9
    period_headers = "".join([f"{p:>{col_w}}" for p in periods])
    print(f"{'ID':<7} {'Product Name':<22}{period_headers}")
    print("-" * (30 + col_w * num_periods))
    
    for prod in products_dataset:
        pid, name, cat, p_list = prod
        price_cells = "".join([f"{p:>{col_w}.2f}" for p in p_list])
        print(f"{pid:<7} {name:<22}{price_cells}")
    print("-" * (30 + col_w * num_periods))
    
    # 2. Volatility Analysis
    print("\nSECTION 2: PERIOD-OVER-PERIOD FLUCTUATION & RISK AUDIT")
    v_fmt = "{:<7} {:<20} {:>10} {:>10} {:>12} {:>12} {:>12} {:<18}"
    headers = ("ID", "Product Name", "Min P", "Max P", "Max Fluct %", "Range Vol %", "Net Shift %", "Risk Status")
    print(v_fmt.format(*headers))
    print("-" * 110)
    
    audit_results = []
    flagged_products = []
    
    for prod in products_dataset:
        pid, name, cat, p_list = prod
        shifts, max_fluct, range_vol, net_shift = calculate_fluctuations(p_list)
        
        if max_fluct > threshold_pct:
            status = "VOLATILE [FLAGGED]"
            flagged_products.append((pid, name, max_fluct, range_vol, net_shift))
        elif max_fluct > (threshold_pct / 2.0):
            status = "MODERATE"
        else:
            status = "HIGHLY STABLE"
            
        audit_results.append([pid, name, cat, min(p_list), max(p_list), max_fluct, range_vol, net_shift, status])
        
        print(v_fmt.format(
            pid, name, f"{min(p_list):.2f}", f"{max(p_list):.2f}",
            f"{max_fluct:+.2f}%", f"{range_vol:.2f}%", f"{net_shift:+.2f}%", status
        ))
        
    print("-" * 110)
    
    # 3. Portfolio Volatility Ranking (Sort by max_fluct descending)
    ranked_volatility = []
    for item in audit_results:
        ranked_volatility.append(item)
        
    for i in range(len(ranked_volatility)):
        for j in range(i + 1, len(ranked_volatility)):
            if ranked_volatility[j][5] > ranked_volatility[i][5]:
                temp = ranked_volatility[i]
                ranked_volatility[i] = ranked_volatility[j]
                ranked_volatility[j] = temp
                
    print("\nSECTION 3: COMMODITY RISK RANKING (MOST VOLATILE TO MOST STABLE):")
    for r_idx in range(len(ranked_volatility)):
        item = ranked_volatility[r_idx]
        print(f"Rank #{r_idx+1}: {item[1]:<22} | Max Single Shift: {item[5]:+6.2f}% | Range Volatility: {item[6]:6.2f}% [{item[8]}]")
        
    # 4. Action Directives
    print(f"\nSECTION 4: THRESHOLD BREACH AUDIT (Max Fluctuation > {threshold_pct}%):")
    if len(flagged_products) == 0:
        print("[OK] All commodities traded within safe price boundaries without excessive swings.")
    else:
        for f_pid, f_name, f_max, f_rng, f_net in flagged_products:
            print(f"[ALERT] {f_name} ({f_pid}): Suffered extreme swing of {f_max:+.2f}% in a single period!")
            print(f"        Peak-to-Trough spread is {f_rng:.2f}%, with net trajectory {f_net:+.2f}%.")
            print("        Directives: Review vendor supply contracts and implement dynamic hedging.")

if __name__ == "__main__":
    # 6 Month Periods
    time_frames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    
    # Historical Prices Dataset: (Product ID, Name, Category, [Price_Jan ... Price_Jun])
    commodity_data = [
        ("CMD01", "Basmati Rice (5kg)",      "Grains",      [450.0, 455.0, 460.0, 458.0, 465.0, 470.0]),  # Highly stable
        ("CMD02", "Refined Sunflower Oil 1L","Edibles",     [135.0, 142.0, 168.0, 175.0, 195.0, 180.0]),  # Volatile (+18.3% Mar)
        ("CMD03", "Fresh Tomatoes (kg)",     "Vegetables",  [ 25.0,  32.0,  55.0,  85.0,  40.0,  30.0]),  # Extreme Fluctuation (+71% Mar-Apr, -52% May)
        ("CMD04", "Granulated Sugar (kg)",   "Sweeteners",  [ 42.0,  43.0,  43.5,  44.0,  44.5,  45.0]),  # Highly stable
        ("CMD05", "Wheat Flour (Atta 10kg)", "Grains",      [380.0, 390.0, 395.0, 400.0, 410.0, 415.0]),  # Steady
        ("CMD06", "Whole Red Onions (kg)",   "Vegetables",  [ 30.0,  35.0,  50.0,  70.0,  45.0,  35.0]),  # Highly volatile (+42.8%, +40%)
    ]
    
    analyze_market_fluctuations(commodity_data, time_frames, threshold_pct=15.0)

