db_config = {'user': 'ece1779',
             'password': 'secret',
             'host': '54.209.253.37',
             'database': 'ece1779_a1'}

ami_id = 'ami-e3f432f5'
instance_type = 't2.small'
security_group = ['a1-worker']
key_name = 'ece1779'

# for assignment 1
ARN = 'arn:aws:elasticloadbalancing:us-east-1:554376045366:targetgroup/a1-worker-group/e254bac50246fab2'

# for dade ec2
# ARN = 'arn:aws:elasticloadbalancing:us-east-1:415416742824:targetgroup/a1-worker-group/a9217aa5e0cdc06b'

# for assignment 1
conn_args = {
    'aws_access_key_id': 'AKIAI7RZC7WJCND5SESA',
    'aws_secret_access_key': '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',
    'region_name': 'us-east-1'
}

# for dade ec2
# conn_args = {
#     'aws_access_key_id': 'AKIAIL4GGZP6HRGUBRUA',
#     'aws_secret_access_key': '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',
#     'region_name': 'us-east-1'
# }

# define userdata to be run at instance launch
userdata = """#cloud-config

runcmd:
 - cd /home/ubuntu
 - locale-gen en_CA.UTF-8
 - echo "locale-gen installed" - `date` >> ins-logs
 - apt-get update
 - echo "apt-get updated" - `date` >> ins-logs
 - git clone https://shengdade:ece1779@github.com/shengdade/ECE1779_Assignment1.git
 - echo "repository cloned" - `date` >> ins-logs
 - cd ECE1779_Assignment1
 - pip install --upgrade pip
 - yes | pip install gunicorn
 - yes | pip install flask
 - yes | pip install boto3
 - yes | pip install celery
 - yes | pip install redis
 - apt -y install redis-server
 - echo "redis-server installed" - `date` >> ins-logs
 - apt -y install supervisor
 - echo "supervisor installed" - `date` >> ins-logs
 - redis-server --daemonize yes
 - echo "redis-server running" - `date` >> ins-logs
 - /home/ubuntu/ECE1779_Assignment1
 - cp celery.conf  /etc/supervisor/conf.d
 - supervisord
 - echo "supervisord running" - `date` >> ins-logs
 - ./run.sh
 - echo "app running" - `date` >> ins-logs
"""

# - ./install_redis.sh
# - redis-stable/src/redis-server --daemonize yes
# - mysql --user=ece1779 --password=secret < ece1779_a1.sql
# - ./run.sh &

# /var/log/cloud-init-output.log
