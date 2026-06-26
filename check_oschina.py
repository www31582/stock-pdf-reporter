from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://www.oschina.net', timeout=20000)
    page.wait_for_timeout(2000)
    
    result = page.evaluate("""() => {
        const links = document.querySelectorAll('a');
        return Array.from(links).filter(l => l.innerText.trim()).map(l => ({
            text: l.innerText.trim().substring(0, 30),
            href: l.href.substring(0, 60)
        }));
    }""")
    for r in result:
        if any(x in r['text'] for x in ['登录','注册','Sign','Login','写博客','发布']):
            print(f"  {r['text']:30s} {r['href']}")
    
    browser.close()