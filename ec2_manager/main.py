import os

import boto3

with open("reagion.txt", "r", encoding="utf-8") as file:
    regions = [line.strip() for line in file]


answer_list = []
for region in regions:
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
print(answer_list)
