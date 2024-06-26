# My Project

This project uses a virtual environment to manage dependencies and includes a
Streamlit app. Follow the instructions below to set up and run the project.

## Prerequisites

- Python 3.11
- `virtualenv` package

## Installing Python 3.11

### Windows

1. Download the Python 3.11 installer from the from Python official website.
2. Run the installer and follow the prompts.
3. Make sure to check the box that says "Add Python to PATH" during
   installation.

### macOS

1. Download the Python 3.11 installer from Python official website.
2. Open the downloaded package and follow the installation steps.
3. Alternatively, you can use Homebrew:
   ```sh
   brew install python@3.11
   ```

### Linux

1. Update your package list:
   ```sh
   sudo apt update
   ```
2. Install Python 3.11 (the exact command may vary depending on your Linux
   distribution):
   ```sh
   sudo apt install -y python3.11
   ```

## Installing `virtualenv`

`virtualenv` is a tool to create isolated Python environments. Here's how to
install it:

```sh
pip install virtualenv
```

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```sh
git clone https://github.com/dllchun/i2_csv_to_word.git
cd your-repo-name
```

### 2. Create and Activate the Virtual Environment

#### On Windows:

```sh
# Create a virtual environment with Python 3.11
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

#### On macOS/Linux:

```sh
# Create a virtual environment with Python 3.11
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

With the virtual environment activated, install the required dependencies:

```sh
pip install -r requirements.txt

pip freeze > requirements.txt
```

### 4. Run the Streamlit App

To start the Streamlit app, run the following command:

```sh
streamlit run app.py
```

## Additional Information

- To deactivate the virtual environment, simply run:

  ```sh
  deactivate
  ```

- If you encounter any issues, make sure you have activated the virtual
  environment and installed all dependencies correctly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.
