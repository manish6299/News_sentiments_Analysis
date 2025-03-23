import os
import pandas as pd
from bs4 import BeautifulSoup
from newspaper import Article
import requests
from categorize_text import classify_text_domain
from time import sleep


# Dictionary to track visited links
visited_links = {}


def get_article_metadata(url, company_name):
    """Fetches metadata from a given article URL."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        # Filter by company name
        if company_name.lower() not in article.text.lower():
            return None  # Skip articles that do not mention the company

        return {
            "title": article.title,
            "summary": article.summary,
            "url": url,
            "publish_date": article.publish_date,
            "domain": classify_text_domain(article.text)
        }

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None


def extract_news(company_name, max_articles=10):
    """Extracts news articles for the given company."""
    
    all_links = [
        f"https://timesofindia.indiatimes.com/topic/{company_name}/news",
        f"https://economictimes.indiatimes.com/topic/{company_name}",
        f"https://www.hindustantimes.com/search?q={company_name}"
    ]

    articles = []
    
    for base_url in all_links:
        try:
            response = requests.get(base_url, timeout=10)
            if response.status_code != 200:
                print(f"Failed to access {base_url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract article links
            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']
                full_link = link if link.startswith("http") else f"{base_url}{link}"

                # Filter for valid TOI, ET, and HT articles
                if ("timesofindia.indiatimes.com" in full_link and "articleshow" in full_link) or \
                   ("economictimes.indiatimes.com" in full_link) or \
                   ("hindustantimes.com" in full_link):
                    
                    if full_link not in visited_links:
                        sleep(1)  # Add delay to prevent rate limiting
                        article_data = get_article_metadata(full_link, company_name)
                        
                        if article_data:
                            visited_links[full_link] = article_data["domain"]
                            articles.append(article_data)
                        
                        if len(articles) >= max_articles:
                            break
        except Exception as e:
            print(f"Error scraping {base_url}: {e}")
            continue

    # Store results in a DataFrame
    df = pd.DataFrame(articles)
    
    if df.empty:
        print(f"No relevant articles found for {company_name}.")
    else:
        print(f"\nExtracted {len(articles)} articles for {company_name}")
        print(df)

    return df


# ✅ List of 10 Companies to Extract News For
companies = [
    "Reliance", "Tata", "Infosys", "Wipro", "HDFC", 
    "ICICI", "L&T", "Adani", "Bharti Airtel", "Bajaj"
]

# ✅ Loop through each company and extract articles
output_dir = "company_news"
os.makedirs(output_dir, exist_ok=True)

for company in companies:
    print(f"\n🔍 Extracting news for {company}...")
    
    result_df = extract_news(company, max_articles=10)

    # Save results to CSV
    if not result_df.empty:
        csv_filename = os.path.join(output_dir, f"{company}_news.csv")
        result_df.to_csv(csv_filename, index=False)
        print(f"✅ Saved {company} news articles to {csv_filename}")
    else:
        print(f"⚠️ No articles found for {company}")

print("\n🎯 Extraction completed for all companies!")
