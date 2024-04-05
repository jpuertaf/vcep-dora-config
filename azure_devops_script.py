from dotenv import load_dotenv
import os
import requests
import base64

# Load environment variables
load_dotenv()

# Azure DevOps Settings
azure_organization = os.getenv('AZURE_ORGANIZATION')
azure_project = os.getenv('AZURE_PROJECT')
azure_pat = os.getenv('AZURE_PERSONAL_ACCESS_TOKEN')

# GitHub Settings
github_organization = os.getenv('GITHUB_ORGANIZATION')
github_pat = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')

# Encode PATs for HTTP header
encoded_azure_pat = str(base64.b64encode(bytes(f':{azure_pat}', 'ascii')), 'ascii')
encoded_github_pat = str(base64.b64encode(bytes(f'{github_pat}:', 'ascii')), 'ascii')

# Headers
azure_headers = {'Authorization': f'Basic {encoded_azure_pat}'}
github_headers = { 'Authorization': f'token {github_pat}'}

# Fetch Azure DevOps pipelines
azure_pipelines_response = requests.get(
    f'https://dev.azure.com/{azure_organization}/{azure_project}/_apis/build/definitions?api-version=6.0',
    headers=azure_headers)

if azure_pipelines_response.status_code == 200:
    azure_pipeline_names = [pipeline['name'] for pipeline in azure_pipelines_response.json().get('value', [])]

# Fetch GitHub repositories starting with "vcep-int-"
github_repos_response = requests.get(
    f'https://api.github.com/orgs/{github_organization}/repos?type=internal',
    headers=github_headers)

if github_repos_response.status_code == 200:
    github_repos = [repo for repo in github_repos_response.json()]
    github_repo_names = [repo['name'] for repo in github_repos]
    #github_repo_names = [repo['name'] for repo in github_repos if repo['name'].startswith('vcep-int-')]
else:
    print(f"Error fetching GitHub repositories: HTTP {github_repos_response.status_code} - {github_repos_response.text}")
    github_repo_names = []

# Directory to save the config files
output_directory = os.path.join(os.getcwd(), 'output_configs')
os.makedirs(output_directory, exist_ok=True)

# Template
template = """project_name: {project_name}
cluster: Customer Care
team: Vcep Integration Team
tags: [Integration Platform, VCEP]
services:
  -
    name: {service_name}
    source: GITHUB
    repo: {git_repo_name}
    project: RCXP
    environments:  
      -
        name: uat
        branch: master
        pipeline: AZURE_PIPELINES
        workflow: {pipeline_name}
        job: Job
      -
        name: prod-emea
        branch: master
        pipeline: AZURE_PIPELINES
        workflow: {pipeline_name}
        job: Job
"""

for name in azure_pipeline_names:
    print(f"azure_pipeline_names: {name}")

# Match and generate config files
for repo_name in github_repo_names:
    print(f"repo_name: {repo_name}")
    if repo_name in azure_pipeline_names:
        repo_dir = os.path.join(output_directory, repo_name)
        os.makedirs(repo_dir, exist_ok=True)
        
        config_path = os.path.join(repo_dir, 'config.yml')
        with open(config_path, 'w') as config_file:
            config_content = template.format(
                project_name=azure_project,
                service_name=repo_name,
                git_repo_name=repo_name,
                pipeline_name=repo_name
            )
            config_file.write(config_content)
        print(f"Config for {repo_name} created at {config_path}")
