import random
import numpy as np

# Setting fixed random seeds for strict reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

CATEGORIES = ["Personal Loan", "Home Loan", "Auto Loan", "Education Loan", "Business Loan"]
STATUSES = ["Submitted", "Under Review", "Approved", "Rejected", "Disbursed"]

def generate_loan_dataset():
    dataset = []
    # Amounts range from 50k to 5M INR, reflecting realistic retail banking brackets for Cred
    for i in range(1, 45):
        category = random.choice(CATEGORIES)
        status = random.choice(STATUSES)
        amount = random.randint(50000, 5000000)
        days = random.randint(0, 30)
        # Sets a 15% historical probability threshold for tracking fraud reviews
        flagged = random.random() < 0.15 
        
        dataset.append({
            "record_id": f"CRED-LN-{1000 + i}",
            "category": category,
            "status": status,
            "loan_amount_inr": amount,
            "days_since_created": days,
            "flagged_for_fraud_review": flagged
        })
    return dataset

LOAN_APPLICATIONS = generate_loan_dataset()

def check_loan_application_status(record_id: str) -> dict:
    record = next((r for r in LOAN_APPLICATIONS if r["record_id"] == record_id), None)
    if not record:
        return {"error": "Record not found"}
    
    # Task 6: Custom multi-factor mathematical escalation formula
    # Allocates 70% weight to active fraud risks and 30% weight to standard processing backlogs
    fraud_signal = 1.0 if record["flagged_for_fraud_review"] else 0.0
    recency_signal = min(record["days_since_created"] / 30.0, 1.0)
    escalation_score = round((0.7 * fraud_signal) + (0.3 * recency_signal), 2)
    
    return {
        "status": record["status"],
        "loan_amount_inr": record["loan_amount_inr"],
        "escalation_score": escalation_score,
        "recommend_escalation": escalation_score >= 0.50
    }


if __name__ == "__main__":
    print(f"Total Records Generated: {len(LOAN_APPLICATIONS)}")
    fraud_pct = (sum(1 for r in LOAN_APPLICATIONS if r["flagged_for_fraud_review"]) / len(LOAN_APPLICATIONS)) * 100
    print(f"Fraud Percentage: {fraud_pct:.2%}")
