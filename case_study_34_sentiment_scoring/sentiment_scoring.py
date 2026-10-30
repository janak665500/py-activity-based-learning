"""
Case Study 34: Student Feedback Sentiment Scoring
Department of Computer Science & Engineering
Dr. RVR NRI Institute of Technology

Description:
Analyses multiple student feedback sentences against supplied positive and negative
keyword lists, counts sentiment indicators, calculates normalized sentiment scores,
and classifies feedback according to predefined thresholds.
Concepts Used: Strings, String Cleaning & Tokenization, Lists, Nested Loops,
               Conditional Statements, Tuples, and Tabular Output Formatting.
"""

def print_banner(title):
    border = "=" * 80
    print(border)
    print(title.center(80))
    print(border)

def clean_and_tokenize(sentence):
    """
    Cleans punctuation and tokenizes sentence into words without external libraries.
    """
    cleaned_chars = []
    punctuation = ".,!?:;\"'()[]{}<>-/*_~"
    for ch in sentence:
        if ch in punctuation:
            cleaned_chars.append(" ")
        else:
            cleaned_chars.append(ch.lower())
    
    cleaned_string = "".join(cleaned_chars)
    tokens = cleaned_string.split()
    return tokens

def count_keyword_matches(tokens, keyword_list):
    """
    Counts matches of words in keyword_list using pure list traversal.
    Returns count and list of matched terms.
    """
    count = 0
    matched = []
    for token in tokens:
        for kw in keyword_list:
            if token == kw:
                count += 1
                matched.append(token)
                break
    return count, matched

def classify_sentiment(pos_count, neg_count):
    total = pos_count + neg_count
    if total == 0:
        return 0, 0.0, "NEUTRAL (No Keywords)"
    
    net_score = pos_count - neg_count
    norm_index = round(net_score / total, 2)
    
    if norm_index >= 0.5 or (pos_count >= 2 and neg_count == 0):
        category = "HIGHLY POSITIVE"
    elif norm_index > 0.0:
        category = "POSITIVE"
    elif norm_index == 0.0:
        category = "MIXED / BALANCED"
    elif norm_index > -0.5:
        category = "NEGATIVE"
    else:
        category = "HIGHLY NEGATIVE"
        
    return net_score, norm_index, category

def run_feedback_sentiment_analysis(feedback_records, pos_keywords, neg_keywords):
    print_banner("STUDENT COURSE EVALUATION SENTIMENT ANALYSIS")
    print(f"Positive Keywords Monitored ({len(pos_keywords)}) : {', '.join(pos_keywords[:6])}...")
    print(f"Negative Keywords Monitored ({len(neg_keywords)}) : {', '.join(neg_keywords[:6])}...\n")
    
    print("DETAILED FEEDBACK SENTIMENT BREAKDOWN:")
    print("-" * 90)
    
    results = []
    category_counts = [
        ["HIGHLY POSITIVE", 0],
        ["POSITIVE", 0],
        ["MIXED / BALANCED", 0],
        ["NEUTRAL (No Keywords)", 0],
        ["NEGATIVE", 0],
        ["HIGHLY NEGATIVE", 0]
    ]
    
    pos_keyword_freq = []
    for kw in pos_keywords:
        pos_keyword_freq.append([kw, 0])
        
    neg_keyword_freq = []
    for kw in neg_keywords:
        neg_keyword_freq.append([kw, 0])
        
    for item in feedback_records:
        fid, author, text = item
        tokens = clean_and_tokenize(text)
        
        pos_cnt, pos_matched = count_keyword_matches(tokens, pos_keywords)
        neg_cnt, neg_matched = count_keyword_matches(tokens, neg_keywords)
        
        # Update keyword frequencies
        for word in pos_matched:
            for entry in pos_keyword_freq:
                if entry[0] == word:
                    entry[1] += 1
                    break
        for word in neg_matched:
            for entry in neg_keyword_freq:
                if entry[0] == word:
                    entry[1] += 1
                    break
                    
        net_score, norm_idx, classification = classify_sentiment(pos_cnt, neg_cnt)
        
        # Update category counts
        for entry in category_counts:
            if entry[0] == classification:
                entry[1] += 1
                break
                
        results.append((fid, author, pos_cnt, neg_cnt, net_score, norm_idx, classification))
        
        print(f"Feedback #{fid} by {author}:")
        print(f"  Comment  : \"{text}\"")
        print(f"  Tokens   : {len(tokens)} words | Positive matches: {pos_cnt} {pos_matched} | Negative: {neg_cnt} {neg_matched}")
        print(f"  Scoring  : Net = {int(net_score):+d} | Normalized Index = {norm_idx:+.2f}")
        print(f"  Outcome  : >>> {classification} <<<")
        print("-" * 90)
        
    print_banner("CONSOLIDATED SENTIMENT AUDIT SUMMARY")
    total_fb = len(feedback_records)
    print("{:<26} {:<15} {:<15}".format("Sentiment Classification", "Feedback Count", "Percentage"))
    print("-" * 60)
    for cat_name, cnt in category_counts:
        pct = (cnt / total_fb) * 100.0 if total_fb > 0 else 0.0
        print("{:<26} {:<15} {:<14.1f}%".format(cat_name, cnt, pct))
    print("-" * 60)
    
    # Calculate Institutional Satisfaction Score (ISS)
    pos_total = 0
    for cat_name, cnt in category_counts:
        if "POSITIVE" in cat_name:
            pos_total += cnt
    approval_rate = (pos_total / total_fb) * 100.0 if total_fb > 0 else 0.0
    print(f"\nNet Course Approval Rating: {approval_rate:.1f}% Positive Sentiment")
    
    print("\nTOP OBSERVED THEMATIC KEYWORDS:")
    # Sort top keywords without external libraries
    for i in range(len(pos_keyword_freq)):
        for j in range(i + 1, len(pos_keyword_freq)):
            if pos_keyword_freq[j][1] > pos_keyword_freq[i][1]:
                temp = pos_keyword_freq[i]
                pos_keyword_freq[i] = pos_keyword_freq[j]
                pos_keyword_freq[j] = temp
                
    for i in range(len(neg_keyword_freq)):
        for j in range(i + 1, len(neg_keyword_freq)):
            if neg_keyword_freq[j][1] > neg_keyword_freq[i][1]:
                temp = neg_keyword_freq[i]
                neg_keyword_freq[i] = neg_keyword_freq[j]
                neg_keyword_freq[j] = temp
                
    print("Most Frequent Positive Themes:", end=" ")
    top_pos = [f"{k} ({c})" for k, c in pos_keyword_freq if c > 0]
    print(", ".join(top_pos) if top_pos else "None")
    
    print("Most Frequent Areas of Concern:", end=" ")
    top_neg = [f"{k} ({c})" for k, c in neg_keyword_freq if c > 0]
    print(", ".join(top_neg) if top_neg else "None")

if __name__ == "__main__":
    positive_words = [
        "excellent", "good", "great", "helpful", "clear",
        "inspiring", "engaging", "interactive", "thorough",
        "effective", "supportive", "awesome", "well"
    ]
    
    negative_words = [
        "poor", "bad", "confusing", "boring", "difficult",
        "unclear", "fast", "slow", "disorganized", "strict",
        "vague", "rushed", "worst"
    ]
    
    sample_feedbacks = [
        ("FB-01", "Shukur", "The Python lectures were excellent, very clear, and extremely engaging!"),
        ("FB-02", "Aarav",  "The explanation was confusing and the pace was too fast and disorganized."),
        ("FB-03", "Bhavya", "Instructor is good and helpful, but some problem statements are difficult."),
        ("FB-04", "Charan", "Today's lab was well structured, interactive, and very supportive."),
        ("FB-05", "Divya",  "The classroom audio was poor and the explanations were unclear and rushed."),
        ("FB-06", "Eshwar", "Submitted the assignment in room 302 on Friday afternoon."),  # Neutral
        ("FB-07", "Farhan", "Great examples and inspiring teaching, thoroughly enjoyed the session!")
    ]
    
    run_feedback_sentiment_analysis(sample_feedbacks, positive_words, negative_words)
