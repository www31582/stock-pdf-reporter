from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.patreon.com/register', timeout=20000)
    page.wait_for_timeout(3000)
    
    # Check for signup form
    inputs = page.evaluate("""() => {
        const inputs = document.querySelectorAll('input');
        return Array.from(inputs).map(i => ({
            name: i.name,
            type: i.type,
            placeholder: i.placeholder,
            id: i.id,
            autocomplete: i.autocomplete,
            outerHTML: i.outerHTML.substring(0, 100)
        }));
    }""")
    
    inps_to_show = [i for i in inputs if i['type'] in ['email','password','text'] and (i['name'] or i['placeholder'])]
    if not inps_to_show:
        # Show all inputs
        inps_to_show = inputs[:10]
    for i in inps_to_show:
        print(f"  type={i['type']:10s} name={i.get('name',''):15s} placeholder={i.get('placeholder',''):15s} id={i.get('id',''):20s}")
    
    # Check buttons
    buttons = page.evaluate("""() => {
        const btns = document.querySelectorAll('button, a[class*=btn], a[href*=signup]');
        return Array.from(btns).slice(0,10).map(b => ({
            text: b.innerText.substring(0, 40),
            href: b.href ? b.href.substring(0, 80) : '',
            tag: b.tagName
        }));
    }""")
    for b in buttons:
        if b['text']:
            print(f"  btn: {b['text'][:30]:30s} {b['href'][:50]}")
    
    browser.close()