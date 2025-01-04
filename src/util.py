import copy
import git
import json
import yaml
import tempfile

def populate_execution_metadata(execution_metadata, component_config):
    # Create a deep copy of 'component_config' to avoid modifying the original list
    # Lists in Python are reference types, so without a deep copy, changes will also reflect in the original list
    component_config = copy.deepcopy(component_config)
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    print(f"Cloning GAM repo at: {temp_dir}")
    git.Repo.clone_from(url='https://github.com/red-hat-data-services/Gated-Auto-Merger.git', to_path=temp_dir, branch='metadata')
    
    # Load the necessary files from the cloned repo
    cvp = json.load(open(temp_dir + '/build/latest/cvp.json'))
    upstream_sources = yaml.safe_load(open(temp_dir + '/build/latest/upstream_sources.yml', 'r'))
    
    # Update the metadata with the NVR from the CVP file
    execution_metadata['metadata']['nvr'] = cvp['artifact']['nvr']
    
    execution_metadata['metadata']['status'] = 'TestingInProgress'
    execution_metadata['metadata']['git'] = component_config['repositories']
    
    # Iterate over the repositories and update 'src.branch' with commit hash from upstream_sources
    for entry in execution_metadata["metadata"]["git"]:
        src_url = entry["src"]["url"]
        src_branch = entry["src"]["branch"]

        for upstream_entry in upstream_sources["git"]:
            if upstream_entry["url"] == src_url:
                if upstream_entry["branch"] == src_branch:
                    # Update src.branch with the commit hash from upstream_sources
                    entry["src"]["branch"] = upstream_entry["commit"]
                else:
                    raise ValueError(f"Source branch '{entry['src']['branch']}' defined in gam-config.yaml for repository '{entry['name']}' did not match with upstream branch '{upstream_entry['branch']}' defined in upstream_sources.yml")

    return execution_metadata