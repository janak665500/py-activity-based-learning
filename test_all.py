"""
Comprehensive Verification Runner for all 10 Case Studies
Python Activity-Based Learning (ABL)
Dr. RVR NRI Institute of Technology
"""

import os
import sys
import subprocess

def run_all():
    print("=" * 80)
    print("PYTHON ACTIVITY-BASED LEARNING (ABL) - AUTOMATED VERIFICATION SUITE")
    print("Institution: Dr. RVR NRI Institute of Technology | Dept. of CSE")
    print("Student    : Shukur (Roll No: 24NR1A0501)")
    print("=" * 80)

    case_scripts = [
        ("Case Study 12", "Attendance Recovery Computation", "case_study_12_attendance_recovery/attendance_recovery.py"),
        ("Case Study 17", "Student Performance Trend Analysis", "case_study_17_performance_trend/performance_trend.py"),
        ("Case Study 28", "Repeated Transaction Detection", "case_study_28_repeated_transactions/repeated_transactions.py"),
        ("Case Study 34", "Student Feedback Sentiment Scoring", "case_study_34_sentiment_scoring/sentiment_scoring.py"),
        ("Case Study 35", "Text Compression Using Character Runs", "case_study_35_text_compression/text_compression.py"),
        ("Case Study 42", "Student Marks Matrix Analysis", "case_study_42_marks_matrix/marks_matrix.py"),
        ("Case Study 45", "Weekly Electricity Consumption Matrix", "case_study_45_electricity_consumption/electricity_consumption.py"),
        ("Case Study 49", "Tuple-Based Product Catalogue Audit", "case_study_49_product_catalogue/product_catalogue.py"),
        ("Case Study 53", "Food Waste Monitoring System", "case_study_53_food_waste_monitoring/food_waste_monitoring.py"),
        ("Case Study 63", "Multi-Product Price Fluctuation Analysis", "case_study_63_price_fluctuation/price_fluctuation.py")
    ]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    passed = 0
    failed = 0

    print(f"\n{'ID':<15} {'Title':<42} {'Status':<12}")
    print("-" * 75)

    for cid, title, rel_path in case_scripts:
        full_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(full_path):
            print(f"{cid:<15} {title:<42} [MISSING FILE]")
            failed += 1
            continue

        res = subprocess.run([sys.executable, full_path], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"{cid:<15} {title:<42} [PASS 100%]")
            passed += 1
        else:
            print(f"{cid:<15} {title:<42} [FAIL]")
            print("Error details:", res.stderr)
            failed += 1

    print("-" * 75)
    print(f"TOTAL EXECUTED: {len(case_scripts)} | PASSED: {passed} | FAILED: {failed}")
    if failed == 0:
        print("[SUCCESS] All 10 case study solutions executed flawlessly with zero errors.")
    else:
        print("[WARNING] Some scripts encountered errors.")

if __name__ == "__main__":
    run_all()

