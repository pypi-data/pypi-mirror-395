import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import time
from datetime import datetime

OKTA_APP_URL = "https://partnershealthcare.okta.com/app/partnershealthcare_ukgwdayprod_1/exkudz8l8l6XLkLBu297/sso/saml"
UKG_URL = "https://massgeneral-ukgssosso.prd.mykronos.com/wfd/home"
COOKIES_FILE = Path("okta_cookies.json")

def save_cookies(cookies):
    COOKIES_FILE.write_text(json.dumps(cookies, indent=2))

def load_cookies():
    if COOKIES_FILE.exists():
        return json.loads(COOKIES_FILE.read_text())
    return None

def _login():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("Opening Okta login page...")
        page.goto(OKTA_APP_URL)

        page.wait_for_load_state("networkidle")
        input("Press ENTER *after* you are logged in and pages have finished redirecting...")

        cookies = context.cookies()
        save_cookies(cookies)
        formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{formatted_datetime}    Cookies saved")

        browser.close()

def _signin():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()

        cookies = load_cookies()
        context.add_cookies(cookies)

        page = context.new_page()

        print(f"Navigating to: {UKG_URL}")
        page.goto(UKG_URL)
        page.wait_for_load_state("domcontentloaded")

        # Click "Sign In" button
        page.locator("[id=\"2\"]").click()

        # Did you do any work since you last signed out?
        iframe_element = page.locator("[id=\"angularIframeSlider\"]")
        frame = iframe_element.content_frame
        frame.locator("[id=\"workflowRadioGroup1_1\"]").check()
        frame.get_by_role("button", name="Submit answer").click()

        # html = page.content()
        # print(html[:2000])

        # wait for submission to go through
         # page.wait_for_load_state("load")
        time.sleep(5)
        formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{formatted_datetime}    Signed in")
        browser.close()

def _signout():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()

        cookies = load_cookies()
        context.add_cookies(cookies)

        page = context.new_page()

        print(f"Navigating to: {UKG_URL}")
        page.goto(UKG_URL)
        page.wait_for_load_state("domcontentloaded")

        # Click "Sign Out" button
        page.locator("[id=\"52\"]").click()

        iframe_element = page.locator("[id=\"angularIframeSlider\"]")
        frame = iframe_element.content_frame

        # Did you have at least a 30 minute lunch break?
        frame.locator("[id=\"workflowRadioGroup1_0\"]").check()
        frame.get_by_role("button", name="Submit answer").click()
        time.sleep(5)

        iframe_element = page.locator("[id=\"angularIframeSlider\"]")
        frame = iframe_element.content_frame
        
        # Are the sign-in and sign-out times you submitted accurate?
        frame.locator("[id=\"workflowRadioGroup1_0\"]").check()
        frame.get_by_role("button", name="Submit answer").click()

        # wait for submission to go through
         # page.wait_for_load_state("load")
        time.sleep(5)
        formatted_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{formatted_datetime}    Signed out")
        browser.close()