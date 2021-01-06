#!/bin/bash

function install_python3 {
    echo '[UPDATE] Start updata APT'
    sudo apt -y update
	echo '[INSTALL] Installing python3 and python3-pip.'
    sudo apt -y install python3 python3-pip
	if [ $? -eq 0 ]; then
        sudo apt -y autoclean
    else
		sudo apt -y remove python3 python3-pip
		echo '[ERROR] Problem with install python3 or python3-pip.'
        exit 1
    fi
}

function check_python3 {
    if ! [ -x "$(command -v python3)" ]; then
        echo '[ERROR] Python3 not found. Please install python3.' >&2
        exit 1
    fi
    python_version="$(python3 --version 2>&1 | awk '{print $2}')"
    py_major=$(echo "$python_version" | cut -d'.' -f1)
    py_minor=$(echo "$python_version" | cut -d'.' -f2)
    if [ "$py_major" -eq "3" ] && [ "$py_minor" -gt "6" ] && [ "$py_minor" -lt "9" ]; then
        echo "[INSTALL] Found Python ${python_version}"
    else
        echo "[ERROR] Project dependencies require Python 3.7/3.8. You have Python version ${python_version} or python3 points to Python ${python_version}."
        exit 1
    fi
}

function check_pip {
    pip_version="$(python3 -m pip -V | awk '{print $2}')"
    if [ $? -eq 0 ]; then
        echo "[INSTALL] Found PIP version ${pip_version}"
        python3 -m pip install --no-cache-dir --upgrade pip --user
    else
        echo '[ERROR] PIP not found. Please install python3-pip.'
        exit 1
    fi
}

function install_requirements {
    echo '[INSTALL] Installing Requirements'
    pip3 install --no-cache-dir -r requirements.txt
}


install_python3
check_python3
check_pip
install_requirements
