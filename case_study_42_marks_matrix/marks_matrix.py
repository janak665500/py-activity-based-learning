"""
Case Study 42: Student Marks Matrix Analysis
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Description:
Analyses a 2D matrix of student examination marks across multiple academic subjects.
Computes row-wise student metrics (totals, percentages, grades, ranks), column-wise
subject diagnostics (averages, highest/lowest marks, pass percentages), and detects
subjects with concerning low average performance.
Concepts Used: 2D Nested Lists, Row-wise & Column-wise Traversals, Nested Loops,
               Conditionals, Tuples, Sorting via Algorithmic Swapping, and Formatted Grids.
"""

def print_banner(title):
    border = "=" * 88
    print(border)
    print(title.center(88))
    print(border)

def determine_grade(percentage):
    if percentage >= 90.0:
        return "O  (Outstanding)"
    elif percentage >= 80.0:
        return "A+ (Excellent)"
    elif percentage >= 70.0:
        return "A  (Very Good)"
    elif percentage >= 60.0:
        return "B  (Good)"
    elif percentage >= 50.0:
        return "C  (Average)"
    else:
        return "F  (Fail)"

def analyze_marks_matrix(students, subjects, marks_matrix, benchmark_avg=65.0):
    num_students = len(students)
    num_subjects = len(subjects)
    
    print_banner("ACADEMIC PERFORMANCE MATRIX EVALUATION")
    print(f"Cohort Size: {num_students} Students | Curricular Subjects: {num_subjects}")
    print(f"Institutional Quality Benchmark Subject Average: {benchmark_avg}%\n")
    
    # 1. Row-Wise Analysis (Student Statistics)
    # student_results: [ [student_name, [scores], total, percentage, grade, rank], ... ]
    student_records = []
    
    for r in range(num_students):
        scores = marks_matrix[r]
        row_total = sum(scores)
        pct = round(row_total / (num_subjects * 100.0) * 100.0, 2)
        grade = determine_grade(pct)
        student_records.append([students[r], scores, row_total, pct, grade, 0])
        
    # Rank computation via sorting a copy of records
    # Manual bubble sort by percentage descending
    ranked_list = []
    for item in student_records:
        ranked_list.append(item)
        
    for i in range(len(ranked_list)):
        for j in range(i + 1, len(ranked_list)):
            if ranked_list[j][3] > ranked_list[i][3]:
                temp = ranked_list[i]
                ranked_list[i] = ranked_list[j]
                ranked_list[j] = temp
                
    # Assign ranks
    for rank_idx in range(len(ranked_list)):
        ranked_list[rank_idx][5] = rank_idx + 1
        
    # Print Student Scorecard Matrix
    print("SECTION 1: STUDENT SCORECARD MATRIX (ROW-WISE ANALYSIS)")
    col_w = 12
    subj_headers = "".join([f"{s[:10]:>{col_w}}" for s in subjects])
    header_line = f"{'Rank':<5} {'Student Name':<16}{subj_headers} {'Total':>8} {'Pct %':>8}  {'Grade'}"
    print(header_line)
    print("-" * len(header_line))
    
    for rec in ranked_list:
        name, scores, tot, pct, grd, rnk = rec
        score_cells = "".join([f"{score:>{col_w}}" for score in scores])
        print(f"#{rnk:<4} {name:<16}{score_cells} {tot:>8} {pct:>7.2f}%  {grd}")
        
    print("-" * len(header_line))
    
    # 2. Column-Wise Analysis (Subject Statistics)
    print("\nSECTION 2: CURRICULAR SUBJECT DIAGNOSTICS (COLUMN-WISE ANALYSIS)")
    diag_hdr = "{:<24} {:>10} {:>10} {:>10} {:>12} {:<20}"
    print(diag_hdr.format("Subject Name", "Avg Mark", "Highest", "Lowest", "Pass Rate %", "Curricular Status"))
    print("-" * 92)
    
    low_performing_subjects = []
    
    for c in range(num_subjects):
        col_scores = []
        for r in range(num_students):
            col_scores.append(marks_matrix[r][c])
            
        subj_total = sum(col_scores)
        subj_avg = round(subj_total / num_students, 2)
        subj_max = max(col_scores)
        subj_min = min(col_scores)
        
        # Pass rate (mark >= 40)
        passes = 0
        for s in col_scores:
            if s >= 40:
                passes += 1
        pass_rate = round((passes / num_students) * 100.0, 1)
        
        # Check if subject is low performing
        if subj_avg < benchmark_avg:
            status = "LOW PERFORMANCE [ALERT]"
            low_performing_subjects.append((subjects[c], subj_avg, pass_rate))
        elif pass_rate < 80.0:
            status = "HIGH FAILURE RATE"
            low_performing_subjects.append((subjects[c], subj_avg, pass_rate))
        else:
            status = "HEALTHY (Satisfactory)"
            
        print(diag_hdr.format(subjects[c], f"{subj_avg:.2f}", subj_max, subj_min, f"{pass_rate:.1f}%", status))
        
    print("-" * 92)
    
    # 3. Top Performers Podium
    print("\nSECTION 3: ACADEMIC MERIT PODIUM (TOP PERFORMERS)")
    podium_titles = ["GOLD MEDALIST (Rank 1)", "SILVER MEDALIST (Rank 2)", "BRONZE MEDALIST (Rank 3)"]
    for idx in range(min(3, len(ranked_list))):
        rec = ranked_list[idx]
        print(f"[*] {podium_titles[idx]:<25} : {rec[0]} - Total: {rec[2]}/{(num_subjects*100)} ({rec[3]:.2f}%) [{rec[4]}]")
        
    # 4. Low Performance Subjects Alerts
    print("\nSECTION 4: INSTITUTIONAL REMEDIAL ACTION ALERTS:")
    if len(low_performing_subjects) == 0:
        print("[OK] All subjects meet or exceed institutional quality standards.")
    else:
        for subj_name, s_avg, s_pass in low_performing_subjects:
            print(f"[!] '{subj_name}' class average of {s_avg:.2f}% (Pass rate: {s_pass:.1f}%) is BELOW the {benchmark_avg}% threshold.")
            print(f"    Recommendation: Conduct remedial tutorials, revise foundational topics, and hold doubt-clearing clinics.")

if __name__ == "__main__":
    cohort_students = [
        "Shukur", "Aarav Kumar", "Bhavya Sri", "Charan Teja",
        "Divya Reddy", "Eshwar Rao", "Farhan Ali"
    ]
    
    curriculum = [
        "Mathematics", "Python Prog", "Data Structures", "Comp. Org.", "Discrete Math"
    ]
    
    # 7 Students x 5 Subjects Marks Matrix (out of 100)
    scores = [
        [94, 98, 92, 88, 85],  # Shukur - Star Performer
        [68, 74, 58, 62, 42],  # Aarav
        [85, 90, 82, 79, 72],  # Bhavya
        [42, 55, 38, 48, 30],  # Charan - Struggles in DS & DM
        [78, 84, 75, 72, 60],  # Divya
        [52, 60, 45, 50, 38],  # Eshwar
        [88, 92, 86, 84, 68]   # Farhan
    ]
    
    analyze_marks_matrix(cohort_students, curriculum, scores, benchmark_avg=65.0)
