import boto3

# Boto3セッションを作成し、リージョン情報を取得
session = boto3.session.Session()
available_regions = session.get_available_regions('ec2')  # 任意のAWSサービスを指定可能

# リージョンリストを表示
print(available_regions)
