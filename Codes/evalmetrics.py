import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

def extract_lines(cell):
    """Extracts line numbers from the CSV cell."""
    if pd.isna(cell) or cell.lower() == 'none':
        return set()
    return set(cell.split(','))

def calculate_metrics(true_lines, detected_lines):
    """Calculates TP, FP, FN, Precision, Recall, F1 for a single file."""
    true_lines = extract_lines(true_lines)
    detected_lines = extract_lines(detected_lines)
    
    tp = len(true_lines.intersection(detected_lines))
    fp = len(detected_lines - true_lines)
    fn = len(true_lines - detected_lines)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1, tp, fp, fn

# Load your dataset
df = pd.read_csv(r'C:\Users\zahra\OneDrive\Desktop\ChatGPTasSAST-main\ChatGPTasSAST-main\Data sets\Siddiq\merged_output_SIDDIQ_EXP4.csv')

# Prepare a list to store metrics for each file
results = []

for index, row in df.iterrows():
    filename = row['Filename']
    true_lines = row['Mr. Chekideh']
    detected_lines = row['Detected']
    
    precision, recall, f1, tp, fp, fn = calculate_metrics(true_lines, detected_lines)
    results.append({
        'Filename': filename,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'TP': tp,
        'FP': fp,
        'FN': fn
    })

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# Calculate macro-averaged metrics
macro_precision = results_df['Precision'].mean()
macro_recall = results_df['Recall'].mean()
macro_f1 = results_df['F1-Score'].mean()

# Calculate micro-averaged metrics
total_tp = results_df['TP'].sum()
total_fp = results_df['FP'].sum()
total_fn = results_df['FN'].sum()

micro_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
micro_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
micro_f1 = 2 * (micro_precision * micro_recall) / (micro_precision + micro_recall) if (micro_precision + micro_recall) > 0 else 0

# Print the results
print("Macro-Averaged Metrics:")
print(f"Precision: {macro_precision:.2f}, Recall: {macro_recall:.2f}, F1-Score: {macro_f1:.2f}")

print("\nMicro-Averaged Metrics:")
print(f"Precision: {micro_precision:.2f}, Recall: {micro_recall:.2f}, F1-Score: {micro_f1:.2f}")
print(total_fn)
print(total_fp)
print(total_tp)

