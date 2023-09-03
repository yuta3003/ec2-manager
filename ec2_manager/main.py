import boto3
import os

with open("reagion.txt", "r") as file:
    regions = [line.strip() for line in file]


answer_list = []
for region in regions:
    answer_dict = {}
    instances = []
    ec2 = boto3.client(
        "ec2",
        aws_access_key_id = os.environ["AccessKey"],
        aws_secret_access_key = os.environ["SecretAccessKey"],
        region_name = region
    )

    ec2_data = ec2.describe_instances()
    for ec2_reservation in ec2_data['Reservations']:
        for ec2_instance in ec2_reservation['Instances']:
            if ec2_instance["InstanceId"]:
                instance = {}
                instance["Status"] = ec2_instance['State']['Name']
                instance["InstanceID"] = ec2_instance["InstanceId"]
                instances.append(instance)
                answer_dict["Region"] = region
                answer_dict["Instances"] = instances

    if answer_dict:
        answer_list.append(answer_dict)
print(answer_list)
