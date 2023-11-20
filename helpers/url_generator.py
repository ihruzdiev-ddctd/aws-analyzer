"""Module that converts string into a clickable link in terminal"""


def generate_uri(uri: str, label=None) -> str:
    """
    Converts string into a clickable link in terminal

    Parameters:
        uri (str): Target URI
        label (str): (Optional) Text to display instead of link

    Returns:
        (str): Clickable link with or without label
    """

    if label is None:
        label = uri

    parameters = ""

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = "\033]8;{};{}\033\\{}\033]8;;\033\\"

    return escape_mask.format(parameters, uri, label)


def generate_aws_uri(
    service: str, query_params: str, resource_id: str, region="us-east-1"
) -> str:
    """
    Using provided parameters generates clickable terminal link to target AWS resource

    Parameters:
        service (str): Type of AWS service (supports vpc or ec2 only)
        query_params (str): URL query parameters to use, e.g.: "InstanceDetails:instanceId"
        resource_id (str): AWS resource ARN
        region (str): AWS account region, default: "us-east-1"

    Returns:
        (str): Clickable link to target AWS resource
    """

    endpoint = ""

    match service:
        case "vpc":
            endpoint = "vpcconsole"
        case "ec2":
            endpoint = "ec2"

    return generate_uri(
        f"https://{region}.console.aws.amazon.com/{endpoint}/home?region={region}#{query_params}={resource_id}",
        resource_id,
    )
