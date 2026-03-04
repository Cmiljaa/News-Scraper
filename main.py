from playwright.sync_api import sync_playwright
import pandas
from dataclasses import dataclass
import config

@dataclass
class Post:
    title: str
    href: str
    score: int
    age: int
    comments: int
    engagement: float

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
            
            count = min(titles.count(), statistics.count())
            
            for i in range(count):
                stat = statistics.nth(i)

                score_locator = stat.locator(".score")
                score = score_locator.inner_text() if score_locator.count() > 0 else "0 points"

                age = stat.locator(".age a").inner_text()

                comments = stat.locator("a").last.inner_text()
                print("-------------------------------------------------------------------")
                print(i + 1)
                print("-", titles.nth(i).inner_text())
                print("-", statistics.nth(i).inner_html())
                print("-", titles.nth(i).get_attribute('href'))
                
                nu_comments = extract_number(comments)
                nu_score = extract_number(score)
                engagement = nu_comments / nu_score if nu_score else 0
                
                post = Post(
					title=titles.nth(i).inner_text(),
					href=titles.nth(i).get_attribute('href') or "",
					score=nu_score,
					age=extract_number(age),
					comments=nu_comments,
					engagement=engagement
				)
                print_data(post)

                data.append(post)        
        print(data)
        browser.close()
        df = pandas.DataFrame(data)
        df_sorted = df.sort_values(by='engagement')
        df_sorted.to_csv("hackernews.csv", index=False)

def print_data(data_object: Post):
    print("-" * 50)
    print(f"Title: {data_object.title}")
    print(f"Link: {data_object.href}")
    print(f"Score: {data_object.score}")
    print(f"Age: {data_object.age}")
    print(f"Comments: {data_object.comments}")
    print(f"Score: {data_object.score}")
    print(f"Engagement: {data_object.engagement}")

def extract_number(text: str) -> int:
    try:
        return int(text.split()[0])
    except (ValueError, IndexError, AttributeError):
        return 0

if __name__ == "__main__":
    fetch_five_pages()