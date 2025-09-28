# import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # Step 1. Create a browser
    # Can use chromium/firefox/webkit
    browser = p.chromium.launch(headless=False)

# Step 2. Create a new BrowserContext (optional)
    context = browser.new_context()

# Step 3. Open a page
    page = context.new_page()
    # time.sleep(5)
    page.goto("https://reddit.com")
    # print(page.title())  # Returns the page's title.
    page.wait_for_selector("main")  # Wait until <main> appears
    for anchor in page.query_selector_all("a"):
        print(anchor.inner_html())
    for anchor in page.query_selector_all("main"):
        print(anchor.inner_text())

    for anchor in page.query_selector_all("a"):
        print(anchor.get_attribute("href"))
    browser.close()
    # print(article.inner_text())

    for elem in page.query_selector_all("article"):  # Return all <article>
        print(elem.inner_text())
