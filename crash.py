import os
import re

def find_errors_in_log(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        pattern = re.compile(
            r"(The Checker Framework crashed\..+?at com\.sun\.tools\.javac\.Main\.main\(Main\.java:43\))",
            re.DOTALL
        )
        print(content)
    return pattern.findall(content)

def parse_logs_in_directory(root_dir):
    errors_by_project = {}

    for project_name in os.listdir(root_dir):
        project_dir = os.path.join(root_dir, project_name)
        if os.path.isdir(project_dir):
            log_file_path = os.path.join(project_dir, 'wpi-log.txt')
            if os.path.isfile(log_file_path):
                errors = find_errors_in_log(log_file_path)
                if errors:
                    errors_by_project[project_name] = errors
    return errors_by_project


def write_errors_to_log(errors_by_project, output_file_path):
    with open(output_file_path, 'w') as out_file:
        for project, errors in errors_by_project.items():
            out_file.write(f"Project: {project}\n")
            for error in errors:
                out_file.write(f"{error}\n")
                out_file.write("\n---\n")
            out_file.write('\n\n\n')

root_directory = '/home/smala009/RLF/dataset/june2020_dataset'
output_log_file = 'errors_summary.log'

errors_by_project = parse_logs_in_directory(root_directory)
write_errors_to_log(errors_by_project, output_log_file)
print(f"Errors written to {output_log_file}")
