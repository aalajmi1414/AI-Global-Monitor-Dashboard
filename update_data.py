import json
import datetime
import requests
import hashlib

# 1. FETCHING LOGIC: Source specific functions
def fetch_eu_updates():
    """
    Example: Hitting the EUR-Lex API or an RSS feed for EU AI Act updates.
    (This uses simulated data for the prototype, but shows where the requests.get() goes)
    """
    # response = requests.get("https://eur-lex.europa.eu/api/...")
    # raw_data = response.json()
    
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Simulating a parsed response from the EU
    return [{
        "countryEn": "European Union", "countryAr": "الاتحاد الأوروبي", "flag": "🇪🇺",
        "layer": 1, "typeEn": "Amendment", "typeAr": "تعديل",
        "statusEn": "In Force", "statusAr": "ساري",
        "titleEn": "AI Act Technical Standards", "titleAr": "المعايير الفنية لقانون الذكاء الاصطناعي",
        "date": current_date,
        "summaryEn": "New technical standards published for high-risk AI systems.",
        "summaryAr": "نشر معايير فنية جديدة لأنظمة الذكاء الاصطناعي عالية المخاطر.",
        "source": "EUR-Lex", "sourceType": "official",
        "url": "https://eur-lex.europa.eu/", "recent": True
    }]

def fetch_mena_region_updates():
    """
    Example: Monitoring regional bodies like SDAIA (Saudi Arabia) or UAE Gov.
    You could use web scraping (BeautifulSoup) here if they don't have an API.
    """
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Simulating a pipeline update caught from a regional news source
    return [{
        "countryEn": "Saudi Arabia", "countryAr": "السعودية", "flag": "🇸🇦",
        "layer": 2, "typeEn": "Draft Guidelines", "typeAr": "مسودة مبادئ توجيهية",
        "statusEn": "Under Consultation", "statusAr": "قيد الاستشارة",
        "titleEn": "AI in Corporate Governance Framework", "titleAr": "إطار عمل الذكاء الاصطناعي في حوكمة الشركات",
        "date": current_date,
        "summaryEn": "Proposed guidelines for integrating AI into corporate governance and real estate development.",
        "summaryAr": "مبادئ توجيهية مقترحة لدمج الذكاء الاصطناعي في حوكمة الشركات والتطوير العقاري.",
        "source": "Regional Legal Tech News", "sourceType": "news",
        "url": "https://sdaia.gov.sa/", "recent": True
    }]

# 2. UTILITY: Create a unique ID to prevent duplicate entries
def generate_id(entry):
    """Creates a unique hash based on the country, title, and date."""
    unique_string = f"{entry['countryEn']}-{entry['titleEn']}-{entry['date']}"
    return int(hashlib.md5(unique_string.encode()).hexdigest()[:8], 16)

# 3. MAIN PIPELINE: Execute fetches, merge, and save
def main():
    db_filepath = 'data.json'
    
    # Load existing dashboard data
    try:
        with open(db_filepath, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    # Gather new updates from all your sources
    new_updates = []
    new_updates.extend(fetch_eu_updates())
    new_updates.extend(fetch_mena_region_updates())
    
    # Process and deduplicate
    existing_ids = {item.get('id') for item in existing_data if item.get('id')}
    added_count = 0
    
    for item in new_updates:
        item_id = generate_id(item)
        
        # If we haven't seen this exact update before, add it
        if item_id not in existing_ids:
            item['id'] = item_id
            # Insert at the beginning of the list so it shows up first
            existing_data.insert(0, item) 
            existing_ids.add(item_id)
            added_count += 1
            
    # Optional: Reset the "recent" flag for items older than 7 days
    today = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
    for item in existing_data:
        try:
            item_date = datetime.datetime.strptime(item['date'], "%Y-%m-%d")
            if (today - item_date).days > 7:
                item['recent'] = False
        except ValueError:
            pass # Skip if date format is weird

    # Save the updated database back to the file
    with open(db_filepath, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
        
    print(f"Pipeline executed successfully. Added {added_count} new entries.")

if __name__ == "__main__":
    main()