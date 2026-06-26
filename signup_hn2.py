from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://news.ycombinator.com/submit', timeout=20000)
    page.wait_for_timeout(1000)
    
    # The second form is for creating account
    # Fill the create account fields (second set)
    inputs = page.query_selector_all('input')
    # Create account inputs are index 3 (acct) and 4 (pw)
    inputs[3].fill('stockreporter')
    inputs[4].fill('HNReporter2024!')
    # Click create account submit (index 5)
    inputs[5].click()
    
    page.wait_for_timeout(5000)
    print('URL:', page.url)
    text = page.inner_text('body')[:1000]
    print(text)
    page.screenshot(path='E:\\kun\\hn_result.png')
    browser.close()