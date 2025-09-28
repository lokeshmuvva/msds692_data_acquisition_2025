import time
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    # Launching a Browser
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://reddit.com")

    # Click the login button and enter id and password.
    page.locator("#login-button").click()
    page.locator("#login-username").click()
    page.keyboard.type("email@gmail.com")
    page.keyboard.press("Tab")
    page.keyboard.type("password")

    time.sleep(10)
    browser.close()
