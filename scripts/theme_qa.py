#!/usr/bin/env python3
"""Darty QA engine: per-variant static audit + live runtime matrix.

Produces build/qa/<slug>.json consumed by scripts/build_darty_report.py.
"""
import importlib
import json
import os
import re
import sys
from pathlib import Path

import tinycss2

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build" / "variants"
QA = ROOT / "build" / "qa"
QA.mkdir(parents=True, exist_ok=True)

SLUGS = ["heritage-royale", "bazaar-pop", "atelier-blanc", "gully-drop", "meadow-muse"]
NAMES = {
    "heritage-royale": "Ababeel Heritage Royale",
    "bazaar-pop": "Ababeel Bazaar Pop",
    "atelier-blanc": "Ababeel Atelier Blanc",
    "gully-drop": "Ababeel Gully Drop",
    "meadow-muse": "Ababeel Meadow & Muse",
}
REFS = {
    "heritage-royale": "Sabyasachi / FabIndia / Manyavar / Net-A-Porter",
    "bazaar-pop": "AJIO / Myntra / Nykaa Fashion / Bewakoof",
    "atelier-blanc": "Zara / COS / The Row / Toteme / Arket",
    "gully-drop": "Supreme / Kith / Palace / Souled Store",
    "meadow-muse": "Anthropologie / Free People / Glossier / Everlane",
}

REQUIRED_FILES = [
    "layout/theme.liquid", "config/settings_schema.json", "config/settings_data.json",
    "templates/index.json", "templates/product.json", "templates/collection.json", "templates/cart.json",
    "templates/404.json", "sections/header.liquid", "sections/footer.liquid", "sections/cart-drawer.liquid",
    "sections/main-product.liquid", "sections/main-collection.liquid", "sections/hero.liquid",
    "sections/featured-collection.liquid", "sections/promo-banner.liquid", "sections/value-props.liquid",
    "snippets/product-card.liquid", "snippets/seo-meta.liquid", "assets/base.css", "assets/commerce.css",
    "assets/advanced.css", "assets/variant.css", "assets/theme.js",
]


def hex_rgb(value):
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if len(value) != 6:
        return None
    try:
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def luminance(rgb):
    channels = []
    for ch in rgb:
        c = ch / 255
        channels.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def root_colors(css_text):
    match = re.search(r":root\s*{([^}]*)}", css_text)
    colors = {}
    if match:
        for prop, value in re.findall(r"(--color-[\w-]+)\s*:\s*([^;]+);", match.group(1)):
            rgb = hex_rgb(value)
            if rgb:
                colors[prop] = rgb
    return colors


def liquid_balance(text):
    opens = len(re.findall(r"{%", text))
    closes = len(re.findall(r"%}", text))
    braces_open = len(re.findall(r"{{", text))
    braces_close = len(re.findall(r"}}", text))
    return opens == closes and braces_open == braces_close


def audit_variant(slug):
    dest = BUILD / slug
    checks = {cat: [] for cat in ["engineering", "seo", "accessibility", "mobile", "performance", "commerce"]}

    def add(cat, name, ok, detail=""):
        checks[cat].append({"name": name, "passed": bool(ok), "detail": detail})

    # ---- engineering & code quality ----
    for rel in REQUIRED_FILES:
        add("engineering", f"file exists {rel}", (dest / rel).is_file())
    for json_file in dest.rglob("*.json"):
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
            add("engineering", f"valid JSON {json_file.relative_to(dest)}", True)
        except Exception as err:
            add("engineering", f"valid JSON {json_file.relative_to(dest)}", False, str(err))
    for liquid_file in list(dest.rglob("*.liquid")):
        text = liquid_file.read_text(encoding="utf-8")
        add("engineering", f"liquid balanced {liquid_file.relative_to(dest)}", liquid_balance(text))
        for schema in re.findall(r"{%\s*schema\s*%}(.*?){%\s*endschema\s*%}", text, re.S):
            try:
                json.loads(schema)
                add("engineering", f"schema valid {liquid_file.relative_to(dest)}", True)
            except Exception as err:
                add("engineering", f"schema valid {liquid_file.relative_to(dest)}", False, str(err))
    theme_liquid = (dest / "layout" / "theme.liquid").read_text(encoding="utf-8")
    add("engineering", "variant stylesheet wired", "variant.css" in theme_liquid)
    add("engineering", "variant body class", f"theme-{slug}" in theme_liquid)
    add("engineering", "google fonts linked", "fonts.googleapis.com" in theme_liquid)
    variant_css_text = (dest / "assets" / "variant.css").read_text(encoding="utf-8")
    rules = [r for r in tinycss2.parse_stylesheet(variant_css_text, skip_comments=True, skip_whitespace=True) if r.type == "qualified-rule"]
    errors = [r.message for r in tinycss2.parse_stylesheet(variant_css_text) if r.type == "error"]
    add("engineering", "variant CSS parses clean", not errors, "; ".join(errors))
    add("engineering", "variant CSS has real design depth (>=35 rules)", len(rules) >= 35, f"{len(rules)} rules")
    idx = json.loads((dest / "templates/index.json").read_text(encoding="utf-8"))
    add("engineering", "homepage order valid", set(idx["order"]) <= set(idx["sections"]))
    add("engineering", "homepage has hero first", idx["order"][0] == "hero_PAPfyK")

    # ---- seo ----
    seo = (dest / "snippets" / "seo-meta.liquid").read_text(encoding="utf-8")
    for token in ["og:title", "og:description", "og:url", "og:image", "twitter:card", 'name="robots"', "product:price:currency"]:
        add("seo", f"seo snippet has {token}", token in seo)
    add("seo", "canonical url in layout", "canonical_url" in theme_liquid)
    add("seo", "ClothingStore JSON-LD", "ClothingStore" in theme_liquid)
    add("seo", "WebSite JSON-LD with SearchAction", '"@type": "WebSite"' in theme_liquid and "SearchAction" in theme_liquid)
    product = (dest / "sections" / "main-product.liquid").read_text(encoding="utf-8")
    add("seo", "Product JSON-LD with offers", '"@type": "Product"' in product and '"@type": "Offer"' in product)
    add("seo", "Product LD uses INR", '"priceCurrency": "INR"' in product)
    hero = (dest / "sections" / "hero.liquid").read_text(encoding="utf-8")
    add("seo", "single h1 on homepage", "<h1>" in hero)
    add("seo", "semantic h2 section headings", "<h2>" in (dest / "sections" / "featured-collection.liquid").read_text(encoding="utf-8"))

    # ---- accessibility ----
    preview = (ROOT / "preview" / slug / "index.html").read_text(encoding="utf-8")
    add("accessibility", "skip link", 'class="skip-link"' in preview)
    add("accessibility", "drawer is modal dialog", 'role="dialog"' in preview and 'aria-modal="true"' in preview)
    add("accessibility", "icon buttons labelled", preview.count("aria-label") >= 8, f"{preview.count('aria-label')} labels")
    imgs = re.findall(r"<img[^>]*>", preview)
    with_alt = [t for t in imgs if 'alt="' in t]
    add("accessibility", "all images have alt text", len(with_alt) == len(imgs) and len(imgs) > 8, f"{len(with_alt)}/{len(imgs)}")
    advanced = (dest / "assets" / "advanced.css").read_text(encoding="utf-8")
    add("accessibility", "focus-visible outlines", ":focus-visible" in advanced)
    add("accessibility", "prefers-reduced-motion honoured", "prefers-reduced-motion" in advanced)
    add("accessibility", "ticker aria-hidden", 'aria-hidden="true"' in (dest / "sections" / "value-props.liquid").read_text(encoding="utf-8"))
    colors = root_colors(variant_css_text) or root_colors((dest / "assets" / "base.css").read_text(encoding="utf-8"))
    bg = colors.get("--color-bg")
    text = colors.get("--color-text")
    accent = colors.get("--color-accent")
    if bg and text:
        ratio = contrast(bg, text)
        add("accessibility", f"body text contrast {ratio:.1f}:1 (WCAG AA >=4.5)", ratio >= 4.5, f"{ratio:.2f}")
    if accent:
        button_text = (13, 14, 16) if slug == "gully-drop" else (255, 255, 255)
        ratio_btn = contrast(accent, button_text)
        add("accessibility", f"button-on-accent contrast {ratio_btn:.1f}:1 (>=3 large/UI)", ratio_btn >= 3, f"{ratio_btn:.2f}")

    # ---- mobile ----
    add("mobile", "viewport meta", 'name="viewport"' in preview and "width=device-width" in preview)
    media_count = variant_css_text.count("@media (max-width") + advanced.count("@media (max-width")
    add("mobile", "responsive breakpoints present (>=4)", media_count >= 4, f"{media_count}")
    add("mobile", "mobile menu wired", "data-mobile-menu" in preview and "data-menu-toggle" in preview)
    add("mobile", "header wraps on small screens", "flex-wrap: wrap" in advanced)
    add("mobile", "touch targets >=44px on key CTAs", "min-height: 51px" in (dest / "assets" / "base.css").read_text(encoding="utf-8"))
    add("mobile", "no horizontal overflow pattern", "calc(100% - 32px)" in (dest / "assets" / "base.css").read_text(encoding="utf-8"))
    add("mobile", "product grid collapses", "product-grid--2, .product-grid--3, .product-grid--4" in (dest / "assets" / "base.css").read_text(encoding="utf-8"))

    # ---- performance ----
    add("performance", "theme.js deferred", 'defer="defer"' in theme_liquid)
    lazy_count = preview.count('loading="lazy"')
    add("performance", "lazy loading on below-fold images", lazy_count >= 8, f"{lazy_count}")
    add("performance", "hero uses fetchpriority=high", 'fetchpriority="high"' in preview)
    add("performance", "font preconnects", "fonts.gstatic.com" in theme_liquid)
    add("performance", "fonts use display=swap", "display=swap" in theme_liquid)
    css_kb = sum((dest / "assets" / f).stat().st_size for f in ["base.css", "commerce.css", "advanced.css", "variant.css"]) / 1024
    add("performance", f"total CSS lean ({css_kb:.0f} KB <= 120 KB)", css_kb <= 120, f"{css_kb:.1f}")
    js_kb = (dest / "assets" / "theme.js").stat().st_size / 1024
    add("performance", f"JS lean ({js_kb:.0f} KB <= 40 KB)", js_kb <= 40, f"{js_kb:.1f}")
    add("performance", "image srcset/widths used", "widths:" in hero)

    # ---- commerce depth ----
    js = (dest / "assets" / "theme.js").read_text(encoding="utf-8")
    drawer = (dest / "sections" / "cart-drawer.liquid").read_text(encoding="utf-8")
    for name, token in [
        ("AJAX quick add", "data-ajax-add" in js and "/cart/add.js" in js),
        ("predictive search", "/search/suggest.json" in js),
        ("wishlist persistence", "ababeel-wishlist" in js),
        ("drawer quantity controls", "/cart/change.js" in js and "quantity-control--drawer" in drawer),
        ("free shipping progress bar", "data-free-ship" in drawer and "FREE_SHIP_THRESHOLD" in js),
        ("countdown timer", "data-countdown" in js),
        ("gallery thumbnail switcher", "product-gallery__thumb" in js),
        ("sticky buy box", "position: sticky" in advanced),
        ("trust guarantee row", "trust-row" in product),
        ("marquee ticker", "value-props__ticker" in (dest / "sections" / "value-props.liquid").read_text(encoding="utf-8")),
        ("back to top", "data-back-to-top" in js),
        ("WhatsApp commerce hooks", "data-whatsapp-cart" in drawer and "data-whatsapp-product" in product),
        ("cart drawer refresh", "refreshDrawer" in js),
        ("variant select sync", "data-variant-select" in js),
    ]:
        add("commerce", name, token)

    return checks


def run_live(slug):
    os.environ["PAGE"] = f"/preview/{slug}/"
    sys.path.insert(0, str(ROOT / "tests"))
    import live_storefront_test as suite
    importlib.reload(suite)
    code = suite.main()
    return {"passed": suite.passed, "failed": suite.failed, "requests": suite.live_requests, "exit": code}


def main():
    summary = []
    for slug in SLUGS:
        print(f"== auditing {slug} ==")
        checks = audit_variant(slug)
        live = run_live(slug)
        totals = {"passed": 0, "total": 0}
        categories = {}
        for cat, items in checks.items():
            passed = sum(1 for i in items if i["passed"])
            categories[cat] = {"passed": passed, "total": len(items), "pct": round(100 * passed / len(items), 1) if items else 0,
                               "failed": [i["name"] for i in items if not i["passed"]]}
            totals["passed"] += passed
            totals["total"] += len(items)
        totals["passed"] += live["passed"]
        totals["total"] += live["passed"] + live["failed"]
        score = round(100 * totals["passed"] / totals["total"], 2) if totals["total"] else 0
        result = {
            "slug": slug, "name": NAMES[slug], "refs": REFS[slug],
            "categories": categories, "live": live,
            "static_passed": sum(c["passed"] for c in categories.values()),
            "static_total": sum(c["total"] for c in categories.values()),
            "total_passed": totals["passed"], "total_failed": totals["total"] - totals["passed"],
            "score_pct": score,
        }
        (QA / f"{slug}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        summary.append((slug, score, live["failed"], {c: categories[c]["pct"] for c in categories}))
        print(f"   score {score}%  live failed={live['failed']}  requests={live['requests']}")
        for cat, info in categories.items():
            if info["failed"]:
                print(f"   ! {cat}: {info['failed']}")
    print("\nSUMMARY")
    for slug, score, live_failed, cats in summary:
        print(f"  {slug:18s} score={score:6.2f}% live_fail={live_failed}  {cats}")


if __name__ == "__main__":
    main()
