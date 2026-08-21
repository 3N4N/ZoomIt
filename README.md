# ZoomIt

A python script to download Zoom recordings without using a browser.

## How to use

- Install the required python packages
  - `python -m venv .venv --prompt ZoomIt
  - `source .venv/bin/activate`
  - `pip install -r requirements.txt`
- Open the script and change the constants `ZOOM_URL`, `PASSWORD`, and `OUTPUT`
- Run the script with `python zoomit.py`
- It should download the recordings (2 if two parts are available, 1 if not)
  - In the same folder
  - With the filename you set with `OUTPUT`
