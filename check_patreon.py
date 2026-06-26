from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.patreon.com/register', timeout=20000)
    page.wait_for_timeout(3000)
    print('Title:', page.title())
    text = page.inner_text('body')[:1000]
    print(text)
    page.screenshot(path='E:\\kun\\patreon.png')
    browser.close()