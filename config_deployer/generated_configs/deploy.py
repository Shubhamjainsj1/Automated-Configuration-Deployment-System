import yaml
import json
import os
import subprocess
import argparse

def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def merge_configs(base, override):
    for key, value in override.items():
        if isinstance(value, dict) and key in base:
            base[key] = merge_configs(base[key], value)
        else:
            base[key] = value
    return base

def write_config(config, output_path):
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)

def git_commit(file_path, env):
    subprocess.run(["git", "add", file_path])
    subprocess.run(["git", "commit", "-m", f"Deploy config to {env}"])
    subprocess.run(["git", "push"])

def deploy(env):
    base = load_yaml("templates/base.yaml")
    override = load_yaml(f"templates/{env}.yaml")
    final_config = merge_configs(base, override)

    output_file = f"generated_configs/config_{env}.json"
    write_config(final_config, output_file)

    git_commit(output_file, env)

    subprocess.run(["deploy.bat", env, output_file])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("env", help="Environment to deploy (dev/staging/prod)")
    args = parser.parse_args()

    deploy(args.env)
