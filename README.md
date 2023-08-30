---
title: Flask Blog
emoji: 🔥
colorFrom: yellow
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 7680
---

# Flask-blog
<h2>Table of Contents</h2>
  <ul> 
   <li><a href="#Installation">Installation</a></li>                    
  </ul>
<h2 id="Installation">Installation</h2>


- Clone this repository
    ```
    git clone https://github.com/soumya-prabha-maiti/Flask-blog.git
    ```
- Go into the repository 
    ```
    cd Flask-blog
    ```
- Run `setup.sh` to perform initial setup
    ```Y
    bash setup.sh
    ```
- A json file will open. Type in the configuration values.
    ```json
    {
        "SECRET_KEY":"type secret key here",
        "SQLALCHEMY_DATABASE_URI":"type database URI here",
        "EMAIL_USERNAME":"type email id here",
        "EMAIL_PASSWORD":"type email password here"
    }
    ```
    After filling in the details, press `Ctrl+X` > `Y` > `Enter` 
    
- Activate the virtual environment 
    ```
    source venv/bin/activate
    ```
- Run 
    ```
    flask run --host=0.0.0.0
    ```
