"""Module responsible for outputing unused load balancers"""
from boto3 import client
from helpers.url_generator import generate_aws_uri


def get_unused_lbs() -> None:
    """
    Outputs unused classic and elastic load balancers
    """

    # Create a Boto3 client for Amazon ELBv2
    elbv2_client = client("elbv2")

    # Create a Boto3 client for Amazon ELB
    elb_client = client("elb")

    # Find unused ALBs and NLBs
    response = elbv2_client.describe_load_balancers()
    elbv2_load_balancers = response["LoadBalancers"]
    unused_elbv2_load_balancers = []

    for lb in elbv2_load_balancers:
        if lb["State"]["Code"] != "active":
            unused_elbv2_load_balancers.append(lb["LoadBalancerName"])

    # Find unused CLBs
    response = elb_client.describe_load_balancers()
    elb_load_balancers = response["LoadBalancerDescriptions"]
    unused_elb_load_balancers = []

    for lb in elb_load_balancers:
        if not lb["Instances"]:
            unused_elb_load_balancers.append(lb["LoadBalancerName"])

    # Print the unused LBs
    print("\nUnused ALBs/NLBs:")
    print("---------------------------")
    for lb_name in unused_elbv2_load_balancers:
        print(f"LB Name: {lb_name}")

    print("\nUnused CLBs:")
    print("---------------------------")
    for lb_name in unused_elb_load_balancers:
        lb_link = generate_aws_uri(
            region=elb_client.meta.region_name,
            service="ec2",
            query_params="LoadBalancer:loadBalancerArn",
            resource_id=lb_name,
        )
        print(f"CLB Name: {lb_link}")
