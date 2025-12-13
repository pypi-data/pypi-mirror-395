from playwright.sync_api import sync_playwright

import tcsolver.silder as silder



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="chrome")
    page = browser.new_page()
    
    page.goto("https://cloud.tencent.com/product/captcha", wait_until="domcontentloaded", timeout=60000)

    options = silder.SliderOptions(validateButtonSelector="#captcha_click", iframeSelector="#tcaptcha_iframe_dy")
    silder.solve_slider(page, options)

    print(page.title())
    page.wait_for_timeout(3000)
    browser.close()
