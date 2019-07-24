This is Coding platform to create coding contests, see user rankings.

### Current Stack

    1. Python 3.8
    2. MySql 5.7
    3. Django 2.2

## Getting Started

---

### Installation (Recommended Ubuntu 18.04)

1. Check python3 version in your machine, and update to 3.8 accordingly.
    ```
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.8
    ```
2. Install MySql 5.7 on your system if not installed, follow [this](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04) tutorial.
3. Install additional python3.8 tools and virtualenv if not existing.
    ```
    sudo apt install python3.8-venv python3.8-dev python3.8-distutils
    python3.8 -m pip install --upgrade pip setuptools wheel
    ```
4. Create a virtual environment with the previously installed python like so
    `python3.8 -m venv coding_plat_env`
5. Install all the requirements with
    `pip install -r requirements.txt`
    
