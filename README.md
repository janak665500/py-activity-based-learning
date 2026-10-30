# Python-Activity-Based-Learning
**Department of Computer Science & Engineering**  
**Dr. RVR NRI Institute of Technology**  
*(An Institution deemed to be University u/s 3 of UGC Act, 1956)*  
*Pothavarappadu (V), Agiripalli (M), Eluru District, Andhra Pradesh - 521212*

---

## 👨‍🎓 Student Profile
- **Student Name**: Shukur
- **Roll Number**: 24NR1A0501
- **Course**: Python Programming (Activity-Based Learning - ABL Assignment)
- **Degree**: B.Tech. (First Year)
- **Branch**: Computer Science & Engineering (CSE)
- **Section**: CSE-A
- **Academic Year**: 2026–2027
- **Submission Date**: First Working Day Post-Dussehra Holidays (Circular Dated: 14-10-2026)

---

## 📌 Assignment Overview & Compliance
In accordance with the official academic circular issued by the Dean (School of Computer Studies) and Course Coordinator on **14-10-2026**, this repository contains complete, production-grade solutions for **10 difficult-level case studies** selected from the prescribed list of 100 problems.

### Strict Syllabus Compliance:
Every solution has been developed strictly utilizing core Python syllabus concepts:
- **Computational Thinking & Problem Decomposition**
- **Algorithms, Flowcharts, and Pseudocode**
- **Variables, Data Types (`int`, `float`, `str`, `bool`)**
- **Operators (Arithmetic, Relational, Logical, Assignment)**
- **Conditional Branching (`if`, `elif`, `else`)**
- **Loops (`for`, `while`, loop control statements)**
- **Strings, Indexing, Slicing, and Built-in String Operations**
- **Lists, List Operations, and In-place Element Swapping**
- **2D / Nested Lists (Matrix Traversals and Grid Computations)**
- **Tuples, Tuple Immutability, and Tuple Unpacking**
- *Strictly Zero External Dependencies (No NumPy, No Pandas, No Dictionaries, No Sets)*

---

## 📑 Portfolio of 10 Selected Case Studies

| # | Case Study ID & Title | Primary Concepts Applied | Directory Link | Status |
|:---:|:---|:---|:---:|:---:|
| 1 | **12. Attendance Recovery Computation** | `while` simulation loops, float arithmetic, tuple unpacking | [`case_study_12_attendance_recovery/`](./case_study_12_attendance_recovery/) | **Verified (100% Pass)** |
| 2 | **17. Student Performance Trend Analysis** | Nested lists (3D matrix), longitudinal difference loops, rule engine | [`case_study_17_performance_trend/`](./case_study_17_performance_trend/) | **Verified (100% Pass)** |
| 3 | **28. Repeated Transaction Detection** | List traversal, pairwise comparisons, threshold filters, risk ranking | [`case_study_28_repeated_transactions/`](./case_study_28_repeated_transactions/) | **Verified (100% Pass)** |
| 4 | **34. Student Feedback Sentiment Scoring** | Text tokenization, string sanitization, list frequency counters | [`case_study_34_sentiment_scoring/`](./case_study_34_sentiment_scoring/) | **Verified (100% Pass)** |
| 5 | **35. Text Compression Using Character Runs** | Run-length encoding (RLE), string reconstruction, lossless verification | [`case_study_35_text_compression/`](./case_study_35_text_compression/) | **Verified (100% Pass)** |
| 6 | **42. Student Marks Matrix Analysis** | 2D nested lists, row/column traversals, bubble sort ranks, merit podium | [`case_study_42_marks_matrix/`](./case_study_42_marks_matrix/) | **Verified (100% Pass)** |
| 7 | **45. Weekly Electricity Consumption Matrix** | 2D list grids, appliance/day totals, surge detection, tiered tariff | [`case_study_45_electricity_consumption/`](./case_study_45_electricity_consumption/) | **Verified (100% Pass)** |
| 8 | **49. Tuple-Based Product Catalogue Audit** | Tuple immutability, data sanitization, inventory asset valuation | [`case_study_49_product_catalogue/`](./case_study_49_product_catalogue/) | **Verified (100% Pass)** |
| 9 | **53. Food Waste Monitoring System** | List of tuples, inventory shrinkage formulas, financial loss audits | [`case_study_53_food_waste_monitoring/`](./case_study_53_food_waste_monitoring/) | **Verified (100% Pass)** |
| 10 | **63. Multi-Product Price Fluctuation Analysis** | Historical price lists, volatility percentages, commodity risk ranking | [`case_study_63_price_fluctuation/`](./case_study_63_price_fluctuation/) | **Verified (100% Pass)** |

---

## 📂 Repository Structure & Artifacts
Each case study directory is organized uniformly to meet all institutional audit requirements:
```text
Python-Activity-Based-Learning/
├── README.md                                          # Master repository documentation (this file)
├── report/
│   ├── generate_pdf.py                                # Automated Python PDF generation engine
│   └── Python_Activity_Based_Learning_Report.pdf      # Official consolidated PDF report
├── case_study_12_attendance_recovery/
│   ├── attendance_recovery.py                         # Complete standalone Python program
│   ├── README.md                                      # Objectives, Assumptions, Algorithm, Flowchart, Pseudocode, Tests
│   └── output.txt                                     # Certified terminal execution log
├── case_study_17_performance_trend/
│   ├── performance_trend.py
│   ├── README.md
│   └── output.txt
├── case_study_28_repeated_transactions/
│   ├── repeated_transactions.py
│   ├── README.md
│   └── output.txt
├── case_study_34_sentiment_scoring/
│   ├── sentiment_scoring.py
│   ├── README.md
│   └── output.txt
├── case_study_35_text_compression/
│   ├── text_compression.py
│   ├── README.md
│   └── output.txt
├── case_study_42_marks_matrix/
│   ├── marks_matrix.py
│   ├── README.md
│   └── output.txt
├── case_study_45_electricity_consumption/
│   ├── electricity_consumption.py
│   ├── README.md
│   └── output.txt
├── case_study_49_product_catalogue/
│   ├── product_catalogue.py
│   ├── README.md
│   └── output.txt
├── case_study_53_food_waste_monitoring/
│   ├── food_waste_monitoring.py
│   ├── README.md
│   └── output.txt
└── case_study_63_price_fluctuation/
    ├── price_fluctuation.py
    ├── README.md
    └── output.txt
```

---

## 🚀 Execution Instructions

### Running Individual Case Studies:
To execute any individual case study, navigate to its folder and run the Python script:
```powershell
# Example: Case Study 12
python case_study_12_attendance_recovery/attendance_recovery.py

# Example: Case Study 42
python case_study_42_marks_matrix/marks_matrix.py
```

### Running All 10 Case Studies in Sequence:
```powershell
python -c "
import os, subprocess
cases = [
    'case_study_12_attendance_recovery/attendance_recovery.py',
    'case_study_17_performance_trend/performance_trend.py',
    'case_study_28_repeated_transactions/repeated_transactions.py',
    'case_study_34_sentiment_scoring/sentiment_scoring.py',
    'case_study_35_text_compression/text_compression.py',
    'case_study_42_marks_matrix/marks_matrix.py',
    'case_study_45_electricity_consumption/electricity_consumption.py',
    'case_study_49_product_catalogue/product_catalogue.py',
    'case_study_53_food_waste_monitoring/food_waste_monitoring.py',
    'case_study_63_price_fluctuation/price_fluctuation.py'
]
for c in cases:
    print('='*70); print('EXECUTING:', c); print('='*70)
    subprocess.run(['python', c])
"
```

---

## 📄 Consolidated PDF Report Generation
To regenerate the consolidated PDF report covering all 10 problems, algorithms, flowcharts, pseudocode, code listings, test suites, and conclusions:
```powershell
python report/generate_pdf.py
```
The output PDF is saved at `report/Python_Activity_Based_Learning_Report.pdf`.

---

## 🌐 GitHub Deployment Instructions
To publish this repository to your GitHub account as required by the circular:
1. Open Git Bash or PowerShell in this project directory:
   ```bash
   git init
   git add .
   git commit -m "Complete Python Activity-Based Learning (ABL) Assignment - 10 Case Studies"
   ```
2. Create a new public repository on [GitHub](https://github.com/new) named `Python-Activity-Based-Learning`.
3. Link the remote origin and push:
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-github-username>/Python-Activity-Based-Learning.git
   git push -u origin main
   ```
4. Copy the repository URL and submit it to the faculty member / lab mentor on the first working day after the Dussehra holidays.
