import json
import boto3

def fetch_aws_details() -> dict[str,str]:
    "Using boto3 to verify the resources"
    ec2_client = boto3.client("ec2")
    elb_client = boto3.client("elbv2")

    instance_id = None
    public_ip = None

    try:
        # Fetch EC2 instances
        instances = ec2_client.describe_instances().get("Reservations", [])
        for instance in instances:
            for inst in instance.get("Instances", []):
                if inst["State"]["Name"] == "running":
                    instance_id = inst["InstanceId"]
                    public_ip = inst.get("PublicIpAddress")
                    break
            # Exit the external loop when a running instance is found
            if instance_id:
                break
    except boto3.exceptions.Boto3Error as e:
        print(f"Error fetching EC2 instances: {e}")
        return {"error": "Failed to fetch EC2 instances"}

    try:
        # Fetch Load Balancer details
        lbs = elb_client.describe_load_balancers().get("LoadBalancers", [])
        if lbs:
            lb_dns = lbs[0]["DNSName"]
    except boto3.exceptions.Boto3Error as e:
        print(f"Error fetching Load Balancer details: {e}")
        return {"error": "Failed to fetch Load Balancer details"}
    
    # Check if EC2 instance and Load Balancer are found
    if not instance_id:
        return "ERROR - No running EC2 instance found"
    if not lb_dns:
        return "ERROR - No Load Balancer found"

    # Prepare validation data
    instance_state = "running" if instance_id else "not found"
    validation_data = {
        "instance_id": instance_id,
        "instance_state": instance_state,
        "public_ip": public_ip,
        "load_balancer_dns": lb_dns
    }

    try:
        # Save the validation data to a file
        with open("aws_validation.json", "w") as f:
            json.dump(validation_data, f, indent=4)
    except IOError as e:
        print(f"Error saving validation data to file: {e}")
        return {"error": "Failed to save validation data"}

    return validation_data
