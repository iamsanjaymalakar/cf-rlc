import os
import shutil
import subprocess
import time

def extract_number(s):
    try:
        x = int(s[len('iteration'):])
        return x
    except ValueError:
        print(f"Error extracting number from {s}")
        return 0

def find_repeating_patterns(diffs):
    patterns = {}
    for i in range(len(diffs)):
        for j in range(i+1, min(i+5, len(diffs))):  # Check for close repeating patterns
            if diffs[i] == diffs[j]:
                if (i, j) not in patterns:
                    patterns[(i, j)] = diffs[i]
    return patterns

def analyze_project_iterations(project_path):
    folder_path = os.path.join(project_path, 'wpi-iterations')
    
    if not os.path.exists(folder_path) or not os.listdir(folder_path):
        return  # Skip if the directory does not exist or is empty

    dirs = os.listdir(folder_path)
    if '.DS_Store' in dirs:
        dirs.remove('.DS_Store')
    if 'temp1' in dirs:
        dirs.remove('temp1')
    if 'temp2' in dirs:
        dirs.remove('temp2')

    if len(dirs) < 20:
        return  # Skip projects with fewer than 20 iterations
    print(f"Analyzing {project_path}")
    # Temporary directories for consistent diff comparisons
    temp_dir1 = os.path.join(folder_path, 'temp1')
    temp_dir2 = os.path.join(folder_path, 'temp2')

    # Ensure temporary directories are empty
    shutil.rmtree(temp_dir1, ignore_errors=True)
    shutil.rmtree(temp_dir2, ignore_errors=True)
    time.sleep(5)  # Pause to ensure the removal has completed

    os.makedirs(temp_dir1, exist_ok=True)
    os.makedirs(temp_dir2, exist_ok=True)

    folder_names = sorted(dirs, key=extract_number)

    diffs = []

    for i in range(len(folder_names) - 1):
        folder1 = os.path.join(folder_path, folder_names[i])
        folder2 = os.path.join(folder_path, folder_names[i + 1])

        # Copy folders to temporary locations
        shutil.copytree(folder1, temp_dir1, dirs_exist_ok=True)
        shutil.copytree(folder2, temp_dir2, dirs_exist_ok=True)

        # Execute the diff command and capture its output
        result = subprocess.run(['diff', '-r', temp_dir1, temp_dir2], capture_output=True, text=True)
        diffs.append(result.stdout)

        # Clean up temporary directories for the next iteration
        shutil.rmtree(temp_dir1)
        shutil.rmtree(temp_dir2)
        os.makedirs(temp_dir1, exist_ok=True)
        os.makedirs(temp_dir2, exist_ok=True)

    patterns = find_repeating_patterns(diffs)

    # Store results in a file named after the project
    results_path = os.path.join('Results', f"{os.path.basename(project_path)}.txt")
    os.makedirs('Results', exist_ok=True)  # Create results directory if it does not exist
    with open(results_path, 'w') as f:
        if patterns:
            for (i, j), diff in patterns.items():
                f.write(f"Repeating pattern between iteration {i+1} and iteration {j+1}:\n{diff}\n\n")
        else:
            f.write("No repeating diff patterns found.\n")

# Loop through each project in the 'BENCH' directory
bench_directory = '../dataset/june2020_dataset_copy'
projects = [os.path.join(bench_directory, d) for d in os.listdir(bench_directory) if os.path.isdir(os.path.join(bench_directory, d))]

for project in projects:
    analyze_project_iterations(project)
