to initialize the project on your machine, you must create a virtual environment
run python -m venv <your_venv_name>
NOTE: venv must be placed in the root folder of the project (leveled with manage.py)

then run pip install -r requirements.txt to install all the project dependencies

IMPORTANT:
don't forget to run pip > freeze requirements.txt before commiting changes. This ensures
that all dependencies and packages you installed in your branch are included in the
requirements.txt file
