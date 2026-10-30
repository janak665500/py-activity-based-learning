# Case Study 12: Attendance Recovery Computation

**Course**: Python Programming (Activity-Based Learning - ABL)  
**Institution**: Dr. RVR NRI Institute of Technology  
**Student Name**: Shukur  
**Roll Number**: 24NR1A0501  
**Branch**: Computer Science & Engineering (CSE)  
**Section**: CSE-A  

---

## 1. Problem Statement
In higher education institutions, maintaining a minimum attendance percentage (typically 75.0%) is a statutory prerequisite for academic semester-end examination eligibility. When students encounter medical or emergency leaves, their attendance falls below this critical threshold. Calculating the exact number of future consecutive classes a student must attend without missing a single period to recover eligibility is mathematically non-trivial due to the moving denominator (each attended upcoming class increments both the numerator and the denominator). The system must compute current attendance percentages, evaluate eligibility tiers (Eligible, Condonation, Critical), simulate future recovery pathways under varying attendance discipline scenarios (100%, 90%, 80%), and determine the allowable bunk buffer for already eligible students.

---

## 2. Objectives
1. Implement accurate floating-point attendance percentage calculations from raw attendance records.
2. Formulate an iterative simulation model to determine the exact minimum consecutive classes required to attain or surpass the 75.0% eligibility benchmark.
3. Model realistic recovery scenarios where future attendance discipline may not be 100% (e.g., 90% or 80% future attendance).
4. For students already possessing compliant attendance, calculate the "bunk buffer" (maximum allowable absences before dipping below 75.0%).
5. Classify students into administrative tiers: **ELIGIBLE** ($\ge 75\%$), **CONDONATION** ($65\% - 74.9\%$), and **CRITICAL SHORTAGE** ($< 65\%$).

---

## 3. Assumptions
1. All classes held are conducted uniformly; fractions of classes are not permitted.
2. The statutory attendance threshold is established at 75.0% by institutional regulation, with 65.0% as the condonation cutoff.
3. In the 100% recovery scenario, the student attends every single future class consecutively without absence.
4. Input data is supplied as a list of tuples containing `(roll_number, student_name, total_classes_held, classes_attended)`.
5. Attended classes cannot exceed total classes conducted ($0 \le \text{Attended} \le \text{Total}$).

---

## 4. Step-by-Step Algorithm

```
Step 1: Define the statutory eligibility threshold (threshold = 75.0) and condonation limit (65.0).
Step 2: Initialize student records as a list of tuples (roll_no, name, total_held, attended).
Step 3: For each student record in the list:
    Step 3.1: Unpack the tuple: roll_no, name, total_held, attended.
    Step 3.2: Compute current attendance percentage:
              current_pct = (attended / total_held) * 100.0.
    Step 3.3: If current_pct >= threshold:
              - Mark status as "ELIGIBLE".
              - Set recovery classes needed = 0.
              - Compute bunk buffer: while ((attended) / (total_held + 1)) * 100 >= threshold,
                increment buffer and total_held.
    Step 3.4: Else:
              - If current_pct >= 65.0, mark status as "CONDONATION", else mark "CRITICAL".
              - Compute minimum classes needed at 100% future attendance:
                Initialize sim_attended = attended, sim_total = total_held, classes_needed = 0.
                While (sim_attended / sim_total) * 100 < threshold:
                    sim_attended += 1
                    sim_total += 1
                    classes_needed += 1
              - Repeat simulation for 90% and 80% future attendance rates.
Step 4: Accumulate cohort statistics: total students, eligible count, condonation count, critical count.
Step 5: Output formatted audit matrix and specific actionable recovery directives for deficient students.
```

---

## 5. Flowchart

### Mermaid Flowchart
```mermaid
flowchart TD
    Start([Start Attendance Recovery Computation]) --> InputData[Read Student Attendance Records]
    InputData --> LoopStart{For Each Student in Record List}
    LoopStart -- Next Student --> Unpack[Unpack Tuple: Roll, Name, Held, Attended]
    Unpack --> CalcPct[Compute: current_pct = Attended / Held * 100]
    CalcPct --> CheckEligible{current_pct >= 75.0%?}
    
    CheckEligible -- Yes --> StatusEligible[Status = ELIGIBLE\nRecovery Needed = 0]
    StatusEligible --> CalcBuffer[Calculate Bunk Buffer Classes]
    CalcBuffer --> PrintRow[Format & Print Student Audit Row]
    
    CheckEligible -- No --> CheckCondonation{current_pct >= 65.0%?}
    CheckCondonation -- Yes --> StatusCond[Status = CONDONATION]
    CheckCondonation -- No --> StatusCrit[Status = CRITICAL]
    StatusCond --> SimRecovery[Simulate Future Classes: sim_att += 1, sim_tot += 1]
    StatusCrit --> SimRecovery
    SimRecovery --> CheckSim{(sim_att / sim_tot) * 100 >= 75%?}
    CheckSim -- No --> SimRecovery
    CheckSim -- Yes --> PrintRow
    
    PrintRow --> LoopStart
    LoopStart -- All Processed --> Summary[Generate Executive Cohort Summary & Action Directives]
    Summary --> End([End Program])
```

---

## 6. Pseudocode

```text
ALGORITHM AttendanceRecoveryComputation:
    INPUT: List students_data containing tuples of (roll_no, name, total_held, attended)
           Float threshold = 75.0
    OUTPUT: Formatted audit table, recovery directives, cohort percentages

    eligible_count = 0
    shortage_count = 0
    critical_count = 0

    FOR EACH record IN students_data DO:
        roll_no, name, total_held, attended = record
        current_pct = ROUND((attended / total_held) * 100, 2)

        IF current_pct >= threshold THEN:
            status = "ELIGIBLE"
            eligible_count = eligible_count + 1
            rec_100 = 0
            bunk_buffer = 0
            temp_held = total_held
            WHILE (attended / (temp_held + 1)) * 100 >= threshold DO:
                bunk_buffer = bunk_buffer + 1
                temp_held = temp_held + 1
            END WHILE
        ELSE:
            shortage_count = shortage_count + 1
            IF current_pct >= 65.0 THEN:
                status = "CONDONATION"
            ELSE:
                status = "CRITICAL"
                critical_count = critical_count + 1
            END IF

            // Simulation of consecutive classes
            sim_att = attended
            sim_tot = total_held
            rec_100 = 0
            WHILE (sim_att / sim_tot) * 100 < threshold DO:
                sim_att = sim_att + 1
                sim_tot = sim_tot + 1
                rec_100 = rec_100 + 1
            END WHILE
        END IF

        PRINT formatted row for roll_no, name, current_pct, status, rec_100, bunk_buffer
    END FOR

    PRINT summary statistics and student directives
END ALGORITHM
```

---

## 7. Python Source Code Listing
The complete, self-contained implementation is available in [`attendance_recovery.py`](file:///e:/shukur%20python%20activity%20based%20learning/case_study_12_attendance_recovery/attendance_recovery.py).

---

## 8. Test Cases & Verification

| Test Case ID | Input `(Held, Attended)` | Expected Attendance % | Expected Status | Expected 100% Recovery Classes | Bunk Buffer | Verification Status |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **TC-01** | `(60, 48)` | 80.00% | ELIGIBLE | 0 | 4 classes | **PASS** |
| **TC-02** | `(60, 42)` | 70.00% | CONDONATION | 12 classes | - | **PASS** |
| **TC-03** | `(60, 52)` | 86.67% | ELIGIBLE | 0 | 9 classes | **PASS** |
| **TC-04** | `(60, 32)` | 53.33% | CRITICAL | 52 classes | - | **PASS** |
| **TC-05** | `(60, 44)` | 73.33% | CONDONATION | 4 classes | - | **PASS** |
| **TC-06** | `(60, 28)` | 46.67% | CRITICAL | 68 classes | - | **PASS** |
| **TC-07** | `(60, 45)` | 75.00% | ELIGIBLE | 0 | 0 classes | **PASS** |

---

## 9. Program Execution Output
```text
==============================================================================
                  STUDENT ATTENDANCE AUDIT & RECOVERY REPORT                  
==============================================================================
Minimum Prescribed Eligibility Threshold: 75.0%

ID       Student Name       Held   Attended  Current %  Status       100% Rec.  90% Rec.   80% Rec.   Bunk Buffer
------------------------------------------------------------------------------------------------------------
24NR1A0501 Shukur             60     48        80.00%     ELIGIBLE     0          0          0          4 classes  
24NR1A0502 Aarav Kumar        60     42        70.00%     CONDONATION  12         21         61         -          
24NR1A0503 Bhavya Sri         60     52        86.67%     ELIGIBLE     0          0          0          9 classes  
24NR1A0504 Charan Teja        60     32        53.33%     CRITICAL     52         87         260        -          
24NR1A0505 Divya Reddy        60     44        73.33%     CONDONATION  4          7          21         -          
24NR1A0506 Eshwar Rao         60     28        46.67%     CRITICAL     68         114        340        -          
24NR1A0507 Farhan Ali         60     57        95.00%     ELIGIBLE     0          0          0          16 classes 
24NR1A0508 Gowri Priya        60     45        75.00%     ELIGIBLE     0          0          0          -          
------------------------------------------------------------------------------------------------------------

EXECUTIVE SUMMARY:
Total Students Evaluated  : 8
Eligible Students (>=75%) : 4 (50.0%)
Shortage Cases (<75%)     : 4 (50.0%)
  - Condonation (65%-74%) : 2
  - Critical Shortage (<65%): 2

ACTIONABLE RECOVERY DIRECTIVES:
[*] Aarav Kumar (24NR1A0502) at 70.0%: Must attend 12 consecutive classes without absence to reach 75.0%.
[*] Charan Teja (24NR1A0504) at 53.3%: Must attend 52 consecutive classes without absence to reach 75.0%.
[*] Divya Reddy (24NR1A0505) at 73.3%: Must attend 4 consecutive classes without absence to reach 75.0%.
[*] Eshwar Rao (24NR1A0506) at 46.7%: Must attend 68 consecutive classes without absence to reach 75.0%.
```

---

## 10. Conclusion & Key Learnings
1. **Dynamic Denominator Effect**: The algorithm clearly demonstrates that attendance recovery is non-linear; recovering a 5% deficit requires significantly more classes when the total number of classes held is already large.
2. **Computational Thinking**: Solving the problem via an iterative `while` simulation provides exact integer answers without relying on complex floating-point algebra that can be susceptible to round-off errors.
3. **Syllabus Mastery**: Implemented strictly utilizing loops, conditionals, tuples, and formatted strings without external math libraries.

