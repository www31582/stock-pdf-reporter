from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://news.ycombinator.com/submit', timeout=20000)
    page.wait_for_timeout(2000)
    
    # Fill create account
    inputs = page.query_selector_all('input')
    for inp in inputs:
        name = inp.get_attribute('name') or ''
        if name == 'acct':
            inp.fill('stockreporter')
        elif name == 'pw':
            inp.fill('HNReporter2024!')
    
    page.query_selector('input[value="Create Account"]').click()
    page.wait_for_timeout(5000)
    
    print('URL:', page.url)
    text = page.inner_text('body')[:1000]
    print(text)
    page.screenshot(path='E:\\kun\\hn_result.png')
    browser.close()