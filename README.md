# IDAMSG
Student project built as part of the Architecture of Integration and Deployment discipline. 
## Development
Assuming you run commands from same directory
- Get `poetry`: https://python-poetry.org/docs/#installation
- Clone repository:
  ```bash
  git clone https://github.com/Te4nick/idamsg.git
  ```
- Cd to folder:
  ```bash
  cd idamsg
  ```
- Checkout to `django` branch:
  ```bash
  git checkout django
  ```
- Get `poetry` shell:
  ```bash
  poetry shell
  ```
- Install dependancies:
  ```bash
  poetry install --with dev --no-root
  ```
- Run django server
  ```bash
  poetry run python ./core/manage.py runserver
- Get another shell
- Cd to folder:
  ```bash
  cd idamsg
  ```
- Get `poetry` shell:
  ```bash
  poetry shell
  ```
- Run tests:
  ```bash
  poetry run pytest
  ```
- NOTE: to pass tests you must restart django runserver
## Links
- API runs at http://127.0.0.1:8000/
- Swagger docs are accessable via http://127.0.0.1:8000/api/docs/
