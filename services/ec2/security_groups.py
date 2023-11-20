from boto3 import client


def get_unused_security_groups() -> None:
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
        network_interfaces = response["NetworkInterfaces"]

        if not network_interfaces:
            response = ec2_client.describe_instances(
                Filters=[{"Name": "instance.group-id", "Values": [group_id]}]
            )
            instances = response["Reservations"]

            if not instances:
                unused_security_groups.append({"id": group_id, "name": group_name})

    # Print the unused Security Groups
    print("\nUnused Security Groups:")
    print("---------------------------")
    for sg in unused_security_groups:
        sg_id = sg["id"] + "\t\t\t" if len(sg["id"]) <= 15 else sg["id"] + "\t"
        print(f"ID: {sg_id}Name: {sg['name']}")
