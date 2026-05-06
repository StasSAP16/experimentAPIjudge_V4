import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

# ============================================================
# HARDCODED EXPERIMENT DATA (from uploaded files)
# ============================================================

# --- Ground Truth ---
ground_truth = [
    {
        "activity_name": "Record the data of each patient",
        "substeps": [
            {"step_number": 1, "description": "Greet the patient and explain the registration process"},
            {"step_number": 2, "description": "Prepare the registration form or system"},
            {"step_number": 3, "description": "Begin collecting patient information"}
        ]
    },
    {
        "activity_name": "Register the SSN of the patient",
        "substeps": [
            {"step_number": 1, "description": "Ask the patient for their Social Security Number (SSN)"},
            {"step_number": 2, "description": "Verify the SSN format for accuracy"},
            {"step_number": 3, "description": "Input the SSN into the registration system"}
        ]
    },
    {
        "activity_name": "Register the Name of the patient",
        "substeps": [
            {"step_number": 1, "description": "Ask the patient for their first name"},
            {"step_number": 2, "description": "Confirm the spelling of the name with the patient"},
            {"step_number": 3, "description": "Enter the name into the registration system"}
        ]
    },
    {
        "activity_name": "Register the Surname of the patient",
        "substeps": [
            {"step_number": 1, "description": "Ask the patient for their surname (last name)"},
            {"step_number": 2, "description": "Confirm the spelling of the surname with the patient"},
            {"step_number": 3, "description": "Enter the surname into the registration system"}
        ]
    },
    {
        "activity_name": "Print referral document",
        "substeps": [
            {"step_number": 1, "description": "Generate the referral document using the registered information"},
            {"step_number": 2, "description": "Review the document for accuracy and completeness"},
            {"step_number": 3, "description": "Print the referral document"}
        ]
    },
    {
        "activity_name": "Archive the record in file system",
        "substeps": [
            {"step_number": 1, "description": "Prepare the patient's record for archiving"},
            {"step_number": 2, "description": "Store the physical record in the appropriate file system"},
            {"step_number": 3, "description": "Update the database with the record's storage location"}
        ]
    }
]

# --- DeepSeek Predictions ---
pred_deepseek = [
    {
        "activity_id": "A1",
        "activity_name": "Record the data of each patient",
        "substeps": [
            {"step_number": 1, "description": "Open the Hospital Information System (HIS) and navigate to the patient registration module."},
            {"step_number": 2, "description": "Select the option to create a new patient record."},
            {"step_number": 3, "description": "Enter the patient's basic demographic information into the required fields."},
            {"step_number": 4, "description": "Review the entered data for accuracy and save the record."}
        ]
    },
    {
        "activity_id": "A2",
        "activity_name": "Register the SSN of the patient",
        "substeps": [
            {"step_number": 1, "description": "Ask the patient for their Social Security Number (SSN) and request their official ID for verification."},
            {"step_number": 2, "description": "Enter the SSN into the designated field in the HIS."},
            {"step_number": 3, "description": "Verify the entered SSN matches the official ID and confirm no errors."},
            {"step_number": 4, "description": "Save the SSN entry in the patient record."}
        ]
    },
    {
        "activity_id": "A3",
        "activity_name": "Register the Name of the patient",
        "substeps": [
            {"step_number": 1, "description": "Request the patient's official identification document (e.g., driver's license or passport)."},
            {"step_number": 2, "description": "Locate the patient's legal first and middle name(s) on the ID."},
            {"step_number": 3, "description": "Type the first and middle name(s) exactly as shown into the corresponding fields in the HIS."},
            {"step_number": 4, "description": "Double-check the spelling against the ID and save the entry."}
        ]
    },
    {
        "activity_id": "A4",
        "activity_name": "Register the Surname of the patient",
        "substeps": [
            {"step_number": 1, "description": "Refer to the patient's official identification document for the surname."},
            {"step_number": 2, "description": "Enter the surname into the surname field in the HIS."},
            {"step_number": 3, "description": "Verify the surname matches the ID exactly and save the record."}
        ]
    },
    {
        "activity_id": "A5",
        "activity_name": "Print referral document",
        "substeps": [
            {"step_number": 1, "description": "Navigate to the referral document generation screen in the HIS."},
            {"step_number": 2, "description": "Select the patient's record and confirm the registration details."},
            {"step_number": 3, "description": "Click the print button to send the document to the printer."},
            {"step_number": 4, "description": "Retrieve the printed referral document from the printer and hand it to the patient."}
        ]
    },
    {
        "activity_id": "A6",
        "activity_name": "Archive the record in file system",
        "substeps": [
            {"step_number": 1, "description": "Ensure the patient record is complete and saved in the HIS."},
            {"step_number": 2, "description": "Scan any paper documents (e.g., signed forms) using the document scanner."},
            {"step_number": 3, "description": "Attach the scanned documents to the patient's electronic record in the HIS."},
            {"step_number": 4, "description": "Confirm the record is archived and accessible for future retrieval."}
        ]
    }
]

# --- Google/Gemini Predictions ---
pred_google = [
    {
        "activity_id": "A1",
        "activity_name": "Record the data of each patient",
        "substeps": [
            {"step_number": 1, "description": "Greet patient and request identification."},
            {"step_number": 2, "description": "Open HIS and navigate to new patient registration."},
            {"step_number": 3, "description": "Enter patient's basic demographic information into HIS."},
            {"step_number": 4, "description": "Confirm data entry with patient."}
        ]
    },
    {
        "activity_id": "A2",
        "activity_name": "Register the SSN of the patient",
        "substeps": [
            {"step_number": 1, "description": "Request patient's Social Security Number."},
            {"step_number": 2, "description": "Enter SSN into the designated field in HIS."},
            {"step_number": 3, "description": "Verify SSN for accuracy with patient."}
        ]
    },
    {
        "activity_id": "A3",
        "activity_name": "Register the Name of the patient",
        "substeps": [
            {"step_number": 1, "description": "Request patient's official identification."},
            {"step_number": 2, "description": "Read legal first and middle name(s) from ID."},
            {"step_number": 3, "description": "Enter first and middle name(s) into HIS."},
            {"step_number": 4, "description": "Return identification to patient."}
        ]
    },
    {
        "activity_id": "A4",
        "activity_name": "Register the Surname of the patient",
        "substeps": [
            {"step_number": 1, "description": "Request patient's official identification."},
            {"step_number": 2, "description": "Read family name from ID."},
            {"step_number": 3, "description": "Enter family name into HIS."},
            {"step_number": 4, "description": "Return identification to patient."}
        ]
    },
    {
        "activity_id": "A5",
        "activity_name": "Print referral document",
        "substeps": [
            {"step_number": 1, "description": "Navigate to the referral document generation module in HIS."},
            {"step_number": 2, "description": "Generate the official registration confirmation."},
            {"step_number": 3, "description": "Print the registration confirmation document."},
            {"step_number": 4, "description": "Hand printed document to patient."}
        ]
    },
    {
        "activity_id": "A6",
        "activity_name": "Archive the record in file system",
        "substeps": [
            {"step_number": 1, "description": "Scan all physical registration documents using the document scanner."},
            {"step_number": 2, "description": "Upload scanned documents to the digital file system."},
            {"step_number": 3, "description": "File physical documents in the designated secure location."},
            {"step_number": 4, "description": "Confirm digital record is accessible in the file system."}
        ]
    }
]

# --- Metrics DeepSeek ---
metrics_ds = {
    "model": "DeepSeek",
    "totalGtSteps": 18,
    "totalPredSteps": 23,
    "coverage": 77.78,
    "metrics": {
        "Identical Match": {"count": 0, "percentage": 0},
        "Functional Equivalence": {"count": 10, "percentage": 55.56},
        "Granularity Difference": {"count": 6, "percentage": 33.33},
        "No Match": {"count": 4, "percentage": 22.22},
        "Extra (Unmatched Response)": {"count": 0, "percentage": 0}
    }
}

# --- Metrics Google/Gemini ---
metrics_gg = {
    "model": "Google",
    "totalGtSteps": 18,
    "totalPredSteps": 23,
    "coverage": 55.56,
    "metrics": {
        "Identical Match": {"count": 2, "percentage": 9.09},
        "Functional Equivalence": {"count": 11, "percentage": 50.00},
        "Granularity Difference": {"count": 3, "percentage": 13.64},
        "No Match": {"count": 8, "percentage": 36.36},
        "Extra (Unmatched Response)": {"count": 4, "percentage": 18.18}
    }
}

# --- Tokenizer Report ---
tokenizer_report = {
    "prompt_length_chars": 4644,
    "deepseek": {"total_tokens": 1120},
    "gemini": {"total_tokens": 1109},
    "fragmentation_analysis": {
        "MUST EXACTLY MATCH": {
            "deepseek": {"tokens": 65, "TFI": 21.666666666666668},
            "gemini": {"tokens": 166, "TFI": 55.333333333333336}
        },
        "decomposition_result": {
            "deepseek": {"tokens": 80, "TFI": 80},
            "gemini": {"tokens": 73, "TFI": 73}
        },
        "Do NOT describe": {
            "deepseek": {"tokens": 50, "TFI": 16.666666666666668},
            "gemini": {"tokens": 184, "TFI": 61.333333333333336}
        },
        "observable staff actions": {
            "deepseek": {"tokens": 62, "TFI": 20.666666666666668},
            "gemini": {"tokens": 180, "TFI": 60}
        },
        "HIS": {
            "deepseek": {"tokens": 30, "TFI": 30},
            "gemini": {"tokens": 15, "TFI": 15}
        },
        "scanner": {
            "deepseek": {"tokens": 53, "TFI": 53},
            "gemini": {"tokens": 46, "TFI": 46}
        },
        "printer": {
            "deepseek": {"tokens": 34, "TFI": 34},
            "gemini": {"tokens": 15, "TFI": 15}
        },
        "filing cabinet": {
            "deepseek": {"tokens": 50, "TFI": 25},
            "gemini": {"tokens": 152, "TFI": 76}
        }
    },
    "json_syntax_ratio": {"deepseek": 0.14107142857142857, "gemini": 0.14517583408476104}
}

# --- Correlation Data ---
correlation = {
    "average_tfi": {"deepseek": 35.125, "gemini": 50.208333333333336},
    "delta_analysis": {
        "delta_tfi": 15.083,
        "delta_no_match": 14.14,
        "delta_granularity": -19.69,
        "delta_functional": -5.56
    }
}

# ============================================================
# VISUALIZATION CODE
# ============================================================

colors_ds = '#2E86AB'
colors_gg = '#E94F37'
colors_gt = '#10B981'

fig = plt.figure(figsize=(24, 30))

# ============================================
# 1. METRICS COMPARISON
# ============================================
ax1 = fig.add_subplot(4, 2, 1)
categories = ['Identical\nMatch', 'Functional\nEquivalence', 'Granularity\nDifference', 'No Match', 'Extra\n(Unmatched)']
ds_values = [
    metrics_ds['metrics']['Identical Match']['percentage'],
    metrics_ds['metrics']['Functional Equivalence']['percentage'],
    metrics_ds['metrics']['Granularity Difference']['percentage'],
    metrics_ds['metrics']['No Match']['percentage'],
    metrics_ds['metrics']['Extra (Unmatched Response)']['percentage']
]
gg_values = [
    metrics_gg['metrics']['Identical Match']['percentage'],
    metrics_gg['metrics']['Functional Equivalence']['percentage'],
    metrics_gg['metrics']['Granularity Difference']['percentage'],
    metrics_gg['metrics']['No Match']['percentage'],
    metrics_gg['metrics']['Extra (Unmatched Response)']['percentage']
]
x = np.arange(len(categories))
width = 0.35
bars1 = ax1.bar(x - width/2, ds_values, width, label='DeepSeek', color=colors_ds, edgecolor='white', linewidth=1.5)
bars2 = ax1.bar(x + width/2, gg_values, width, label='Gemini-2.5-flash', color=colors_gg, edgecolor='white', linewidth=1.5)
ax1.set_ylabel('Percentage (%)', fontsize=12)
ax1.set_title('A. Validation Metrics Comparison', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontsize=10)
ax1.legend(fontsize=11)
ax1.set_ylim(0, 65)
ax1.grid(axis='y', alpha=0.3)
for bar in bars1:
    height = bar.get_height()
    ax1.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width()/2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, color=colors_ds)
for bar in bars2:
    height = bar.get_height()
    ax1.annotate(f'{height:.1f}%', xy=(bar.get_x() + bar.get_width()/2, height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, color=colors_gg)

# ============================================
# 2. COVERAGE & STEPS
# ============================================
ax2 = fig.add_subplot(4, 2, 2)
metrics_names = ['Coverage (%)', 'Total Steps\nGenerated', 'Steps per\nActivity (avg)']
ds_vals = [metrics_ds['coverage'], metrics_ds['totalPredSteps'], metrics_ds['totalPredSteps']/6]
gg_vals = [metrics_gg['coverage'], metrics_gg['totalPredSteps'], metrics_gg['totalPredSteps']/6]
x2 = np.arange(len(metrics_names))
ax2_left = ax2
ax2_right = ax2.twinx()
bars_ds_cov = ax2_left.bar(x2[0] - 0.175, ds_vals[0], 0.35, color=colors_ds, edgecolor='white', linewidth=1.5)
bars_gg_cov = ax2_left.bar(x2[0] + 0.175, gg_vals[0], 0.35, color=colors_gg, edgecolor='white', linewidth=1.5)
bars_ds_steps = ax2_right.bar(x2[1] - 0.175, ds_vals[1], 0.35, color=colors_ds, alpha=0.7, edgecolor='white', linewidth=1.5)
bars_gg_steps = ax2_right.bar(x2[1] + 0.175, gg_vals[1], 0.35, color=colors_gg, alpha=0.7, edgecolor='white', linewidth=1.5)
bars_ds_avg = ax2_right.bar(x2[2] - 0.175, ds_vals[2], 0.35, color=colors_ds, alpha=0.5, edgecolor='white', linewidth=1.5, hatch='//')
bars_gg_avg = ax2_right.bar(x2[2] + 0.175, gg_vals[2], 0.35, color=colors_gg, alpha=0.5, edgecolor='white', linewidth=1.5, hatch='//')
ax2_left.set_ylabel('Coverage (%)', fontsize=12, color='#333')
ax2_right.set_ylabel('Step Count', fontsize=12, color='#666')
ax2_left.set_title('B. Coverage & Step Generation', fontsize=14, fontweight='bold', pad=15)
ax2_left.set_xticks(x2)
ax2_left.set_xticklabels(metrics_names, fontsize=10)
ax2_left.set_ylim(0, 100)
ax2_right.set_ylim(0, 30)
ax2_left.legend(handles=[mpatches.Patch(facecolor=colors_ds, label='DeepSeek'), mpatches.Patch(facecolor=colors_gg, label='Gemini')], loc='upper right', fontsize=11)
for bar, val in zip([bars_ds_cov, bars_gg_cov], [ds_vals[0], gg_vals[0]]):
    ax2_left.annotate(f'{val:.1f}%', xy=(bar[0].get_x() + bar[0].get_width()/2, val), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10)
for bar, val in zip([bars_ds_steps, bars_gg_steps], [ds_vals[1], gg_vals[1]]):
    ax2_right.annotate(f'{val}', xy=(bar[0].get_x() + bar[0].get_width()/2, val), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10)
for bar, val in zip([bars_ds_avg, bars_gg_avg], [ds_vals[2], gg_vals[2]]):
    ax2_right.annotate(f'{val:.1f}', xy=(bar[0].get_x() + bar[0].get_width()/2, val), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=10)

# ============================================
# 3. TFI BY PHRASE
# ============================================
ax3 = fig.add_subplot(4, 2, 3)
phrases = list(tokenizer_report['fragmentation_analysis'].keys())
ds_tfi = [tokenizer_report['fragmentation_analysis'][p]['deepseek']['TFI'] for p in phrases]
gg_tfi = [tokenizer_report['fragmentation_analysis'][p]['gemini']['TFI'] for p in phrases]
phrase_labels = [p.replace('MUST EXACTLY MATCH', 'MUST EXACTLY\nMATCH').replace('observable staff actions', 'observable\nstaff actions').replace('decomposition_result', 'decomp.\nresult').replace('filing cabinet', 'filing\ncabinet').replace('Do NOT describe', 'Do NOT\ndescribe') for p in phrases]
x3 = np.arange(len(phrases))
bars_ds3 = ax3.bar(x3 - 0.35/2, ds_tfi, 0.35, label='DeepSeek', color=colors_ds, edgecolor='white', linewidth=1.5)
bars_gg3 = ax3.bar(x3 + 0.35/2, gg_tfi, 0.35, label='Gemini-2.5-flash', color=colors_gg, edgecolor='white', linewidth=1.5)
ax3.set_ylabel('TFI (Tokens / Word)', fontsize=12)
ax3.set_title('C. Token Fragmentation Index (TFI) by Constraint Phrase', fontsize=14, fontweight='bold', pad=15)
ax3.set_xticks(x3)
ax3.set_xticklabels(phrase_labels, fontsize=9)
ax3.legend(fontsize=11)
ax3.grid(axis='y', alpha=0.3)
ax3.axhline(y=sum(ds_tfi)/len(ds_tfi), color=colors_ds, linestyle='--', alpha=0.5)
ax3.axhline(y=sum(gg_tfi)/len(gg_tfi), color=colors_gg, linestyle='--', alpha=0.5)
ax3.text(len(phrases)-0.3, sum(ds_tfi)/len(ds_tfi)+1.5, f'Avg DS: {sum(ds_tfi)/len(ds_tfi):.1f}', fontsize=9, color=colors_ds, ha='right')
ax3.text(len(phrases)-0.3, sum(gg_tfi)/len(gg_tfi)+1.5, f'Avg Gem: {sum(gg_tfi)/len(gg_tfi):.1f}', fontsize=9, color=colors_gg, ha='right')

# ============================================
# 4. TFI SCATTER
# ============================================
ax4 = fig.add_subplot(4, 2, 4)
phrases_short = ['MUST MATCH', 'decomp_res', 'Do NOT desc', 'obs. actions', 'HIS', 'scanner', 'printer', 'filing cab']
delta_tfi = [gg_tfi[i] - ds_tfi[i] for i in range(len(phrases))]
colors_scatter = [colors_gg if d > 0 else colors_ds for d in delta_tfi]
ax4.scatter(ds_tfi, gg_tfi, s=250, c=colors_scatter, alpha=0.8, edgecolors='black', linewidth=1.5)
max_val = max(max(ds_tfi), max(gg_tfi)) + 5
ax4.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, linewidth=1)
ax4.fill_between([0, max_val], [0, max_val], [max_val, max_val], alpha=0.05, color=colors_gg)
ax4.fill_between([0, max_val], [0, 0], [0, max_val], alpha=0.05, color=colors_ds)
for i, phrase in enumerate(phrases_short):
    ax4.annotate(phrase, (ds_tfi[i], gg_tfi[i]), textcoords="offset points", xytext=(6, 6), fontsize=9, alpha=0.9)
ax4.set_xlabel('DeepSeek TFI', fontsize=12)
ax4.set_ylabel('Gemini TFI', fontsize=12)
ax4.set_title('D. TFI Correlation: DeepSeek vs Gemini', fontsize=14, fontweight='bold', pad=15)
ax4.grid(alpha=0.3)
ax4.text(max_val*0.05, max_val*0.92, 'Gemini fragments more ->', fontsize=10, color=colors_gg, fontweight='bold')
ax4.text(max_val*0.55, max_val*0.05, '<- DeepSeek fragments more', fontsize=10, color=colors_ds, fontweight='bold')

# ============================================
# 5. STEPS PER ACTIVITY
# ============================================
ax5 = fig.add_subplot(4, 2, 5)
activities = [gt['activity_name'] for gt in ground_truth]
act_labels = [a.replace('Register the ', '').replace(' of the patient', '').replace('Record the data of each patient', 'Record data').replace('Print referral document', 'Print referral').replace('Archive the record in file system', 'Archive record') for a in activities]
gt_counts = [len(gt['substeps']) for gt in ground_truth]
ds_counts = [len(next(p['substeps'] for p in pred_deepseek if p['activity_name'] == a)) for a in activities]
gg_counts = [len(next(p['substeps'] for p in pred_google if p['activity_name'] == a)) for a in activities]
x5 = np.arange(len(activities))
width5 = 0.25
bars_gt = ax5.bar(x5 - width5, gt_counts, width5, label='Ground Truth', color=colors_gt, edgecolor='white', linewidth=1.5)
bars_ds5 = ax5.bar(x5, ds_counts, width5, label='DeepSeek', color=colors_ds, edgecolor='white', linewidth=1.5)
bars_gg5 = ax5.bar(x5 + width5, gg_counts, width5, label='Gemini', color=colors_gg, edgecolor='white', linewidth=1.5)
ax5.set_ylabel('Number of Steps', fontsize=12)
ax5.set_title('E. Steps per Activity: Ground Truth vs Models', fontsize=14, fontweight='bold', pad=15)
ax5.set_xticks(x5)
ax5.set_xticklabels(act_labels, fontsize=10, rotation=15, ha='right')
ax5.legend(fontsize=10)
ax5.grid(axis='y', alpha=0.3)
for bars in [bars_gt, bars_ds5, bars_gg5]:
    for bar in bars:
        height = bar.get_height()
        ax5.annotate(f'{int(height)}', xy=(bar.get_x() + bar.get_width()/2, height), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=9)

# ============================================
# 6. DeepSeek Match Distribution by Activity
# ============================================
ax6 = fig.add_subplot(4, 2, 6)
match_types = ['Identical Match', 'Functional Equivalence', 'Granularity Difference', 'No Match']
match_colors = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444']

# Hardcoded mapping data extracted from mapping files
activity_match_data = {
    'DeepSeek': {
        'Record the data of each patient': {'Identical Match': 0, 'Functional Equivalence': 0, 'Granularity Difference': 2, 'No Match': 1},
        'Register the SSN of the patient': {'Identical Match': 0, 'Functional Equivalence': 2, 'Granularity Difference': 1, 'No Match': 0},
        'Register the Name of the patient': {'Identical Match': 0, 'Functional Equivalence': 3, 'Granularity Difference': 0, 'No Match': 0},
        'Register the Surname of the patient': {'Identical Match': 0, 'Functional Equivalence': 3, 'Granularity Difference': 0, 'No Match': 0},
        'Print referral document': {'Identical Match': 0, 'Functional Equivalence': 0, 'Granularity Difference': 2, 'No Match': 1},
        'Archive the record in file system': {'Identical Match': 0, 'Functional Equivalence': 2, 'Granularity Difference': 1, 'No Match': 0}
    }
}

bottom = np.zeros(len(activities))
for i, mt in enumerate(match_types):
    values = [activity_match_data['DeepSeek'].get(a, {}).get(mt, 0) for a in activities]
    ax6.bar(act_labels, values, bottom=bottom, label=mt, color=match_colors[i], edgecolor='white', linewidth=1)
    bottom += values
ax6.set_ylabel('Ground Truth Steps', fontsize=12)
ax6.set_title('F. DeepSeek: Match Type Distribution by Activity', fontsize=14, fontweight='bold', pad=15)
ax6.set_xticks(range(len(act_labels)))
ax6.set_xticklabels(act_labels, fontsize=10, rotation=15, ha='right')
ax6.legend(fontsize=9, loc='upper right')
ax6.grid(axis='y', alpha=0.3)

# ============================================
# 7. TOKENIZER OVERVIEW
# ============================================
ax7 = fig.add_subplot(4, 2, 7)
token_metrics = ['Total Tokens', 'JSON Syntax\nRatio (%)']
ds_token_vals = [tokenizer_report['deepseek']['total_tokens'], tokenizer_report['json_syntax_ratio']['deepseek'] * 100]
gg_token_vals = [tokenizer_report['gemini']['total_tokens'], tokenizer_report['json_syntax_ratio']['gemini'] * 100]
x7 = np.arange(len(token_metrics))
ax7_left = ax7
ax7_right = ax7.twinx()
bars_ds_t1 = ax7_left.bar(x7[0] - 0.175, ds_token_vals[0], 0.35, color=colors_ds, edgecolor='white', linewidth=1.5)
bars_gg_t1 = ax7_left.bar(x7[0] + 0.175, gg_token_vals[0], 0.35, color=colors_gg, edgecolor='white', linewidth=1.5)
bars_ds_t2 = ax7_right.bar(x7[1] - 0.175, ds_token_vals[1], 0.35, color=colors_ds, alpha=0.7, edgecolor='white', linewidth=1.5)
bars_gg_t2 = ax7_right.bar(x7[1] + 0.175, gg_token_vals[1], 0.35, color=colors_gg, alpha=0.7, edgecolor='white', linewidth=1.5)
ax7_left.set_ylabel('Total Tokens', fontsize=12, color='#333')
ax7_right.set_ylabel('JSON Syntax Ratio (%)', fontsize=12, color='#666')
ax7_left.set_title('G. Tokenizer Analysis: Token Count & JSON Ratio', fontsize=14, fontweight='bold', pad=15)
ax7_left.set_xticks(x7)
ax7_left.set_xticklabels(token_metrics, fontsize=11)
ax7_left.set_ylim(0, 1300)
ax7_right.set_ylim(0, 20)
ax7_left.legend(handles=[mpatches.Patch(facecolor=colors_ds, label='DeepSeek'), mpatches.Patch(facecolor=colors_gg, label='Gemini')], loc='upper right', fontsize=11)
for bar, val in zip([bars_ds_t1, bars_gg_t1], [ds_token_vals[0], gg_token_vals[0]]):
    ax7_left.annotate(f'{val}', xy=(bar[0].get_x() + bar[0].get_width()/2, val), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='bold')
for bar, val in zip([bars_ds_t2, bars_gg_t2], [ds_token_vals[1], gg_token_vals[1]]):
    ax7_right.annotate(f'{val:.1f}%', xy=(bar[0].get_x() + bar[0].get_width()/2, val), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='bold')

# ============================================
# 8. DELTA ANALYSIS
# ============================================
ax8 = fig.add_subplot(4, 2, 8)
delta_data = correlation['delta_analysis']
metrics_delta = ['Delta TFI', 'Delta No Match %', 'Delta Granularity\nDiff %', 'Delta Functional\nEq %']
delta_values = [delta_data['delta_tfi'], delta_data['delta_no_match'], delta_data['delta_granularity'], delta_data['delta_functional']]
colors_delta = [colors_gg if v > 0 else colors_ds for v in delta_values]
bars_delta = ax8.barh(metrics_delta, delta_values, color=colors_delta, edgecolor='black', linewidth=1.5, height=0.6)
ax8.axvline(x=0, color='black', linewidth=1)
ax8.set_xlabel('Delta (Gemini - DeepSeek)', fontsize=12)
ax8.set_title('H. Delta Analysis: TFI vs Validation Metrics', fontsize=14, fontweight='bold', pad=15)
ax8.grid(axis='x', alpha=0.3)
for bar, val in zip(bars_delta, delta_values):
    width = bar.get_width()
    ax8.annotate(f'{val:+.2f}', xy=(width, bar.get_y() + bar.get_height()/2), xytext=(5 if width >= 0 else -5, 0), textcoords="offset points", ha='left' if width >= 0 else 'right', va='center', fontsize=11, fontweight='bold')
ax8.text(0.98, 0.02, 'Positive -> Gemini higher\nNegative -> DeepSeek higher', transform=ax8.transAxes, fontsize=10, verticalalignment='bottom', horizontalalignment='right', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout(pad=4.0)
plt.savefig('experiment_dashboard.png', dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
print("Dashboard saved to experiment_dashboard.png")