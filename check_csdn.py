from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://passport.csdn.net/register', timeout=20000)
    page.wait_for_timeout(2000)
    print('Title:', page.title())
    print('URL:', page.url)
    text = page.inner_text('body')[:1500]
    print(text)
    browser.close()