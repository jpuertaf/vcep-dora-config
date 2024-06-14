import os
import re
import shutil

directory = r'C:\Users\jpuerta\source\repos\vcep-int-inbound-contact'

patterns = [
    (r'Vcep\.Int\.Inbound\.Contact', r'${{values.dotnet_solution_name}}'),
    (r'ContactMarketingConsent', r'${{values.incoming_event_name}}'),
    (r'MarketingConsent', r'${{values.incoming_event_name}}'),
    (r'contactMarketingConsent', r'${{values.incoming_event_variable_name}}'),
    (r'vcep-int-inbound-contact', r'${{values.integration_name}}'),
    (r'This is an Inbound Integration for Contact object in Salesforce', r'${{values.description | dump}}'),
    (r'VcepContact', r'${{values.domain_class_name}}'),
    (r'vcepContact', r'${{values.domain_class_variable_name}}'),
    (r'Contact', r'${{values.domain_object_name}}'),
    (r'contact', r'${{values.domain_object_variable_name}}'),
    (r'cld-vcep-integration-team-sg', r'${{values.owner}}'),
    (r'vcep-integration', r'${{values.system}}'),
    (r'4418', r'${{values.app_id}}'),
    (r'preferenceengine-', r''),
    (r'marketingconsent-', r'')
]

def remove_unused_directories(directory):
    for root, dirs, _ in os.walk(directory, topdown=False):
        for d in ['bin', 'obj', 'debug', 'release']:
            dir_path = os.path.join(root, d)
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                print(f"Removed directory: {dir_path}")

def replace_in_file(file_path, patterns):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        for search_pattern, replace_pattern in patterns:
            content = re.sub(search_pattern, replace_pattern, content)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except (UnicodeDecodeError, FileNotFoundError, PermissionError) as e:
        print(f"Skipping file {file_path}: {e}")

def rename_item(old_path, search_pattern, replace_pattern):
    new_name = re.sub(search_pattern, replace_pattern, os.path.basename(old_path))
    new_path = os.path.join(os.path.dirname(old_path), new_name)
    
    os.rename(old_path, new_path)
    return new_path

def rename_files(root, files, patterns):
    for filename in files:
        old_file = os.path.join(root, filename)
        for search_pattern, replace_pattern in patterns:
            if re.search(search_pattern, filename):
                old_file = rename_item(old_file, search_pattern, replace_pattern)
        replace_in_file(old_file, patterns)

def rename_dirs(root, dirs, patterns):
    for dirname in dirs:
        old_dir = os.path.join(root, dirname)
        for search_pattern, replace_pattern in patterns:
            if re.search(search_pattern, dirname):
                old_dir = rename_item(old_dir, search_pattern, replace_pattern)

def rename_files_and_dirs(directory, patterns):
    remove_unused_directories(directory)
    
    for root, dirs, files in os.walk(directory, topdown=False):
        rename_files(root, files, patterns)
        rename_dirs(root, dirs, patterns)

rename_files_and_dirs(directory, patterns)