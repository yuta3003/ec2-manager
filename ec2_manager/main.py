import os

import boto3
import botocore.exceptions


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
        except botocore.exceptions.ClientError as error:
            print(f"{region}は有効になっていないリージョンです。スキップします。")

    return answer_list

if __name__ == "__main__":
    instances_info = fetch_instances_status()
    print(instances_info)
