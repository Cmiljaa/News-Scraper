from playwright.sync_api import sync_playwright

BASE_URL = "https://news.ycombinator.com/?p={}"

def fetch_five_pages():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        data = []

        for page_number in range(1, 6):
            url = BASE_URL.format(page_number)
            print(f"Opening: {url}")

            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")

            titles = page.locator("span.titleline > a")
            statistics = page.locator("tr.athing + tr > td.subtext > span.subline")
            count = titles.count()
            print(f"Page {page_number} has {count} posts")
            
            for i in range(count):
                print("-------------------------------------------------------------------")
                print(i + 1)
                print("-", titles.nth(i).inner_text())
                print("-", statistics.nth(i).inner_html())
                print("-", titles.nth(i).get_attribute('href'))
                
                
        browser.close()


if __name__ == "__main__":
    fetch_five_pages()