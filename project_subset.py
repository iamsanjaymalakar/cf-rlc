import os
import random

# Define the path to the debug folder
debug_folder_path = 'fix_results/cf_3.43_WPI_JDK11/debug'

# Define the output file path
output_file_path = 'sampled_projects_field_escape.txt'

def get_field_escape_projects(folder_path):
    field_escape_projects = {}
    
    # List all files in the debug folder
    files = os.listdir(folder_path)
    
    # Filter out only .txt files
    txt_files = [file for file in files if file.endswith('.txt')]
    
    # Process each .txt file
    for txt_file in txt_files:
        # Extract project name from the file name
        project_name = os.path.splitext(txt_file)[0]
        
        # Construct full file path
        file_path = os.path.join(folder_path, txt_file)
        
        # Read and process the file
        with open(file_path, 'r') as file:
            for line in file:
                columns = line.strip().split('^')
                if len(columns) == 10 and "Field escape" in columns[9]:
                    if project_name not in field_escape_projects:
                        field_escape_projects[project_name] = []
                    field_escape_projects[project_name].append(line.strip())
    
    return field_escape_projects

def sample_projects(projects_dict, sample_size=40):
    # Filter projects with at least two "Field escape" cases
    eligible_projects = {k: v for k, v in projects_dict.items() if len(v) >= 2}
    
    # Randomly sample projects
    sampled_projects = random.sample(list(eligible_projects.items()), min(sample_size, len(eligible_projects)))
    
    return sampled_projects

# Get projects with "Field escape" cases
field_escape_projects = get_field_escape_projects(debug_folder_path)

# Sample 40 projects with at least two "Field escape" cases
sampled_projects = sample_projects(field_escape_projects, sample_size=40)

# Write the sampled projects and their "Field escape" cases to a file
with open(output_file_path, 'w') as output_file:
    for project_name, cases in sampled_projects:
        output_file.write(f'Project: {project_name}\n')
        for case in cases:
            output_file.write(f'{case}\n')
        output_file.write('-' * 80 + '\n')

print(f'Sampled projects have been written to {output_file_path}')
