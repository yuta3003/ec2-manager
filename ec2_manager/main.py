import os

import boto3
from botocore.exceptions import ClientError


def fetch_instances_status():
    answer_list = []

    session = boto3.session.Session()
    available_regions = session.get_available_regions('ec2')

    for region in available_regions:
        try:
            answer_dict = {}
            instances = []
            ec2 = boto3.client(
                "ec2",
                region_name=region,
            )
            ec2_data = ec2.describe_instances()
            for ec2_reservation in ec2_data["Reservations"]:
                for ec2_instance in ec2_reservation["Instances"]:
                    if ec2_instance["InstanceId"]:
                        instance = {}
                        instance["Status"] = ec2_instance["State"]["Name"]
                        instance["InstanceID"] = ec2_instance["InstanceId"]
                        instances.append(instance)
                        answer_dict["Region"] = region
                        answer_dict["Instances"] = instances

            if answer_dict:
                answer_list.append(answer_dict)
        except ClientError as error:
            print(f"{region}は有効になっていないリージョンです。スキップします。")

    return answer_list

if __name__ == "__main__":

    running_list = []
    stopped_list = []

    ec2_info = fetch_instances_status()
    for region_ec2 in ec2_info:
        for instances in region_ec2["Instances"]:
            if instances["Status"] == "running":
                running_list.append(instances)
            elif instances["Status"] == "stopped":
                stopped_list.append(instances)

    print("----run--------")
    print(running_list)
    print("----stop-------")
    print(stopped_list)

