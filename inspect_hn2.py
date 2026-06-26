from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://news.ycombinator.com/submit', timeout=20000)
    page.wait_for_timeout(1000)
    
    inputs = page.query_selector_all('input')
    print(f"Found {len(inputs)} inputs")
    for i, inp in enumerate(inputs):
        name = inp.get_attribute('name') or '-'
        val = inp.get_attribute('value') or '-'
        itype = inp.get_attribute('type') or '-'
        print(f"  [{i}] name={name} type={itype} value={val}")
    
    browser.close()