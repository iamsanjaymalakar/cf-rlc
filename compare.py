'''
This script compares the error logs of the Checker Framework analysis results of three different versions of the Checker Framework.
  - Checker Framework 3.21.0
  - Checker Framework 3.43.0
  - Checker Framework 3.43.0 with WPI
  
The comparison results are written to a CSV file. Also, it generates an image that shows the comparison results.
'''

import csv
import os
import matplotlib.pyplot as plt


CF_3_21 = '/home/smala009/RLF/cf-rlc/cf_analysis_results/checkerframework_results'
CF_3_43 = '/home/smala009/RLF/cf-rlc/cf_analysis_results/checkerframework_3.42.0_results'
CF_3_43_WPI = '/home/smala009/RLF/cf-rlc/cf_analysis_results/checkerframework_3.42.0_results_WPI'
OUT_CSV = 'comparison_results/comparison_output.csv'


def read_error_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def extract_errors_and_count_v5(error_text: str, project_name=""):
    # Replace old and new start paths with a standardized start path
    standardized_start_path = "../dataset"
    error_text = error_text.replace(
        "../../../../datasets", standardized_start_path)
    # Split the error text into lines
    lines = error_text.split("\n")

    # Initialize a list to hold extracted errors and a counter for the errors
    errors = []
    error_count = 0
    reported_error_count = None

    # Define a general pattern to match the start of errors
    error_start_patterns = ["../dataset/",
                            "../../../../datasets/june2020_dataset/"]

    # Loop through lines to find and extract errors and check for the total error count line
    current_error = []
    exception_errors = 0
    for line in lines:
        # Skip if the line is a "Note:" line or contains a warning
        if line.strip().startswith("Note:") or "warning:" in line:
            continue
        if line.startswith("error: "):
            exception_errors += 1
        # Check for the total error count line
        if line.strip().endswith(" errors"):
            reported_error_count = int(line.strip().split(" ")[0])
            continue  # Skip adding this line to any current error

        # Check if line starts with any of the specified patterns indicating a new error
        if any(line.startswith(pattern) for pattern in error_start_patterns):
            if current_error:  # If there is a current error being processed, add it to errors
                errors.append("\n".join(current_error))
                current_error = []  # Reset current error
            current_error.append(line)
            error_count += 1  # Increment error count since this line indicates a new error
        elif current_error:  # If we are in the middle of an error, add the line to the current error
            current_error.append(line)

    # Check if there's an error being processed when the loop ends
    if current_error:
        errors.append("\n".join(current_error))

    # Assert the error count matches the reported error count, if present
    assert reported_error_count is None or reported_error_count - exception_errors == error_count, \
        f"Error count mismatch: extracted count is {error_count}, but reported count is {reported_error_count}, {project_name}, {errors}"

    return errors, error_count


def compare_errors(old_errors_text, new_errors_text, old_pname, new_pname):
    old_errors, old_count = extract_errors_and_count_v5(
        old_errors_text, old_pname)
    new_errors, new_count = extract_errors_and_count_v5(
        new_errors_text, new_pname)

    common_errors = set(old_errors) & set(new_errors)
    new_detected_errors = set(new_errors) - set(old_errors)
    no_longer_detected_errors = set(old_errors) - set(new_errors)

    return len(common_errors), len(new_detected_errors), len(no_longer_detected_errors)


def compare_versions_and_generate_csv(old_errors, new_v1_errors, new_v2_errors, output_csv):
    # Container for the rows to be written to the CSV
    headers = ["Project Name", "CF 3.21 Err Count", "CF 3.43 Err Count",
               "CF 3.43 w/ WPI Err Conut", "Comparison between CF 3.21 vs CF 3.43", "Comparison between CF 3.21 vs CF 3.43 w/ WPI"]
    rows = [headers]

    # Assuming the projects are the same across versions, list all projects from the OLD directory
    # Assuming directory names are provided as arguments
    projects = os.listdir(old_errors)

    for project in projects:
        old_text = read_error_file(os.path.join(old_errors, project))
        new_v1_text = read_error_file(os.path.join(new_v1_errors, project))
        new_v2_text = read_error_file(os.path.join(new_v2_errors, project))

        # Extract errors and counts
        _, old_count = extract_errors_and_count_v5(old_text, project)
        _, new_v1_count = extract_errors_and_count_v5(new_v1_text, project)
        _, new_v2_count = extract_errors_and_count_v5(new_v2_text, project)

        # Compare OLD vs NEW_V1
        common_v1, new_v1, missed_v1 = compare_errors(
            old_text, new_v1_text, project, project)
        common_v2, new_v2, missed_v2 = compare_errors(
            old_text, new_v2_text, project, project)

        comparison_v1 = f"Common: {common_v1}, Missed: {missed_v1}, New: {new_v1}"
        comparison_v2 = f"Common: {common_v2}, Missed: {missed_v2}, New: {new_v2}"
        # Add comparison results to the rows list
        rows.append([project, old_count, new_v1_count,
                    new_v2_count, comparison_v1, comparison_v2])

    # Write the comparison results to a CSV file
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    print(f"CSV generated: {output_csv}")


compare_versions_and_generate_csv(
    CF_3_21, CF_3_43, CF_3_43_WPI, OUT_CSV)


def generate_error_count_graph(csv_file, output_dir):
    # Lists to store the error counts for each project
    project_numbers = []
    cf3_21_counts = []
    cf3_43_counts = []
    cf3_43_wpi_counts = []

    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            # Extract error counts from each row
            project_numbers.append(i + 1)
            cf3_21_count = int(row["CF 3.21 Err Count"])
            cf3_43_count = int(row["CF 3.43 Err Count"])
            cf3_43_wpi_count = int(row["CF 3.43 w/ WPI Err Conut"])

            # Append error counts to the respective lists
            cf3_21_counts.append(cf3_21_count)
            cf3_43_counts.append(cf3_43_count)
            cf3_43_wpi_counts.append(cf3_43_wpi_count)

    # Plot the error counts with higher resolution
    plt.figure(dpi=300)
    plt.plot(project_numbers, cf3_21_counts, label='CF 3.21', linewidth=.5)
    plt.plot(project_numbers, cf3_43_counts, label='CF 3.43', linewidth=.5)
    plt.plot(project_numbers, cf3_43_wpi_counts, label='CF 3.43 w/ WPI', linewidth=.5)
    plt.xlabel('Project Number')
    plt.ylabel('Bug Count')
    plt.title('Bug Count Comparison by Project')
    plt.legend()

    # Save the image to the output directory
    output_path = os.path.join(output_dir, 'error_count_comparison.png')
    plt.savefig(output_path, dpi=300)
    print(f"Image saved: {output_path}")

# Call the function to generate the graph
generate_error_count_graph(OUT_CSV, 'comparison_results')
