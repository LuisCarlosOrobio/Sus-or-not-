# Sus or not?
This hacky app lets users search Twitter for suspicious content linked to a specific name. 

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3
- Firefox
- Geckodriver

### Installing Dependencies on macOS/Linux/Windows

You can install the required dependencies using the following methods:

1. **Python and Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. **Install Python Packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Install Firefox:**
    - Download and install Firefox from [here](https://www.mozilla.org/en-US/firefox/new/).

4. **Install Geckodriver:**
    - Download the appropriate version of Geckodriver from the [Geckodriver releases page](https://github.com/mozilla/geckodriver/releases).
    - On macOS/Linux:
      ```bash
      sudo mv geckodriver /usr/local/bin/
      ```
    - On Windows:
      - Move the `geckodriver.exe` to a directory of your choice and add that directory to your `PATH` environment variable.

### Setting Up the Environment

1. Clone the Repository
   ```bash
   git clone https://github.com/LuisCarlosOrobio/Sus-or-not-.git
   cd Sus-or-not
