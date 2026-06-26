from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://gumroad.com/signup', timeout=20000)
    page.wait_for_timeout(3000)
    
    result = page.evaluate("""() => {
        const inputs = Array.from(document.querySelectorAll('input'));
        const forms = Array.from(document.querySelectorAll('form'));
        return {
            inputCount: inputs.length,
            inputs: inputs.map(i => ({
                id: i.id, name: i.name, type: i.type, placeholder: i.placeholder,
                className: i.className, autocomplete: i.autocomplete, required: i.required,
                outerHTML: i.outerHTML.substring(0, 120)
            })),
            formCount: forms.length,
            forms: forms.map(f => ({id: f.id, action: f.action, method: f.method}))
        };
    }""")
    
    for inp in result['inputs']:
        if inp['type'] in ['email', 'password', 'text'] or inp['placeholder']:
            print(f"  id={inp['id']:20s} type={inp['type']:10s} placeholder={inp['placeholder']:10s} cls={inp['className'][:30]}")
    
    for f in result['forms']:
        print(f"  FORM: id={f['id']:15s} action={f['action'][:80]}")
    
    browser.close()