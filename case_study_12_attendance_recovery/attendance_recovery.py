"""
Case Study 12: Attendance Recovery Computation
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Description:
Calculates current attendance percentages and determines the minimum consecutive
classes required to reach eligibility thresholds under different future attendance scenarios.
Concepts Used: Variables, Data Types, Operators, Conditional Statements, While/For Loops,
               Tuples, Tuple Unpacking, Lists, and String Formatting.
"""

def print_banner(title):
    border = "=" * 78
    print(border)
    print(title.center(78))
    print(border)

def calculate_attendance_percentage(attended, total):
    if total <= 0:
        return 0.0
    return round((attended / total) * 100.0, 2)

def calculate_consecutive_needed(attended, total, threshold, future_rate=1.0):
    """
    Simulates upcoming classes to reach target attendance percentage threshold.
    future_rate: proportion of upcoming classes attended (e.g., 1.0 for 100%, 0.8 for 80%).
    Returns the minimum number of total upcoming classes required.
    """
    current_pct = calculate_attendance_percentage(attended, total)
    if current_pct >= threshold:
        return 0
    
    # If future_rate is less than or equal to threshold / 100, student can never reach threshold
    if future_rate <= (threshold / 100.0):
        return -1  # Mathematically impossible to reach
    
    classes_needed = 0
    sim_attended = float(attended)
    sim_total = float(total)
    
    # Simulate step-by-step using while loop
    while (sim_attended / sim_total) * 100.0 < threshold:
        classes_needed += 1
        sim_total += 1
        sim_attended += future_rate
        
        # Guard against excessive simulation
        if classes_needed > 500:
            break
            
    return classes_needed

def calculate_missable_classes(attended, total, threshold):
    """
    If student is already above threshold, how many upcoming classes can they miss
    consecutively without dropping below the threshold?
    """
    current_pct = calculate_attendance_percentage(attended, total)
    if current_pct < threshold:
        return 0
    
    missable = 0
    sim_attended = float(attended)
    sim_total = float(total)
    
    while ((sim_attended) / (sim_total + 1)) * 100.0 >= threshold:
        missable += 1
        sim_total += 1
    
    return missable

def run_attendance_analysis(students_data, threshold=75.0):
    print_banner("STUDENT ATTENDANCE AUDIT & RECOVERY REPORT")
    print(f"Minimum Prescribed Eligibility Threshold: {threshold}%\n")
    
    headers = ("ID", "Student Name", "Held", "Attended", "Current %", "Status", "100% Rec.", "90% Rec.", "80% Rec.", "Bunk Buffer")
    header_fmt = "{:<8} {:<18} {:<6} {:<9} {:<10} {:<12} {:<10} {:<10} {:<10} {:<11}"
    print(header_fmt.format(*headers))
    print("-" * 108)
    
    # Summary counters
    total_students = len(students_data)
    eligible_count = 0
    shortage_count = 0
    critical_count = 0  # < 65% (below condonation)
    
    recovery_summary = []
    
    for record in students_data:
        # Tuple unpacking
        roll_no, name, total_held, attended = record
        
        current_pct = calculate_attendance_percentage(attended, total_held)
        
        # Evaluate eligibility status
        if current_pct >= threshold:
            status = "ELIGIBLE"
            eligible_count += 1
            rec_100 = 0
            rec_90 = 0
            rec_80 = 0
            buffer_classes = calculate_missable_classes(attended, total_held, threshold)
        elif current_pct >= 65.0:
            status = "CONDONATION"
            shortage_count += 1
            rec_100 = calculate_consecutive_needed(attended, total_held, threshold, 1.0)
            rec_90 = calculate_consecutive_needed(attended, total_held, threshold, 0.9)
            rec_80 = calculate_consecutive_needed(attended, total_held, threshold, 0.8)
            buffer_classes = 0
        else:
            status = "CRITICAL"
            shortage_count += 1
            critical_count += 1
            rec_100 = calculate_consecutive_needed(attended, total_held, threshold, 1.0)
            rec_90 = calculate_consecutive_needed(attended, total_held, threshold, 0.9)
            rec_80 = calculate_consecutive_needed(attended, total_held, threshold, 0.8)
            buffer_classes = 0
            
        r100_str = str(rec_100) if rec_100 >= 0 else "N/A"
        r90_str = str(rec_90) if rec_90 >= 0 else "N/A"
        r80_str = str(rec_80) if rec_80 >= 0 else "N/A"
        buf_str = f"{buffer_classes} classes" if buffer_classes > 0 else "-"
        
        print(header_fmt.format(
            roll_no, name, total_held, attended, f"{current_pct:.2f}%",
            status, r100_str, r90_str, r80_str, buf_str
        ))
        
        recovery_summary.append((roll_no, name, current_pct, status, rec_100))

    print("-" * 108)
    print("\nEXECUTIVE SUMMARY:")
    print(f"Total Students Evaluated  : {total_students}")
    print(f"Eligible Students (>=75%) : {eligible_count} ({round((eligible_count/total_students)*100, 1)}%)")
    print(f"Shortage Cases (<75%)     : {shortage_count} ({round((shortage_count/total_students)*100, 1)}%)")
    print(f"  - Condonation (65%-74%) : {shortage_count - critical_count}")
    print(f"  - Critical Shortage (<65%): {critical_count}")
    
    print("\nACTIONABLE RECOVERY DIRECTIVES:")
    for roll_no, name, pct, status, rec in recovery_summary:
        if status != "ELIGIBLE":
            print(f"[*] {name} ({roll_no}) at {pct:.1f}%: Must attend {rec} consecutive classes without absence to reach {threshold}%.")

if __name__ == "__main__":
    # Test dataset: List of tuples representing (Roll No, Student Name, Total Held, Classes Attended)
    sample_students = [
        ("24NR1A0501", "Shukur", 60, 48),       # 80.00% - Eligible
        ("24NR1A0502", "Aarav Kumar", 60, 42),  # 70.00% - Condonation
        ("24NR1A0503", "Bhavya Sri", 60, 52),   # 86.67% - Eligible
        ("24NR1A0504", "Charan Teja", 60, 32),  # 53.33% - Critical
        ("24NR1A0505", "Divya Reddy", 60, 44),  # 73.33% - Condonation
        ("24NR1A0506", "Eshwar Rao", 60, 28),   # 46.67% - Critical
        ("24NR1A0507", "Farhan Ali", 60, 57),   # 95.00% - Eligible
        ("24NR1A0508", "Gowri Priya", 60, 45),  # 75.00% - Eligible (Borderline)
    ]
    
    run_attendance_analysis(sample_students, threshold=75.0)

