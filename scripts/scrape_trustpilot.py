import requests
from bs4 import BeautifulSoup

def scrape_url(url):
    res = requests.get(url)
    if (res.status_code != 200):
        return None
    return res.content

def filter_reviews(content):
    soup = BeautifulSoup(content, "html.parser")
    cards = soup.select("div[data-testid='service-review-card-v2']")
    results = []

    for card in cards:
        # Reviewer name
        name_el = card.select_one("[data-consumer-name-typography]")
        reviewer = name_el.get_text(strip=True) if name_el else None

        # Review date (ISO datetime)
        date_el = card.select_one("time[data-service-review-date-time-ago]")
        review_date = date_el["datetime"] if date_el and date_el.has_attr("datetime") else None

        # Review text (may be missing on some cards)
        text_el = card.select_one("p[data-service-review-text-typography]")
        review_text = text_el.get_text(strip=True) if text_el else None

        # Stars / rating
        rating_el = card.select_one("[data-service-review-rating]")
        stars = int(rating_el["data-service-review-rating"]) if rating_el and rating_el.has_attr("data-service-review-rating") else None

        results.append({
            "reviewer": reviewer,
            "date": review_date,
            "text": review_text,
            "stars": stars,
        })

    return results

if __name__ == "__main__":
    content = scrape_url("https://www.trustpilot.com/review/taskrabbit.it?page=10")
    res = filter_reviews(content)
    print(len(res))
