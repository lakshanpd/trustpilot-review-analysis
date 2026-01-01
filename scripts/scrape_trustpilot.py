import requests
from bs4 import BeautifulSoup
import csv
import os
from dotenv import load_dotenv

load_dotenv()

TRUSTPILOT_URL = os.getenv("TRUSTPILOT_URL")

def scrape_url(url):
    res = requests.get(url)
    if (res.status_code != 200):
        return None
    return res.content

def extract_reviews_from_page(url):
    content = scrape_url(url)
    
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

def scrape_reviews_across_pages(base_url, max_pages=50):
    all_reviews = []
    page = 1

    while page <= max_pages:
        url = f"{base_url}?page={page}" if page > 1 else base_url

        reviews = extract_reviews_from_page(url)

        if not reviews:
            break

        all_reviews.extend(reviews)
        page += 1

    return all_reviews

def save_reviews_to_csv(
    reviews,
    filename,
    base_dir="data/trustpilot"
):
    if not reviews:
        print("No reviews to save.")
        return

    os.makedirs(base_dir, exist_ok=True)
    filepath = os.path.join(base_dir, filename)

    fieldnames = ["reviewer", "date", "text", "stars"]

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reviews)

    print(f"Saved {len(reviews)} reviews to {filepath}")


if __name__ == "__main__":
    reviews = scrape_reviews_across_pages(TRUSTPILOT_URL)
    save_reviews_to_csv(reviews=reviews, filename="task_rabbit.csv")
