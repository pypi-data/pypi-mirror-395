from socket import timeout
from playwright.sync_api import sync_playwright
import tcsolver.silder as silder

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        args=["--disable-blink-features=AutomationControlled"],
        #proxy={"server": "http://36.110.143.55:8080"}
    )
    context = browser.new_context(ignore_https_errors=True)
    page = browser.new_page()
    response = page.goto("https://www.urbtix.hk/event-detail/14351/", timeout=30000)

    page.locator('div[title="Purchase Ticket"]').first.click()
    page.wait_for_timeout(2000)

    page.locator('div[aria-label="NON-MEMBER LOGIN"]').first.click()
    page.wait_for_timeout(2000)

    options = silder.SliderOptions(validateButtonSelector="div[aria-label='Login']")
    silder.solve_slider(page, options)

    page.wait_for_timeout(5000)

    print(response)
    page.wait_for_timeout(30000)
    browser.close()