import feedparser
import time
import re

# Configuration
RSS_FEED_URL = 'https://www.upwork.com/ab/feed/jobs/rss?paging=NaN-undefined&q=(website%20AND%20title%3AWebsite)%20OR%20(Html%20AND%20title%3AHtml)%20OR%20(HTML%20AND%20title%3AHTML)%20OR%20(React%20AND%20title%3AReact)%20OR%20(Front%20End%20AND%20title%3AFront%20End)%20OR%20(Css%20AND%20title%3ACss)%20OR%20(CSS%20AND%20title%3ACSS)%20OR%20(Data%20Entry%20AND%20title%3AData%20Entry)%20OR%20(Python%20AND%20title%3APython)%20OR%20(Web%20Developer%20AND%20title%3AWeb%20Developer)%20OR%20(Developer%20AND%20title%3ADeveloper)%20OR%20(Website%20Design%20AND%20title%3AWebsite%20Design)%20OR%20(Web%20Design%20AND%20title%3AWeb%20Design)&sort=recency&api_params=1&securityToken=ba1ad280580d59ffe1bad05c806148039d2b9e8bba06c2cf9e75a2ff68760387af7f9d0464833ab7dd83e29e03f23c33400ba53ac7f77fa6abca4ab47b8da24f&userUid=1657056936382869504&orgUid=1657056936382869505'
CHECK_INTERVAL = 10  # Interval between checks in seconds

# Store the last seen entry's ID
last_entry_id = None

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace('&nbsp;', ' ').replace('&#039;', "'")
    cleantext = re.sub(r'\s*\n\s*', '\n', cleantext).strip()  # Remove extra newlines and spaces
    return cleantext

def display_latest_entry(entry):
    title = entry.title
    description = clean_html(entry.description.replace("<br />", "\n").replace("<br>", "\n"))

    hourly_range = re.search(r'<b>Hourly Range</b>:\s*([\d\.\$-]+)', entry.description)
    hourly_range = hourly_range.group(1) if hourly_range else 'Not specified'

    budget_match = re.search(r'<b>Budget</b>:\s*\$([\d\.]+)', entry.description)
    budget = f"${budget_match.group(1)}" if budget_match else "Not specified"

    country = re.search(r'<b>Country</b>:\s*([\w\s]+)', entry.description)
    country = country.group(1) if country else 'Not specified'

    link = entry.link

    print(f"Title: {title}\n")
    print(f"Description: {description}\n")
    if budget != "Not specified":
        print(f"Budget: {budget}\n")
    else:
        print(f"Hourly Range: {hourly_range}\n")
    print(f"Country: {country}\n")
    print(f"Link: {link}\n")
    print("﹌" * 80 + "\n")

def check_rss_feed():
    global last_entry_id
    feed = feedparser.parse(RSS_FEED_URL)
    if feed.entries:
        latest_entry = feed.entries[0]
        if latest_entry.id != last_entry_id:
            last_entry_id = latest_entry.id
            display_latest_entry(latest_entry)
        else:
            print("No new posts.")
    else:
        print("Failed to fetch RSS feed.")

# Continuous check
print("Starting RSS feed monitor...")
while True:
    check_rss_feed()
    time.sleep(CHECK_INTERVAL)
