#!/usr/bin/env python3
"""Build 5 radically different Ababeel Fashions Shopify theme variants.

Concepts (from market research on Indian + global fashion ecommerce):
 1 heritage-royale  - editorial Indian heritage luxury (Sabyasachi / FabIndia / Manyavar / Net-A-Porter)
 2 bazaar-pop       - high-energy marketplace retail (AJIO / Myntra / Nykaa Fashion / Bewakoof)
 3 atelier-blanc    - quiet-luxury minimalism (Zara / COS / The Row / Toteme / Arket)
 4 gully-drop       - dark streetwear drop culture (Supreme / Kith / Palace / Souled Store / 5PM Hustle)
 5 meadow-muse      - soft botanical boho (Anthropologie / Free People / Glossier / Everlane warmth)
"""
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "shopify-theme"
BUILD = ROOT / "build" / "variants"
OUT = ROOT / "deliverables"

GOOGLE = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'

VARIANTS = [
    # ---------------------------------------------------------------- 1
    dict(
        n=1, slug="heritage-royale", name="Ababeel Heritage Royale",
        refs="Sabyasachi, FabIndia, Manyavar, Net-A-Porter editorial",
        fonts=GOOGLE + '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Mulish:wght@400;600;700;800&display=swap" rel="stylesheet">',
        order=["hero_PAPfyK", "promises", "featured", "story", "categories", "promo", "instagram", "newsletter"],
        hero=dict(
            eyebrow="The Heritage Edit · Festive 2026",
            heading="Woven for the moments that matter.",
            text="<p>Hand-picked ethnic elegance from our Kerala home to yours — heirloom-worthy kurtis, sets and occasion wear.</p>",
            button_label="Discover the collection",
            secondary_label="Book custom tailoring",
            note="Heirloom fabrics · Sizes M–XXL · All-India delivery",
        ),
        featured=dict(eyebrow="Curated this week", heading="Pieces with a pedigree."),
        css="""
:root {
  --color-bg: #f5eddd; --color-surface: #fbf6ea; --color-text: #2b1a12; --color-muted: #7d6a58;
  --color-line: #e0d3b8; --color-accent: #6d1f2c; --color-accent-light: #a06b32; --color-gold: #b98a3e;
  --serif: 'Cormorant Garamond', Georgia, serif; --sans: 'Mulish', ui-sans-serif, system-ui, sans-serif; --radius: 0px;
}
body { background-image: radial-gradient(rgba(185,138,62,.07) 1px, transparent 1px); background-size: 22px 22px; }
h1, h2 { font-weight: 500; }
.commerce-utility { background: #6d1f2c; }
.commerce-header { background: rgba(251,246,234,.97); }
.logo-mark { border-color: #b98a3e; color: #6d1f2c; }
.logo-wordmark { font-size: 30px; color: #6d1f2c; }
.commerce-nav a { letter-spacing: .22em; font-size: 9.5px; }
.commerce-nav a::after { background: #b98a3e; }
.eyebrow { color: #b98a3e; letter-spacing: .28em; }
.eyebrow::before, .eyebrow::after { content: "✦"; margin: 0 8px; font-size: 8px; vertical-align: 2px; }
.hero-section { padding: 92px 0 110px; }
.hero-section__grid { grid-template-columns: 1fr; gap: 64px; text-align: center; }
.hero-copy { padding: 0; max-width: 860px; margin: 0 auto; }
.hero-copy h1 { color: #6d1f2c; }
.hero-copy__text { margin: 0 auto 34px; }
.hero-actions { justify-content: center; }
.hero-note { justify-content: center; }
.button { letter-spacing: .26em; border-radius: 0; }
.button--dark { background: #6d1f2c; border: 1px solid #6d1f2c; }
.button--dark:hover { background: #521621; }
.text-link { color: #6d1f2c; }
.hero-media { height: min(720px, 80vw); }
.hero-media::after { inset: 14px; border: 1px solid #b98a3e; outline: 1px solid rgba(185,138,62,.4); outline-offset: 5px; }
.hero-media__stamp { width: 118px; height: 118px; display: grid; place-items: center; text-align: center; border-radius: 50%; background: #6d1f2c; color: #f5eddd; border: 1px solid #b98a3e; font-size: 15px; transform: rotate(-8deg); }
.section-heading h2 { color: #6d1f2c; }
.product-card { border: 1px solid #e0d3b8; background: #fbf6ea; padding: 10px 10px 14px; }
.product-card__info h3 a { font-family: var(--serif); font-size: 18px; }
.product-badge { border-radius: 0; background: #6d1f2c; }
.shop-category-card { border-radius: 0; }
.shop-category-card__content h3 { font-family: var(--serif); font-size: 27px; font-weight: 500; }
.value-prop__icon { border-color: #b98a3e; color: #6d1f2c; }
.value-props { background: #fbf6ea; }
.promo-banner__inner { background: #6d1f2c; outline: 1px solid #b98a3e; outline-offset: -10px; }
.brand-story__label { background: #6d1f2c; color: #f5eddd; }
.instagram-tile { border-radius: 0; }
.newsletter-card { background: #fbf6ea; border: 1px solid #b98a3e; border-radius: 0; }
.site-footer { background: #47141d; }
.site-footer, .site-footer a, .site-footer p { color: #e9dcc3; }
.footer-column h3 { color: #b98a3e; }
.footer-logo .logo-wordmark { color: #f5eddd; }
.empty-collection { border-color: #b98a3e; }
""",
    ),
    # ---------------------------------------------------------------- 2
    dict(
        n=2, slug="bazaar-pop", name="Ababeel Bazaar Pop",
        refs="AJIO, Myntra, Nykaa Fashion, Bewakoof",
        fonts=GOOGLE + '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800;900&display=swap" rel="stylesheet">',
        order=["hero_PAPfyK", "categories", "featured", "promises", "promo", "instagram", "newsletter"],
        hero=dict(
            eyebrow="MEGA DROP LIVE NOW",
            heading="New drop. Zero chill. All style.",
            text="<p>Fresh festive fits for women & kids — COD at your door, anywhere in India, in 3–7 days.</p>",
            button_label="Shop the drop",
            secondary_label="Grab sale deals",
            note="COD available · Free shipping over ₹999 · Easy exchange",
        ),
        featured=dict(eyebrow="TRENDING NOW", heading="Bestsellers selling fast."),
        css="""
:root {
  --color-bg: #f6f7fb; --color-surface: #ffffff; --color-text: #12142b; --color-muted: #5c6072;
  --color-line: #e3e6f0; --color-accent: #f22c6d; --color-accent-light: #6a5cff; --color-gold: #ffb100;
  --serif: 'Archivo', ui-sans-serif, system-ui, sans-serif; --sans: 'Archivo', ui-sans-serif, system-ui, sans-serif; --radius: 14px;
}
h1, h2 { font-family: var(--serif); font-weight: 900; letter-spacing: -.02em; line-height: 1.02; }
h1 { font-size: clamp(44px, 5.6vw, 78px); }
.commerce-utility { background: #12142b; color: #fff; font-weight: 700; }
.commerce-utility__links { color: #aab0d0; }
.commerce-header { background: #fff; border-bottom: 2px solid #12142b; }
.logo-wordmark { font-family: var(--serif); font-weight: 900; color: #12142b; }
.logo-mark { border: 2px solid #f22c6d; color: #f22c6d; font-weight: 700; }
.commerce-search input { border-radius: 999px; border: 2px solid #12142b; background: #fff; height: 46px; }
.commerce-search button { top: 4px; right: 4px; width: 38px; height: 38px; background: #f22c6d; border-radius: 50%; color: #fff; }
.commerce-nav-wrap { border: 0; background: #12142b; }
.commerce-nav a { color: #fff; }
.commerce-nav a::after { background: #ffb100; }
.commerce-nav .commerce-nav__sale { color: #ffb100; }
.eyebrow { color: #f22c6d; font-weight: 800; letter-spacing: .14em; }
.hero-section { padding: 44px 0 64px; }
.hero-section__grid { gap: 44px; }
.hero-copy h1 { color: #12142b; }
.button { border-radius: 12px; border: 2px solid #12142b; box-shadow: 4px 4px 0 #12142b; font-weight: 800; letter-spacing: .04em; }
.button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0 #12142b; }
.button--dark { background: #f22c6d; color: #fff; }
.button--dark:hover { background: #d81b58; }
.button--light { background: #ffb100; color: #12142b; }
.text-link { color: #6a5cff; font-weight: 800; }
.hero-media { border-radius: 24px; }
.hero-media::after { display: none; }
.hero-media__stamp { background: #ffb100; color: #12142b; font-family: var(--serif); font-weight: 800; font-size: 16px; border-radius: 14px; transform: rotate(5deg); }
.product-card { background: #fff; border: 1px solid #e3e6f0; border-radius: 18px; overflow: hidden; box-shadow: 0 8px 22px rgba(18,20,43,.07); }
.product-card__info h3 a { font-weight: 700; }
.product-badge { background: #ffb100; color: #12142b; border-radius: 999px; font-weight: 800; }
.shop-category-card { border-radius: 22px; }
.shop-category-card__content h3 { font-family: var(--serif); font-weight: 800; }
.value-props { background: #fff; border-top: 2px solid #12142b; border-bottom: 2px solid #12142b; }
.value-prop__icon { background: #f22c6d; border: 0; color: #fff; }
.promo-banner__inner { background: linear-gradient(120deg, #f22c6d, #6a5cff); border-radius: 26px; color: #fff; }
.brand-story__media { border-radius: 24px; }
.instagram-tile { border-radius: 16px; }
.newsletter-card { background: #12142b; color: #fff; border-radius: 26px; }
.newsletter-card p { color: #c9cde0; }
.site-footer { background: #12142b; }
.site-footer, .site-footer a, .site-footer p { color: #c9cde0; }
.footer-column h3 { color: #ffb100; }
""",
    ),
    # ---------------------------------------------------------------- 3
    dict(
        n=3, slug="atelier-blanc", name="Ababeel Atelier Blanc",
        refs="Zara, COS, The Row, Toteme, Arket",
        fonts=GOOGLE + '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600&display=swap" rel="stylesheet">',
        order=["hero_PAPfyK", "featured", "categories", "story", "newsletter"],
        hero=dict(
            eyebrow="Autumn / Winter 2026",
            heading="Quiet pieces, considered well.",
            text="<p>A small, careful edit of ethnic essentials. Nothing loud. Nothing extra.</p>",
            button_label="View the edit",
            secondary_label="Lookbook",
            note="Natural fabrics · Limited runs · India-wide delivery",
        ),
        featured=dict(eyebrow="The edit", heading="Fewer, better pieces."),
        css="""
:root {
  --color-bg: #fbfbfa; --color-surface: #ffffff; --color-text: #191919; --color-muted: #8b877e;
  --color-line: #e8e6e0; --color-accent: #191919; --color-accent-light: #8b877e; --color-gold: #b3ada1;
  --serif: 'Manrope', ui-sans-serif, system-ui, sans-serif; --sans: 'Manrope', ui-sans-serif, system-ui, sans-serif; --radius: 0px;
}
body { font-size: 14px; letter-spacing: .01em; }
h1, h2 { font-family: var(--serif); font-weight: 200; letter-spacing: -.03em; }
h1 { font-size: clamp(52px, 7vw, 96px); }
.section-spacing { padding: 140px 0; }
.commerce-utility { background: #fbfbfa; color: #8b877e; border-bottom: 1px solid #e8e6e0; }
.commerce-utility__links { color: #8b877e; }
.commerce-utility__links a { color: #191919; }
.commerce-header { background: #fbfbfa; border-bottom: 0; }
.logo-wordmark { font-weight: 300; letter-spacing: .02em; color: #191919; }
.logo-mark { border-color: #191919; color: #191919; }
.commerce-search input { border: 0; border-bottom: 1px solid #191919; border-radius: 0; background: transparent; }
.commerce-nav-wrap { border: 0; }
.commerce-nav a { font-weight: 500; letter-spacing: .2em; font-size: 9.5px; }
.commerce-nav a::after { background: #191919; height: 1px; }
.eyebrow { color: #8b877e; letter-spacing: .32em; font-weight: 600; }
.hero-section { padding: 120px 0; }
.hero-copy h1 { color: #191919; }
.hero-copy__text { font-size: 15px; }
.button { background: transparent; color: #191919; border: 0; border-bottom: 1px solid #191919; border-radius: 0; min-height: 34px; padding: 0 2px; letter-spacing: .24em; font-weight: 500; }
.button:hover { transform: none; opacity: .55; }
.button--dark, .button--outline, .button--light { background: transparent; color: #191919; border: 0; border-bottom: 1px solid #191919; }
.text-link { color: #191919; font-weight: 500; }
.hero-media { height: min(760px, 70vw); }
.hero-media::after { display: none; }
.hero-media__stamp { display: none; }
.product-card__image { filter: grayscale(.12); }
.product-card__info h3 a { font-weight: 400; letter-spacing: 0; }
.product-badge { border-radius: 0; background: #191919; }
.shop-category-card { border-radius: 0; }
.shop-category-card__content h3 { font-weight: 300; letter-spacing: .06em; text-transform: uppercase; font-size: 21px; }
.value-props { border: 0; background: #fbfbfa; }
.value-prop { border-right: 0; padding: 34px 20px; }
.value-prop__icon { border: 0; width: auto; height: auto; color: #8b877e; font-size: 13px; }
.value-prop h3 { font-weight: 400; }
.promo-banner__inner { background: #f4f2ec; color: #191919; border: 1px solid #e8e6e0; }
.promo-banner .button--light { color: #191919; }
.brand-story__label { background: #191919; }
.instagram-tile { border-radius: 0; }
.newsletter-card { background: #fff; border: 1px solid #e8e6e0; border-radius: 0; }
.site-footer { background: #fbfbfa; border-top: 1px solid #e8e6e0; }
.site-footer, .site-footer a, .site-footer p { color: #191919; }
.footer-column h3 { color: #8b877e; }
.floating-whatsapp { border-radius: 0; }
""",
    ),
    # ---------------------------------------------------------------- 4
    dict(
        n=4, slug="gully-drop", name="Ababeel Gully Drop",
        refs="Supreme, Kith, Palace, The Souled Store, 5PM Hustle",
        fonts=GOOGLE + '<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">',
        order=["hero_PAPfyK", "featured", "promo", "categories", "instagram", "newsletter"],
        hero=dict(
            eyebrow="DROP 04 — LIVE",
            heading="Street-ready festive heat.",
            text="<p>Limited festive fits. When they're gone, they're gone. COD across India.</p>",
            button_label="Cop the drop",
            secondary_label="Peep the sale",
            note="Limited stock · All-India shipping · WhatsApp support",
        ),
        featured=dict(eyebrow="HEAT CHECK", heading="Most-wanted pieces."),
        css="""
:root {
  --color-bg: #0d0e10; --color-surface: #15171b; --color-text: #f2f1ea; --color-muted: #9d9f98;
  --color-line: #2a2d33; --color-accent: #ccff00; --color-accent-light: #8f7bff; --color-gold: #ff5c1f;
  --serif: 'Bebas Neue', 'Arial Narrow', sans-serif; --sans: 'Space Grotesk', ui-sans-serif, system-ui, sans-serif; --radius: 0px;
}
body { background: #0d0e10; color: #f2f1ea; }
h1, h2 { font-family: var(--serif); letter-spacing: .02em; line-height: .92; }
h1 { font-size: clamp(72px, 9.5vw, 148px); color: #f2f1ea; }
h2 { font-size: clamp(48px, 6vw, 88px); }
h3 { font-family: var(--sans); }
.skip-link { background: #ccff00; color: #0d0e10; }
.commerce-utility { background: #ccff00; color: #0d0e10; font-weight: 700; }
.commerce-utility__links { color: #0d0e10; }
.commerce-utility__links a { color: #0d0e10; border-color: #0d0e10; }
.commerce-header { background: #0d0e10; }
.logo-wordmark { font-family: var(--serif); font-size: 30px; letter-spacing: .08em; color: #f2f1ea; }
.logo-mark { border-color: #ccff00; color: #ccff00; border-radius: 0; }
.commerce-search input { background: #15171b; border: 1px solid #2a2d33; color: #f2f1ea; border-radius: 0; }
.commerce-action { color: #f2f1ea; }
.commerce-action:hover { color: #ccff00; }
.commerce-nav-wrap { border-top: 1px solid #2a2d33; border-bottom: 1px solid #2a2d33; background: #0d0e10; }
.commerce-nav a { color: #f2f1ea; }
.commerce-nav a::after { background: #ccff00; }
.commerce-nav .commerce-nav__sale { color: #ff5c1f; }
.eyebrow { color: #ccff00; letter-spacing: .3em; }
.text-link { color: #ccff00; }
.hero-section { padding: 0 0 40px; }
.hero-section__grid { grid-template-columns: 1fr; gap: 0; }
.hero-media { order: -1; height: min(76vh, 700px); min-height: 500px; }
.hero-media::after { display: none; }
.hero-copy { padding: 0; margin-top: -110px; position: relative; z-index: 2; }
.hero-copy h1 { color: #ccff00; text-transform: uppercase; }
.hero-copy__text { display: inline-block; background: rgba(13,14,16,.82); color: #f2f1ea; padding: 10px 14px; }
.hero-actions .button--dark { background: #ccff00; color: #0d0e10; transform: skewX(-8deg); font-weight: 700; }
.hero-actions .button--dark:hover { background: #ccff00; transform: skewX(-8deg) translateY(-2px); }
.hero-note { color: #f2f1ea; }
.hero-media__stamp { background: #ff5c1f; color: #0d0e10; font-family: var(--serif); font-size: 26px; letter-spacing: .05em; border: 2px solid #0d0e10; transform: rotate(6deg); }
.product-card { background: #15171b; }
.product-card__info h3 a { font-family: var(--sans); font-weight: 600; color: #f2f1ea; }
.product-card__price, .product-card__price .price { color: #ccff00; }
.product-badge { background: #ccff00; color: #0d0e10; border-radius: 0; font-weight: 700; }
.product-card__quick { background: #ccff00; color: #0d0e10; border-radius: 0; }
.shop-category-card { border-radius: 0; border: 1px solid #2a2d33; }
.shop-category-card__content h3 { font-family: var(--serif); font-size: 36px; letter-spacing: .04em; }
.value-props { background: #0d0e10; border-color: #2a2d33; }
.value-prop { border-color: #2a2d33; }
.value-prop h3 { color: #f2f1ea; }
.value-prop__icon { border-color: #ccff00; color: #ccff00; border-radius: 0; }
.promo-banner__inner { background: #ccff00; color: #0d0e10; }
.promo-banner__inner h2, .promo-banner__inner p { color: #0d0e10; }
.promo-banner .eyebrow { color: #0d0e10; }
.promo-banner .button--light { background: #0d0e10; color: #ccff00; }
.brand-story__label { background: #ccff00; color: #0d0e10; }
.instagram-tile { border-radius: 0; }
.newsletter-card { background: #15171b; border: 1px solid #2a2d33; border-radius: 0; color: #f2f1ea; }
.newsletter-card p { color: #9d9f98; }
.newsletter-form input { background: #0d0e10; border-color: #2a2d33; color: #f2f1ea; border-radius: 0; }
.site-footer { background: #000; border-top: 2px solid #ccff00; }
.site-footer, .site-footer a, .site-footer p { color: #9d9f98; }
.footer-column h3, .footer-logo .logo-wordmark { color: #f2f1ea; }
.empty-collection { background: #15171b; }
.empty-collection h3, .empty-collection p { color: #f2f1ea; }
""",
    ),
    # ---------------------------------------------------------------- 5
    dict(
        n=5, slug="meadow-muse", name="Ababeel Meadow & Muse",
        refs="Anthropologie, Free People, Glossier, Everlane",
        fonts=GOOGLE + '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Karla:wght@400;500;700&family=Caveat:wght@600&display=swap" rel="stylesheet">',
        order=["hero_PAPfyK", "categories", "featured", "story", "promises", "instagram", "newsletter"],
        hero=dict(
            eyebrow="the gentle edit",
            heading="Softness you can wear every day.",
            text="<p>Breathable cottons, dreamy drapes and little joys for kids — chosen with love in Kerala.</p>",
            button_label="Browse gently",
            secondary_label="Our story",
            note="Skin-friendly fabrics · Made with care · Delivered across India",
        ),
        featured=dict(eyebrow="little joys", heading="The pieces we can't stop wearing."),
        css="""
:root {
  --color-bg: #fdf9f2; --color-surface: #fffdf8; --color-text: #40382e; --color-muted: #8a7f6d;
  --color-line: #eee2cf; --color-accent: #7d8c6f; --color-accent-light: #cf8266; --color-gold: #c9704f;
  --serif: 'Fraunces', Georgia, serif; --sans: 'Karla', ui-sans-serif, system-ui, sans-serif; --radius: 18px;
}
body::before { content: ''; position: fixed; inset: 0; z-index: -1; pointer-events: none;
  background: radial-gradient(620px 420px at 88% 6%, rgba(207,130,102,.13), transparent 62%),
              radial-gradient(720px 520px at 6% 32%, rgba(125,140,111,.15), transparent 62%); }
h1, h2 { font-family: var(--serif); font-weight: 500; letter-spacing: -.02em; }
.eyebrow { color: #7d8c6f; letter-spacing: .18em; text-transform: lowercase; }
.eyebrow::before { content: '✿ '; color: #c9704f; }
.commerce-utility { background: #7d8c6f; color: #fdf9f2; }
.commerce-header { background: rgba(255,253,248,.96); }
.logo-wordmark { color: #7d8c6f; }
.logo-mark { border-color: #c9704f; color: #c9704f; }
.commerce-search input { border-radius: 999px; border: 1px solid #eee2cf; background: #fff; }
.commerce-nav a { color: #40382e; }
.commerce-nav a::after { background: #c9704f; }
.commerce-nav .commerce-nav__sale { color: #c9704f; }
.text-link { color: #c9704f; }
.hero-section { padding: 84px 0 96px; }
.hero-copy h1 { color: #40382e; }
.hero-note__dot { background: #c9704f; box-shadow: 0 0 0 5px rgba(201,112,79,.15); }
.button { border-radius: 999px; min-height: 52px; letter-spacing: .06em; }
.button--dark { background: #7d8c6f; }
.button--dark:hover { background: #66755a; }
.hero-media { border-radius: 999px 999px 26px 26px; height: min(680px, 66vw); }
.hero-media::after { inset: 12px; border-color: rgba(255,255,255,.75); border-radius: 999px 999px 18px 18px; }
.hero-media__stamp { font-family: 'Caveat', cursive; font-size: 25px; background: #c9704f; color: #fff; border-radius: 18px; transform: rotate(-6deg); }
.product-card__media { display: block; border-radius: 22px; overflow: hidden; }
.product-card__info h3 a { font-family: var(--serif); font-size: 17px; }
.product-badge { border-radius: 999px; background: #7d8c6f; }
.shop-category-card { border-radius: 999px 999px 24px 24px; }
.shop-category-card__content h3 { font-family: var(--serif); font-size: 25px; }
.value-prop__icon { border-color: #c9704f; color: #7d8c6f; background: #fff; }
.promo-banner__inner { background: #7d8c6f; border-radius: 30px; color: #fff; }
.brand-story__media { border-radius: 26px; }
.brand-story__label { background: #c9704f; color: #fff; }
.instagram-tile { border-radius: 20px; }
.newsletter-card { background: #fff; border: 1px solid #eee2cf; border-radius: 30px; }
.site-footer { background: #37423a; }
.site-footer, .site-footer a, .site-footer p { color: #e9e4d6; }
.footer-column h3 { color: #cf8266; }
""",
    ),
]


PREMIUM = {
    "heritage-royale": """
.value-props__ticker { display: block; }
.value-props__ticker-track { animation: none; width: auto; flex-wrap: wrap; justify-content: center; gap: 8px 28px; padding: 12px 16px; }
.value-props__ticker-track span { color: #6d1f2c; }
.countdown strong { font-family: var(--serif); color: #6d1f2c; font-size: 24px; }
.free-ship-progress__track span { background: #b98a3e; }
.trust-row li span { color: #b98a3e; }
.product-gallery__thumb { border-radius: 0; }
.back-to-top { border-radius: 0; border-color: #b98a3e; color: #6d1f2c; }
""",
    "bazaar-pop": """
.value-props__ticker { display: block; background: #ffb100; border-top: 2px solid #12142b; }
.value-props__ticker-track span { color: #12142b; font-weight: 800; }
.countdown strong { color: #f22c6d; font-weight: 900; }
.free-ship-progress__track span { background: linear-gradient(90deg, #f22c6d, #6a5cff); }
.trust-row li { border: 2px solid #12142b; border-radius: 999px; padding: 6px 12px; background: #fff; color: #12142b; }
.product-gallery__thumb { border-radius: 10px; }
.back-to-top { border-radius: 12px; border: 2px solid #12142b; box-shadow: 3px 3px 0 #12142b; }
""",
    "atelier-blanc": """
.countdown strong { font-weight: 200; letter-spacing: .3em; }
.free-ship-progress__track { height: 2px; border-radius: 0; }
.free-ship-progress__track span { background: #191919; border-radius: 0; }
.trust-row li { font-weight: 400; letter-spacing: .18em; }
.product-gallery__thumb { border-radius: 0; }
.back-to-top { border-radius: 0; border-color: #191919; color: #191919; }
.quantity-control--drawer { border-radius: 0; }
""",
    "gully-drop": """
.value-props__ticker { display: block; background: #ccff00; border-top: 1px solid #0d0e10; }
.value-props__ticker-track span { color: #0d0e10; font-weight: 700; }
.countdown strong { font-family: var(--serif); color: #ccff00; font-size: 30px; }
.free-ship-progress__track span { background: #ccff00; }
.trust-row li { color: #f2f1ea; }
.trust-row li span { color: #ccff00; }
.product-gallery__thumb { border-radius: 0; border-color: #2a2d33; }
.back-to-top { border-radius: 0; background: #15171b; border-color: #ccff00; color: #ccff00; }
.quantity-control--drawer { border-color: #2a2d33; }
""",
    "meadow-muse": """
.value-props__ticker { display: block; }
.value-props__ticker-track { animation-duration: 40s; }
.value-props__ticker-track span { color: #7d8c6f; }
.countdown strong { font-family: var(--serif); color: #c9704f; }
.free-ship-progress__track span { background: #7d8c6f; }
.trust-row li { color: #8a7f6d; }
.product-gallery__thumb { border-radius: 12px; }
.back-to-top { background: #7d8c6f; border: 0; color: #fff; }
""",
}


def build_variant(v):
    dest = BUILD / v["slug"]
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(SRC, dest)

    # 1. variant css (concept + premium component styling)
    (dest / "assets" / "variant.css").write_text(v["css"] + PREMIUM[v["slug"]], encoding="utf-8")

    # 1b. per-variant static preview snapshot for the live test matrix
    snapshot = (ROOT / "preview" / "index.html").read_text(encoding="utf-8")
    snapshot = snapshot.replace('<body class="template-index">', f'<body class="theme-{v["slug"]} template-index">')
    snapshot = snapshot.replace(
        '<link rel="stylesheet" href="/shopify-theme/assets/advanced.css">',
        '<link rel="stylesheet" href="/shopify-theme/assets/advanced.css">\n  '
        + v["fonts"]
        + f'\n  <link rel="stylesheet" href="/build/variants/{v["slug"]}/assets/variant.css">',
    )
    preview_dir = ROOT / "preview" / v["slug"]
    preview_dir.mkdir(parents=True, exist_ok=True)
    (preview_dir / "index.html").write_text(snapshot, encoding="utf-8")

    # 2. theme.liquid: fonts + variant.css + body class
    tl = (dest / "layout" / "theme.liquid").read_text(encoding="utf-8")
    anchor = "{{ 'advanced.css' | asset_url | stylesheet_tag }}"
    assert anchor in tl
    tl = tl.replace(anchor, anchor + "\n    {{ 'variant.css' | asset_url | stylesheet_tag }}\n    " + v["fonts"])
    tl = tl.replace('<body class="template-', '<body class="theme-' + v["slug"] + ' template-')
    (dest / "layout" / "theme.liquid").write_text(tl, encoding="utf-8")

    # 3. settings_schema: theme name
    ss = json.loads((dest / "config" / "settings_schema.json").read_text(encoding="utf-8"))
    ss[0]["theme_name"] = v["name"]
    ss[0]["theme_version"] = "3.0-" + v["slug"]
    (dest / "config" / "settings_schema.json").write_text(json.dumps(ss, indent=2, ensure_ascii=False), encoding="utf-8")

    # 4. index.json: order + hero + featured copy
    idx = json.loads((dest / "templates" / "index.json").read_text(encoding="utf-8"))
    idx["order"] = v["order"]
    hero = idx["sections"]["hero_PAPfyK"]["settings"]
    for k, val in v["hero"].items():
        hero[k] = val
    idx["sections"]["featured"]["settings"].update(v["featured"])
    (dest / "templates" / "index.json").write_text(json.dumps(idx, indent=2, ensure_ascii=False), encoding="utf-8")

    # 5. zip
    OUT.mkdir(parents=True, exist_ok=True)
    zpath = OUT / f"ababeel-theme-{v['n']}-{v['slug']}.zip"
    if zpath.exists():
        zpath.unlink()
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(dest.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(dest).as_posix())
    return zpath


def validate(v):
    zpath = OUT / f"ababeel-theme-{v['n']}-{v['slug']}.zip"
    with zipfile.ZipFile(zpath) as z:
        bad = z.testzip()
        assert bad is None, f"corrupt entry {bad}"
        tl = z.read("layout/theme.liquid").decode("utf-8")
        assert "variant.css" in tl and f'theme-{v["slug"]}' in tl
        idx = json.loads(z.read("templates/index.json"))
        assert set(idx["order"]) <= set(idx["sections"]), "order references missing sections"
        json.loads(z.read("config/settings_schema.json"))
        z.read("assets/variant.css")
    print(f"  ok  {zpath.name}  ({zpath.stat().st_size//1024} KB)  order={len(idx['order'])} sections")


for v in VARIANTS:
    print(f"[{v['n']}/5] building {v['slug']}  (refs: {v['refs']})")
    build_variant(v)
    validate(v)

print("\nALL 5 VARIANT THEMES BUILT + VALIDATED")
