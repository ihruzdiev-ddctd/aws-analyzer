# AWS Analyzer

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/downloads/)

## Overview

This Python script uses the boto3 library to identify and display unused AWS VPC and EC2 resources. It helps you manage and optimize your AWS infrastructure by detecting resources that might no longer be in use.

## Prerequisites

- Python 3.10 or higher
- Install required dependencies:

```bash
pip install -r requiremets
```

## Configuration

Configure AWS credentials:

- Make sure you have AWS CLI installed.
- Run aws configure and enter your AWS access key, secret key, region, and output format.

Adjust script settings (if necessary):

- Open run.py.
- Modify the configuration parameters such as SNAPSHOT_THRESHOLD to set the threshold for considering a resource as unused.

## Usage

Run the script:

```bash
python run.py
```

The script will analyze your AWS account and print a list of unused VPC and EC2 resources.

Example Output

```yaml
Unused Subnets:
---------------------------
Subnet ID: subnet-abcde1     Subnet Name: subnet-a
Subnet ID: subnet-abcde2     Subnet Name: subnet-b

Unused EC2 Instances:
---------------------------
Instance ID: i-abcde1  Instance name: instance-1
Instance ID: i-abcde2  Instance name: instance-2
```

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Thanks to the [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library for simplifying AWS interactions.
