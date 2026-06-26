from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://news.ycombinator.com/submit', timeout=20000)
    page.wait_for_timeout(2000)
    
    # The "Create Account" is a separate form below
    # Let me check the page structure
    result = page.evaluate("""() => {
        const forms = document.querySelectorAll('form');
        return Array.from(forms).map(f => {
            const inputs = Array.from(f.querySelectorAll('input'));
            return {
                action: f.action,
                inputs: inputs.map(i => ({name: i.name, value: i.value, type: i.type}))
            };
        });
    }""")
    for f in result:
        print('Form:', f['action'])
        for inp in f['inputs']:
            print(f'  {inp["name"]:10s} {inp["type"]:10s} {inp["value"]}')
    
    browser.close()