raw_header = """From: support@softnexis.com
To: hemanth31917@gmail.com
Subject: 	You’re In — Confirm Your Soft Nexis Internship (24 hrs to accept)
Date: Mon, 07 May 2026 10:10:00 +0000
Received: 	softnexis.com
Reply-To: support@softnexis.com
Return-Path:support@softnexis.com"""

def parse_headers(raw_text):
    result = {}                          
    for line in raw_text.splitlines():   
        if ":" in line:                  
            key, value = line.split(":", 1)   
            result[key.strip()] = value.strip()  
    return result

def check_spam(headers):

    warnings = []
    spam_score = 0

    
    subject = headers.get("Subject", "")

    if subject.count("!") > 2:
        warnings.append("Too many exclamation marks in subject")
        spam_score += 2

    dangerous_words = ["urgent", "winner", "free", "click", "verify"]

    for word in dangerous_words:
        if word.lower() in subject.lower():
            warnings.append(f"Suspicious keyword found: {word}")
            spam_score += 1
    received = headers.get("Received", "")
    return_path = headers.get("Return-Path", "")

    for bad_domain in [".ru", ".cn", ".xyz"]:
        if bad_domain in received or bad_domain in return_path:
            warnings.append(f"Suspicious domain detected: {bad_domain}")
            spam_score += 3

    
    sender = headers.get("From", "")
    reply_to = headers.get("Reply-To", "")

    if reply_to and reply_to not in sender:
        warnings.append("Reply-To differs from sender")
        spam_score += 4

    return warnings, spam_score

def print_report(headers):
    warnings, spam_score = check_spam(headers)

    
    if len(warnings) == 0:
        verdict = "CLEAN — looks safe"
    elif len(warnings) <= 2:
        verdict = "SUSPICIOUS — be careful"
    else:
        verdict = "DANGER — likely spam or phishing"

    
    print()
    print("=" * 50)
    print("       EMAIL HEADER ANALYSIS REPORT")
    print("=" * 50)
    print(f"  From     : {headers.get('From',    'Not found')}")
    print(f"  To       : {headers.get('To',      'Not found')}")
    print(f"  Subject  : {headers.get('Subject', 'Not found')}")
    print(f"  Date     : {headers.get('Date',    'Not found')}")
    print(f"  Calculated Spam Score : {spam_score}")
    print()
    print(f"  VERDICT  : {verdict}")
    print()

    if warnings:
        print("  WARNING FLAGS:")
        for w in warnings:
            print(f"    ⚠  {w}")
    else:
        print("  No suspicious patterns found.")

    print("=" * 50)
    print()

parsed = parse_headers(raw_header)   
print_report(parsed)                
