"""
Case Study 28: Repeated Transaction Detection & Fraud Audit
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Description:
Processes transaction records stored in lists of tuples, detects duplicate transactions,
identifies threshold violations, and generates a structured audit log of suspicious entries.
Concepts Used: Lists, Tuples, Tuple Unpacking, Nested Loops, Conditional Statements,
               Arithmetic Computations, and Formatted Outputs.
"""

def print_banner(title):
    border = "=" * 85
    print(border)
    print(title.center(85))
    print(border)

def detect_suspicious_transactions(transactions, max_single_limit=50000.0, max_sender_limit=100000.0):
    """
    Scans transaction lists using pure list/tuple operations without sets or dicts.
    Identifies:
    1. Duplicate Transaction IDs.
    2. Duplicate Transfers (Identical Sender, Receiver, and Amount - Potential Replay).
    3. Single Transaction Threshold Violations (> max_single_limit).
    4. Cumulative Velocity Violations (Sender total exceeding max_sender_limit).
    """
    n = len(transactions)
    suspicious_records = []  # List of tuples: (tx_id, sender, receiver, amount, reason, risk_level)
    
    # 1. Check for Duplicate IDs & Duplicate Transfers via pairwise comparisons
    for i in range(n):
        id_i, sender_i, rec_i, amt_i, time_i = transactions[i]
        
        # Check single threshold violation
        if amt_i > max_single_limit:
            suspicious_records.append((id_i, sender_i, rec_i, amt_i, f"Exceeds Single Txn Limit (INR {max_single_limit:,.2f})", "HIGH"))
            
        # Pairwise check for duplicate IDs or duplicate content
        for j in range(i + 1, n):
            id_j, sender_j, rec_j, amt_j, time_j = transactions[j]
            
            # Duplicate transaction ID
            if id_i == id_j:
                suspicious_records.append((id_j, sender_j, rec_j, amt_j, f"Duplicate Txn ID collision with index #{i+1}", "CRITICAL"))
                
            # Duplicate transfer (same sender, receiver, and amount)
            elif sender_i == sender_j and rec_i == rec_j and amt_i == amt_j:
                reason = f"Duplicate Transfer: Replay match with {id_i} (Amt: INR {amt_i:,.2f})"
                suspicious_records.append((id_j, sender_j, rec_j, amt_j, reason, "HIGH"))

    # 2. Check Cumulative Volume per sender using nested lists (no dicts)
    # List of unique senders: [ [sender_name, total_volume, count], ... ]
    sender_summaries = []
    for tx in transactions:
        tx_id, sender, receiver, amt, time_str = tx
        
        # Find if sender exists in sender_summaries
        found = False
        for entry in sender_summaries:
            if entry[0] == sender:
                entry[1] += amt
                entry[2] += 1
                found = True
                break
        if not found:
            sender_summaries.append([sender, amt, 1])
            
    # Flag senders who exceeded cumulative limit or made high frequency txns
    for entry in sender_summaries:
        sender_name, total_vol, count = entry
        if total_vol > max_sender_limit:
            # Flag all txns from this sender that contributed to breach
            for tx in transactions:
                tx_id, sender, receiver, amt, time_str = tx
                if sender == sender_name and amt > 25000:
                    suspicious_records.append((
                        tx_id, sender, receiver, amt,
                        f"Cumulative Sender Limit Exceeded (Total: INR {total_vol:,.2f})",
                        "MEDIUM"
                    ))
                    
    return suspicious_records, sender_summaries

def generate_audit_report(transactions, max_single=50000.0, max_cumulative=100000.0):
    print_banner("FINANCIAL TRANSACTION INTEGRITY & DUPLICATE AUDIT REPORT")
    print(f"Total Transactions Ingested    : {len(transactions)}")
    print(f"Single Transaction Threshold   : INR {max_single:,.2f}")
    print(f"Cumulative Sender Limit        : INR {max_cumulative:,.2f}\n")
    
    print("INGESTED TRANSACTION LEDGER:")
    row_fmt = "{:<5} {:<10} {:<14} {:<14} {:>14} {:<15}"
    print(row_fmt.format("#", "Txn ID", "Sender", "Receiver", "Amount (INR)", "Timestamp"))
    print("-" * 80)
    for idx in range(len(transactions)):
        tx = transactions[idx]
        print(row_fmt.format(idx + 1, tx[0], tx[1], tx[2], f"{tx[3]:,.2f}", tx[4]))
    print("-" * 80)
    
    suspicious, senders = detect_suspicious_transactions(transactions, max_single, max_cumulative)
    
    print("\nSUSPICIOUS ENTRIES & THRESHOLD VIOLATIONS DETECTED:")
    if len(suspicious) == 0:
        print("[OK] No anomalies or duplicate transactions detected. Ledger verified clean.")
    else:
        s_fmt = "{:<10} {:<12} {:<12} {:>14} {:<10} {:<40}"
        print(s_fmt.format("Txn ID", "Sender", "Receiver", "Amount (INR)", "Risk", "Violation Description"))
        print("-" * 105)
        total_flagged_amt = 0.0
        for s in suspicious:
            tx_id, snd, rec, amt, reason, risk = s
            total_flagged_amt += amt
            print(s_fmt.format(tx_id, snd, rec, f"{amt:,.2f}", risk, reason))
        print("-" * 105)
        print(f"Total Flagged Anomaly Count : {len(suspicious)}")
        print(f"Total Value Under Review    : INR {total_flagged_amt:,.2f}")
        
    print("\nSENDER CUMULATIVE EXPOSURE SUMMARY:")
    c_fmt = "{:<18} {:<15} {:>18} {:<15}"
    print(c_fmt.format("Sender Account", "Txn Count", "Total Outflow (INR)", "Velocity Status"))
    print("-" * 72)
    for s_entry in senders:
        s_name, s_tot, s_cnt = s_entry
        status = "BREACH (>100k)" if s_tot > max_cumulative else "NORMAL"
        print(c_fmt.format(s_name, s_cnt, f"{s_tot:,.2f}", status))
    print("-" * 72)

if __name__ == "__main__":
    # Test batch of transactions: (ID, Sender, Receiver, Amount, Timestamp)
    sample_transactions = [
        ("TX1001", "ACC_SHUKUR", "ACC_RAVI",    15000.0, "2026-10-30 09:15"),
        ("TX1002", "ACC_PRIYA",  "ACC_ANANYA",   8500.0, "2026-10-30 09:30"),
        ("TX1003", "ACC_KIRAN",  "ACC_VISHAL",  65000.0, "2026-10-30 09:45"),  # Single limit violation (>50k)
        ("TX1004", "ACC_PRIYA",  "ACC_ANANYA",   8500.0, "2026-10-30 10:00"),  # Duplicate transfer (same as TX1002)
        ("TX1005", "ACC_AMAR",   "ACC_SUNIL",   45000.0, "2026-10-30 10:15"),
        ("TX1005", "ACC_AMAR",   "ACC_SUNIL",   45000.0, "2026-10-30 10:16"),  # Duplicate Txn ID & duplicate transfer!
        ("TX1007", "ACC_AMAR",   "ACC_DEEPAK",  35000.0, "2026-10-30 10:45"),  # AMAR cumulative total reaches 125,000 (>100k)
        ("TX1008", "ACC_SHUKUR", "ACC_ROHAN",    5000.0, "2026-10-30 11:00"),
    ]
    
    generate_audit_report(sample_transactions)

