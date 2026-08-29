# ZoomIt

For my pakhi.  A python script to download Zoom recordings without using a browser.

## How to use

- Install the required python packages
  - `python -m venv .venv --prompt ZoomIt
  - `source .venv/bin/activate`
  - `pip install -r requirements.txt`
- Populate the file `input.json` with your Zoom URLs, passcodes, and titles
- Run the script with `python zoomit.py`
- It should download the recordings (2 if two parts are available, 1 if not)
  - In the same folder
  - With the filename you set with the field `Title` in file `input.json`
