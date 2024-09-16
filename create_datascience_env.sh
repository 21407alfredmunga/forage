#!/bin/bash

# Name of the virtual environment
ENV_NAME="datascience_env"

# Python version
PYTHON_VERSION="python3"

# Check if venv module is available (it's included in Python 3.3+)
if ! $PYTHON_VERSION -c "import venv" &> /dev/null; then
    echo "Python venv module not found. Please ensure you have Python 3.3+ installed."
    exit 1
fi

# Create a virtual environment
echo "Creating virtual environment: $ENV_NAME"
$PYTHON_VERSION -m venv $ENV_NAME

# Activate the virtual environment
source $ENV_NAME/bin/activate

# Upgrade pip
pip install --upgrade pip

# List of common data science packages to install
PACKAGES=(
    numpy
    pandas
    scipy
    matplotlib
    seaborn
    scikit-learn
    jupyter
    jupyterlab
    statsmodels
    sympy
    tensorflow
    keras
    torch
    torchvision
    xgboost
    lightgbm
    catboost
    plotly
    bokeh
    streamlit
    pydot
)

# Install packages
echo "Installing data science packages..."
for package in "${PACKAGES[@]}"
do
    pip install $package
done

# Deactivate the virtual environment
deactivate

echo "Data science Python environment setup complete!"
echo "To activate the environment, use: source $ENV_NAME/bin/activate"
