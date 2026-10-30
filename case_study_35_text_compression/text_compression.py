"""
Case Study 35: Text Compression Using Character Runs (Run-Length Encoding)
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Description:
Encodes input strings by grouping consecutive repeated characters into (char + run_count),
evaluates lossless compressibility, and identifies threshold cases where encoding produces
negative savings or expansions.
Concepts Used: Strings, String Indexing & Slicing, While/For Loops, Conditionals,
               Tuples, Lists, and Verification Algorithms.
"""

def print_banner(title):
    border = "=" * 80
    print(border)
    print(title.center(80))
    print(border)

def encode_character_runs(text):
    """
    Performs Run-Length Encoding on an input string.
    Returns: encoded_string, list_of_runs as [(char, count), ...]
    """
    if len(text) == 0:
        return "", []
    
    encoded_parts = []
    runs = []
    
    n = len(text)
    i = 0
    while i < n:
        curr_char = text[i]
        run_len = 1
        
        while i + 1 < n and text[i + 1] == curr_char:
            run_len += 1
            i += 1
            
        runs.append((curr_char, run_len))
        encoded_parts.append(curr_char + str(run_len))
        i += 1
        
    encoded_text = "".join(encoded_parts)
    return encoded_text, runs

def decode_character_runs(encoded_text):
    """
    Decompresses run-length encoded text to verify lossless integrity.
    """
    if len(encoded_text) == 0:
        return ""
        
    decoded_chars = []
    i = 0
    n = len(encoded_text)
    
    while i < n:
        char = encoded_text[i]
        i += 1
        count_str = ""
        while i < n and encoded_text[i].isdigit():
            count_str += encoded_text[i]
            i += 1
        count = int(count_str) if len(count_str) > 0 else 1
        decoded_chars.append(char * count)
        
    return "".join(decoded_chars)

def evaluate_compression(original_text):
    orig_len = len(original_text)
    encoded, runs = encode_character_runs(original_text)
    comp_len = len(encoded)
    
    # Lossless integrity check
    restored = decode_character_runs(encoded)
    is_lossless = (restored == original_text)
    
    if orig_len == 0:
        savings_pct = 0.0
        recommendation = "EMPTY INPUT"
    else:
        savings_pct = round(((orig_len - comp_len) / orig_len) * 100.0, 2)
        if comp_len < orig_len:
            recommendation = "BENEFICIAL (Compress)"
        elif comp_len == orig_len:
            recommendation = "NEUTRAL (No Gain)"
        else:
            recommendation = "INEFFECTIVE (Reject / Store Raw)"
            
    return encoded, runs, orig_len, comp_len, savings_pct, recommendation, is_lossless

def run_compression_audit_suite(test_cases):
    print_banner("RUN-LENGTH CHARACTER COMPRESSION AUDIT BENCHMARK")
    print(f"Total Test Payloads Ingested: {len(test_cases)}\n")
    
    row_fmt = "{:<4} {:<24} {:<24} {:<8} {:<8} {:<12} {:<22} {:<10}"
    headers = ("#", "Original Sample", "Encoded Output", "Orig Len", "Enc Len", "Savings %", "Recommendation", "Integrity")
    print(row_fmt.format(*headers))
    print("-" * 116)
    
    beneficial_count = 0
    ineffective_count = 0
    
    for idx in range(len(test_cases)):
        sample = test_cases[idx]
        encoded, runs, o_len, c_len, savings, verdict, lossless = evaluate_compression(sample)
        
        if "BENEFICIAL" in verdict:
            beneficial_count += 1
        elif "INEFFECTIVE" in verdict:
            ineffective_count += 1
            
        display_sample = sample if len(sample) <= 22 else sample[:19] + "..."
        display_encoded = encoded if len(encoded) <= 22 else encoded[:19] + "..."
        lossless_str = "PASS [OK]" if lossless else "FAIL"
        savings_str = f"{savings:+6.2f}%"
        
        print(row_fmt.format(
            idx + 1,
            display_sample,
            display_encoded,
            o_len,
            c_len,
            savings_str,
            verdict,
            lossless_str
        ))
        
    print("-" * 116)
    print("\nANALYTICAL SUMMARY & ENGINE HEURISTICS:")
    print(f"Total Sequences Processed   : {len(test_cases)}")
    print(f"Beneficial Compressions     : {beneficial_count}")
    print(f"Ineffective (Expansion) Cases: {ineffective_count}")
    print("Core Finding: Run-Length Encoding demonstrates optimal performance when")
    print("average consecutive character frequency exceeds 2. When text has non-repeating")
    print("characters, run counts cause payload duplication and expansion penalty (approx -100%).")

if __name__ == "__main__":
    sample_payloads = [
        "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWW",      # Highly repetitive
        "AAAAAAAGGGGGTTTTTTTCCCCCCCAAAAA",               # Genomic repeated runs
        "AABBBCCCCDDDDDEEEEEEFFFFFFGGGGGGG",             # Progressive frequency runs
        "ABCDEFGHIJKLMN",                                 # Strictly non-repeating (Worst case)
        "ABABABABABABAB",                                 # Alternating characters (Expansion case)
        "ZZZZZZZZZZZZZZZZZZZZ",                           # Single repeated char
        "Hellooooo Worlddd",                              # Mixed conversational text
        "MISSISSIPPI",                                    # Short multi-runs
        ""                                                # Boundary condition (Empty)
    ]
    
    run_compression_audit_suite(sample_payloads)
