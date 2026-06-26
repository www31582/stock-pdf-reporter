from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    page.goto('https://gumroad.com/signup', timeout=20000)
    page.wait_for_timeout(2000)
    
    # Try using the exact selectors
    page.evaluate("""() => {
        const emailInput = document.querySelector(\'input[id$="-email"]\');
        const passInput = document.querySelector(\'input[id$="-password"]\');
        if (emailInput) {
            emailInput.value = "aiquanttools@proton.me";
            emailInput.dispatchEvent(new Event("input", {bubbles: true}));
            emailInput.dispatchEvent(new Event("change", {bubbles: true}));
        }
        if (passInput) {
            passInput.value = "TradingPDF2024!";
            passInput.dispatchEvent(new Event("input", {bubbles: true}));
            passInput.dispatchEvent(new Event("change", {bubbles: true}));
        }
        return {email: !!emailInput, pass: !!passInput};
    }""")
    
    page.wait_for_timeout(1000)
    
    # Click the Create account button
    buttons = page.query_selector_all('button')
    for b in buttons:
        txt = b.inner_text()
        if 'Create' in txt or 'create' in txt:
            print(f'Clicking: {txt}')
            b.click()
            break
    
    page.wait_for_timeout(5000)
    print('URL:', page.url)
    print('Title:', page.title())
    
    text = page.inner_text('body')[:1000]
    print('Body:', text[:500])
    
    page.screenshot(path='E:\\kun\\gumroad_result3.png')
    
    time.sleep(3)
    browser.close()