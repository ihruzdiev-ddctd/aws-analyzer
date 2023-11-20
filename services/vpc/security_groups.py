"""Module responsible for outputing unused security group's id and name"""
from boto3 import client
from helpers.url_generator import generate_aws_uri


def get_unused_security_groups() -> None:
    """
    Outputs unused security group's id and name
    """

    # Create a Boto3 client for Amazon EC2
    ec2_client = client("ec2")

    response = ec2_client.describe_security_groups()
    security_groups = response["SecurityGroups"]

    unused_security_groups = []

    for sg in security_groups:
        group_id = sg["GroupId"]
        group_name = sg["GroupName"]

        # Check if the security group is associated with any instances or network interfaces
        response = ec2_client.describe_network_interfaces(
            Filters=[{"Name": "group-id", "Values": [group_id]}]
        )

        if not response['NetworkInterfaces']:
            response = ec2_client.describe_instances(
                Filters=[{"Name": "instance.group-id", "Values": [group_id]}]
            )

            if not response["Reservations"]:
                unused_security_groups.append({"id": group_id, "name": group_name})

    # Print the unused Security Groups
    print("\nUnused Security Groups:")
    print("---------------------------")
    for sg in unused_security_groups:
        sg_id = sg["id"] + "\t\t\t" if len(sg["id"]) <= 15 else sg["id"] + "\t"
        sg_link = generate_aws_uri(
            region=ec2_client.meta.region_name,
            service="vpc",
            query_params="SecurityGroup:groupId",
            resource_id=sg_id,
        )
        print(f"ID: {sg_link}Name: {sg['name']}")
