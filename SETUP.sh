cd
git clone https://github.com/shengdade/ECE1779_Assignment1.git
cd ECE1779_Assignment1
sudo pip install gunicorn
sudo pip install flask
sudo pip install boto3
mv ~/.aws ~/.aws-back
cp .aws ~/.aws
mysql --user=ece1779 --password=secret < ece1779_a1.sql
./run.sh