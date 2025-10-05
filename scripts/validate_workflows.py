#!/usr/bin/env python3
"""
GitHub Workflows Validation Script
Validates that all workflows are properly configured for the project
"""
import os
import yaml
import sys
from pathlib import Path


def validate_workflow_file(workflow_path):
    """Validate a single workflow file"""
    print(f"Validating {workflow_path}...")
    
    try:
        with open(workflow_path, 'r', encoding='utf-8') as f:
            workflow = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error in {workflow_path}: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading {workflow_path}: {e}")
        return False
    
    if not workflow:
        print(f"  No content loaded from {workflow_path}")
        return False
    
    issues = []
    
    # Check for required fields
    if 'name' not in workflow:
        issues.append("Missing 'name' field")
    
    # Note: 'on' might be parsed as boolean True by YAML parser
    if 'on' not in workflow and True not in workflow:
        issues.append("Missing 'on' field")
    
    if 'jobs' not in workflow:
        issues.append("Missing 'jobs' field")
    
    # Check Python version consistency
    jobs = workflow.get('jobs', {})
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])
        for step in steps:
            if step.get('uses') == 'actions/setup-python@v4':
                python_version = step.get('with', {}).get('python-version')
                if python_version and python_version != '3.13':
                    issues.append(f"Job '{job_name}' uses Python {python_version}, should be 3.13")
    
    # Check for virtual environment usage
    has_venv_setup = False
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])
        for step in steps:
            step_run = step.get('run', '')
            if 'python -m venv' in step_run or 'setup-venv' in step_run:
                has_venv_setup = True
                break
        if has_venv_setup:
            break
    
    if not has_venv_setup and any('pip install' in str(step.get('run', '')) for job in jobs.values() for step in job.get('steps', [])):
        issues.append("Uses pip install but doesn't set up virtual environment")
    
    if issues:
        print(f"❌ Issues found in {workflow_path}:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print(f"✅ {workflow_path} is valid")
        return True


def validate_requirements():
    """Validate requirements.txt"""
    print("Validating requirements.txt...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    required_packages = [
        'platformio',
        'esptool',
        'pyserial',
        'flake8',
        'black'
    ]
    
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            content = f.read().lower()
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False
    
    missing_packages = []
    for package in required_packages:
        if package not in content:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages in requirements.txt: {missing_packages}")
        return False
    
    print("✅ requirements.txt is valid")
    return True


def validate_python_version():
    """Validate Python version compatibility"""
    print("Validating Python version...")
    
    try:
        import sys
        version = sys.version_info
        
        if version.major != 3 or version.minor < 8:
            print(f"⚠️ Python {version.major}.{version.minor} detected. Python 3.8+ recommended for GitHub Actions compatibility")
            return True  # Warning, not error
        
        if version.minor == 13:
            print(f"✅ Python {version.major}.{version.minor} is perfect for this project")
        else:
            print(f"✅ Python {version.major}.{version.minor} is compatible")
        
        return True
    except Exception as e:
        print(f"❌ Error checking Python version: {e}")
        return False


def main():
    """Main validation function"""
    print("🔍 GitHub Workflows Validation")
    print("=" * 40)
    
    # Find all workflow files
    workflows_dir = Path('.github/workflows')
    if not workflows_dir.exists():
        print("❌ .github/workflows directory not found")
        return False
    
    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
    
    if not workflow_files:
        print("❌ No workflow files found")
        return False
    
    print(f"Found {len(workflow_files)} workflow files")
    
    # Validate each workflow
    all_valid = True
    for workflow_file in workflow_files:
        if not validate_workflow_file(workflow_file):
            all_valid = False
    
    # Validate requirements
    if not validate_requirements():
        all_valid = False
    
    # Validate Python version
    if not validate_python_version():
        all_valid = False
    
    print("\n" + "=" * 40)
    if all_valid:
        print("🎉 All validations passed!")
        print("Your GitHub workflows are properly configured.")
        return True
    else:
        print("❌ Some validations failed!")
        print("Please fix the issues above before committing.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)