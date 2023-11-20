"""Module used for outputing unused IGW's information"""
from boto3 import client
from helpers.url_generator import generate_aws_uri


def get_unused_igws() -> None:
    """
    Outputs unused IGW's id and correlating VPC's id
    """

    # Create a Boto3 client for EC2 service
    ec2_client = client("ec2")

    # Retrieve all VPCs in the AWS account
    response = ec2_client.describe_vpcs()

    # Print the unused IGWs
    print("\nUnused IGWs:")
    print("---------------------------")
    # Iterate over each VPC
    for vpc in response["Vpcs"]:
        vpc_id = vpc["VpcId"]

        # Retrieve all IGWs attached to the VPC
        igw_response = ec2_client.describe_internet_gateways(
            Filters=[{"Name": "attachment.vpc-id", "Values": [vpc_id]}]
        )

        # Check if there are any attached IGWs
        if len(igw_response["InternetGateways"]) == 0:
            # Iterate over each unused IGW
            for igw in igw_response["InternetGateways"]:
                igw_id = igw["InternetGatewayId"]
                igw_link = generate_aws_uri(
                    region=ec2_client.meta.region_name,
                    service="vpc",
                    query_params="InternetGateway:internetGatewayId",
                    resource_id=igw_id,
                )
                print(f"IGW ID for VPC {vpc_id}: {igw_link}")
