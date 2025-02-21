import subprocess
import os
from terraform_template import terraform_jinja2
from terraform_run import run_terraform

DEFAULT_REGION = "us-east-1"
DEFAULT_AVAILABILITY_ZONE = "us-east-1a"
AMI_OPTIONS = {
    "ubuntu": "ami-0dee1ac7107ae9f8c",
    "amazon-linux": "ami-0f1a6835595fb9246"
}
INSTANCE_TYPES = {
    "small": "t3.small",
    "medium": "t3.medium"
}

def get_user_choose() -> dict:
    """
    User needs to choose ami, instance type, region, and load balancer
    the func return a dictionary with the user chosen values!
    """

    ami = input("Choose AMI (ubuntu / amazon-linux): ").lower()
    if ami not in AMI_OPTIONS:
        print("Invalid AMI choice. Then your ami is default value: 'ubuntu'")
        ami = "ubuntu"

    instance_type = input("Choose INSTANCE TYPE (small / medium): ").lower()
    if instance_type not in INSTANCE_TYPES:
        print("Invalid instance type. Then your instance is default value: 'small'.")
        instance_type = "small"

    region = input(f"Choose REGION (default: {DEFAULT_REGION}): ").lower()
    if not region:
        region = DEFAULT_REGION
    elif region != DEFAULT_REGION:
        print(f"Invalid region, defaulting to {DEFAULT_REGION}")
        region = DEFAULT_REGION

    alb = input("Choose LOAD BALANCER Name: ")

    return {
        "ami": AMI_OPTIONS.get(ami),
        "instance_type": INSTANCE_TYPES.get(instance_type),
        "region": region,
        "alb": alb,
        "availability_zone": DEFAULT_AVAILABILITY_ZONE
    }

def main():
    # use subprocess
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = f"pip install -r {os.path.join(current_dir, 'requirements.txt')}"

    try:
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during pip install: {e}")
        return
    
    print("Cloud Deployment Configuration")

    user_choose = get_user_choose()
    terraform_jinja2(user_choose)
    run_terraform()

if __name__ == "__main__":
    main()