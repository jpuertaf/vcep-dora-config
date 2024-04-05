import os
import json

with open('repo.json', 'r') as file:
    repos = json.load(file)

template = """project_name: {project_name}
cluster: Customer Care
team: Vcep Integration Team
tags: [Integration Platform, VCEP]
services:
  - name: {service_name}
    source: GITHUB
    repo: {git_repo_name}
    environments:  
      - name: uat
        branch: master
        pipeline: AZURE_PIPELINES
        workflow: {pipeline_name}
        job: Job
        project: RCXP
      - name: prod-emea
        branch: master
        pipeline: AZURE_PIPELINES
        workflow: {pipeline_name}
        job: Job
        project: RCXP
"""

def format_name(name):
    """Transforms repository name to project name format."""
    return ' '.join([word.capitalize() for word in name.replace('vcep-int-', '').split('-')])

base_output_directory = os.path.join(os.getcwd(), 'output_configs')
os.makedirs(base_output_directory, exist_ok=True)

for repo in repos:
    if repo['pipeline']:  
        formatted_project_name = format_name(repo['repository'])
        service_name = formatted_project_name
        git_repo_name = repo['repository']
        pipeline_name = repo['pipeline']
        job_name = "Job" 

        folder_name = git_repo_name.replace('vcep-', '')
        repo_dir = os.path.join(base_output_directory, folder_name)
        os.makedirs(repo_dir, exist_ok=True)

        config_filename = 'config.yaml'
        config_path = os.path.join(repo_dir, config_filename)

        with open(config_path, 'w') as config_file:
            config_file.write(template.format(
                project_name=formatted_project_name,
                service_name=service_name,
                git_repo_name=git_repo_name,
                pipeline_name=pipeline_name
            ))

        print(f"Config for {git_repo_name} created at {config_path}")
