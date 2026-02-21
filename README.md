# Local browser testing local app hosted on 127
## Safari
python -m pytest -q -s --base-url=http://127.0.0.1:9292
## Chrome
python -m pytest -q -s --browser=chrome --base-url=http://127.0.0.1:9292
## Chrome headless
python -m pytest -q -s --browser=chrome --headless --base-url=http://127.0.0.1:9292

# Local browser testing https://the-internet.herokuapp.com
python -m pytest -q -s  --base-url=https://the-internet.herokuapp.com
python -m pytest -q -s --browser=chrome  --base-url=https://the-internet.herokuapp.com
python -m pytest -q --browser=chrome --headless  --base-url=https://the-internet.herokuapp.com

# Remote browser hosted on Sauce Labs testing https://the-internet.herokuapp.com/slow
## Edge on Windows 11
python -m pytest -q \
  --remote \
  --browser=edge \
  --platform="Windows 11" \
  --browser-version=latest \
  --sauce-region=us-west-1 \
  --base-url=https://the-internet.herokuapp.com
  
## Chrome on macOS 13
  python -m pytest -q \
  --remote \
  --browser=chrome \
  --platform="macOS 13" \  
  --browser-version=latest \
  --sauce-region=us-west-1 \
  --base-url=https://the-internet.herokuapp.com