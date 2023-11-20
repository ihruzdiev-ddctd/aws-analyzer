"""Module used for outputing unused ACL's information"""
from boto3 import client
from helpers.url_generator import generate_aws_uri


def get_unused_acls() -> None:
    """
    Outputs unused ACL's id and correlating VPC's id
    """

    # Create a Boto3 client for Amazon EC2
    ec2_client = client("ec2")

    # Retrieve all VPCs and their associated network ACLs
    vpcs = ec2_client.describe_vpcs()["Vpcs"]

    print("\nUnused ACLs:")
    print("---------------------------")
    # Iterate over each VPC
    for vpc in vpcs:
        vpc_id = vpc["VpcId"]

        # Retrieve the list of network ACLs associated with the VPC
        network_acls = ec2_client.describe_network_acls(
            Filters=[{"Name": "vpc-id", "Values": [vpc_id]}]
        )["NetworkAcls"]

        # Check if each network ACL is associated with any subnets
        for network_acl in network_acls:
            acl_link = generate_aws_uri(
                region=ec2_client.meta.region_name,
                service="vpc",
                query_params="NetworkAclDetails:networkAclId",
                resource_id=network_acl["NetworkAclId"],
            )
            if not network_acl["Associations"]:
                print(f"ACL ID in VPC {vpc_id}: {acl_link}")
