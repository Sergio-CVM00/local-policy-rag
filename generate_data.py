import os
import random

DATA_PATH = "./data"

# Ensure directory exists
os.makedirs(DATA_PATH, exist_ok=True)

departments = ["HR", "IT", "Finance", "Legal", "Operations", "Sales"]
topics = ["Remote Work", "Security", "Expense", "Leave", "Conduct", "Assets"]

templates = [
    "Employees in the {dept} department must adhere to strict guidelines regarding {topic}.",
    "The purpose of this policy is to ensure all {topic} procedures align with {dept} standards.",
    "Failure to comply with {topic} regulations may result in disciplinary action from {dept}.",
    "All {topic} requests must be submitted to the {dept} manager by Friday.",
]

def generate_content(i):
    dept = random.choice(departments)
    topic = random.choice(topics)
    intro = random.choice(templates).format(dept=dept, topic=topic)
    
    # Create specific "Easter eggs" for us to find later
    special_rule = ""
    if i == 42:
        intro = "The 'Answer to Life' policy."
        special_rule = "All employees are entitled to a towel on their desk at all times."
    elif i == 100:
        intro = "The 'Centennial' celebration policy."
        special_rule = "Employees get a bonus of 100 cookies on their 100th day."
    elif i == 500:
        intro = "The 'Mars Colonization' initiative."
        special_rule = "Transfers to the Mars office require a 6-month swimming certification."
        
    return f"""# Policy {i}: {dept} {topic} Protocol

## 1. Overview
{intro}

## 2. Guidelines
1. Ensure all documentation is filed within 24 hours.
2. {dept} requires quarterly reviews of this document.
3. {special_rule if special_rule else "Standard operating procedures apply."}

## 3. Contact
For questions, contact {dept.lower()}@company.com.
"""

print(f"Generating 500 files in {DATA_PATH}...")

# Clear existing files first (optional, be careful)
for f in os.listdir(DATA_PATH):
    os.remove(os.path.join(DATA_PATH, f))

# Generate new files
for i in range(1, 501):
    filename = f"policy_{i:03d}_{random.choice(departments)}_{random.choice(topics)}.md"
    with open(os.path.join(DATA_PATH, filename), "w") as f:
        f.write(generate_content(i))

print("Done! 500 markdown files created.")