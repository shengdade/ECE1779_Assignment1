db_config = {'user': 'ece1779',
             'password': 'secret',
             'host': '54.159.199.112',
             'database': 'ece1779_a1'}

ami_id = 'ami-a33c95b5'
instance_type = 't2.small'
security_group = ['a1-worker']
key_name = 'ece1779'

ARN = 'arn:aws:elasticloadbalancing:us-east-1:554376045366:targetgroup/a1-worker-group/e254bac50246fab2'

conn_args = {
    'aws_access_key_id': 'AKIAI7RZC7WJCND5SESA',
    'aws_secret_access_key': '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',
    'region_name': 'us-east-1'
}

# define userdata to be run at instance launch
userdata = """#cloud-config

runcmd:
 - cd /home/ubuntu/ECE1779_Assignment1
 - git pull https://shengdade:ece1779@github.com/shengdade/ECE1779_Assignment1.git
 - supervisord
 - echo "1. supervisord running" - `date` >> init-log
 - ./run_worker.sh &
 - echo "2. app running" - `date` >> init-log
"""

# userdata = """#cloud-config

# runcmd:
#  - cd /home/ubuntu
#  - locale-gen en_CA.UTF-8
#  - echo "1. locale-gen installed" - `date` >> ins-logs
#  - apt-get update
#  - echo "2. apt-get updated" - `date` >> ins-logs
#  - apt -y install redis-server
#  - echo "3. redis-server installed" - `date` >> ins-logs
#  - apt -y install supervisor
#  - echo "4. supervisor installed" - `date` >> ins-logs
#  - git clone https://shengdade:ece1779@github.com/shengdade/ECE1779_Assignment1.git
#  - echo "5. repository cloned" - `date` >> ins-logs
#  - cd ECE1779_Assignment1
#  - pip install --upgrade pip
#  - yes | pip install gunicorn
#  - yes | pip install flask
#  - yes | pip install boto3
#  - yes | pip install celery
#  - yes | pip install redis
#  - /usr/bin/redis-server --daemonize yes
#  - echo "6. redis-server running" - `date` >> ins-logs
#  - /home/ubuntu/ECE1779_Assignment1
#  - cp celery_master.conf  /etc/supervisor/conf.d
#  - supervisord
#  - echo "7. supervisord running" - `date` >> ins-logs
#  - ./run.sh
#  - echo "8. app running" - `date` >> ins-logs
# """

# - ./install_redis.sh
# - redis-stable/src/redis-server --daemonize yes
# - mysql --user=ece1779 --password=secret < ece1779_a1.sql
# - ./run.sh &

# /var/log/cloud-init-output.log
