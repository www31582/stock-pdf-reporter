from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://juejin.cn/register', timeout=20000)
    page.wait_for_timeout(3000)
    
    result = page.evaluate("""() => {
        const links = document.querySelectorAll('a, button, span, div[class*=btn], div[class*=button]');
        return Array.from(links).filter(el => el.innerText && el.innerText.trim()).map(el => ({
            text: el.innerText.trim().substring(0, 40),
            tag: el.tagName,
            href: el.href || el.getAttribute('data-href') || ''
        }));
    }""")
    
    for r in result:
        txt = r['text']
        if any(x in txt for x in ['GitHub','Google','微信','手机','邮箱','登录','注册','Sign','授权']):
            print(f"{r['tag']}: {txt[:30]} | {r['href'][:60]}")
    
    browser.close()