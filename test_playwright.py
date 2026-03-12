from playwright.sync_api import sync_playwright

def test_google_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()

        page.goto("https://google.com")
        title = page.title()
        print(f"Page title: {title}")

        assert "Google" in title
        browser.close()

test_google_loads()