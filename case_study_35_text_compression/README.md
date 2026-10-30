# Case Study 35: Text Compression Using Character Runs

**Course**: Python Programming (Activity-Based Learning - ABL)  
**Institution**: Dr. RVR NRI Institute of Technology  
**Student Name**: Shukur  
**Roll Number**: 24NR1A0501  
**Branch**: Computer Science & Engineering (CSE)  
**Section**: CSE-A  

---

## 1. Problem Statement
Data transmission and storage systems rely on compression algorithms to minimize bandwidth consumption and disk footprint. Run-Length Encoding (RLE) is an elementary form of lossless data compression that replaces consecutive identical data elements (character runs) with a single character followed by the run count. However, RLE is not universally optimal; when applied to high-entropy or non-repeating strings, appending run counts inflates the payload size (causing severe expansion). A robust computational audit system is needed to encode strings by grouping consecutive repeated characters, compare original and compressed lengths, calculate percentage savings or expansion penalties, verify 100% lossless decompression integrity, and formally reject compression when it is not beneficial.

---

## 2. Objectives
1. Implement a character-by-character run scanning loop to perform lossless Run-Length Encoding without external compression libraries.
2. Build an inverse decompression decoder to mathematically verify lossless round-trip restoration ($D(E(S)) \equiv S$).
3. Formulate comparative metrics: Original Length, Encoded Length, and Space Savings Percentage.
4. Establish decision heuristics to classify cases into **BENEFICIAL** (Savings $> 0$), **NEUTRAL** (Savings $= 0$), and **INEFFECTIVE / EXPANSION** (Savings $< 0$).
5. Demonstrate boundary testing across highly repetitive sequences, genomic DNA strings, non-repeating alphabets, and empty strings.

---

## 3. Assumptions
1. Input sequences consist of printable ASCII characters.
2. Runs are defined strictly by identical consecutive characters ($C_i = C_{i+1}$).
3. When compression yields an encoded length greater than or equal to the original length, the system recommends rejecting compression and preserving raw uncompressed text.
4. The algorithm strictly uses loops, string slicing, concatenation, and tuples within syllabus bounds.

---

## 4. Step-by-Step Algorithm

```
Step 1: Ingest input string text.
Step 2: If length of text is 0, return empty string and flag as "EMPTY INPUT".
Step 3: Encoding Phase (Run-Length Compression):
    - Initialize index i = 0, encoded_parts = [], runs = [].
    - While i < length(text):
        Set curr_char = text[i], run_len = 1.
        While (i + 1 < length(text)) AND (text[i + 1] == curr_char):
            run_len = run_len + 1
            i = i + 1
        Append (curr_char, run_len) to runs.
        Append curr_char + str(run_len) to encoded_parts.
        i = i + 1
    - Join encoded_parts into encoded_text.
Step 4: Decoding Phase (Lossless Verification):
    - Parse encoded_text: extract character and following integer run count.
    - Reconstruct decompressed_text = sum(character * count).
    - Verify: is_lossless = (decompressed_text == text).
Step 5: Comparative Evaluation:
    - orig_len = len(text), comp_len = len(encoded_text).
    - savings_pct = ((orig_len - comp_len) / orig_len) * 100.
    - If comp_len < orig_len: Verdict = "BENEFICIAL (Compress)".
    - Else if comp_len == orig_len: Verdict = "NEUTRAL (No Gain)".
    - Else: Verdict = "INEFFECTIVE (Reject / Store Raw)".
Step 6: Output comparative benchmarking ledger and compression heuristics report.
```

---

## 5. Flowchart

```mermaid
flowchart TD
    Start([Start Run-Length Compression]) --> Ingest[Ingest Raw Text String]
    Ingest --> CheckEmpty{Length == 0?}
    CheckEmpty -- Yes --> ReturnEmpty[Return Empty Payload & Log Empty Status]
    
    CheckEmpty -- No --> InitPointers[Set i = 0, run_len = 1]
    InitPointers --> ScanLoop{i + 1 < Length AND text[i+1] == text[i]?}
    
    ScanLoop -- Yes --> IncRun[run_len = run_len + 1\ni = i + 1]
    IncRun --> ScanLoop
    
    ScanLoop -- No --> EmitRun[Append char + str run_len to Encoded\ni = i + 1]
    EmitRun --> MoreChars{i < Length?}
    MoreChars -- Yes --> ScanLoop
    
    MoreChars -- No --> Decompress[Decompress Encoded Payload\nVerify Lossless Integrity]
    Decompress --> CalcSavings[Compute Savings % = Orig - Comp / Orig * 100]
    CalcSavings --> Decision{Comp Len < Orig Len?}
    
    Decision -- Yes --> RecBeneficial[Verdict: BENEFICIAL (Compress)]
    Decision -- No --> RecReject[Verdict: INEFFECTIVE (Reject / Store Raw)]
    
    RecBeneficial --> PrintRow[Format & Print Audit Matrix Row]
    RecReject --> PrintRow
    PrintRow --> End([End Program])
```

---

## 6. Pseudocode

```text
ALGORITHM TextCompressionCharacterRuns:
    INPUT: String text
    OUTPUT: Encoded string, Savings %, Decision verdict, Lossless verification

    IF LENGTH(text) == 0 THEN:
        RETURN "", 0, 0, 0.0, "EMPTY INPUT", TRUE
    END IF

    encoded_list = []
    i = 0
    n = LENGTH(text)

    WHILE i < n DO:
        ch = text[i]
        run_count = 1
        WHILE (i + 1 < n) AND (text[i + 1] == ch) DO:
            run_count = run_count + 1
            i = i + 1
        END WHILE
        APPEND (ch + STRING(run_count)) TO encoded_list
        i = i + 1
    END WHILE

    encoded_str = CONCATENATE(encoded_list)
    orig_len = LENGTH(text)
    comp_len = LENGTH(encoded_str)

    // Lossless round-trip check
    restored_str = DECODE(encoded_str)
    is_lossless = (restored_str == text)

    savings_pct = ((orig_len - comp_len) / orig_len) * 100.0
    IF comp_len < orig_len THEN:
        verdict = "BENEFICIAL (Compress)"
    ELSE:
        verdict = "INEFFECTIVE (Reject / Store Raw)"
    END IF

    RETURN encoded_str, orig_len, comp_len, savings_pct, verdict, is_lossless
END ALGORITHM
```

---

## 7. Python Source Code Listing
The complete implementation is available in [`text_compression.py`](file:///e:/shukur%20python%20activity%20based%20learning/case_study_35_text_compression/text_compression.py).

---

## 8. Test Cases & Verification

| Payload Description | Original Sample | Encoded Output | Orig $\rightarrow$ Enc Len | Savings % | Recommendation | Verification |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Highly Repetitive** | `WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWW` | `W12B1W12B3W12` | $40 \rightarrow 13$ | +67.50% | BENEFICIAL (Compress) | **PASS** |
| **Genomic DNA Runs** | `AAAAAAAGGGGGTTTTTTTCCCCCCCAAAAA` | `A7G5T7C7A5` | $31 \rightarrow 10$ | +67.74% | BENEFICIAL (Compress) | **PASS** |
| **Progressive Runs** | `AABBBCCCCDDDDDEEEEEEFFFFFFGGGGGGG` | `A2B3C4D5E6F6G7` | $33 \rightarrow 14$ | +57.58% | BENEFICIAL (Compress) | **PASS** |
| **Strictly Non-Repeating** | `ABCDEFGHIJKLMN` | `A1B1C1D1...` | $14 \rightarrow 28$ | -100.00% | INEFFECTIVE (Reject) | **PASS** |
| **Alternating Sequence** | `ABABABABABABAB` | `A1B1A1B1...` | $14 \rightarrow 28$ | -100.00% | INEFFECTIVE (Reject) | **PASS** |
| **Single Character** | `ZZZZZZZZZZZZZZZZZZZZ` | `Z20` | $20 \rightarrow 3$ | +85.00% | BENEFICIAL (Compress) | **PASS** |
| **Natural Conversational**| `Hellooooo Worlddd` | `H1e1l2o5 1W1o1r1l1d3` | $17 \rightarrow 20$ | -17.65% | INEFFECTIVE (Reject) | **PASS** |
| **Empty String** | `""` | `""` | $0 \rightarrow 0$ | 0.00% | EMPTY INPUT | **PASS** |

---

## 9. Program Execution Output
```text
================================================================================
                RUN-LENGTH CHARACTER COMPRESSION AUDIT BENCHMARK                
================================================================================
Total Test Payloads Ingested: 9

#    Original Sample          Encoded Output           Orig Len Enc Len  Savings %    Recommendation         Integrity 
--------------------------------------------------------------------------------------------------------------------
1    WWWWWWWWWWWWBWWWWWW...   W12B1W12B3W12            40       13       +67.50%      BENEFICIAL (Compress)  PASS [OK] 
2    AAAAAAAGGGGGTTTTTTT...   A7G5T7C7A5               31       10       +67.74%      BENEFICIAL (Compress)  PASS [OK] 
3    AABBBCCCCDDDDDEEEEE...   A2B3C4D5E6F6G7           33       14       +57.58%      BENEFICIAL (Compress)  PASS [OK] 
4    ABCDEFGHIJKLMN           A1B1C1D1E1F1G1H1I1J...   14       28       -100.00%     INEFFECTIVE (Reject / Store Raw) PASS [OK] 
5    ABABABABABABAB           A1B1A1B1A1B1A1B1A1B...   14       28       -100.00%     INEFFECTIVE (Reject / Store Raw) PASS [OK] 
6    ZZZZZZZZZZZZZZZZZZZZ     Z20                      20       3        +85.00%      BENEFICIAL (Compress)  PASS [OK] 
7    Hellooooo Worlddd        H1e1l2o5 1W1o1r1l1d3     17       20       -17.65%      INEFFECTIVE (Reject / Store Raw) PASS [OK] 
8    MISSISSIPPI              M1I1S2I1S2I1P2I1         11       16       -45.45%      INEFFECTIVE (Reject / Store Raw) PASS [OK] 
9                                                      0        0         +0.00%      EMPTY INPUT            PASS [OK] 
--------------------------------------------------------------------------------------------------------------------

ANALYTICAL SUMMARY & ENGINE HEURISTICS:
Total Sequences Processed   : 9
Beneficial Compressions     : 4
Ineffective (Expansion) Cases: 4
Core Finding: Run-Length Encoding demonstrates optimal performance when
average consecutive character frequency exceeds 2. When text has non-repeating
characters, run counts cause payload duplication and expansion penalty (approx -100%).
```

---

## 10. Conclusion & Key Learnings
1. **Mathematical Heuristic**: Run-Length Encoding is only beneficial when the average run length exceeds 2. For strings with run length 1 (unique characters), encoding adds an integer digit for every character, causing a catastrophic 100% expansion.
2. **Lossless Verification**: Integrating a decompressor directly into the test suite guarantees that no data corruption occurs during compression.
3. **Engine Robustness**: Handling edge cases (empty strings, single repeated letters, natural language text) ensures real-world production reliability.
