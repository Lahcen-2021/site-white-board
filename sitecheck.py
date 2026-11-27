#!/usr/bin/env python3
"""Daily health check for www.sitewhiteboard.com.

Measures instead of guessing: every number here comes from a real HTTP response.
Prints a report to stdout, writes report.html, and exits non-zero if anything
critical is down so a scheduler can alert on it.

  python sitecheck.py                     # check and print
  python sitecheck.py --html report.html  # also write the HTML report
  python sitecheck.py --json out.json     # machine-readable results

Why this exists: the previous checker asked for /about/ (with a slash) while the
site serves /about.html, read the 404 as "page missing", and reported a false
alarm every day for a week. It also used a page-summarising fetcher that does not
return HTTP status codes at all, so it could not tell 200 from 404. This script
reads status codes directly and prints the ones it saw.
"""

import argparse
import json
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timezone

# The Windows console defaults to cp1252, which cannot print Arabic. Force UTF-8
# so the summary line does not crash the whole run after every check passed.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

SITE = "https://www.sitewhiteboard.com"
UA = "SiteWhiteboard-Monitor/1.0 (+https://www.sitewhiteboard.com)"
TIMEOUT = 20

# Paths that must work. These are the real served paths: the legal pages are
# .html files, NOT directories. Getting this list wrong is what caused the
# false "ads.txt missing" and "duplicate description" alarms.
PAGES = ["/", "/fr/", "/ar/", "/board/", "/blog/", "/fr/blog/", "/ar/blog/"]
DOCS = ["/about.html", "/contact.html", "/privacy.html", "/terms.html"]
FILES = ["/ads.txt", "/robots.txt", "/sitemap.xml"]
CRITICAL = {"/", "/board/"}          # down = wake someone up
SLOW_MS = 1500                       # total time over this is a warning
DESC_MAX = 160                       # Google truncates past roughly this
STALE_DAYS = 21                      # no new article in this long = warning

results = []   # (severity, area, message); severity: ok | warn | crit | nd


def log(sev, area, msg):
    results.append((sev, area, msg))
    mark = {"ok": "  ok ", "warn": "WARN ", "crit": "CRIT ", "nd": "  -- "}[sev]
    print(f"{mark} [{area}] {msg}")


def fetch(path_or_url, method="GET"):
    """Return (status, headers, body, elapsed_ms). Status is 0 if it never connected.

    Redirects are NOT followed, so a 301 is visible as a 301 instead of silently
    looking like a 200 at a different address.
    """
    url = path_or_url if path_or_url.startswith("http") else SITE + path_or_url

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None

    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": UA,
        "Accept-Encoding": "identity",   # keep Content-Length honest
    })
    t0 = time.perf_counter()
    try:
        with opener.open(req, timeout=TIMEOUT) as r:
            body = r.read()
            return r.status, dict(r.headers), body, (time.perf_counter() - t0) * 1000
    except urllib.error.HTTPError as e:
        # A 404 is an answer, not a failure. Keep it.
        return e.code, dict(e.headers or {}), e.read(), (time.perf_counter() - t0) * 1000
    except Exception as e:
        print(f"       ! {url}: {type(e).__name__}: {e}", file=sys.stderr)
        return 0, {}, b"", (time.perf_counter() - t0) * 1000


def text(body):
    return body.decode("utf8", "replace")


def one(pattern, s, group=1):
    m = re.search(pattern, s, re.I | re.S)
    return m.group(group).strip() if m else None


# ---------------------------------------------------------------- 1. uptime

def check_availability():
    print("\n=== 1. availability ===")
    timings = {}
    for p in PAGES:
        st, _, body, ms = fetch(p)
        timings[p] = ms
        kb = len(body) / 1024
        if st == 200:
            sev = "warn" if ms > SLOW_MS else "ok"
            note = " (slow)" if ms > SLOW_MS else ""
            log(sev, "uptime", f"{p} -> 200, {ms:.0f}ms, {kb:.1f}KB{note}")
        else:
            sev = "crit" if p in CRITICAL else "warn"
            log(sev, "uptime", f"{p} -> {st or 'no connection'}")
    return timings


def check_redirects():
    print("\n=== 2. redirects and 404 ===")
    st, h, _, _ = fetch("https://sitewhiteboard.com/")
    loc = h.get("Location", "")
    if st in (301, 308) and "www." in loc:
        log("ok", "redirect", f"apex -> www ({st})")
    else:
        log("warn", "redirect", f"apex returned {st}, Location: {loc or 'none'}")

    st, h, _, _ = fetch("http://www.sitewhiteboard.com/")
    loc = h.get("Location", "")
    if st in (301, 308) and loc.startswith("https://"):
        log("ok", "redirect", f"http -> https ({st})")
    else:
        log("warn", "redirect", f"http returned {st}, Location: {loc or 'none'}")

    st, _, _, _ = fetch("/this-page-does-not-exist-" + date.today().isoformat())
    if st == 404:
        log("ok", "404", "missing URL returns 404")
    else:
        log("warn", "404", f"missing URL returns {st}, expected 404 (soft 404 risks indexing junk)")


# ------------------------------------------------------------------ 3. seo

def check_seo():
    print("\n=== 3. technical seo ===")
    st, _, body, _ = fetch("/robots.txt")
    if st != 200:
        log("crit", "robots", f"robots.txt -> {st}")
        return None
    rb = text(body)
    blocked = [l.split(":", 1)[1].strip() for l in rb.splitlines()
               if l.lower().startswith("disallow:") and l.split(":", 1)[1].strip()]
    # /app/ only forwards old links to /board/, so blocking it is intended.
    unexpected = [b for b in blocked if b not in ("/app/",)]
    if unexpected:
        log("warn", "robots", f"blocks unexpected paths: {unexpected}")
    else:
        log("ok", "robots", f"blocks only {blocked or 'nothing'} (expected)")
    if "sitemap:" in rb.lower():
        log("ok", "robots", "points to the sitemap")
    else:
        log("warn", "robots", "no Sitemap: line")

    st, _, body, _ = fetch("/sitemap.xml")
    if st != 200:
        log("crit", "sitemap", f"sitemap.xml -> {st}")
        return None
    sm = text(body)
    locs = re.findall(r"<loc>([^<]+)</loc>", sm)
    fr = [u for u in locs if "/fr/" in u]
    ar = [u for u in locs if "/ar/" in u]
    alts = len(re.findall(r"xhtml:link", sm))
    log("ok", "sitemap", f"{len(locs)} URLs: {len(fr)} fr, {len(ar)} ar, {alts} hreflang alternates")
    if not fr or not ar:
        log("warn", "sitemap", "a language is missing from the sitemap")

    mods = sorted(re.findall(r"<lastmod>([^<]+)</lastmod>", sm))
    if mods:
        log("ok", "sitemap", f"newest lastmod {mods[-1]}")

    # Sample real URLs and confirm they are 200, not redirects or errors.
    import random
    sample = random.sample(locs, min(5, len(locs)))
    bad = []
    for u in sample:
        st, _, _, _ = fetch(u)
        if st != 200:
            bad.append(f"{u} -> {st}")
    if bad:
        for b in bad:
            log("warn", "sitemap", f"listed URL not 200: {b}")
    else:
        log("ok", "sitemap", f"sampled {len(sample)} listed URLs, all 200")
    return locs


# -------------------------------------------------------------- 4. quality

def check_pages(locs):
    print("\n=== 4. page quality ===")
    targets = [SITE + "/", SITE + "/ar/", SITE + "/fr/"]
    # One article per language, so a translated page is checked too.
    for pre in ("/blog/", "/fr/blog/", "/ar/blog/"):
        pat = re.escape(SITE + pre) + r"[a-z0-9-]+/$"
        post = next((u for u in (locs or []) if re.match(pat, u)), None)
        if post:
            targets.append(post)

    seen_desc = {}
    for url in targets:
        st, _, body, _ = fetch(url)
        if st != 200:
            log("warn", "page", f"{url} -> {st}")
            continue
        h = text(body)
        short = url.replace(SITE, "") or "/"

        title = one(r"<title>(.*?)</title>", h) or ""
        desc = one(r'name="description"\s+content="(.*?)"', h) or ""
        canon = one(r'rel="canonical"\s+href="(.*?)"', h) or ""
        htmltag = one(r"(<html[^>]*>)", h) or ""
        h1s = len(re.findall(r"<h1[\s>]", h))
        hreflangs = len(re.findall(r'rel="alternate"\s+hreflang=', h))
        types = sorted(set(re.findall(r'"@type"\s*:\s*"([^"]+)"', h)))
        words = len(re.sub(r"<[^>]*>", " ", h).split())

        if not title:
            log("warn", "page", f"{short}: no title")
        elif len(title) > 65:
            log("warn", "page", f"{short}: title {len(title)} chars, will be truncated")
        else:
            log("ok", "page", f"{short}: title {len(title)} chars")

        if not desc:
            log("warn", "page", f"{short}: no meta description")
        elif len(desc) > DESC_MAX:
            log("warn", "page", f"{short}: description {len(desc)} chars, over {DESC_MAX}, will be truncated")
        else:
            log("ok", "page", f"{short}: description {len(desc)} chars")

        # Real duplicate detection: compare the actual strings across pages.
        if desc:
            if desc in seen_desc:
                log("warn", "page", f"{short}: description identical to {seen_desc[desc]}")
            else:
                seen_desc[desc] = short

        if h1s == 1:
            log("ok", "page", f"{short}: exactly one h1")
        else:
            log("warn", "page", f"{short}: {h1s} h1 tags, expected 1")

        want = url.rstrip("/") + "/" if url.endswith("/") else url
        if canon.rstrip("/") == want.rstrip("/"):
            log("ok", "page", f"{short}: canonical self-references")
        else:
            log("warn", "page", f"{short}: canonical is {canon or 'missing'}, expected {want}")

        if "/ar/" in url:
            if 'lang="ar"' in htmltag and 'dir="rtl"' in htmltag:
                log("ok", "page", f"{short}: lang=ar dir=rtl")
            else:
                log("warn", "page", f"{short}: Arabic page html tag is {htmltag}")

        if hreflangs >= 3:
            log("ok", "page", f"{short}: {hreflangs} hreflang tags")
        else:
            log("warn", "page", f"{short}: only {hreflangs} hreflang tags")

        if types:
            log("ok", "page", f"{short}: JSON-LD {', '.join(types[:6])}")
        else:
            log("warn", "page", f"{short}: no JSON-LD structured data")

        if words < 300:
            log("warn", "page", f"{short}: only ~{words} words, thin content")
        else:
            log("ok", "page", f"{short}: ~{words} words")

    # Freshness: how long since the newest article changed.
    if locs:
        st, _, body, _ = fetch("/sitemap.xml")
        sm = text(body)
        posts = re.findall(
            r"<loc>[^<]*/blog/[a-z0-9-]+/</loc>\s*<lastmod>([^<]+)</lastmod>", sm)
        if posts:
            newest = max(posts)
            try:
                age = (date.today() - date.fromisoformat(newest)).days
                sev = "warn" if age > STALE_DAYS else "ok"
                log(sev, "content", f"newest article {newest}, {age} days ago")
            except ValueError:
                log("nd", "content", f"could not parse lastmod {newest}")
        # Anchor on the full host so the English pattern does not also match
        # /fr/blog/ and /ar/blog/ and triple its own count.
        counts = {}
        for pre, label in (("/blog/", "en"), ("/fr/blog/", "fr"), ("/ar/blog/", "ar")):
            pat = re.escape(SITE + pre) + r"[a-z0-9-]+/$"
            counts[label] = len([u for u in locs if re.match(pat, u)])
        log("ok", "content", f"articles per language: {counts}")
        if len(set(counts.values())) > 1:
            log("warn", "content", "languages have different article counts, a translation is missing")


# ------------------------------------------------------------ 5. money

def check_monetization():
    print("\n=== 5. monetization readiness ===")
    for p in DOCS:
        st, _, _, _ = fetch(p)
        if st == 200:
            log("ok", "adsense", f"{p} -> 200")
        else:
            log("warn", "adsense", f"{p} -> {st}, AdSense wants these pages reachable")

    st, _, body, _ = fetch("/ads.txt")
    if st != 200:
        log("warn", "adsense", f"/ads.txt -> {st}")
    else:
        line = text(body).strip()
        if re.match(r"google\.com,\s*pub-\d+,\s*DIRECT", line):
            log("ok", "adsense", f"ads.txt valid: {line.splitlines()[0]}")
        else:
            log("warn", "adsense", f"ads.txt present but malformed: {line[:80]}")

    # The real test: are the ad slot ids filled in? Empty ids mean site.js
    # skips every container (if(!id)return) and no ad ever renders.
    st, _, body, _ = fetch("/assets/config.js")
    if st != 200:
        log("nd", "adsense", f"config.js -> {st}, cannot check ad slots")
    else:
        cfg = text(body)
        client = one(r'"adsenseClient"\s*:\s*"([^"]*)"', cfg) or ""
        slots = dict(re.findall(r'"(top|middle|bottom)"\s*:\s*"([^"]*)"', cfg))
        if not client:
            log("warn", "adsense", "no adsenseClient configured, ads are off")
        else:
            log("ok", "adsense", f"publisher id {client}")
        empty = [k for k, v in slots.items() if not v]
        if empty:
            log("warn", "adsense",
                f"ad slot ids empty: {empty}. site.js skips containers without an id, "
                f"so NO ads render. Create units in AdSense and rebuild with "
                f"--slot-top/--slot-middle/--slot-bottom")
        elif slots:
            log("ok", "adsense", f"all ad slots configured: {slots}")

        price = one(r'"proPrice"\s*:\s*"([^"]*)"', cfg)
        checkout = one(r'"proCheckoutUrl"\s*:\s*"([^"]*)"', cfg)
        if not checkout:
            # Intentional while there is no payment provider. Not a defect.
            log("ok", "pricing", "no checkout URL set, so the Pro card is hidden by design")
        elif not price:
            log("warn", "pricing", "checkout URL set but proPrice is empty, card shows no price")
        else:
            log("ok", "pricing", f"Pro plan live at {price}")

    # Ads must never appear on the drawing canvas: accidental clicks there
    # violate AdSense policy.
    st, _, body, _ = fetch("/board/")
    if st == 200:
        n = len(re.findall(r'data-ad[=\s]', text(body)))
        if n == 0:
            log("ok", "adsense", "/board/ has no ad containers (correct, avoids accidental clicks)")
        else:
            log("warn", "adsense", f"/board/ has {n} ad containers, AdSense prohibits ads on a canvas")


# ----------------------------------------------------- 6. speed and security

def check_speed(timings):
    print("\n=== 6. speed ===")
    # Connection phase breakdown for the home page.
    host = "www.sitewhiteboard.com"
    try:
        t0 = time.perf_counter()
        ip = socket.gethostbyname(host)
        dns = (time.perf_counter() - t0) * 1000

        t1 = time.perf_counter()
        sock = socket.create_connection((host, 443), timeout=TIMEOUT)
        tcp = (time.perf_counter() - t1) * 1000

        t2 = time.perf_counter()
        ctx = ssl.create_default_context()
        ssock = ctx.wrap_socket(sock, server_hostname=host)
        tls = (time.perf_counter() - t2) * 1000

        cert = ssock.getpeercert()
        proto = ssock.version()
        ssock.close()

        log("ok", "speed", f"{host} is {ip}: DNS {dns:.0f}ms, TCP {tcp:.0f}ms, TLS {tls:.0f}ms ({proto})")

        exp = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        left = (exp - datetime.now(timezone.utc)).days
        sev = "crit" if left < 7 else "warn" if left < 21 else "ok"
        log(sev, "tls", f"certificate expires in {left} days ({cert['notAfter']})")
    except Exception as e:
        log("nd", "speed", f"connection breakdown failed: {type(e).__name__}: {e}")

    for p, ms in timings.items():
        if ms > SLOW_MS:
            log("warn", "speed", f"{p} took {ms:.0f}ms")
    if timings:
        avg = sum(timings.values()) / len(timings)
        log("ok", "speed", f"average page time {avg:.0f}ms over {len(timings)} pages")

    # Compression and caching, read from the real response headers.
    req = urllib.request.Request(SITE + "/", headers={
        "User-Agent": UA, "Accept-Encoding": "gzip, br"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            h = dict(r.headers)
        enc = h.get("Content-Encoding", "")
        if enc:
            log("ok", "speed", f"compression active: {enc}")
        else:
            log("warn", "speed", "no Content-Encoding, responses are uncompressed")
        cc = h.get("Cache-Control", "")
        if "no-cache" in cc or "no-store" in cc:
            log("warn", "speed", f"HTML Cache-Control is '{cc}', browsers refetch every visit; "
                                 f"consider max-age=300, must-revalidate")
        elif cc:
            log("ok", "speed", f"HTML Cache-Control: {cc}")
        if "Strict-Transport-Security" in h:
            log("ok", "security", f"HSTS: {h['Strict-Transport-Security']}")
        else:
            log("warn", "security", "no HSTS header")
        for hdr, why in (("X-Content-Type-Options", "stops MIME sniffing"),
                         ("Referrer-Policy", "limits referrer leakage")):
            if hdr not in h:
                log("warn", "security", f"no {hdr} header ({why})")
    except Exception as e:
        log("nd", "speed", f"header check failed: {type(e).__name__}: {e}")


def check_ssl_grade():
    print("\n=== 7. ssl labs ===")
    url = ("https://api.ssllabs.com/api/v3/analyze"
           "?host=www.sitewhiteboard.com&fromCache=on&maxAge=24")
    for attempt in range(3):
        st, _, body, _ = fetch(url)
        if st != 200:
            log("nd", "ssl", f"SSL Labs API returned {st}")
            return
        try:
            d = json.loads(text(body))
        except json.JSONDecodeError:
            log("nd", "ssl", "SSL Labs returned unparseable JSON")
            return
        status = d.get("status")
        if status == "READY":
            for ep in d.get("endpoints", []):
                g = ep.get("grade", "?")
                sev = "ok" if g.startswith("A") else "warn"
                log(sev, "ssl", f"{ep.get('ipAddress')} grade {g}")
            return
        if status == "ERROR":
            log("warn", "ssl", f"SSL Labs error: {d.get('statusMessage')}")
            return
        if attempt < 2:
            print(f"       SSL Labs still {status}, waiting 25s...")
            time.sleep(25)
    log("nd", "ssl", f"SSL Labs still {status} after 3 tries, not measured")


def check_pagespeed(api_key=None):
    print("\n=== 8. pagespeed ===")
    url = ("https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
           "?url=https%3A%2F%2Fwww.sitewhiteboard.com%2F&strategy=mobile")
    if api_key:
        url += "&key=" + api_key
    st, _, body, _ = fetch(url)
    if st == 429:
        log("nd", "pagespeed",
            "429 rate limited. Without an API key this is expected; the speed numbers "
            "in section 6 are measured directly instead. Get a free key at "
            "console.cloud.google.com and pass --psi-key to enable this check")
        return
    if st != 200:
        log("nd", "pagespeed", f"API returned {st}, not measured")
        return
    try:
        lh = json.loads(text(body))["lighthouseResult"]
    except (json.JSONDecodeError, KeyError):
        log("nd", "pagespeed", "unexpected API response shape")
        return
    score = round(lh["categories"]["performance"]["score"] * 100)
    sev = "ok" if score >= 90 else "warn"
    log(sev, "pagespeed", f"mobile performance score {score}/100")
    for k in ("first-contentful-paint", "largest-contentful-paint",
              "cumulative-layout-shift", "total-blocking-time"):
        a = lh["audits"].get(k, {})
        if a.get("displayValue"):
            log("ok", "pagespeed", f"{k}: {a['displayValue']}")


# ---------------------------------------------------------------- reporting

def write_html(path, counts, overall):
    rows = []
    for sev, area, msg in results:
        color = {"ok": "#15803d", "warn": "#b45309", "crit": "#b91c1c", "nd": "#78716c"}[sev]
        label = {"ok": "سليم", "warn": "تحذير", "crit": "حرِج", "nd": "غير مُقاس"}[sev]
        safe = (msg.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        rows.append(
            f'<tr><td style="padding:6px;border:1px solid #e7e5e4;color:{color};'
            f'white-space:nowrap;"><strong>{label}</strong></td>'
            f'<td style="padding:6px;border:1px solid #e7e5e4;white-space:nowrap;">{area}</td>'
            f'<td style="padding:6px;border:1px solid #e7e5e4;direction:ltr;text-align:left;">{safe}</td></tr>')

    html = f"""<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>تقرير SiteWhiteboard</title></head>
<body style="margin:0;background:#f5f5f4;">
<div dir="rtl" style="max-width:860px;margin:0 auto;padding:24px;background:#fff;
 font-family:'Segoe UI',Tahoma,Arial,sans-serif;color:#1c1917;line-height:1.7;font-size:15px;text-align:right;">
<h1 style="font-size:22px;margin:0 0 4px;">تقرير SiteWhiteboard اليومي</h1>
<p style="margin:0 0 20px;color:#57534e;font-size:14px;">
{date.today().isoformat()} &middot; www.sitewhiteboard.com &middot;
الحالة العامة: <strong>{overall}</strong></p>
<p style="margin:0 0 16px;font-size:14px;">
حرِج: {counts['crit']} &middot; تحذير: {counts['warn']} &middot;
سليم: {counts['ok']} &middot; غير مُقاس: {counts['nd']}</p>
<table style="width:100%;border-collapse:collapse;font-size:13px;">
<tr style="background:#f5f5f4;">
<th style="text-align:right;padding:6px;border:1px solid #e7e5e4;">التقييم</th>
<th style="text-align:right;padding:6px;border:1px solid #e7e5e4;">المحور</th>
<th style="text-align:right;padding:6px;border:1px solid #e7e5e4;">التفصيل</th></tr>
{''.join(rows)}
</table>
<p style="margin:24px 0 0;padding-top:12px;border-top:1px solid #e7e5e4;color:#78716c;font-size:12px;">
كل رقم في هذا التقرير مقاس من رد HTTP حقيقي. ما لم يُقَس مُسمّى بذلك صراحةً.</p>
</div></body></html>"""
    with open(path, "w", encoding="utf8") as f:
        f.write(html)
    print(f"\nHTML report written to {path}")


def main():
    ap = argparse.ArgumentParser(description="Daily health check for sitewhiteboard.com")
    ap.add_argument("--html", metavar="FILE", help="write an Arabic HTML report")
    ap.add_argument("--json", metavar="FILE", help="write raw results as JSON")
    ap.add_argument("--psi-key", metavar="KEY", help="PageSpeed Insights API key")
    ap.add_argument("--skip-slow", action="store_true",
                    help="skip SSL Labs and PageSpeed (faster, for frequent runs)")
    a = ap.parse_args()

    print(f"SiteWhiteboard check {datetime.now().isoformat(timespec='seconds')}")
    timings = check_availability()
    check_redirects()
    locs = check_seo()
    check_pages(locs)
    check_monetization()
    check_speed(timings)
    if not a.skip_slow:
        check_ssl_grade()
        check_pagespeed(a.psi_key)

    counts = {k: sum(1 for s, _, _ in results if s == k)
              for k in ("ok", "warn", "crit", "nd")}
    overall = "حرِج" if counts["crit"] else "تحذير" if counts["warn"] else "سليم"

    print("\n" + "=" * 60)
    print(f"RESULT: {overall}  |  crit {counts['crit']}  warn {counts['warn']}  "
          f"ok {counts['ok']}  not-measured {counts['nd']}")
    if counts["crit"]:
        print("\nCRITICAL:")
        for sev, area, msg in results:
            if sev == "crit":
                print(f"  [{area}] {msg}")
    if counts["warn"]:
        print("\nWARNINGS:")
        for sev, area, msg in results:
            if sev == "warn":
                print(f"  [{area}] {msg}")

    if a.html:
        write_html(a.html, counts, overall)
    if a.json:
        with open(a.json, "w", encoding="utf8") as f:
            json.dump({"date": date.today().isoformat(), "overall": overall,
                       "counts": counts,
                       "results": [{"severity": s, "area": ar, "message": m}
                                   for s, ar, m in results]}, f, ensure_ascii=False, indent=2)
        print(f"JSON written to {a.json}")

    # Exit code so a scheduler can alert: 2 = something critical, 0 = fine.
    return 2 if counts["crit"] else 0


if __name__ == "__main__":
    sys.exit(main())
