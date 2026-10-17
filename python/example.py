"""Export the videos of one or more Likee creators (views, likes, comments, shares, engagement) to CSV.

Usage: python example.py baby.miaa itz.danila --limit 30 [--popular] [--min-views 10000]
"""
import argparse
import csv
import os
import sys

from apify_client import ApifyClient

ACTOR = "lagenuina_agency/likee-scraper"
TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")

FIELDS = ["authorUsername", "publishedAt", "description", "views", "likes", "comments", "shares",
          "engagementRate", "hashtags", "musicTitle", "postUrl", "thumbnailUrl"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("profiles", nargs="+", help="Likee usernames or https://likee.video/@username links")
    p.add_argument("--limit", type=int, default=30, help="videos per profile")
    p.add_argument("--popular", action="store_true", help="most viewed recent videos instead of latest")
    p.add_argument("--min-views", type=int, default=0)
    a = p.parse_args()

    client = ApifyClient(TOKEN)
    run = client.actor(ACTOR).call(run_input={
        "profileUrls": [{"url": x if x.startswith("http") else f"https://likee.video/@{x.lstrip('@')}"} for x in a.profiles],
        "maxVideosPerProfile": a.limit,
        "profileVideoSorting": "popular" if a.popular else "latest",
        "minViews": a.min_views,
        "maxItems": a.limit * len(a.profiles) + len(a.profiles),
    })
    out = "likee_videos.csv"
    n = 0
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            if item.get("recordType") == "profile_summary":
                print(f"@{item['authorUsername']}: {item['followers']} followers, median views {item['medianViews']}, "
                      f"avg engagement {item['avgEngagementRate']}%")
                continue
            w.writerow({**item, "hashtags": " ".join(item.get("hashtags") or [])})
            n += 1
    print(f"{n} videos -> {out}")


if __name__ == "__main__":
    main()
