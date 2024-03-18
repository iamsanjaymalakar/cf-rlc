import matplotlib.pyplot as plt

# Data initialization for the three versions
datasets = {
    "Checker Framework 3.21": {
        "Total Count": 2179,
        "Duplicates": 148,
        "Unmatched Count": 358,
        "Total (minus duplicates and unmatched) Count": 1673,
        "Both_array_and_field": 38,
        "Array Escapes": 113,
        "Field Escapes": 634,
        "Unfixable Count": 809,
        "Unfixable Percentage": 0.48356246264196057
    },
    "Checker Framework 3.43": {
        "Total Count": 1947,
        "Duplicates": 75,
        "Unmatched Count": 357,
        "Total (minus duplicates and unmatched) Count": 1515,
        "Both_array_and_field": 38,
        "Array Escapes": 114,
        "Field Escapes": 619,
        "Unfixable Count": 799,
        "Unfixable Percentage": 0.5273927392739274
    },
    "Checker Framework 3.43 with WPI": {
        "Total Count": 1835,
        "Duplicates": 82,
        "Unmatched Count": 367,
        "Total (minus duplicates and unmatched) Count": 1386,
        "Both_array_and_field": 32,
        "Array Escapes": 115,
        "Field Escapes": 549,
        "Unfixable Count": 720,
        "Unfixable Percentage": 0.5194805194805194
    }
}

# Define the colors and categories for the graph
colors = ['green', 'blue', 'orange', 'red']
categories = ['Fixable Rate', 'Unfixed due to Data-Structure Escape',
              'Unfixed due to Field Escape', 'Unfixed due to Other Reasons']

# Recalculate the percentages correctly for each dataset
for data in datasets.values():
    total = data["Total (minus duplicates and unmatched) Count"]
    data["Fixable Percentage"] = 100 - (data["Unfixable Percentage"] * 100)
    data["Unfix due to Data-Structure Escape Percentage"] = (
        data["Array Escapes"] / total) * 100
    data["Unfix due to Field Escape Percentage"] = (
        data["Field Escapes"] / total) * 100
    data["Unfix due to Other Reasons Percentage"] = 100 - (data["Fixable Percentage"] +
                                                           data["Unfix due to Data-Structure Escape Percentage"] +
                                                           data["Unfix due to Field Escape Percentage"])

# Set up the figure for plotting
fig, ax = plt.subplots(figsize=(10, 3))

# Thickness of the bars
bar_thickness = 0.4

# Plot the data for each version
for idx, (version, data) in enumerate(reversed(list(datasets.items()))):
    percentages = [
        data["Fixable Percentage"],
        data["Unfix due to Data-Structure Escape Percentage"],
        data["Unfix due to Field Escape Percentage"],
        data["Unfix due to Other Reasons Percentage"]
    ]

    left = 0
    for i, (category, color) in enumerate(zip(categories, colors)):
        ax.barh(version, percentages[i], left=left, color=color, edgecolor='white',
                height=bar_thickness, label=category if idx == len(datasets) - 1 else "")
        percentage_text = f'{percentages[i]:.1f}%' if percentages[i] > 0 else ''
        ax.text(left + percentages[i]/2, version, percentage_text,
                ha='center', va='center', color='white', fontsize=10, weight='bold')
        left += percentages[i]

# Remove the top, right, and bottom borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Add titles and legend
ax.set_title('Resource Leak Fixes Proportions Across Versions')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(categories))

# Adjust the layout
plt.tight_layout()

# Save the final corrected graph
file_path_final_correction = 'comparison_results/fixable_rate_comparison.png'
plt.savefig(file_path_final_correction)
plt.show()
