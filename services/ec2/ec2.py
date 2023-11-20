"""Module responsible for outputing unused EC2 Instances"""
from datetime import datetime, timedelta
from boto3 import client


def check_date_range(date: datetime, days: int) -> bool:
    """
    Checks if given date is within provided date range

    Parameters:
        date (datetime): Offset-aware date to check
        days (int): Number of non-usage days to consider instance as used

    Returns:
        bool: Boolean result
    """

    if not date.tzinfo:
        raise ValueError("Date should be offset-aware")

    current_datetime = datetime.now(date.tzinfo)

    if date < current_datetime - timedelta(days=days):
        return False

    return True


def get_unused_instances(unused_threshold: int) -> None:
    """
    Checks EC2 instances and outputs instances that are stopped for more than X days

    Parameters:
        unused_threshold (int): Number of days to consider instance as unused
    """

    # Create a Boto3 client for Amazon EC2
    ec2_client = client("ec2")

    # Retrieve information about all EC2 instances
    response = ec2_client.describe_instances()

    unused_instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_name = "-"

            # Get the instance name from tags
            if "Tags" in instance:
                for tag in instance["Tags"]:
                    if tag["Key"] == "Name":
                        instance_name = tag["Value"]
                        break

            if instance["State"]["Name"] == "stopped" and not check_date_range(
                instance["UsageOperationUpdateTime"], unused_threshold
            ):
                unused_instances.append(
                    {"id": instance["InstanceId"], "name": instance_name}
                )

    print("\nUnused EC2 Instances:")
    print("---------------------------")
    for instance in unused_instances:
        instance_id = (
            instance["id"] + "\t\t\t"
            if len(instance["id"]) <= 15
            else instance["id"] + "\t"
        )
        print(f"Instance ID: {instance_id}Instance name: {instance['name']}")
