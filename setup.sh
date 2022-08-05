# Installing dependencies
sudo apt install python3-pip
sudo apt install python3.10-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create a configuration file
sudo touch /etc/flask_blog_config.json
sudo sh -c "printf '{\n\t\"SECRET_KEY\":\"\",\n\t\"SQLALCHEMY_DATABASE_URI\":\"\",\n\t\"EMAIL_USERNAME\":\"\",\n\t\"EMAIL_PASSWORD\":\"\"\n}'> /etc/flask_blog_config.json"
sudo nano /etc/flask_blog_config.json

# Set the flask app
printf 'export FLASK_APP=run.py'>.bashrc
source .bashrc