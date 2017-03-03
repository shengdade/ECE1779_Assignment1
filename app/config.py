db_config = {'user': 'ece1779',
             'password': 'secret',
             'host': '54.89.25.75',
             'database': 'ece1779_a1'}

ami_id = 'ami-e3f432f5'
instance_type = 't2.small'
security_group = ['a1-worker']
key_name = 'ece1779'

conn_args = {
    'aws_access_key_id': 'AKIAJ3J2T2OKN4H6HDCA',
    'aws_secret_access_key': '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',
    'region_name': 'us-east-1'
}

# define userdata to be run at instance launch
userdata = """#cloud-config

runcmd:
 - cd
 - git clone https://github.com/shengdade/ECE1779_Assignment1.git
 - cd ECE1779_Assignment1
 - yes | pip install gunicorn
 - yes | pip install flask
 - yes | pip install boto3
 - mysql --user=ece1779 --password=secret < ece1779_a1.sql
 - ./run.sh
"""
