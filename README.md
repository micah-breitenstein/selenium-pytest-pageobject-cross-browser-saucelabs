# 🧪 Selenium + Pytest + Sauce Labs  
## Page Object Model Cross-Browser Test Framework

This project demonstrates a **Python Selenium test automation framework** built with:

- 🐍 Python
- 🧪 Pytest
- 🌐 Selenium WebDriver
- 🏗 Page Object Model (POM)
- ☁️ Sauce Labs (Cloud Cross-Browser Testing)

It supports:

- Local browser execution (Safari, Chrome)
- Headless execution
- Testing against:
  - Local app (`http://127.0.0.1:9292`)
  - Hosted app (`https://the-internet.herokuapp.com`)
- Remote cross-browser execution via Sauce Labs (Windows + macOS)

---

# Selenium + Pytest + Sauce Labs
## Page Object Model Cross-Browser Test Framework

This project demonstrates a Python Selenium automation framework using:

- Python
- Pytest
- Selenium WebDriver
- Page Object Model (POM)
- Sauce Labs for cross-browser cloud testing

It supports:

- Local browser testing
- Headless execution
- Local app testing (`127.0.0.1`)
- Hosted app testing (`the-internet.herokuapp.com`)
- Remote cross-browser testing on Sauce Labs

---

# Local browser testing local app hosted on 127 
### Bring up project https://github.com/saucelabs/the-internet.git

Target:
http://127.0.0.1:9292

## Safari
python -m pytest -q -s --base-url=http://127.0.0.1:9292

## Chrome
python -m pytest -q -s --browser=chrome --base-url=http://127.0.0.1:9292

## Chrome headless
python -m pytest -q --browser=chrome --headless --base-url=http://127.0.0.1:9292

---

# Local browser testing https://the-internet.herokuapp.com

## Safari
python -m pytest -q -s

## Chrome
python -m pytest -q -s --browser=chrome

## Chrome headless
python -m pytest -q --browser=chrome --headless

---

# Remote browser hosted on Sauce Labs testing https://the-internet.herokuapp.com/slow

Before running remote tests, export your Sauce Labs credentials:

export SAUCE_USERNAME=your-username  
export SAUCE_ACCESS_KEY=your-access-key  

---

## Edge on Windows 11

python -m pytest -q \
  --remote \
  --browser=edge \
  --platform="Windows 11" \
  --browser-version=latest \
  --sauce-region=us-west-1 \
  --base-url=https://the-internet.herokuapp.com

---

## Chrome on macOS 13

python -m pytest -q \
  --remote \
  --browser=chrome \
  --platform="macOS 13" \
  --browser-version=latest \
  --sauce-region=us-west-1 \
  --base-url=https://the-internet.herokuapp.com

---

# Project Structure

pages/  
  core/  
    base_page.py  
  landing_page.py  
  login_page.py  
  dropdown_page.py  
  checkboxes_page.py  
  dynamic_loading_page.py  

tests/  
  test_login_flow.py  
  test_dropdown.py  
  test_checkboxes.py  
  test_dynamic_loading.py  

conftest.py  

---

# Framework Highlights

- Page Object Model architecture
- CLI-driven configuration
- Local and Remote driver switching
- Cross-browser execution (Safari, Chrome, Edge)
- Cross-platform execution (macOS, Windows)
- Screenshot capture on failure
- Sauce Labs W3C capability configuration

---

Author: Micah Breitenstein
