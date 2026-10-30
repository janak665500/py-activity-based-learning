"""
Case Study 53: Food Waste Monitoring System
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Description:
Audits institutional dining hall food utilization across operating days.
Compares prepared meals, actual meals served, and leftover quantities.
Calculates percentage wastage, flags days breaching acceptable waste thresholds,
detects unaccounted inventory shrinkage, and computes financial wastage costs.
Concepts Used: Lists of Tuples, Tuple Unpacking, Arithmetic Operations, Loops,
               Conditional Statements, and Executive Tabular Reporting.
"""

def print_banner(title):
    border = "=" * 88
    print(border)
    print(title.center(88))
    print(border)

def analyze_food_waste(daily_records, acceptable_threshold=10.0, meal_unit_cost=65.0):
    num_days = len(daily_records)
    
    print_banner("INSTITUTIONAL DINING HALL FOOD WASTE & SUSTAINABILITY AUDIT")
    print(f"Audit Horizon               : {num_days} Operating Days")
    print(f"Acceptable Wastage Limit    : {acceptable_threshold:.1f}% of Prepared Volume")
    print(f"Standard Meal Production Cost: INR {meal_unit_cost:,.2f} / plate\n")
    
    row_fmt = "{:<12} {:>10} {:>10} {:>10} {:>12} {:>10} {:>14} {:<18}"
    headers = ("Day", "Prepared", "Served", "Leftover", "Discrepancy", "Waste %", "Loss (INR)", "Audit Status")
    print(row_fmt.format(*headers))
    print("-" * 102)
    
    total_prepared = 0
    total_served = 0
    total_leftovers = 0
    total_discrepancy = 0
    total_financial_loss = 0.0
    
    breach_days = []
    
    max_waste_pct = -1.0
    max_waste_day = ""
    min_waste_pct = 999.0
    min_waste_day = ""
    
    for record in daily_records:
        day_name, prep, served, leftovers = record
        
        # Unaccounted meals (shrinkage/spillage)
        discrepancy = prep - (served + leftovers)
        waste_pct = round((leftovers / prep) * 100.0, 2) if prep > 0 else 0.0
        fin_loss = round(leftovers * meal_unit_cost, 2)
        
        total_prepared += prep
        total_served += served
        total_leftovers += leftovers
        total_discrepancy += discrepancy
        total_financial_loss += fin_loss
        
        # Track extremes
        if waste_pct > max_waste_pct:
            max_waste_pct = waste_pct
            max_waste_day = day_name
        if waste_pct < min_waste_pct:
            min_waste_pct = waste_pct
            min_waste_day = day_name
            
        # Check threshold
        if waste_pct > acceptable_threshold:
            status = "EXCESSIVE [BREACH]"
            breach_days.append((day_name, waste_pct, leftovers, fin_loss))
        elif discrepancy != 0:
            status = "DISCREPANCY ALERT"
        else:
            status = "ACCEPTABLE [OK]"
            
        disc_str = f"{discrepancy:+d}" if discrepancy != 0 else "0"
        print(row_fmt.format(
            day_name, prep, served, leftovers, disc_str,
            f"{waste_pct:.2f}%", f"{fin_loss:,.2f}", status
        ))
        
    print("-" * 102)
    
    overall_waste_pct = round((total_leftovers / total_prepared) * 100.0, 2) if total_prepared > 0 else 0.0
    served_pct = round((total_served / total_prepared) * 100.0, 2) if total_prepared > 0 else 0.0
    
    tot_row = row_fmt.format(
        "CUMULATIVE", total_prepared, total_served, total_leftovers,
        f"{total_discrepancy:+d}", f"{overall_waste_pct:.2f}%",
        f"{total_financial_loss:,.2f}", "OVERALL EVAL"
    )
    print(tot_row)
    print("-" * 102)
    
    # Analytical Insights
    print("\nEXECUTIVE SUSTAINABILITY METRICS:")
    print(f"Total Food Volume Cooked    : {total_prepared:,} Meals")
    print(f"Successfully Consumed Volume: {total_served:,} Meals ({served_pct:.1f}%)")
    print(f"Total Leftovers Discarded   : {total_leftovers:,} Meals ({overall_waste_pct:.1f}%)")
    print(f"Total Financial Wastage Loss: INR {total_financial_loss:,.2f}")
    print(f"Most Efficient Service Day  : {min_waste_day} ({min_waste_pct:.2f}% waste)")
    print(f"Worst Wastage Spike Day     : {max_waste_day} ({max_waste_pct:.2f}% waste)")
    
    # Action Directives
    print("\nTHRESHOLD VIOLATION DIRECTIVES (> 10.0% Waste Limit):")
    if len(breach_days) == 0:
        print("[OK] Food wastage remained within permissible green limits on all days.")
    else:
        for b_day, b_pct, b_qty, b_cost in breach_days:
            excess_pct = b_pct - acceptable_threshold
            print(f"[!] {b_day:<10}: Wastage of {b_pct:.1f}% ({b_qty} meals) exceeded threshold by +{excess_pct:.1f}%.")
            print(f"    Direct Financial Loss: INR {b_cost:,.2f} on {b_day}.")
            
    print("\nOPERATIONAL RECOMMENDATIONS:")
    print("1. Re-calibrate kitchen batch sizes on Fridays and Sundays using predictive attendance.")
    print("2. Implement dynamic cook-to-order stations for final 45 minutes of dining windows.")
    print("3. Partner with local food banks/shelters to donate clean surplus leftovers immediately.")

if __name__ == "__main__":
    # Test dataset: List of tuples (Day, Meals Prepared, Meals Served, Leftovers Counted)
    dining_hall_data = [
        ("Monday",    850, 785,  65),  # 7.65% - OK
        ("Tuesday",   820, 750,  70),  # 8.54% - OK
        ("Wednesday", 880, 810,  70),  # 7.95% - OK
        ("Thursday",  800, 735,  65),  # 8.12% - OK
        ("Friday",    950, 780, 160),  # 16.84% - Major breach (students traveling home)
        ("Saturday",  600, 550,  50),  # 8.33% - OK
        ("Sunday",    750, 610, 130),  # 17.33% - Major breach (weekend dine-outs)
        ("Holiday",   500, 475,  20)   # 4.00% - Discrepancy check: 500 - (475 + 20) = 5 uncounted
    ]
    
    analyze_food_waste(dining_hall_data, acceptable_threshold=10.0, meal_unit_cost=65.0)

