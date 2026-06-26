from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.jianshu.com/sign_up', timeout=20000)
    page.wait_for_timeout(3000)
    print('Title:', page.title())
    
    result = page.evaluate("""() => {
        const inputs = document.querySelectorAll('input');
        return Array.from(inputs).map(i => ({
            id: i.id, name: i.name, type: i.type, placeholder: i.placeholder
        }));
    }""")
    for inp in result:
        if inp['type'] in ['email','password','text'] or inp['placeholder']:
            print(f"  {inp['id']:20s} type={inp['type']:10s} placeholder={inp['placeholder']}")
    
    buttons = page.evaluate("""() => {
        const btns = document.querySelectorAll('button');
        return Array.from(btns).slice(0, 5).map(b => b.innerText.trim().substring(0, 30));
    }""")
    for b in buttons:
        if b: print(f"  button: {b}")
    
    browser.close()