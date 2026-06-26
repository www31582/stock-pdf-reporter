from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Go directly to gumroad.com signup
    page.goto('https://gumroad.com/signup', timeout=20000)
    page.wait_for_timeout(2000)
    
    print('URL:', page.url)
    
    # Fill in form
    inputs = page.query_selector_all('input')
    for inp in inputs:
        name = inp.get_attribute('name') or ''
        ph = inp.get_attribute('placeholder') or ''
        itype = inp.get_attribute('type') or ''
        print(f'  name={name:20s} type={itype:10s} placeholder={ph}')
        if ph == 'Email':
            inp.fill('aiquanttools@proton.me')
        elif ph == 'Password':
            inp.fill('TradingPDF2024!')
    
    # Click submit
    page.click('button:has-text("Create account")')
    page.wait_for_timeout(5000)
    
    print('URL after:', page.url)
    print('Title:', page.title())
    
    text = page.inner_text('body')[:1000]
    print('Body:', text)
    
    page.screenshot(path='E:\\kun\\gumroad_result2.png')
    
    time.sleep(2)
    browser.close()