# Flask-blog
## Installation steps
1. Clone the repository
1. Go into the cloned directory
1. Run `setup.sh`
1. Enter the details in the json file that will open, and then save and exit
1. Activate virtual environment
    ```
    source venv/bin/activate
    ```
1. Run the app
    ```
    export FLASK_APP=run.py
    flask run --host=0.0.0.0
    ```