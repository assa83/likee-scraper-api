// Stats of Likee videos from share links (views, likes, direct .mp4).
// Usage: node example.mjs https://likee.video/v/sepkYQ
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set APIFY_TOKEN first: https://console.apify.com/settings/integrations');
    process.exit(1);
}

const links = process.argv.slice(2);
const client = new ApifyClient({ token });
const run = await client.actor('lagenuina_agency/likee-scraper').call({
    startUrls: (links.length ? links : ['https://likee.video/v/sepkYQ']).map((url) => ({ url })),
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const v of items) {
    console.log(`@${v.authorUsername}  ${v.views} views  ${v.likes} likes  ${v.engagementRate}%  ${v.description}\n    ${v.videoUrl || v.postUrl}`);
}
