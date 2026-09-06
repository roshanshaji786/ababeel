#!/usr/bin/env python3
"""Live smoke and mobile-readiness tests for the Ababeel storefront preview.

Usage:
    python tests/live_storefront_test.py
    BASE_URL=http://127.0.0.1:4173 python tests/live_storefront_test.py

The test suite intentionally makes more than 100 HTTP requests so it catches
intermittent asset and routing issues rather than testing only one page load.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:4173").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "shopify-theme"
PREVIEW = ROOT / "preview" / "index.html"

passed = 0
failed = 0
live_requests = 0
failures: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    global passed, failed
    if condition:
        passed += 1
    else:
        failed += 1
        failures.append(f"{name}: {detail}" if detail else name)


def fetch(path: str, user_agent: str = "AbabeelLiveTest/1.0") -> tuple[int, str, dict[str, str]]:
    global live_requests
    live_requests += 1
    url = path if path.startswith("http") else f"{BASE_URL}{path}"
    request = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            body = response.read()
            headers = {key.lower(): value for key, value in response.headers.items()}
            content_type = headers.get("content-type", "")
            try:
                text = body.decode("utf-8")
            except UnicodeDecodeError:
                text = ""
            return response.status, text, {**headers, "_content_length": str(len(body)), "_content_type": content_type}
    except Exception as error:  # urllib raises different exceptions for network/HTTP failures
        return 0, "", {"_error": str(error)}


def test_live_page_matrix() -> None:
    mobile_agents = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/126.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 Chrome/125.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; moto g power) AppleWebKit/537.36 Chrome/124.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 Chrome/123.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 Chrome/120.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; OnePlus CPH2581) AppleWebKit/537.36 Chrome/126.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; vivo V27) AppleWebKit/537.36 Chrome/124.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6a) AppleWebKit/537.36 Chrome/122.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; JioPhone) AppleWebKit/537.36 Chrome/118.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    ]
    mobile_queries = ["", "?utm_source=instagram", "?utm_source=meta&utm_medium=paid", "?preview_theme_id=demo", "?view=mobile"]
    page_snapshots: list[str] = []
    for agent_index, agent in enumerate(mobile_agents):
        for query in mobile_queries:
            status, body, headers = fetch("/preview/" + query, agent)
            label = f"mobile page {agent_index + 1}/{len(mobile_agents)} query {query or 'none'}"
            check(f"{label} status", status == 200, str(headers.get("_error", status)))
            check(f"{label} content type", "text/html" in headers.get("_content_type", ""), headers.get("_content_type", ""))
            check(f"{label} has viewport", 'name="viewport"' in body and "width=device-width" in body)
            check(f"{label} has mobile menu", 'data-mobile-menu' in body and 'data-menu-toggle' in body)
            check(f"{label} has no localhost URL", "localhost" not in body and "127.0.0.1" not in body)
            page_snapshots.append(body)

    desktop_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 Version/17.5 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 Version/17.4 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    ]
    desktop_queries = ["", "?utm_source=google", "?utm_source=instagram&utm_medium=organic"]
    for agent_index, agent in enumerate(desktop_agents):
        for query in desktop_queries:
            status, body, headers = fetch("/preview/" + query, agent)
            label = f"desktop page {agent_index + 1}/{len(desktop_agents)} query {query or 'none'}"
            check(f"{label} status", status == 200, str(headers.get("_error", status)))
            check(f"{label} content type", "text/html" in headers.get("_content_type", ""), headers.get("_content_type", ""))
            check(f"{label} body is complete", len(body) > 10000, f"{len(body)} bytes")
            check(f"{label} has footer", "site-footer" in body)

    # Ensure the live page is stable across a few cache-busting request IDs.
    for request_number in range(1, 11):
        status, body, headers = fetch(f"/preview/?live_test={request_number}", mobile_agents[request_number % len(mobile_agents)])
        check(f"cache-bust request {request_number} status", status == 200, headers.get("_error", ""))
        check(f"cache-bust request {request_number} non-empty", len(body) > 10000, f"{len(body)} bytes")

    check("mobile matrix captured", len(page_snapshots) == 60, str(len(page_snapshots)))


def test_live_assets_and_links() -> None:
    status, html, headers = fetch("/preview/")
    check("canonical preview status", status == 200, headers.get("_error", ""))
    check("canonical preview body", len(html) > 10000, f"{len(html)} bytes")

    references = set(re.findall(r'(?:src|href)="([^"]+)"', html))
    local_references = []
    for reference in references:
        absolute = urljoin(f"{BASE_URL}/preview/", reference)
        parsed = urlparse(absolute)
        if parsed.netloc == urlparse(BASE_URL).netloc and parsed.path not in {"/", "#"}:
            local_references.append(parsed.path)
    check("preview has expected local references", len(local_references) >= 7, str(local_references))

    expected_assets = [
        "/shopify-theme/assets/base.css",
        "/shopify-theme/assets/commerce.css",
        "/shopify-theme/assets/advanced.css",
        "/shopify-theme/assets/theme.js",
        "/shopify-theme/assets/hero-editorial.jpg",
        "/shopify-theme/assets/category-women.jpg",
        "/shopify-theme/assets/category-kids.jpg",
        "/shopify-theme/assets/category-wedding.jpg",
    ]
    for repeat in range(4):
        for asset in expected_assets:
            status, body, headers = fetch(asset, "Mozilla/5.0 (Linux; Android 14; Mobile)" if repeat % 2 else "AbabeelDesktopTest/1.0")
            check(f"asset {asset} pass {repeat + 1} status", status == 200, headers.get("_error", str(status)))
            check(f"asset {asset} pass {repeat + 1} has body", int(headers.get("_content_length", "0")) > 0, f"{headers.get('_content_length', 0)} bytes")

    for reference in local_references:
        if reference.endswith(('.css', '.js', '.jpg', '.jpeg', '.png', '.svg')):
            status, body, headers = fetch(reference)
            check(f"referenced asset {reference}", status == 200, headers.get("_error", str(status)))


def test_static_theme_quality() -> None:
    html = PREVIEW.read_text(encoding="utf-8")
    base_css = (THEME / "assets" / "base.css").read_text(encoding="utf-8")
    commerce_css = (THEME / "assets" / "commerce.css").read_text(encoding="utf-8")
    advanced_css = (THEME / "assets" / "advanced.css").read_text(encoding="utf-8")
    javascript = (THEME / "assets" / "theme.js").read_text(encoding="utf-8")
    layout = (THEME / "layout" / "theme.liquid").read_text(encoding="utf-8")

    check("HTML has charset", '<meta charset="utf-8">' in html)
    check("HTML has viewport", 'content="width=device-width, initial-scale=1"' in html)
    check("HTML has accessible skip link", 'class="skip-link"' in html)
    check("HTML has search form", 'class="commerce-search"' in html)
    check("HTML has cart drawer", 'data-cart-drawer' in html)
    check("HTML has WhatsApp action", "wa.me/917012045854" in html)
    check("HTML has category cards", html.count("shop-category-card") >= 4)
    check("HTML has product cards", html.count("product-card") >= 4)
    check("HTML has brand story", "brand-story" in html)
    check("HTML has Instagram showcase", "instagram-showcase" in html)
    check("HTML has newsletter", "newsletter-card" in html)
    check("HTML has mobile nav", "MobileMenu" in html)
    check("HTML has no unclosed preview marker", html.count("<!--") == html.count("-->") )

    check("base CSS has mobile breakpoint", "@media (max-width: 680px)" in base_css)
    check("commerce CSS has mobile breakpoint", "@media (max-width: 680px)" in commerce_css)
    check("advanced CSS has mobile breakpoint", "@media (max-width: 680px)" in advanced_css)
    check("mobile header wraps", "commerce-header__main { flex-wrap: wrap" in advanced_css or "commerce-header__main { flex-wrap: wrap" in commerce_css)
    check("mobile search is full width", "flex-basis: 100%" in commerce_css)
    check("mobile product grid is two columns", "product-grid--2, .product-grid--3, .product-grid--4" in base_css)
    check("mobile category grid is two columns", "shop-categories__grid { grid-template-columns: repeat(2" in advanced_css)
    check("mobile filters become a drawer", "position: fixed" in advanced_css and "collection-filters.is-open" in advanced_css)
    check("mobile newsletter stacks", "newsletter-card { display: block" in advanced_css)
    check("buttons have touch-friendly minimum", "min-height: 51px" in base_css)
    check("page width avoids desktop overflow", "calc(100% - 32px)" in base_css)
    check("predictive search has hidden state", ".predictive-search-results[hidden]" in advanced_css)
    check("drawer locks page scroll", "cart-drawer-open" in advanced_css)

    check("JavaScript has mobile menu", "data-menu-toggle" in javascript)
    check("JavaScript has AJAX quick add", "data-ajax-add" in javascript and "/cart/add.js" in javascript)
    check("JavaScript has cart refresh", "refreshDrawer" in javascript and "/cart.js" in javascript)
    check("JavaScript has wishlist storage", "ababeel-wishlist" in javascript)
    check("JavaScript has predictive search", "/search/suggest.json" in javascript)
    check("JavaScript has WhatsApp handling", "openWhatsApp" in javascript)
    check("JavaScript has filter toggle", "data-filter-toggle" in javascript)
    check("layout loads advanced CSS", "advanced.css" in layout)
    check("layout loads cart drawer", "section 'cart-drawer'" in layout)
    check("layout has structured data", "ClothingStore" in layout)
    check("layout has canonical link", "canonical_url" in layout)

    expected_files = [
        "layout/theme.liquid", "config/settings_schema.json", "config/settings_data.json",
        "templates/index.json", "templates/product.json", "templates/collection.json", "templates/cart.json",
        "sections/header.liquid", "sections/footer.liquid", "sections/cart-drawer.liquid",
        "sections/main-product.liquid", "sections/main-collection.liquid", "sections/main-list-collections.liquid",
        "sections/instagram-showcase.liquid", "sections/newsletter.liquid", "snippets/product-card.liquid",
    ]
    for relative in expected_files:
        check(f"theme file exists {relative}", (THEME / relative).is_file())

    for json_file in THEME.rglob("*.json"):
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
            check(f"valid JSON {json_file.relative_to(ROOT)}", True)
        except Exception as error:
            check(f"valid JSON {json_file.relative_to(ROOT)}", False, str(error))


def main() -> int:
    print(f"Testing live preview: {BASE_URL}")
    test_live_page_matrix()
    test_live_assets_and_links()
    test_static_theme_quality()
    print(f"\nPASS: {passed}")
    print(f"FAIL: {failed}")
    print(f"LIVE HTTP REQUESTS: {live_requests}")
    if failures:
        print("\nFailures:")
        for failure in failures[:30]:
            print(f" - {failure}")
        if len(failures) > 30:
            print(f" - ... and {len(failures) - 30} more")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
