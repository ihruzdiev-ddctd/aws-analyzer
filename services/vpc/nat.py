from boto3 import client


def get_unused_nat_gateways() -> None:
    # Create a Boto3 client for the EC2 service
    ec2_client = client("ec2")

    # Retrieve a list of all NAT Gateways
    response = ec2_client.describe_nat_gateways()
    nat_gateways = response["NatGateways"]

    # Retrieve a list of all VPCs
    response = ec2_client.describe_vpcs()
    vpcs = response["Vpcs"]

    # Retrieve a list of all VPCs associated with a NAT Gateway
    vpc_ids_with_nat_gateway = set(nat_gateway["VpcId"] for nat_gateway in nat_gateways)

    # Find the VPCs without a NAT Gateway
    unused_vpcs = [vpc for vpc in vpcs if vpc["VpcId"] not in vpc_ids_with_nat_gateway]

    # Find the NAT Gateways that are associated with the unused VPCs
    unused_nat_gateways = [
        nat_gateway
        for nat_gateway in nat_gateways
        if nat_gateway["VpcId"] in [vpc["VpcId"] for vpc in unused_vpcs]
    ]

    # Print the unused NAT Gateways
    print("\nUnused NAT Gateways:")
    print("---------------------------")
    for nat_gateway in unused_nat_gateways:
        print(f"NAT Gateway ID:, {nat_gateway['NatGatewayId']}")
