from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://app.gumroad.com/signup', timeout=20000)
    page.wait_for_timeout(2000)
    
    # Fill email and password
    page.fill('[id=":r0:-email"]', 'aiquanttools@proton.me')
    page.fill('[id=":r0:-password"]', 'TradingPDF2024!')
    
    # Click create account
    page.click('button:has-text("Create account")')
    
    page.wait_for_timeout(5000)
    
    print('URL after submit:', page.url)
    print('Title:', page.title())
    
    # Check if we got in
    content = page.inner_text('body')[:1000]
    print('Body:', content)
    
    page.screenshot(path='E:\\kun\\gumroad_result.png')
    
    time.sleep(3)
    browser.close()