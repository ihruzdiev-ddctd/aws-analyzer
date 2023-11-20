"""Module used for outputing unused subnet's information"""
from boto3 import client


def get_subnet_name(subnet: list) -> str:
    """
    Returns subnet name if present

    Returns:
        str: Subnet name
    """

    if "Tags" in subnet:
        for tag in subnet["Tags"]:
            if tag["Key"] == "Name":
                return tag["Value"]
    return "-"


def get_unused_subnets() -> None:
    "Outputs unused subnet's id and name"

    ec2_client = client("ec2")

    response = ec2_client.describe_subnets()
    subnets = response["Subnets"]

    unused_subnets = []

    for subnet in subnets:
        subnet_id = subnet["SubnetId"]

        response = ec2_client.describe_network_interfaces(
            Filters=[{"Name": "subnet-id", "Values": [subnet_id]}]
        )

        network_interfaces = response["NetworkInterfaces"]

        if len(network_interfaces) == 0:
            subnet_name = get_subnet_name(subnet)
            unused_subnets.append((subnet_id, subnet_name))

    # Print the unused subnets
    print("\nUnused Subnets:")
    print("---------------------------")
    for subnet_id, subnet_name in unused_subnets:
        subnet_id = subnet_id + "\t\t" if len(subnet_id) <= 15 else subnet_id + "\t"
        print(f"Subnet ID: {subnet_id}Subnet Name: {subnet_name}")
