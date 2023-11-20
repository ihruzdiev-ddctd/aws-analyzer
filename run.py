from services.ec2 import elb, ec2, security_groups, snapshots
from services.vpc import acl, igw, subnets, nat, route_tables

SNAPSHOT_THRESHOLD = 365
EC2_THRESHOLD = 90


def check_vpc() -> None:
    acl.get_unused_acls()
    igw.get_unused_igws()
    subnets.get_unused_subnets()
    nat.get_unused_nat_gateways()
    route_tables.get_unused_route_tables()


def check_ec2() -> None:
    elb.get_unused_lbs()
    snapshots.get_old_snapshots(SNAPSHOT_THRESHOLD)
    ec2.get_unused_instances(EC2_THRESHOLD)
    security_groups.get_unused_security_groups()


if __name__ == "__main__":
    check_vpc()
    check_ec2()
