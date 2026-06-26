from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://app.gumroad.com/signup', timeout=20000)
    page.wait_for_timeout(3000)
    print(page.title())
    
    result = page.evaluate("""() => {
        const inputs = document.querySelectorAll('input');
        return Array.from(inputs).map(i => ({
            name: i.name, type: i.type, placeholder: i.placeholder, id: i.id, autocomplete: i.autocomplete
        }));
    }""")
    for r in result:
        print(f"  {r['id']:20s} {r['name']:15s} {r['type']:10s} {r['placeholder']}")
    
    buttons = page.evaluate("""() => {
        const btns = document.querySelectorAll('button');
        return Array.from(btns).map(b => ({text: b.innerText.substring(0, 40), type: b.type}));
    }""")
    for b in buttons:
        print(f"  button: {b['text']}")
    
    browser.close()