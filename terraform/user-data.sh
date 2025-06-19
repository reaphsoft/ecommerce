# user-data.sh (add this file in the terraform/ directory)
#!/bin/bash
sudo apt-get update -y
sudo apt-get install -y python3-pip git
cd /home/ubuntu
git clone https://github.com/reaphsoft/ecommerce.git
cd ecommerce
pip3 install -r requirements.txt
nohup python3 app.py > app.log 2>&1 &
