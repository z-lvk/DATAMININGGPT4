import pandas as pd

# Example DataFrame containing TP, FP, FN for each dataset
data = {
    'Dataset': ['Siddiq', 'PYT1', 'PYT2'],
    'TP': [7, 2, 1],
    'FP': [128, 15, 20],
    'FN': [422, 30, 57]
}

df = pd.DataFrame(data)

# Calculate total TP, FP, FN
total_tp = df['TP'].sum()
total_fp = df['FP'].sum()
total_fn = df['FN'].sum()

# Calculate overall micro-averaged metrics
precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Print the results
print(f"Overall Micro-Averaged Metrics:")
print(f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1-Score: {f1_score:.4f}")
