from datetime import datetime, timedelta
from boto3 import client


def get_old_snapshots(old_threshold: int):
    """
    Outputs snapshot's id if it's older than X days

    Parameters:
        old_threshold (int): Number of days to consider snapshot as old
    """

    # Create a Boto3 client for Amazon EC2
    ec2_client = client("ec2")

    # Retrieve all EC2 snapshots
    snapshots = ec2_client.describe_snapshots(OwnerIds=["self"])["Snapshots"]

    print("\nOld snapshots:")
    print("---------------------------")
    # Iterate over each snapshot
    for snapshot in snapshots:
        snapshot_id = (
            snapshot["SnapshotId"] + "\t\t"
            if len(snapshot["SnapshotId"]) <= 15
            else snapshot["SnapshotId"] + "\t"
        )
        start_time = snapshot["StartTime"]

        # Calculate the age of the snapshot
        age = datetime.now(start_time.tzinfo) - start_time

        # Check if the age of the snapshot is more than one year
        if age > timedelta(days=old_threshold):
            print(f"Snapshot ID: {snapshot_id}Volume size: {snapshot['VolumeSize']} GB")
