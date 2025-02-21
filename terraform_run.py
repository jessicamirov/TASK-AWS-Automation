import os
from python_terraform import Terraform

def run_terraform() -> str:
    terraform = Terraform(working_dir=os.path.dirname(__file__))
    terraform.init()
    terraform.plan()
    try:
        return_code, stdout, stderr = terraform.apply(skip_plan=True, capture_output=True, auto_approve=True)
        if return_code != 0:
            raise Exception(f"Terraform Apply Failed: {stderr}")
        return stdout
    except Exception as e:
        print(f"Error executing Terraform: {e}")
        exit(1)