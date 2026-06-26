from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://news.ycombinator.com/submit', timeout=20000)
    page.wait_for_timeout(1000)
    
    inputs = page.query_selector_all('input')
    
    # Fill create account fields
    inputs[4].fill('stockreporter')
    inputs[5].fill('HNReporter2024!')
    inputs[6].click()
    
    page.wait_for_timeout(5000)
    print('URL:', page.url)
    text = page.inner_text('body')[:1000]
    print(text)
    page.screenshot(path='E:\\kun\\hn_after_signup.png')
    browser.close()