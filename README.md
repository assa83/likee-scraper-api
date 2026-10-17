# Likee Scraper API – working example (Python, JS, n8n)

Export **Likee** videos and creator stats – views, likes, comments, shares, engagement rate, caption, hashtags, music, direct `.mp4` for share links, followers, total likes, median views and posts per week – to CSV or JSON. Works with video share links (`likee.video/v/…`), profiles (`likee.video/@username`) and single posts (`username/postId`).

Powered by the [likee-scraper](https://apify.com/lagenuina_agency/likee-scraper) actor on Apify. No browser, no Likee account, no login, no API key from Likee.

## Example output (real result, shortened)

```json
{
  "recordType": "video",
  "postId": "7697594831836915986",
  "postUrl": "https://likee.video/@baby.miaa/video/7697594831836915986",
  "authorUsername": "baby.miaa",
  "authorFollowers": 1492827,
  "description": "На очередном квесте 😜",
  "views": 9741,
  "likes": 2017,
  "comments": 137,
  "shares": 11,
  "engagementRate": 22.23,
  "publishedAt": "2026-10-17T11:19:19.000Z"
}
```

Each profile also returns one `profile_summary` row: followers, following, total likes, verified badge, posts per week, average and median views, average engagement rate and best video.

## Quickstart (3 steps)

1. Create a free Apify account and copy your API token from [Settings → Integrations](https://console.apify.com/settings/integrations).
2. Put it in an environment variable (never in code): `export APIFY_TOKEN=your_token`
3. Run the example:

```bash
pip install -r python/requirements.txt
python python/example.py baby.miaa itz.danila --limit 30 --popular
```

JavaScript: `cd js && npm install && node example.mjs https://likee.video/v/sepkYQ`

## Examples

**Python** (`pip install "apify-client<2"`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("lagenuina_agency/likee-scraper").call(run_input={
  "profileUrls": [{"url": "https://likee.video/@baby.miaa"}],
  "maxVideosPerProfile": 30,
  "minViews": 10000
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item.get("description"), item.get("views"), item.get("engagementRate"))
```

**JavaScript / Node.js** (`npm install apify-client`)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('lagenuina_agency/likee-scraper').call({ startUrls: [{ url: 'https://likee.video/v/sepkYQ' }] });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

**cURL / any language** – one HTTP call, results in the response:

```bash
curl -X POST "https://api.apify.com/v2/acts/lagenuina_agency~likee-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profileUrls": [{"url": "https://likee.video/@baby.miaa"}], "maxVideosPerProfile": 20}'
```

All input fields are documented on the [actor page](https://apify.com/lagenuina_agency/likee-scraper) (Input tab).

## Use case: Likee influencer shortlist in CSV

`python/example.py` reads the videos of the creators you pass, prints each creator's followers, median views and average engagement, and writes `likee_videos.csv` (author, date, caption, views, likes, comments, shares, engagement rate, hashtags, music, post link, cover) – ready for Excel or Google Sheets.

## n8n workflow

[`n8n/workflow.json`](n8n/workflow.json): every Monday 08:00 → run the actor on a creator with `onlyNewVideos` (only videos not seen in the previous run) → keep the main fields with a Set node → append to Google Sheets.

1. In n8n: **Workflows → Import from File** and pick `n8n/workflow.json`.
2. Create a **Header Auth** credential named `Apify API token` with name `Authorization` and value `Bearer <your token>`, and select it in the *Run Apify actor* node.
3. Edit the JSON body (profiles, limits), set your Google Sheet ID and activate.

The `run-sync-get-dataset-items` endpoint waits up to 300 s; for bigger runs use `/runs` plus a webhook.

## Use with AI agents (MCP)

Give Claude, ChatGPT, Cursor or any MCP client this actor as a tool:

```
https://mcp.apify.com/?actors=lagenuina_agency/likee-scraper
```

Example config (Claude Desktop, Cursor, VS Code):

```json
{
  "mcpServers": {
    "likee-scraper": {
      "url": "https://mcp.apify.com/?actors=lagenuina_agency/likee-scraper"
    }
  }
}
```

Sign in with Apify OAuth when asked, or send `Authorization: Bearer <APIFY_TOKEN>`.

## Pricing

Pay per result (one video or one profile summary row), platform usage included, no start fee:

| Apify plan | Per 1,000 results |
|---|---|
| Free | $8.00 |
| Bronze | $7.20 |
| Silver | $6.40 |
| Gold, Platinum, Diamond | $5.60 |

Filtered-out videos are never charged. Details on [lagenuina_agency/likee-scraper](https://apify.com/lagenuina_agency/likee-scraper).

## More tools from Quelli di Carne Genuina

- **Ad intelligence:** [Google Ads Transparency](https://github.com/assa83/google-ads-transparency-api) · [Meta Ad Library](https://github.com/assa83/facebook-ad-library-api) · [TikTok Top Ads](https://github.com/assa83/tiktok-top-ads-api) · [LinkedIn Ad Library](https://github.com/assa83/linkedin-ad-library-api)
- **Competitor & SEO research:** [Similarweb traffic](https://github.com/assa83/similarweb-traffic-api) · [Google Trends](https://github.com/assa83/google-trends-api-python) · [Google Play](https://github.com/assa83/google-play-scraper-api)
- **Travel prices:** [Google Hotels](https://github.com/assa83/google-hotels-prices-api) · [Google Flights](https://github.com/assa83/google-flights-api)
- **Retail prices:** [Woolworths & Coles](https://github.com/assa83/australian-supermarket-prices-api)
- **Content & social data:** [YouTube Transcript](https://github.com/assa83/youtube-transcript-scraper-api) · [Medium](https://github.com/assa83/medium-scraper-api)

All actors: [apify.com/lagenuina_agency](https://apify.com/lagenuina_agency) · Tutorials: [assa83.github.io](https://assa83.github.io)

## Disclaimer

Independent, not affiliated with Likee or BIGO Technology. It reads only publicly available data. Profiles and captions can contain personal data: process only what you have a legitimate reason to, in line with GDPR, other applicable laws and Likee's terms.

## License

[MIT](LICENSE) © Quelli di Carne Genuina
