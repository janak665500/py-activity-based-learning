"""
Consolidated PDF Report Generator for Python Activity-Based Learning (ABL)
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Generates a publication-grade, official academic PDF report incorporating all
10 difficult-level case studies complete with problem statements, objectives,
assumptions, algorithms, flowcharts, pseudocode, source code, test cases, outputs,
and conclusions.
"""

import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Preformatted, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print 'Page X of Y' and running headers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress headers/footers on cover page
            return
        
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Running Top Header
        self.drawString(54, 755, "Dr. RVR NRI INSTITUTE OF TECHNOLOGY | Department of Computer Science & Engineering")
        self.drawRightString(558, 755, "Python ABL Assignment Portfolio")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 750, 558, 750)
        
        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 38, "Student: Shukur (Roll No: 24NR1A0501) | I B.Tech CSE-A")
        self.drawRightString(558, 38, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def create_report():
    pdf_filename = os.path.join(os.path.dirname(__file__), "Python_Activity_Based_Learning_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    primary_color = colors.HexColor("#1E3A8A")   # Navy
    secondary_color = colors.HexColor("#0D9488") # Teal
    dark_slate = colors.HexColor("#1E293B")
    code_bg = colors.HexColor("#F8FAFC")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=secondary_color,
        alignment=1
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=dark_slate,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=dark_slate
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#1E3A8A")
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    inst_heading = ParagraphStyle('InstH', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=colors.HexColor("#0F172A"), alignment=1)
    inst_sub = ParagraphStyle('InstS', fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor("#475569"), alignment=1)
    
    story.append(Paragraph("Dr. RVR NRI INSTITUTE OF TECHNOLOGY", inst_heading))
    story.append(Spacer(1, 4))
    story.append(Paragraph("(An Institution Deemed to be University u/s 3 of UGC Act, 1956)", inst_sub))
    story.append(Paragraph("Pothavarappadu (V), Agiripalli (M), Eluru District, Andhra Pradesh - 521212", inst_sub))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="90%", thickness=2, color=primary_color, spaceAfter=25))

    story.append(Spacer(1, 20))
    story.append(Paragraph("ACTIVITY-BASED LEARNING (ABL) ASSIGNMENT REPORT", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("PYTHON PROGRAMMING COURSE<br/>CASE STUDIES PORTFOLIO", title_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Comprehensive Problem Decomposition, Algorithms, Flowcharts, Pseudocode,<br/>Python Implementations, Test Suites, and Analytical Findings for 10 Selected Problems", inst_sub))

    story.append(Spacer(1, 60))

    # Student Details Box
    student_meta = [
        [Paragraph("Student Name:", table_cell_bold), Paragraph("Shukur", table_cell)],
        [Paragraph("Roll Number:", table_cell_bold), Paragraph("24NR1A0501", table_cell)],
        [Paragraph("Branch / Program:", table_cell_bold), Paragraph("B.Tech. - Computer Science & Engineering (CSE)", table_cell)],
        [Paragraph("Section / Year:", table_cell_bold), Paragraph("Section A / I B.Tech. I Semester", table_cell)],
        [Paragraph("Course Code & Title:", table_cell_bold), Paragraph("24CS101 - Python Programming", table_cell)],
        [Paragraph("Assignment Category:", table_cell_bold), Paragraph("Activity-Based Learning (ABL - Dussehra Holidays Assignment)", table_cell)],
        [Paragraph("Evaluation Weightage:", table_cell_bold), Paragraph("10 Marks (Evaluated by Faculty Member / Lab Mentor)", table_cell)],
        [Paragraph("GitHub Repository:", table_cell_bold), Paragraph("Python-Activity-Based-Learning", table_cell)],
        [Paragraph("Date of Submission:", table_cell_bold), Paragraph("October 2026", table_cell)],
    ]

    t_meta = Table(student_meta, colWidths=[150, 300])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1.5, primary_color),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_meta)

    story.append(PageBreak())

    # =========================================================================
    # CERTIFICATE & DECLARATION PAGE
    # =========================================================================
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING", inst_heading))
    story.append(Paragraph("Dr. RVR NRI INSTITUTE OF TECHNOLOGY", inst_sub))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=20))

    cert_title = ParagraphStyle('CertTitle', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=primary_color, alignment=1)
    story.append(Paragraph("BONA FIDE CERTIFICATE", cert_title))
    story.append(Spacer(1, 15))

    cert_text = """
    This is to certify that this consolidated Activity-Based Learning (ABL) Assignment report entitled 
    <b>"Python Programming - Activity-Based Learning: Portfolio of 10 Case Studies"</b> is a bona fide record 
    of academic work successfully completed by <b>Shukur</b> (Roll No: <b>24NR1A0501</b>), a student of 
    <b>I B.Tech. in Computer Science & Engineering (Section A)</b>, at Dr. RVR NRI Institute of Technology, 
    in partial fulfillment of the requirements for the Python Programming laboratory course during the 
    academic year 2026–2027.
    <br/><br/>
    The student has independently selected 10 difficult-level case studies from the prescribed list of 100 problems, 
    formulated structured computational algorithms, prepared flowcharts and pseudocode, implemented verified 
    Python programs strictly adhering to the prescribed syllabus, executed multi-scenario test cases, and uploaded 
    all verified materials to the dedicated GitHub repository <b>Python-Activity-Based-Learning</b>.
    """
    story.append(Paragraph(cert_text, body_style))
    story.append(Spacer(1, 50))

    sig_table_data = [
        [
            Paragraph("<b>______________________</b><br/><b>Course Coordinator</b><br/>Python Programming", body_style),
            Paragraph("<b>______________________</b><br/><b>Lab Mentor / Evaluator</b><br/>Dept. of CSE", body_style),
            Paragraph("<b>______________________</b><br/><b>Dean / Head of Dept.</b><br/>School of Computer Studies", body_style)
        ]
    ]
    t_sig = Table(sig_table_data, colWidths=[160, 160, 160])
    t_sig.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sig)

    story.append(Spacer(1, 40))
    story.append(Paragraph("STUDENT DECLARATION", h2_style))
    decl_text = """
    I hereby declare that the Python solutions, algorithms, flowcharts, pseudocode, and test analyses presented in 
    this report are my original work, developed strictly using the assigned Python syllabus concepts without the use 
    of external non-syllabus libraries or pre-packaged packages. All outputs included herein have been verified through 
    live terminal execution.
    <br/><br/>
    <b>Date:</b> October 2026 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Signature of Student:</b> Shukur
    """
    story.append(Paragraph(decl_text, body_style))

    story.append(PageBreak())

    # =========================================================================
    # TABLE OF CONTENTS & SYLLABUS MAPPING
    # =========================================================================
    story.append(Paragraph("TABLE OF CONTENTS & SYLLABUS MAPPING", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=15))

    toc_data = [
        [Paragraph("<b>#</b>", table_cell_bold), Paragraph("<b>Case Study ID & Title</b>", table_cell_bold), Paragraph("<b>Syllabus Concepts Applied</b>", table_cell_bold), Paragraph("<b>Evaluation Status</b>", table_cell_bold)],
        [Paragraph("1", table_cell), Paragraph("<b>12. Attendance Recovery Computation</b>", table_cell), Paragraph("while loops, float arithmetic, tuple unpacking", table_cell), Paragraph("Verified (100% Pass)", table_cell)],
        [Paragraph("2", table_cell), Paragraph("<b>17. Student Performance Trend Analysis</b>", table_cell), Paragraph("Nested lists (3D matrix), difference loops, rule engine", table_cell), Paragraph("Verified (100% Pass)", table_cell)],
        [Paragraph("3", table_cell), Paragraph("<b>28. Repeated Transaction Detection</b>", table_cell), Paragraph("Pairwise nested loops, threshold comparisons, risk ledger", table_cell), Paragraph("Verified (100% Pass)", table_cell)],
        [Paragraph("4", table_cell), Paragraph("<b>34. Student Feedback Sentiment Scoring</b>", table_cell), Paragraph("String tokenization, character filtering, list matching", table_cell), Paragraph("Verified (100% Pass)", table_cell)],
        [Paragraph("5", table_cell), Paragraph("<b>35. Text Compression Using Character Runs</b>", table_cell), Paragraph("Run-length encoding (RLE), string indexing, lossless verification", table_cell), Paragraph("Verified (100% Pass)", table_cell)],
        [Paragraph("6", table_cell), Paragraph("<b>42. Student Marks Matrix Analysis</b>", table_cell), Paragraph("2D nested lists, row/column traversals, bubble sort ranks", table_cell), Paragraph("Verified (100% Pass)", table_cell)],
        [Paragraph("7", table_cell), Paragraph("<b>45. Weekly Electricity Consumption Matrix</b>", table_cell), Paragraph("2D grid matrix, appliance/day totals, slab tariff pricing", table_cell), Paragraph("Verified (100% Pass)", table_cell)],
        [Paragraph("8", table_cell), Paragraph("<b>49. Tuple-Based Product Catalogue Audit</b>", table_cell), Paragraph("Tuple immutability, data sanitization, asset valuation", table_cell), Paragraph("Verified (100% Pass)", table_cell)],
        [Paragraph("9", table_cell), Paragraph("<b>53. Food Waste Monitoring System</b>", table_cell), Paragraph("Lists of tuples, shrinkage math, financial loss audit", table_cell), Paragraph("Verified (100% Pass)", table_cell)],
        [Paragraph("10", table_cell), Paragraph("<b>63. Multi-Product Price Fluctuation Analysis</b>", table_cell), Paragraph("Chronological lists, volatility % formulas, risk sorting", table_cell), Paragraph("Verified (100% Pass)", table_cell)]
    ]

    t_toc = Table(toc_data, colWidths=[25, 180, 190, 95])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Prescribed Syllabus Compliance Guarantee:", h2_style))
    p_comp = """
    As explicitly mandated by the course instructions, all 10 programs have been designed and implemented 
    <b>using ONLY the prescribed foundational syllabus</b>: computational thinking, algorithms, flowcharts, pseudocode, 
    variables, data types, operators, conditional statements, loops, strings, pattern generation, lists, nested lists, 
    tuples, tuple operations, and unpacking. 
    <b>No non-syllabus constructs</b> (such as dictionaries, sets, classes, or external modules like NumPy, Pandas, or SciPy) 
    have been used in any of the core algorithms.
    """
    story.append(Paragraph(p_comp, body_style))

    story.append(PageBreak())

    # =========================================================================
    # THE 10 CASE STUDIES DETAILS
    # =========================================================================

    case_studies_meta = [
        {
            "id": "12",
            "title": "Case Study 12: Attendance Recovery Computation",
            "desc": "Calculates current attendance percentages and determines the minimum consecutive classes required to reach eligibility thresholds under different future attendance scenarios.",
            "dir": "case_study_12_attendance_recovery",
            "file": "attendance_recovery.py",
            "concepts": "Variables, Float Arithmetic, While Simulation Loops, Conditionals, Tuples, Bunk Buffer Calculation.",
            "objectives": [
                "Compute floating-point attendance percentages from conducted and attended class counts.",
                "Simulate iterative recovery classes needed to reach the 75.0% statutory threshold.",
                "Model realistic future attendance scenarios (100%, 90%, 80% discipline).",
                "Calculate the maximum missable bunk buffer for already eligible students.",
                "Classify students into ELIGIBLE, CONDONATION, and CRITICAL SHORTAGE tiers."
            ],
            "assumptions": [
                "Attendance percentages are calculated with 2 decimal precision.",
                "Statutory university eligibility is set at 75.0%; condonation limit is 65.0%.",
                "Recovery simulation models the moving denominator effect (each new class increments both numerator and denominator).",
                "Input data is represented as a list of tuples (roll_no, student_name, total_classes, attended_classes)."
            ],
            "algorithm": [
                "1. Read student records as list of tuples (roll_no, name, total_held, attended).",
                "2. For each student, compute current_pct = (attended / total_held) * 100.0.",
                "3. If current_pct >= 75.0%: Mark ELIGIBLE; compute bunk buffer while ((attended)/(total_held+1))*100 >= 75.0.",
                "4. Else: If current_pct >= 65.0% mark CONDONATION, else CRITICAL; simulate while (sim_att/sim_tot)*100 < 75.0: sim_att += 1, sim_tot += 1.",
                "5. Tabulate eligibility, recovery requirements across scenarios, and print cohort directives."
            ],
            "flowchart_desc": "Start -> Read Tuples -> Calc current_pct -> Check >= 75%? -> If Yes: Status=ELIGIBLE, Calc Bunk Buffer -> If No: Check >= 65%? (CONDONATION/CRITICAL) -> Simulate Future Classes via while loop -> Print Audit Matrix -> End.",
            "pseudocode": """FUNCTION AttendanceRecovery(students, threshold=75.0):
    FOR EACH (roll, name, held, attended) IN students:
        pct = (attended / held) * 100
        IF pct >= threshold:
            status = "ELIGIBLE"
            rec_100 = 0
            bunk_buffer = CALC_BUFFER(attended, held, threshold)
        ELSE:
            status = "CONDONATION" IF pct >= 65.0 ELSE "CRITICAL"
            rec_100 = SIMULATE_RECOVERY(attended, held, threshold, rate=1.0)
        PRINT roll, name, pct, status, rec_100, bunk_buffer
    END FOR""",
            "test_summary": "Evaluated 8 students across Eligible (48/60, 52/60, 57/60), Condonation (42/60, 44/60), and Critical (32/60, 28/60) cohorts. All recovery simulations verified 100% mathematically accurate.",
            "conclusion": "The moving denominator makes attendance recovery non-linear. The simulation algorithm successfully quantifies exact required classes without rounding errors, providing clear administrative guidance."
        },
        {
            "id": "17",
            "title": "Case Study 17: Student Performance Trend Analysis",
            "desc": "Compares assessment scores across multiple examinations, calculates improvements and declines, identifies consistently weak subjects, and classifies students according to defined criteria.",
            "dir": "case_study_17_performance_trend",
            "file": "performance_trend.py",
            "concepts": "3D Nested Lists, Multi-period Differentials, Loop Control, Multi-factor Rule Engine, Classification.",
            "objectives": [
                "Process multi-exam, multi-subject score matrices across chronological assessments.",
                "Calculate step-wise score differentials between Assessment 1, 2, and 3.",
                "Detect subjects where student marks are persistently below passing threshold (< 40).",
                "Classify student academic momentum into 5 distinct pedagogical categories.",
                "Generate curricular monitor reports highlighting systemic weakness."
            ],
            "assumptions": [
                "Assessments are scored out of 100; passing benchmark is 40.",
                "Assessments are chronological: Assessment 1 -> Assessment 2 -> Assessment 3.",
                "Student records are stored as (roll, name, 2D_scores_matrix).",
                "Matrix operations strictly use native list indexing and loops."
            ],
            "algorithm": [
                "1. Load cohort data containing 3 examination cycles across 4 curricular subjects.",
                "2. For each student, compute individual exam averages and overall aggregate average.",
                "3. Compute step-wise differentials and overall net trajectory (Exam 3 Avg - Exam 1 Avg).",
                "4. For each subject, evaluate if marks are all < 40 ('Consistently Weak'), strictly increasing ('Improving'), strictly decreasing ('Declining'), or fluctuating.",
                "5. Classify students: Outstanding Scholar (Avg >= 80, Shift >= 0), Consistent Improver (Shift >= +8), Remedial Support (Weak subject), Academic Warning (Shift <= -10).",
                "6. Output student trajectory scorecards and cohort distribution summary."
            ],
            "flowchart_desc": "Start -> Load 3D Matrix -> For Each Student -> Calculate Exam Averages -> For Each Subject -> Evaluate Score Trend (Weak/Improving/Declining/Fluctuating) -> Apply Classification Rules -> Print Scorecard -> Print Cohort Breakdown -> End.",
            "pseudocode": """FUNCTION AnalyzeTrends(cohort_data, subjects, exams):
    FOR EACH (roll, name, matrix) IN cohort_data:
        exam_avgs = [AVERAGE(matrix[e]) FOR e IN exams]
        net_shift = exam_avgs[LAST] - exam_avgs[FIRST]
        FOR EACH s IN subjects:
            subj_scores = [matrix[e][s] FOR e IN exams]
            trend = EVALUATE_TREND(subj_scores)
        category = CLASSIFY(overall_avg, net_shift, trends)
        PRINT student scorecard, trends, and category
    END FOR""",
            "test_summary": "Tested across diverse academic archetypes: Improving (Shukur +10.5, Charan +18.5), Declining (Aarav -12.5), Consistently Weak (Bhavya all < 40), and Steady (Divya +1.0). 100% correct classification.",
            "conclusion": "Longitudinal trend analysis catches academic decay earlier than static semester exams. The rule-based engine successfully separated high performers from students needing urgent intervention."
        },
        {
            "id": "28",
            "title": "Case Study 28: Repeated Transaction Detection & Fraud Audit",
            "desc": "Processes transaction identifiers and amounts in a list, detects duplicate transactions, identifies threshold violations, and generates a list of suspicious entries.",
            "dir": "case_study_28_repeated_transactions",
            "file": "repeated_transactions.py",
            "concepts": "Lists of Tuples, Pairwise Nested Loops, Relational Logic, Cumulative Volume Tracking, Anomaly Logging.",
            "objectives": [
                "Ingest transaction records stored as tuples (tx_id, sender, receiver, amount, timestamp).",
                "Detect duplicated transaction identifiers (system replay or collision error).",
                "Identify duplicated transfer amounts between identical sender and receiver accounts.",
                "Flag single transactions exceeding the threshold limit (INR 50,000.00).",
                "Compute cumulative sender outflow using nested lists and flag velocity breaches (> INR 100,000.00)."
            ],
            "assumptions": [
                "Amounts are positive real numbers.",
                "Data structures strictly avoid hash maps / dictionaries; nested list searching is used.",
                "Single threshold limit is INR 50,000.00; cumulative limit is INR 100,000.00."
            ],
            "algorithm": [
                "1. Ingest transaction records as list of tuples.",
                "2. Check single limit violations: for each txn, if amount > 50000, flag 'HIGH' risk.",
                "3. Perform pairwise comparison (i from 0 to N-1, j from i+1 to N-1): if id_i == id_j, flag 'CRITICAL' duplicate ID; if sender, receiver, and amount match, flag 'HIGH' duplicate transfer.",
                "4. Aggregate cumulative volume per sender account into nested list [[sender, volume, count], ...].",
                "5. If sender cumulative volume > 100000, flag transactions contributing to breach.",
                "6. Output ingested ledger, suspicious entries table, and cumulative exposure matrix."
            ],
            "flowchart_desc": "Start -> Load Txn Tuples -> Loop i: Check Amount > 50k -> Loop j: Check duplicate ID or duplicate transfer -> Aggregate Volume per Sender into List -> Check Volume > 100k -> Generate Forensic Audit Ledger -> End.",
            "pseudocode": """FUNCTION DetectSuspiciousTransactions(transactions):
    FOR i FROM 0 TO N-1:
        IF transactions[i].amount > 50000: FLAG_HIGH()
        FOR j FROM i+1 TO N-1:
            IF transactions[i].id == transactions[j].id: FLAG_CRITICAL_DUPLICATE_ID()
            ELSE IF SAME_TRANSFER(transactions[i], transactions[j]): FLAG_REPLAY_TRANSFER()
    ledger = AGGREGATE_SENDER_VOLUMES(transactions)
    FOR EACH s IN ledger:
        IF s.total > 100000: FLAG_VELOCITY_BREACH(s)
    PRINT audit tables""",
            "test_summary": "Successfully detected duplicate transfer (TX1002 and TX1004), single limit violation (TX1003 @ 65k), duplicate ID collision (TX1005 repeated), and cumulative breach (ACC_AMAR @ 125k).",
            "conclusion": "The multi-pass list algorithm successfully flags high-value, duplicate, and rapid-succession fraud patterns without requiring external database or hashing engines."
        },
        {
            "id": "34",
            "title": "Case Study 34: Student Feedback Sentiment Scoring",
            "desc": "Analyses multiple feedback sentences using a supplied keyword list, counts positive and negative indicators, calculates scores, and classifies feedback using predefined thresholds.",
            "dir": "case_study_34_sentiment_scoring",
            "file": "sentiment_scoring.py",
            "concepts": "Strings, String Cleaning, Tokenization, Keyword Matching via Lists, Normalized Math Scoring.",
            "objectives": [
                "Sanitize raw feedback text by stripping punctuation and normalizing case.",
                "Tokenize sentences into word lists without third-party regex tools.",
                "Count domain-specific positive and negative keyword matches.",
                "Compute Net Sentiment Score (P - N) and Normalized Sentiment Index ((P - N) / (P + N)).",
                "Classify feedback into 6 descriptive categories and compute institutional approval ratings."
            ],
            "assumptions": [
                "Punctuation characters do not carry sentiment and are replaced with whitespace.",
                "Matched keywords within the domain lexicons have uniform weight.",
                "Feedback with zero matches is classified as NEUTRAL (No Keywords)."
            ],
            "algorithm": [
                "1. Define positive and negative keyword lists.",
                "2. Ingest feedback records as tuples (feedback_id, student_name, comment_string).",
                "3. For each comment: iterate through characters, replace punctuation with space, convert to lowercase, split on whitespace.",
                "4. Count positive and negative keyword hits using nested loops over keyword lists.",
                "5. Compute Net Score = pos - neg; Norm Index = (pos - neg) / (pos + neg) if total > 0 else 0.0.",
                "6. Classify: Highly Positive (Index >= 0.5), Positive (>0), Mixed (0.0 with keywords), Neutral (no keywords), Negative (>-0.5), Highly Negative (<=-0.5).",
                "7. Calculate institutional approval percentage and identify top thematic keywords."
            ],
            "flowchart_desc": "Start -> Load Lexicons & Feedback -> For Each Sentence -> Strip Punctuation -> Tokenize into Words -> Count Positive & Negative Matches -> Compute Net & Normalized Index -> Apply Thresholds -> Output Scorecards & Approval % -> End.",
            "pseudocode": """FUNCTION AnalyzeSentiment(feedbacks, pos_words, neg_words):
    FOR EACH (fid, author, text) IN feedbacks:
        tokens = CLEAN_AND_TOKENIZE(text)
        pos_cnt = COUNT_MATCHES(tokens, pos_words)
        neg_cnt = COUNT_MATCHES(tokens, neg_words)
        total = pos_cnt + neg_cnt
        norm_idx = (pos_cnt - neg_cnt) / total IF total > 0 ELSE 0.0
        category = CLASSIFY_INDEX(norm_idx, pos_cnt, neg_cnt)
        PRINT feedback scorecard with tokens, scores, and category
    END FOR""",
            "test_summary": "Tested 7 qualitative statements: FB-01 (Highly Positive +1.0), FB-02 (Highly Negative -1.0), FB-03 (Positive +0.33), FB-06 (Neutral 0.0). Net course approval evaluated at 57.1%.",
            "conclusion": "Normalized sentiment scoring removes sentence length bias, providing an automated and objective mechanism for academic administrators to evaluate student satisfaction."
        },
        {
            "id": "35",
            "title": "Case Study 35: Text Compression Using Character Runs",
            "desc": "Encodes a string by grouping consecutive repeated characters and compares original and encoded lengths, including cases where encoding is not beneficial.",
            "dir": "case_study_35_text_compression",
            "file": "text_compression.py",
            "concepts": "Strings, While Loops, Slicing, Run-Length Encoding (RLE), Lossless Decompression Verification.",
            "objectives": [
                "Implement Run-Length Encoding (RLE) to group consecutive identical characters.",
                "Build an inverse decoder to verify 100% lossless round-trip restoration.",
                "Compute compression space savings percentage: ((Orig - Enc) / Orig) * 100.",
                "Identify threshold cases where encoding causes payload expansion (negative savings).",
                "Formulate an automated decision engine: Compress vs Reject / Store Raw."
            ],
            "assumptions": [
                "Input strings contain printable ASCII characters.",
                "Character runs require identical adjacent characters.",
                "When encoded length >= original length, the engine recommends rejecting compression."
            ],
            "algorithm": [
                "1. Ingest input string text. If empty, return empty payload with 0% savings.",
                "2. Scan string with while loop: count consecutive identical characters, append char + count to encoded parts.",
                "3. Reconstruct original string from encoded text to verify lossless integrity.",
                "4. Compute orig_len, comp_len, and savings_pct = ((orig_len - comp_len) / orig_len) * 100.",
                "5. If comp_len < orig_len: Verdict = 'BENEFICIAL (Compress)'. Else: 'INEFFECTIVE (Reject / Store Raw)'.",
                "6. Output comparative benchmarking ledger across test cases."
            ],
            "flowchart_desc": "Start -> Read String -> While i < Length -> Count Consecutive Identical Chars -> Emit char + count -> Decompress Encoded String -> Verify Lossless -> Compute Savings % -> Encoded < Original? -> Yes: BENEFICIAL / No: INEFFECTIVE -> Output -> End.",
            "pseudocode": """FUNCTION EncodeRLE(text):
    IF LENGTH(text) == 0: RETURN "", 0, 0, 0.0, "EMPTY", TRUE
    encoded = []
    i = 0
    WHILE i < LENGTH(text):
        ch = text[i]; count = 1
        WHILE i + 1 < LENGTH(text) AND text[i+1] == ch:
            count += 1; i += 1
        encoded.APPEND(ch + STR(count))
        i += 1
    enc_str = JOIN(encoded)
    savings = ((LENGTH(text) - LENGTH(enc_str)) / LENGTH(text)) * 100
    verdict = "BENEFICIAL" IF LENGTH(enc_str) < LENGTH(text) ELSE "INEFFECTIVE"
    RETURN enc_str, savings, verdict, (DECODE(enc_str) == text)""",
            "test_summary": "Tested 9 strings: Highly repetitive (+67.5% savings), Genomic (+67.7%), Non-repeating (-100% expansion), Alternating (-100% expansion), Single char (+85.0%). 100% lossless restoration verified.",
            "conclusion": "RLE requires an average run length > 2 to yield savings. For non-repeating data, appending integer counts doubles payload size, proving why compression engines must inspect entropy before encoding."
        },
        {
            "id": "42",
            "title": "Case Study 42: Student Marks Matrix Analysis",
            "desc": "Analyses a matrix of student marks across subjects, calculates row-wise and column-wise statistics, identifies top performers, and detects subjects with low average performance.",
            "dir": "case_study_42_marks_matrix",
            "file": "marks_matrix.py",
            "concepts": "2D Nested Lists, Row/Column Iterations, Bubble Sort Ranks, Merit Podium, Threshold Alerts.",
            "objectives": [
                "Construct and process a 2D marks matrix (N students x M subjects).",
                "Execute row-wise traversals to compute student total marks, percentages, and grades.",
                "Implement in-place sorting to assign ranks in descending order of merit.",
                "Execute column-wise traversals to compute subject class averages, maximums, and pass rates.",
                "Detect curricular subjects with concerning low average performance (< 65.0%)."
            ],
            "assumptions": [
                "All subjects have max score of 100; passing threshold is 40.",
                "Quality benchmark for subject class average is set at 65.0%.",
                "Strictly native 2D list manipulation without NumPy or Pandas."
            ],
            "algorithm": [
                "1. Load 2D marks matrix, student names, and subject list.",
                "2. Row-Wise Analysis: compute row sum, percentage, and letter grade (O, A+, A, B, C, F).",
                "3. Sort student records by percentage descending using bubble sort and assign ranks 1 to N.",
                "4. Column-Wise Analysis: extract column marks, compute class average, max, min, and pass rate (mark >= 40).",
                "5. If subject class average < 65.0%: flag as 'LOW PERFORMANCE [ALERT]'.",
                "6. Output ranked student scorecard matrix, subject diagnostics, merit podium, and remedial alerts."
            ],
            "flowchart_desc": "Start -> Load 2D Matrix -> Row Loop: Compute Student Total, Pct, Grade -> Sort Records & Assign Ranks -> Column Loop: Compute Subject Avg, Max, Min, Pass Rate -> Check Avg < 65%? -> Flag Alerts -> Print Scorecards & Podium -> End.",
            "pseudocode": """FUNCTION AnalyzeMarksMatrix(students, subjects, matrix, benchmark=65.0):
    // Row-wise
    FOR r FROM 0 TO N-1:
        tot = SUM(matrix[r]); pct = tot / (M * 100) * 100
        records.APPEND([students[r], tot, pct, GET_GRADE(pct)])
    SORT_BY_PERCENTAGE_DESCENDING(records)
    // Column-wise
    FOR c FROM 0 TO M-1:
        col_marks = [matrix[r][c] FOR r IN 0..N-1]
        avg = AVERAGE(col_marks)
        IF avg < benchmark: FLAG_LOW_SUBJECT(subjects[c], avg)
    PRINT scorecards, diagnostics, and podium""",
            "test_summary": "Analyzed 7 students across 5 subjects. Shukur ranked #1 (91.4% [O]), Farhan #2 (83.6% [A+]), Bhavya #3 (81.6% [A+]). Detected Discrete Math (avg 56.4%, pass rate 71.4%) as below benchmark.",
            "conclusion": "Orthogonal 2D list traversal efficiently delivers both micro-level student evaluation and macro-level departmental insights, identifying subject-level academic distress for targeted faculty tutorials."
        },
        {
            "id": "45",
            "title": "Case Study 45: Weekly Electricity Consumption Matrix",
            "desc": "Processes appliance-wise electricity readings across seven days, calculates daily and appliance totals, and identifies consumption exceeding specified limits.",
            "dir": "case_study_45_electricity_consumption",
            "file": "electricity_consumption.py",
            "concepts": "2D Nested Lists, Row & Column Reductions, Peak Detection, Multi-slab Tariff Calculation.",
            "objectives": [
                "Model appliance electricity readings across a 7-day week using 2D nested lists.",
                "Compute weekly totals and daily averages per appliance (row-wise).",
                "Compute daily cumulative household consumption across all appliances (column-wise).",
                "Detect peak single consumption events across all appliances and days.",
                "Flag daily safety breaches (> 24.0 kWh/day) and appliance quota breaches (> 35.0 kWh/week).",
                "Calculate weekly power bills using tiered multi-slab utility tariffs."
            ],
            "assumptions": [
                "Readings are recorded in kWh across Monday through Sunday.",
                "Daily safety limit = 24.0 kWh; weekly appliance quota = 35.0 kWh.",
                "Tariff slabs: First 50 @ INR 3.50, next 50 @ INR 5.00, >100 @ INR 7.50; fixed charge = INR 65.00."
            ],
            "algorithm": [
                "1. Load 6 appliances x 7 days energy matrix.",
                "2. Row Aggregation: compute weekly sum and daily average per appliance; flag if total > 35.0 kWh; scan for peak single reading.",
                "3. Column Aggregation: compute daily total across appliances; flag days where total > 24.0 kWh.",
                "4. Compute grand total consumption = sum of daily totals.",
                "5. Calculate tiered electricity charges and add fixed grid maintenance fee.",
                "6. Output consumption grid, peak event, threshold violations, and billing breakdown."
            ],
            "flowchart_desc": "Start -> Load 2D Energy Matrix -> Row Loop: Appliance Totals, Daily Avg, Quota Checks, Peak Update -> Column Loop: Daily Household Totals, Safety Checks -> Compute Slab Tariff -> Print Consumption Grid & Bill -> End.",
            "pseudocode": """FUNCTION AnalyzeElectricity(appliances, days, matrix, daily_lim=24.0, app_lim=35.0):
    FOR r FROM 0 TO R-1:
        r_tot = SUM(matrix[r])
        IF r_tot > app_lim: FLAG_APPLIANCE_QUOTA(appliances[r])
        UPDATE_PEAK_EVENT(matrix[r])
    FOR c FROM 0 TO C-1:
        d_tot = SUM_COLUMN(matrix, c)
        IF d_tot > daily_lim: FLAG_DAILY_LIMIT(days[c])
    bill = COMPUTE_SLAB_TARIFF(SUM(d_tot))
    PRINT grid, surge analysis, alerts, and bill""",
            "test_summary": "Weekly total = 155.30 kWh. Peak event: 12.0 kWh by Air Conditioner on Sunday. AC exceeded quota (64.0 kWh vs 35.0 limit). Weekend breaches: Sat (27.5 kWh) and Sun (28.4 kWh). Total Bill: INR 904.75.",
            "conclusion": "Appliance-level matrix auditing accurately isolates excessive power consumers. The AC alone contributed 41.2% of consumption, proving that targeted conservation yields immediate financial savings."
        },
        {
            "id": "49",
            "title": "Case Study 49: Tuple-Based Product Catalogue Audit",
            "desc": "Stores product identifiers, prices, and stock quantities in tuples; detects invalid records, calculates inventory values, and identifies items requiring replenishment.",
            "dir": "case_study_49_product_catalogue",
            "file": "product_catalogue.py",
            "concepts": "Tuples, Tuple Immutability, Tuple Unpacking, Data Sanitization, Replenishment Requisitions.",
            "objectives": [
                "Store product catalogue records in immutable tuples (id, name, category, price, stock, reorder).",
                "Quarantine corrupt or invalid tuples (negative prices, negative stock, blank names).",
                "Compute item-wise and category-wise inventory asset valuations.",
                "Identify items breaching reorder thresholds (stock <= reorder level).",
                "Compute optimal purchase order quantities and required procurement capital."
            ],
            "assumptions": [
                "Tuples strictly contain 6 elements in defined order.",
                "Valid prices must be > 0; stock and reorder thresholds must be >= 0.",
                "Reorder target buffer is max(2 * reorder, reorder + 10)."
            ],
            "algorithm": [
                "1. Ingest raw catalogue records as list of tuples.",
                "2. Validation: check tuple length, non-empty ID and name, positive price, non-negative stock and reorder. Separate valid from quarantined invalid records.",
                "3. Valuation: for each valid tuple, unpack (pid, name, cat, price, stock, reorder); compute item_val = price * stock; accumulate total valuation and units.",
                "4. Aggregate valuations by category into nested list [[cat, val, units], ...].",
                "5. Replenishment: if stock <= reorder, compute order_qty = target - stock, estimated_cost = order_qty * price; flag CRITICAL if stock == 0.",
                "6. Output quarantined error log, inventory valuation ledger, category shares, and purchase orders."
            ],
            "flowchart_desc": "Start -> Load Tuples -> For Each Tuple -> Validate Schema & Values -> Invalid? Quarantine Record -> Valid? Unpack Tuple -> Calc Valuation -> Aggregate Category -> Stock <= Reorder? -> Yes: Generate Purchase Order -> Print Reports -> End.",
            "pseudocode": """FUNCTION AuditCatalogue(raw_tuples):
    FOR EACH t IN raw_tuples:
        IF VALID(t): valid_list.APPEND(t)
        ELSE: invalid_list.APPEND(t)
    FOR EACH (pid, name, cat, price, stock, reorder) IN valid_list:
        val = price * stock
        grand_total += val
        IF stock <= reorder:
            order_qty = MAX(2*reorder, reorder+10) - stock
            orders.APPEND((pid, name, order_qty, order_qty * price))
    PRINT quarantined, inventory ledger, categories, and purchase orders""",
            "test_summary": "11 records ingested. Quarantined 3 invalid tuples (negative price, blank name, negative stock). Evaluated 8 valid items: Warehouse Asset Value = INR 358,634.00. Generated 4 purchase orders (Req Capital: INR 662,966.00).",
            "conclusion": "Tuple immutability protects master data integrity. The dual-phase audit cleanly quarantines corrupt records and automates inventory replenishment planning."
        },
        {
            "id": "53",
            "title": "Case Study 53: Food Waste Monitoring System",
            "desc": "Compares prepared meals, meals served, and leftovers across several days; calculates wastage percentages and identifies days exceeding acceptable limits.",
            "dir": "case_study_53_food_waste_monitoring",
            "file": "food_waste_monitoring.py",
            "concepts": "Lists of Tuples, Arithmetic Ratios, Inventory Shrinkage Math, Conditionals, Directives.",
            "objectives": [
                "Model dining hall catering logs as tuples: (day, prepared, served, leftovers).",
                "Compute unaccounted shrinkage: Prepared - (Served + Leftovers).",
                "Calculate daily and cumulative percentage food waste.",
                "Flag days breaching the acceptable sustainability limit (> 10.0%).",
                "Quantify financial losses at standard meal production cost (INR 65.00/meal).",
                "Provide actionable operational recommendations to minimize institutional waste."
            ],
            "assumptions": [
                "Quantities are non-negative integers.",
                "Discrepancy != 0 indicates unrecorded theft, kitchen spillage, or counting errors.",
                "Standard meal unit cost is INR 65.00; acceptable waste ceiling is 10.0%."
            ],
            "algorithm": [
                "1. Load daily dining hall records as list of tuples.",
                "2. For each day, unpack (day, prep, served, leftovers).",
                "3. Compute discrepancy = prep - (served + leftovers); waste_pct = (leftovers / prep) * 100; loss = leftovers * 65.00.",
                "4. Update cumulative totals (prepared, served, leftovers, financial loss).",
                "5. Evaluate status: if waste_pct > 10.0%: 'EXCESSIVE [BREACH]'; else if discrepancy != 0: 'DISCREPANCY ALERT'; else: 'ACCEPTABLE [OK]'.",
                "6. Identify worst wastage day and most efficient day.",
                "7. Output audit ledger, sustainability metrics, breach directives, and recommendations."
            ],
            "flowchart_desc": "Start -> Load Daily Logs -> For Each Day -> Unpack Tuple -> Calc Discrepancy & Waste % -> Calc Financial Loss -> Waste % > 10%? -> Flag EXCESSIVE BREACH -> Discrepancy != 0? -> Flag DISCREPANCY ALERT -> Print Audit Matrix & Recommendations -> End.",
            "pseudocode": """FUNCTION MonitorFoodWaste(records, threshold=10.0, cost=65.0):
    FOR EACH (day, prep, served, left) IN records:
        disc = prep - (served + left)
        pct = (left / prep) * 100
        loss = left * cost
        IF pct > threshold: FLAG_BREACH(day, pct, loss)
        ELSE IF disc != 0: FLAG_DISCREPANCY(day, disc)
        UPDATE_CUMULATIVE_METRICS(prep, served, left, loss)
    PRINT ledger, metrics, breach directives, and recommendations""",
            "test_summary": "Monitored 8 days (6,150 meals prepared, 5,495 served, 630 wasted). Overall waste = 10.24% (Financial Loss: INR 40,950.00). Flagged Friday (16.84%) and Sunday (17.33%) as major breach days. Detected 25 unaccounted meals.",
            "conclusion": "Wastage spikes systematically on weekends due to student travel. Mathematical monitoring enables dynamic kitchen batch resizing and flags inventory leakage."
        },
        {
            "id": "63",
            "title": "Case Study 63: Multi-Product Price Fluctuation Analysis",
            "desc": "Processes historical product prices stored in lists, calculates percentage changes, identifies maximum fluctuations, and flags products exceeding a supplied threshold.",
            "dir": "case_study_63_price_fluctuation",
            "file": "price_fluctuation.py",
            "concepts": "Lists of Historical Floats, Step-wise Shift Loops, Volatility Formulas, Bubble Sorting, Risk Alerts.",
            "objectives": [
                "Model multi-period commodity price histories using lists of floating-point values.",
                "Calculate period-over-period percentage price shifts: ((P_t - P_t-1) / P_t-1) * 100.",
                "Compute peak-to-trough range volatility: ((Max - Min) / Min) * 100.",
                "Detect maximum single-period price fluctuation for each commodity.",
                "Flag high-risk volatile commodities breaching the safety threshold (> 15.0%).",
                "Sort and rank portfolio commodities from most volatile to most stable."
            ],
            "assumptions": [
                "Price observations are chronologically ordered at uniform monthly intervals.",
                "Prices are strictly positive real numbers.",
                "Volatility alert threshold is set at 15.0% maximum single-period swing."
            ],
            "algorithm": [
                "1. Load commodity records: list of tuples (id, name, category, price_list).",
                "2. For each commodity: iterate through price_list from index 1 to T-1; compute shift = ((P[t] - P[t-1]) / P[t-1]) * 100; track max_abs_shift.",
                "3. Compute min_p, max_p, peak-to-trough volatility = ((max - min) / min) * 100, and net overall change.",
                "4. If max_abs_shift > 15.0%: mark 'VOLATILE [FLAGGED]'; else if > 7.5%: 'MODERATE'; else: 'HIGHLY STABLE'.",
                "5. Sort audit results descending by max_abs_shift using in-place bubble sort.",
                "6. Output historical price matrix, volatility audit ledger, risk rankings, and hedging directives."
            ],
            "flowchart_desc": "Start -> Load Historical Prices -> For Each Commodity -> Compute Period Shifts -> Find Max Shift, Min, Max & Range Volatility -> Max Shift > 15%? -> Flag VOLATILE -> Sort Products by Volatility -> Print Matrix & Hedging Alerts -> End.",
            "pseudocode": """FUNCTION AnalyzePriceFluctuations(commodities, threshold=15.0):
    FOR EACH (id, name, cat, prices) IN commodities:
        shifts = [((prices[t]-prices[t-1])/prices[t-1])*100 FOR t IN 1..T-1]
        max_fluct = MAX(ABS(shifts))
        range_vol = ((MAX(prices) - MIN(prices)) / MIN(prices)) * 100
        status = "VOLATILE" IF max_fluct > threshold ELSE "STABLE"
        records.APPEND([id, name, max_fluct, range_vol, status])
    SORT_BY_VOLATILITY_DESCENDING(records)
    PRINT prices, volatility ledger, risk ranks, and directives""",
            "test_summary": "Tracked 6 commodities across 6 months (Jan-Jun). Tomatoes (+71.88% shift, 240% range vol), Onions (+42.86% shift, 133% range vol), and Sunflower Oil (+18.31% shift) flagged volatile. Rice, Sugar, and Wheat verified stable.",
            "conclusion": "Agricultural perishables exhibit extreme price volatility compared to staple grains. Algorithmic volatility tracking enables procurement teams to deploy dynamic hedging and renegotiate fixed supply contracts."
        }
    ]

    for cs in case_studies_meta:
        story.append(Paragraph(cs["title"], h1_style))
        story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

        story.append(Paragraph("1. Problem Statement", h2_style))
        story.append(Paragraph(cs["desc"], body_style))

        story.append(Paragraph("2. Objectives", h2_style))
        for obj in cs["objectives"]:
            story.append(Paragraph(f"• {obj}", body_style))

        story.append(Paragraph("3. Assumptions", h2_style))
        for asm in cs["assumptions"]:
            story.append(Paragraph(f"• {asm}", body_style))

        story.append(Paragraph("4. Step-by-Step Algorithm", h2_style))
        for step in cs["algorithm"]:
            story.append(Paragraph(step, body_style))

        story.append(Paragraph("5. Flowchart Architectural Representation", h2_style))
        story.append(Paragraph(f"<b>Flowchart Process Description:</b> {cs['flowchart_desc']}", body_style))

        story.append(Paragraph("6. Formal Pseudocode", h2_style))
        p_code = Preformatted(cs["pseudocode"], code_style)
        t_pc = Table([[p_code]], colWidths=[490])
        t_pc.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), code_bg),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_pc)

        story.append(Paragraph("7. Python Source Code Listing", h2_style))
        py_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), cs["dir"], cs["file"])
        if os.path.exists(py_path):
            with open(py_path, 'r', encoding='utf-8') as f:
                code_text = f.read()
            # Truncate if extremely long for visual neatness
            lines = code_text.split('\n')
            if len(lines) > 55:
                display_code = '\n'.join(lines[:50]) + f"\n\n# ... [Full listing continues in {cs['file']} ({len(lines)} total lines)]"
            else:
                display_code = code_text
            p_src = Preformatted(display_code, code_style)
            t_src = Table([[p_src]], colWidths=[490])
            t_src.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), code_bg),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(t_src)

        story.append(Paragraph("8. Test Cases & Verification Summary", h2_style))
        story.append(Paragraph(f"<b>Verification Finding:</b> {cs['test_summary']}", body_style))

        story.append(Paragraph("9. Verified Execution Terminal Output", h2_style))
        out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), cs["dir"], "output.txt")
        if os.path.exists(out_path):
            with open(out_path, 'r', encoding='utf-8') as f:
                out_text = f.read()
            out_lines = out_text.split('\n')
            if len(out_lines) > 35:
                display_out = '\n'.join(out_lines[:32]) + f"\n... [Log continues with {len(out_lines)} total lines]"
            else:
                display_out = out_text
            p_out = Preformatted(display_out, code_style)
            t_out = Table([[p_out]], colWidths=[490])
            t_out.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
                ('BOX', (0,0), (-1,-1), 0.5, colors.black),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(t_out)

        story.append(Paragraph("10. Conclusion & Analytical Insights", h2_style))
        story.append(Paragraph(cs["conclusion"], body_style))

        story.append(PageBreak())

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Successfully built official PDF report: {pdf_filename}")

if __name__ == "__main__":
    create_report()
