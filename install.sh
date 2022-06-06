python3 -m venv venv
source venv/bin/activate
pip install pkg/pip-20.3.4-py2.py3-none-any.whl
pip install --find-links pkg -r requirements.txt
echo 'DB_HOST = ""
DB_DATABASE = ""
DB_USER = ""
DB_PORT = ""
DB_PASSWORD = ""' > config.py
