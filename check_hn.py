from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://news.ycombinator.com/submit', timeout=20000)
    page.wait_for_timeout(2000)
    print('Title:', page.title())
    text = page.inner_text('body')[:1000]
    print(text)
    browser.close()