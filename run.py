"""Outputs unused EC2 and VPC resource's information"""
from services.ec2 import elb, ec2, snapshots
from services.vpc import acl, igw, subnets, nat, route_tables, security_groups

SNAPSHOT_THRESHOLD = 365
EC2_THRESHOLD = 90


def check_vpc() -> None:
    """
    Outputs VPC resource's informantion
    """

    acl.get_unused_acls()
    igw.get_unused_igws()
    subnets.get_unused_subnets()
    nat.get_unused_nat_gateways()
    route_tables.get_unused_route_tables()
    security_groups.get_unused_security_groups()


def check_ec2() -> None:
    """
    Outputs EC2 resource's informantion
    """

    elb.get_unused_lbs()
    snapshots.get_old_snapshots(SNAPSHOT_THRESHOLD)
    ec2.get_unused_instances(EC2_THRESHOLD)


if __name__ == "__main__":
    check_vpc()
    check_ec2()
