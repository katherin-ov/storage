## Задание
### Приложение для управления складом
# Setup

This file provides some instructions on how to do local setup and run backend

## Setup python virtual environment

Here it is provided instructions to set up venv using python standard library [venv module](https://docs.python.org/3/library/venv.html).
But you welcome to use any tool you comfortable with (e.g. [pyenv](https://github.com/pyenv/pyenv))

1. Navigate to the project directory:
    ```shell
    cd storage
    ```
2. Setup python virtual environment for the project:
    ```shell
   python -m venv .venv
   ```
3. Activate python virtual environment:
    ```shell
   source .venv/bin/activate
   ```
   
4. Install the required packages for the **local development**:
    ```shell
    pip install -r requirements.txt  
    ```
   
## Run

Run program by command:
 ```shell
uvicorn src.storage.entrypoints.app:app --reload 
 ```
