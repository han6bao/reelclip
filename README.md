# Reelclip

Seattle production company website. Static site: `index.html` plus `img/`.

Pushing to `main` deploys to Vercel automatically.

## SEO pages

Static, crawlable pages live in `/services`, `/work`, `/industries` and `/locations`, plus `sitemap.xml` and `robots.txt`.
They are generated, so edit the copy in `tools/seo_content.py` (or portfolio data in `index.html`) and rebuild:

    node tools/extract-data.js && python3 tools/build_seo.py

Contact form email goes through `api/contact.js` (Resend). Vercel env vars: `RESEND_API_KEY` (required), `CONTACT_TO`, `CONTACT_FROM`.
