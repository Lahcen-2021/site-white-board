# SiteWhiteboard – static site

A whiteboard web app plus a marketing site in English, French and Arabic.
Everything is plain HTML, CSS and JavaScript: no server code, no database.

## Folders

- `dist/`   the finished site. Upload the **contents** of this folder to the root of your domain (`public_html` on Hostinger).
- `src/`    the source files (whiteboard app, styles, scripts).
- `build.py` rebuilds `dist/` with your own settings.

The site must sit at the root of a domain or subdomain (links start with `/`).

## Build with your settings

    python build.py

The domain defaults to `https://www.sitewhiteboard.com` (pass `--domain` to change it).
The canonical links, hreflang links, sitemap and robots.txt all contain it.

Optional settings (add them when you have them, then rebuild and re-upload):

    --email contact@your-domain.com      contact address shown on About / Privacy / Terms
    --adsense ca-pub-XXXXXXXXXXXXXXXX    turns ads on and writes ads.txt
    --slot-top 1111111111                AdSense ad unit ids for the three places on the pages
    --slot-middle 2222222222
    --slot-bottom 3333333333
    --checkout https://...               the payment page where people buy Pro
    --validate https://...               licence check address (see below)
    --price "$4 / month"                 price text shown next to Pro
    --free 3                             number of boards on the free plan

The same values end up in `dist/assets/config.js`, which you can also edit by hand.

## Ads (AdSense)

- With no `--adsense` id, no ad code loads at all.
- With an id, the AdSense script loads on the landing, About, Privacy and Terms pages,
  so Auto ads work even without slot ids. Slot ids fill the three fixed places.
- The drawing screen (`/app/`) carries no ads on purpose: ads next to a canvas people
  click and drag on invite accidental clicks, which AdSense does not allow.
- Visitors with Pro active see no ads.
- For visitors in Europe, turn on Google's consent message in your AdSense account
  (Privacy & messaging).

## Pro

Free plan: 3 boards, PNG export with a small "Made with SiteWhiteboard" mark.
Pro: unlimited boards, no ads, 2x exports without the mark, backup and restore.

Pro is unlocked with a licence key. The app sends the key to `--validate` as
`POST license_key=...` and expects a JSON answer containing `"valid": true`.
Use a payment provider that issues licence keys and offers such a check
address, and confirm in its documentation that it can be called from a browser.

Until `--checkout` and `--validate` are set, the site says "Pro is not on sale yet".

Limit to know about: the check runs in the visitor's browser, so a technical
user can bypass it. That is normal for a site without a server; a server-side
check would be needed to close it.

## Before you go live

- Read the Privacy and Terms pages and adjust them to your business. They are a
  starting template, not legal advice.
- Submit `https://your-domain.com/sitemap.xml` in Google Search Console.
