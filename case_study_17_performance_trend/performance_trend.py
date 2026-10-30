"""
Case Study 17: Student Performance Trend Analysis
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Description:
Compares assessment scores across multiple examinations, calculates improvements and declines,
identifies consistently weak subjects, and classifies students according to defined academic criteria.
Concepts Used: Nested Lists, Tuples, Tuple Unpacking, For/While Loops, Conditional Statements,
               String Manipulation, and List Accumulations.
"""

def print_banner(title):
    border = "=" * 80
    print(border)
    print(title.center(80))
    print(border)

def evaluate_subject_trend(scores, passing_mark=40):
    """
    Evaluates trend across assessments for a single subject:
    scores = [exam1, exam2, exam3]
    """
    n = len(scores)
    diffs = []
    for i in range(1, n):
        diffs.append(scores[i] - scores[i - 1])
    
    # Check consistently weak
    is_weak = True
    for s in scores:
        if s >= passing_mark:
            is_weak = False
            break
            
    if is_weak:
        trend = "Consistently Weak"
    elif all_positive(diffs):
        trend = "Improving (+)"
    elif all_negative(diffs):
        trend = "Declining (-)"
    else:
        trend = "Fluctuating"
        
    net_change = scores[-1] - scores[0]
    return trend, net_change

def all_positive(lst):
    for x in lst:
        if x <= 0:
            return False
    return True

def all_negative(lst):
    for x in lst:
        if x >= 0:
            return False
    return True

def classify_student(overall_avg, net_change, has_weak_subject, has_declining):
    """
    Classifies students based on academic performance metrics:
    - Outstanding Scholar: Avg >= 80 and net improvement >= 0
    - Remedial Intervention Needed: Any subject consistently weak (< 40)
    - Academic Warning: Net change < -10 or multiple declining subjects
    - Consistent Improver: Net change >= +8
    - Steady Performer: Consistent and stable
    """
    if has_weak_subject:
        return "Remedial Support"
    elif overall_avg >= 80.0 and net_change >= 0:
        return "Outstanding Scholar"
    elif net_change >= 8.0:
        return "Consistent Improver"
    elif net_change <= -10.0 or has_declining:
        return "Academic Warning"
    else:
        return "Steady Performer"

def analyze_performance_trends(students_data, subjects, exam_names):
    print_banner("LONGITUDINAL STUDENT PERFORMANCE TREND ANALYSIS")
    print(f"Examinations Tracked : {', '.join(exam_names)}")
    print(f"Subjects Evaluated   : {', '.join(subjects)}\n")
    
    num_subjects = len(subjects)
    num_exams = len(exam_names)
    
    classification_counts = [
        ("Outstanding Scholar", 0),
        ("Consistent Improver", 0),
        ("Steady Performer", 0),
        ("Academic Warning", 0),
        ("Remedial Support", 0)
    ]
    
    # To identify subjects with widespread weakness
    subject_weakness_counter = [0] * num_subjects
    
    for student in students_data:
        roll_no, name, score_matrix = student
        print(f"--- Student: {name} (Roll: {roll_no}) ---")
        
        exam_averages = []
        for exam_idx in range(num_exams):
            exam_sum = 0
            for subj_idx in range(num_subjects):
                exam_sum += score_matrix[exam_idx][subj_idx]
            exam_avg = exam_sum / num_subjects
            exam_averages.append(exam_avg)
            
        overall_student_avg = sum(exam_averages) / num_exams
        overall_net_change = exam_averages[-1] - exam_averages[0]
        
        has_weak = False
        has_declining = False
        
        subj_header = "{:<18} " + " ".join(["{:<10}"] * num_exams) + " {:<12} {:<18}"
        print(subj_header.format("Subject", *exam_names, "Net Shift", "Trend"))
        print("-" * 75)
        
        for subj_idx in range(num_subjects):
            subj_scores = []
            for exam_idx in range(num_exams):
                subj_scores.append(score_matrix[exam_idx][subj_idx])
            
            trend, net_shift = evaluate_subject_trend(subj_scores)
            
            if trend == "Consistently Weak":
                has_weak = True
                subject_weakness_counter[subj_idx] += 1
            if trend == "Declining (-)":
                has_declining = True
                
            formatted_scores = [f"{s:5.1f}" for s in subj_scores]
            shift_str = f"{net_shift:+5.1f}"
            print(subj_header.format(subjects[subj_idx], *formatted_scores, shift_str, trend))
            
        category = classify_student(overall_student_avg, overall_net_change, has_weak, has_declining)
        
        # Update classification counts
        for i in range(len(classification_counts)):
            if classification_counts[i][0] == category:
                classification_counts[i] = (category, classification_counts[i][1] + 1)
                break
                
        print("-" * 75)
        avg_str = " | ".join([f"{exam_names[k]}: {exam_averages[k]:.1f}" for k in range(num_exams)])
        print(f"Exam Averages : {avg_str}")
        print(f"Overall Avg   : {overall_student_avg:.2f} | Net Trajectory: {overall_net_change:+5.2f}")
        print(f"Classification: >>> {category.upper()} <<<\n")
        
    print_banner("BATCH PERFORMANCE SUMMARY & COHORT DISTRIBUTION")
    print("{:<30} {:<15} {:<15}".format("Classification Category", "Student Count", "Percentage"))
    print("-" * 60)
    total_students = len(students_data)
    for cat_name, cnt in classification_counts:
        pct = (cnt / total_students) * 100.0 if total_students > 0 else 0.0
        print("{:<30} {:<15} {:<14.1f}%".format(cat_name, cnt, pct))
    print("-" * 60)
    
    print("\nSUBJECT-WISE WEAKNESS CONCERN MONITOR:")
    for subj_idx in range(num_subjects):
        weak_count = subject_weakness_counter[subj_idx]
        print(f"- {subjects[subj_idx]:<18}: {weak_count} student(s) persistently below 40 passing threshold.")

if __name__ == "__main__":
    subjects_list = ["Mathematics", "Python Prog.", "Applied Physics", "Data Structures"]
    exams_list = ["Assessment 1", "Assessment 2", "Assessment 3"]
    
    # Dataset: (Roll, Name, [Assessment1_Scores, Assessment2_Scores, Assessment3_Scores])
    cohort_data = [
        ("24NR1A0501", "Shukur", [
            [82, 85, 78, 80],
            [88, 90, 84, 85],
            [92, 95, 89, 91]
        ]),
        ("24NR1A0502", "Aarav Sharma", [
            [70, 72, 68, 65],
            [68, 65, 62, 60],
            [62, 58, 55, 50]
        ]),
        ("24NR1A0503", "Bhavya Sri", [
            [35, 38, 32, 30],
            [36, 35, 34, 32],
            [38, 36, 35, 34]
        ]),
        ("24NR1A0504", "Charan Teja", [
            [55, 60, 58, 62],
            [65, 72, 68, 70],
            [74, 80, 76, 79]
        ]),
        ("24NR1A0505", "Divya Lakshmi", [
            [75, 80, 70, 78],
            [78, 79, 72, 77],
            [76, 81, 71, 79]
        ])
    ]
    
    analyze_performance_trends(cohort_data, subjects_list, exams_list)
