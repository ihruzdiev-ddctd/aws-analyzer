"""Module used for outputing unused route table's information"""
from boto3 import client
from helpers.url_generator import generate_aws_uri


def get_unused_route_tables() -> None:
    """
    Outputs unused route table's id
    """

    # Create a Boto3 client for the EC2 service
    ec2_client = client("ec2")

    # Retrieve all Route Tables
    response = ec2_client.describe_route_tables()

    # Print the unused route tables
    print("\nUnused route tables:")
    print("---------------------------")
    # Iterate over each route table
    for table in response["RouteTables"]:
        table_id = table["RouteTableId"]
        table_link = generate_aws_uri(
            region=ec2_client.meta.region_name,
            service="vpc",
            query_params="RouteTableDetails:RouteTableId",
            resource_id=table_id,
        )
        # Check if the route table is associated with any subnet
        if len(table["Associations"]) == 0:
            print(f"Route Table ID: {table_link}")
