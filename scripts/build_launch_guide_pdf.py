#!/usr/bin/env python3
"""Build the Ababeel Fashions final launch + Meta Ads implementation guide PDF."""
from fpdf import FPDF

DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJAVU_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MAROON = (122, 37, 64)
DARK = (51, 37, 42)
GOLD = (197, 154, 92)
CREAM = (248, 245, 240)
LIGHT = (240, 233, 226)
GREY = (110, 100, 104)

W, H = 210, 297
ML, MR = 14, 14
CW = W - ML - MR


class Guide(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DV", "", DEJAVU)
        self.add_font("DV", "B", DEJAVU_B)
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DV", "B", 7.5)
        self.set_text_color(*GREY)
        self.set_xy(ML, 8)
        self.cell(120, 5, "ABABEEL FASHIONS  •  STORE LAUNCH & META ADS GUIDE")
        self.set_xy(W - MR - 60, 8)
        self.cell(60, 5, "FINAL EDITION  •  OCT 2026", align="R")
        self.set_draw_color(*GOLD)
        self.set_line_width(0.5)
        self.line(ML, 14.5, W - MR, 14.5)
        self.set_y(20)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_font("DV", "", 7.5)
        self.set_text_color(*GREY)
        self.cell(0, 5, f"Ababeel Fashions  •  ababeeltvm.com  •  Page {self.page_no()}", align="C")

    def ensure(self, h):
        if self.get_y() + h > H - 20:
            self.add_page()

    def mheight(self, w, text, lh):
        lines = self.multi_cell(w, lh, text, dry_run=True, output="LINES")
        return max(1, len(lines)) * lh

    def phase(self, num, title):
        self.add_page()
        self.set_font("DV", "B", 9)
        self.set_text_color(*GOLD)
        self.set_xy(ML, self.get_y() + 2)
        self.cell(0, 6, num.upper())
        self.ln(7)
        self.set_font("DV", "B", 16)
        self.set_text_color(*MAROON)
        self.multi_cell(CW, 7.5, title)
        self.set_draw_color(*GOLD)
        self.set_line_width(0.8)
        self.line(ML, self.get_y() + 1.5, ML + 40, self.get_y() + 1.5)
        self.ln(7)

    def h2(self, text):
        self.ensure(14)
        self.ln(2)
        self.set_font("DV", "B", 11)
        self.set_text_color(*MAROON)
        self.set_x(ML)
        self.multi_cell(CW, 6, text)
        self.ln(2)

    def p(self, text, size=9.5, color=DARK, bold=False):
        self.set_font("DV", "B" if bold else "", size)
        self.set_text_color(*color)
        self.set_x(ML)
        self.multi_cell(CW, 5, text)
        self.ln(2.5)

    def step(self, n, text):
        self.set_font("DV", "", 9.5)
        h = self.mheight(CW - 9, text, 5)
        self.ensure(h + 4)
        self.set_font("DV", "B", 9.5)
        self.set_text_color(*MAROON)
        self.set_xy(ML, self.get_y())
        self.cell(9, 5, f"{n}.")
        self.set_xy(ML + 9, self.get_y())
        self.set_font("DV", "", 9.5)
        self.set_text_color(*DARK)
        self.multi_cell(CW - 9, 5, text)
        self.ln(1.8)

    def bullet(self, text, indent=6):
        self.set_font("DV", "", 9)
        h = self.mheight(CW - indent - 5, text, 5)
        self.ensure(h + 3)
        self.set_text_color(*GOLD)
        self.set_xy(ML + indent, self.get_y())
        self.cell(5, 5, "•")
        self.set_xy(ML + indent + 5, self.get_y())
        self.set_text_color(*DARK)
        self.multi_cell(CW - indent - 5, 5, text)
        self.ln(1.2)

    def check(self, text):
        self.set_font("DV", "", 9.5)
        h = self.mheight(CW - 10, text, 5)
        self.ensure(h + 4)
        y = self.get_y()
        self.set_draw_color(*MAROON)
        self.set_line_width(0.4)
        self.rect(ML + 2, y + 0.6, 4.2, 4.2)
        self.set_xy(ML + 10, y)
        self.set_font("DV", "", 9.5)
        self.set_text_color(*DARK)
        self.multi_cell(CW - 10, 5, text)
        self.ln(1.6)

    def note(self, title, text):
        self.set_font("DV", "", 9)
        th = self.mheight(CW - 16, text, 4.8)
        h = th + 12
        self.ensure(h + 4)
        y = self.get_y()
        self.set_fill_color(*CREAM)
        self.rect(ML, y, CW, h, "F")
        self.set_fill_color(*GOLD)
        self.rect(ML, y, 2, h, "F")
        self.set_xy(ML + 7, y + 3)
        self.set_font("DV", "B", 9)
        self.set_text_color(*MAROON)
        self.cell(CW - 16, 5, title)
        self.set_xy(ML + 7, y + 8.5)
        self.set_font("DV", "", 9)
        self.set_text_color(*DARK)
        self.multi_cell(CW - 16, 4.8, text)
        self.set_y(y + h + 4)

    def table(self, head, rows, widths):
        self.set_font("DV", "B", 8.5)
        colh = 6.5
        # header
        self.ensure(colh + 10)
        x = ML
        self.set_fill_color(*MAROON)
        self.set_text_color(255, 255, 255)
        for i, htxt in enumerate(head):
            self.set_xy(x, self.get_y())
            self.cell(widths[i], colh, "  " + htxt, fill=True)
            x += widths[i]
        self.ln(colh)
        # rows
        for r_i, row in enumerate(rows):
            self.set_font("DV", "", 8.5)
            heights = []
            for i, c in enumerate(row):
                heights.append(self.mheight(widths[i] - 4, c, 4.4))
            rh = max(heights) + 3
            self.ensure(rh + 2)
            y = self.get_y()
            if r_i % 2 == 0:
                self.set_fill_color(*LIGHT)
                self.rect(ML, y, sum(widths), rh, "F")
            x = ML
            self.set_text_color(*DARK)
            for i, c in enumerate(row):
                self.set_xy(x + 2, y + 1.8)
                self.multi_cell(widths[i] - 4, 4.4, c)
                x += widths[i]
            self.set_y(y + rh)
        self.ln(4)


pdf = Guide()

# ---------------- COVER ----------------
pdf.add_page()
pdf.set_fill_color(*CREAM)
pdf.rect(0, 0, W, H, "F")
pdf.set_fill_color(*MAROON)
pdf.rect(0, 0, W, 60, "F")
pdf.set_fill_color(*GOLD)
pdf.rect(0, 60, W, 2.2, "F")
pdf.set_xy(ML, 18)
pdf.set_font("DV", "B", 24)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 11, "ABABEEL FASHIONS")
pdf.set_xy(ML, 31)
pdf.set_font("DV", "", 10)
pdf.set_text_color(*GOLD)
pdf.cell(0, 6, "Ambalathara, Thiruvananthapuram, Kerala  •  Modest & elegant fashion")

pdf.set_xy(ML, 82)
pdf.set_font("DV", "B", 21)
pdf.set_text_color(*MAROON)
pdf.multi_cell(150, 10.5, "Complete Store Launch &\nMeta Ads Implementation Guide")
pdf.set_xy(ML, 112)
pdf.set_font("DV", "", 11)
pdf.set_text_color(*DARK)
pdf.multi_cell(160, 6.5, "Every step, in order, from uploading the fixed Shopify theme to running\nprofitable Facebook & Instagram ads for ababeeltvm.com.")

pdf.set_draw_color(*GOLD)
pdf.set_line_width(0.8)
pdf.line(ML, 132, ML + 55, 132)

facts = [
    ("Store", "Ababeel Fashions (Shopify)"),
    ("Domain", "ababeeltvm.com"),
    ("Instagram", "@ababeelfashions2024"),
    ("WhatsApp", "+91 70120 45854"),
    ("Storefront", "English only  •  INR prices"),
    ("Payments", "COD + UPI / online"),
    ("Delivery", "All India, 3-7 working days"),
    ("Edition", "Final  •  October 2026"),
]
y = 140
for k, v in facts:
    pdf.set_xy(ML, y)
    pdf.set_font("DV", "B", 9.5)
    pdf.set_text_color(*MAROON)
    pdf.cell(34, 6, k)
    pdf.set_font("DV", "", 9.5)
    pdf.set_text_color(*DARK)
    pdf.cell(0, 6, v)
    y += 7.2

pdf.set_fill_color(*MAROON)
pdf.rect(0, H - 26, W, 26, "F")
pdf.set_xy(ML, H - 20)
pdf.set_font("DV", "", 8.5)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 6, "Do not spend ad budget until Phase 16 (Master Launch Checklist) is fully ticked.")
pdf.set_xy(ML, H - 13)
pdf.set_text_color(*GOLD)
pdf.cell(0, 6, "Shopify  •  Meta Pixel + Conversions API  •  Catalogue  •  Domain  •  Creative  •  Retargeting")

# ---------------- HOW TO USE ----------------
pdf.phase("Introduction", "How to use this guide")
pdf.p("This guide is the single source of truth for launching Ababeel Fashions online. It covers the website, store settings, products, domain, Meta tracking, testing, and the exact ad account structure to run.", 10)
pdf.h2("Two control rooms")
pdf.bullet("Shopify Admin (yourstore.myshopify.com/admin) - website, products, orders, payments, shipping, policies, domain.")
pdf.bullet("Meta Business Suite / Ads Manager (business.facebook.com, adsmanager) - pixel, domain verification, catalogues, campaigns, results.")
pdf.h2("Rules of the road")
pdf.bullet("Follow the phases in order. Each phase ends with 'Done when' boxes - tick them all before moving on.")
pdf.bullet("Never run paid ads to a password-protected store or to an unfinished homepage.")
pdf.bullet("Test every payment, shipping and tracking step yourself on a phone before customers do.")
pdf.bullet("Keep one Meta pixel. Do not paste extra pixel code into the theme - Shopify's Facebook & Instagram channel already sends Pixel + Conversions API events.")
pdf.bullet("Work in small sessions (20-40 min per phase). The whole build is roughly 2-3 focused days.")
pdf.note("Golden rule", "Meta can only optimise for what it can measure. A verified domain, a connected pixel on MAXIMUM data sharing, and a tested Purchase event matter more than any ad trick.")

# ---------------- STORE PROFILE ----------------
pdf.phase("Profile", "Store profile (decisions already locked)")
pdf.table(
    ["Item", "Locked decision"],
    [
        ["Brand", "Ababeel Fashions - modest, elegant, family-run boutique feel"],
        ["Reference style", "AJIO-like layout, but simpler and faster"],
        ["Theme colour", "Deep maroon (from your old footer) + gold accents on warm cream"],
        ["Language", "English only"],
        ["Currency", "INR (Indian Rupees)"],
        ["Domain", "ababeeltvm.com (primary)"],
        ["Instagram", "instagram.com/ababeelfashions2024 - demo / creative source"],
        ["WhatsApp", "+91 70120 45854 (temporary number, swappable later)"],
        ["Payments", "Cash on Delivery + UPI / cards / netbanking online"],
        ["Delivery promise", "All-India delivery in 3-7 working days"],
        ["Catalogue", "Large launch catalogue: women's ethnic, kids, wedding edit, tailoring"],
        ["Checkout", "Full Shopify checkout (not draft orders / not manual)"],
        ["Ads goal", "Website purchases (Sales objective), plus WhatsApp leads for tailoring"],
    ],
    [45, 137],
)
pdf.note("Why this matters", "Every setting below repeats these locked decisions. If a future choice conflicts with this table, this table wins unless you consciously change it.")

# ---------------- PHASE 1 ----------------
pdf.phase("Phase 1", "Upload & publish the fixed theme")
pdf.p("The package to upload is ababeel-fashions-shopify-theme-v2-fixed.zip (also on the GitHub branch under deliverables/). It contains the corrected homepage template, your saved hero image + collection settings, and all advanced sections.", 9.5)
pdf.step(1, "Open Shopify Admin -> Online Store -> Themes.")
pdf.step(2, "Scroll to 'Theme library', click 'Add theme' -> 'Upload zip file'.")
pdf.step(3, "Select ababeel-fashions-shopify-theme-v2-fixed.zip and wait for the upload to finish.")
pdf.step(4, "A new unpublished theme card appears. On that card click the three dots (...) -> 'Customize' (called 'Edit default theme content' in some accounts - open the editor).")
pdf.step(5, "CRITICAL FIX: at the top centre of the editor a template selector may show '404 page'. Click the arrow next to it and choose 'Home page'. Your old export had accidentally saved the homepage INSIDE the 404 template - the fixed package restores a real Home page template, but the editor can still open on 404 first.")
pdf.step(6, "Confirm the left sidebar lists: Header, Hero, Featured collection, Value props, Shop categories, Brand story, Promo banner, Instagram showcase, Newsletter, Footer, Cart drawer.")
pdf.step(7, "Click the preview (eye) icon - you must see the hero image and sections, NOT the maroon 404 artwork.")
pdf.step(8, "Click Save (top right).")
pdf.step(9, "Back on Online Store -> Themes, on the fixed theme card click ... -> 'Publish' and confirm. It becomes your live theme.")
pdf.step(10, "Open your .myshopify.com address in a private browser window and confirm the homepage loads.")
pdf.h2("Done when")
pdf.check("Fixed zip uploaded as a new theme")
pdf.check("Editor template selector shows 'Home page' with all sections")
pdf.check("Preview shows hero + collections, not the 404 design")
pdf.check("Theme is Published (live)")

# ---------------- PHASE 2 ----------------
pdf.phase("Phase 2", "Customise the homepage in the editor")
pdf.step(1, "Hero section: keep or replace the image; headline 'Elegance, stitched with intention.'; sub-text about modest, elegant outfits curated in Thiruvananthapuram; buttons 'Shop new arrivals' + 'WhatsApp us'.")
pdf.step(2, "Announcement bar: 'ALL-INDIA DELIVERY IN 3-7 DAYS  •  COD AVAILABLE  •  WHATSAPP SUPPORT'.")
pdf.step(3, "Featured collection: set to 'for-front' (your handle). Put your 8-12 best products in that collection later.")
pdf.step(4, "Value props: All-India delivery / COD available / Easy exchange / WhatsApp support.")
pdf.step(5, "Shop categories tiles link to collections created in Phase 8 - keep names: Women, Kids, Wedding edit.")
pdf.step(6, "Brand story: 2-3 honest sentences about Ababeel Fashions, Ambalathara; button to About page.")
pdf.step(7, "Promo banner: current drop or festive edit; link to a collection.")
pdf.step(8, "Instagram showcase: link cards to instagram.com/ababeelfashions2024 posts; button 'Follow @ababeelfashions2024'.")
pdf.step(9, "Newsletter: 'Get first looks at new drops' - connects to Shopify customer list.")
pdf.step(10, "Theme settings (sidebar gear icon): set WhatsApp number, store phone, address, Instagram URL, and brand colours if you ever want to tweak them.")
pdf.note("Save habit", "Click Save after every section. The editor does not warn you about unsaved changes when switching templates.")

# ---------------- PHASE 3 ----------------
pdf.phase("Phase 3", "Core store settings")
pdf.step(1, "Settings -> Store details: legal name, store name 'Ababeel Fashions', address Ambalathara, Thiruvananthapuram, Kerala, India; support email; order-processing phone.")
pdf.step(2, "Settings -> General: confirm store currency is INR.")
pdf.step(3, "Settings -> Languages: keep English only; remove any extra published languages.")
pdf.step(4, "Settings -> Notifications: open the order-confirmation template preview; make sure store name + address appear; add a line like 'Questions? WhatsApp +91 70120 45854' to the footer of customer emails.")
pdf.step(5, "Settings -> Customer privacy: keep it simple - no marketing cookies before consent is fine; the Meta channel handles its own consent-safe events.")
pdf.step(6, "Settings -> Plan: confirm the store is on a paid plan that allows checkout (a store on trial blocks real payments).")
pdf.h2("Done when")
pdf.check("Store details show correct Indian address + contact")
pdf.check("Currency INR, language English")
pdf.check("Plan allows live checkout")

# ---------------- PHASE 4 ----------------
pdf.phase("Phase 4", "Shipping - All-India + COD rules")
pdf.step(1, "Settings -> Shipping and delivery -> General shipping rates.")
pdf.step(2, "Create a zone named 'India' covering the whole country.")
pdf.step(3, "Add rates, e.g.: Flat Rs.79 below Rs.999 order value; FREE at Rs.999+. (Adjust numbers to your margins - the mechanic is what matters.)")
pdf.step(4, "Optionally add a 'Kerala express' zone with a lower rate / faster promise for local orders.")
pdf.step(5, "If you restrict COD (certain pincodes or order values), write the rule in the Shipping policy and repeat it on product pages - never only at checkout.")
pdf.step(6, "Set handling time text used across the site: 'Dispatch in 24-48 hrs, delivery 3-7 working days'.")
pdf.note("COD reality", "COD rejection is your biggest hidden cost. Common rule: COD up to Rs.2,999 order value; above that, prepaid only. Announce it in the announcement bar and policy.")

# ---------------- PHASE 5 ----------------
pdf.phase("Phase 5", "Payments - COD + UPI")
pdf.step(1, "Settings -> Payments.")
pdf.step(2, "Manual payment methods -> activate 'Cash on Delivery (COD)'. Rename the label exactly like that and add the instruction line shown to buyers.")
pdf.step(3, "Online: add a gateway available in India - Razorpay is the usual choice (UPI, cards, netbanking, wallets). Install the Razorpay app or connect via Payments page, complete KYC with your business details.")
pdf.step(4, "Enable UPI explicitly in the gateway dashboard; test a Rs.1 or test-mode payment.")
pdf.step(5, "In the gateway, set auto-capture for prepaid orders so money lands without manual steps.")
pdf.step(6, "Decide refund mechanics: refunds to original method for prepaid; store credit / bank transfer for COD returns. Write this into the Refund policy (Phase 6).")
pdf.h2("Done when")
pdf.check("COD appears as a payment option at checkout")
pdf.check("A real UPI test payment succeeds end-to-end")
pdf.check("Order shows 'Paid' in Shopify admin after prepaid test")

# ---------------- PHASE 6 ----------------
pdf.phase("Phase 6", "Policies (legal + trust)")
pdf.p("Settings -> Policies. Fill all four; Shopify auto-links them in checkout and the theme footer shows them.", 9.5)
pdf.bullet("Shipping policy: dispatch 24-48 hrs; 3-7 working days all India; tracking shared on WhatsApp/email; COD rules; free shipping threshold.")
pdf.bullet("Refund / Return policy: exchange window (e.g. 7 days), condition (unworn, tags on), non-returnable items (innerwear, custom tailoring, sale >50% off if you choose), who pays return shipping, refund timeline 5-7 business days after QC.")
pdf.bullet("Privacy policy: what you collect (name, address, phone, email), why (order fulfilment, delivery updates, marketing with consent), that Meta/Facebook receives shopping events for ads (required when data sharing is Enhanced/Maximum), how to contact you.")
pdf.bullet("Terms of service: pricing errors, stock limits, custom tailoring measurement responsibility, governing law India.")
pdf.note("Trust = conversion", "Indian shoppers check return policy before buying fashion. A clear 7-day exchange promise stated on product pages lifts Add-to-Cart rates.")

# ---------------- PHASE 7 ----------------
pdf.phase("Phase 7", "Pages & navigation")
pdf.p("Online Store -> Pages. Create these four pages; the theme already has matching templates, so they will look designed automatically.", 9.5)
pdf.table(
    ["Page", "Handle (must match)", "Content"],
    [
        ["About", "about", "Story, Ambalathara roots, what 'modest & elegant' means, photos"],
        ["Contact", "contact", "WhatsApp button, phone, email, hours, address, 'reply within 24 hrs'"],
        ["Size guide", "size-guide", "Kurti/set size chart in inches + cm, how to measure, fit notes"],
        ["Custom tailoring", "custom-tailoring", "How it works, 4 steps, price-from ranges, WhatsApp CTA"],
    ],
    [30, 45, 107],
)
pdf.p("Navigation (Online Store -> Navigation, main menu) should end up as:", 9.5, bold=True)
pdf.bullet("Shop all -> /collections")
pdf.bullet("Women -> /collections/womens-ethnic-wear")
pdf.bullet("Kids -> /collections/kids-wear")
pdf.bullet("Wedding edit -> /collections/wedding-collection")
pdf.bullet("New arrivals by Ababeel -> /collections/new-arrivals")
pdf.bullet("Custom tailoring -> /pages/custom-tailoring")
pdf.bullet("Sale -> /collections/sale")

# ---------------- PHASE 8 ----------------
pdf.phase("Phase 8", "Collections - exact handles")
pdf.p("Online Store -> Collections. Create each, then edit the 'Search engine listing' / handle so the URL handle is EXACTLY as below (the theme's menu links point to these handles).", 9.5)
pdf.table(
    ["Collection", "Handle", "Purpose"],
    [
        ["For Front", "for-front", "Homepage featured grid - your 8-12 best pieces"],
        ["New arrivals", "new-arrivals", "Every fresh drop; feed the IG + ads from here"],
        ["Women's ethnic wear", "womens-ethnic-wear", "Kurtis, sets, dresses, co-ords"],
        ["Kids' wear", "kids-wear", "Girls & boys occasion + daily wear"],
        ["Wedding collection", "wedding-collection", "Festive / wedding guest edits"],
        ["Sale", "sale", "Markdowns; keep compare-at prices visible"],
    ],
    [45, 50, 87],
)
pdf.step(1, "Create collection, set title.")
pdf.step(2, "In 'Search engine listing preview' click Edit -> set handle exactly.")
pdf.step(3, "Choose 'Manual' sort for for-front (you control the hero grid order); 'Best selling' or 'Created: descending' for new-arrivals.")
pdf.step(4, "Add a short collection description with one keyword-rich sentence each (e.g. 'Modest kurti sets for women, online in India with COD').")
pdf.note("Handles are load-bearing", "If a handle differs, the menu item opens an empty page. After creating, click each menu link from the live site to verify.")

# ---------------- PHASE 9 ----------------
pdf.phase("Phase 9", "Products - the launch catalogue")
pdf.p("Target: 10-20 excellent products at launch, growing weekly. Quality of product pages decides ad ROI more than any setting.", 9.5)
pdf.h2("Per-product checklist")
pdf.check("Clear title: 'Navy embroidered kurti with beige palazzo set'")
pdf.check("4-6 photos: full look, fabric close-up, back detail, size-reference shot; consistent warm background; compressed (<300 KB each)")
pdf.check("Price + compare-at price where discounted")
pdf.check("Size variants S-XXL with stock per size")
pdf.check("Description: fabric, length, lining, wash care, occasion, model height + size worn")
pdf.check("Assigned to 1-3 collections including for-front or new-arrivals")
pdf.check("Alt text on every image (accessibility + SEO)")
pdf.check("Delivery line: 'Ships in 24-48 hrs, all-India 3-7 days, COD available'")
pdf.h2("Bulk upload")
pdf.step(1, "For many products use Products -> Import with a Shopify CSV (Handle, Title, Variant Size, Price, Inventory, Image Src, Collection).")
pdf.step(2, "Import 3 rows first, verify on the live site, then the rest.")
pdf.note("Image sourcing", "You said product data/images live in mixed sources. Consolidate into one folder, rename like ababeel-kurti-001-front.jpg, and compress before upload - slow product photos kill mobile ads.")

# ---------------- PHASE 10 ----------------
pdf.phase("Phase 10", "Connect the domain ababeeltvm.com")
pdf.step(1, "Shopify Admin -> Online Store -> Domains -> 'Connect existing domain' -> type ababeeltvm.com.")
pdf.step(2, "At your domain registrar, add/replace DNS records:  A record @ -> 23.227.38.65 ;  CNAME www -> shops.myshopify.com")
pdf.step(3, "Back in Shopify click 'Verify connection' (can take minutes to 48 hrs; usually fast).")
pdf.step(4, "When verified, set ababeeltvm.com as PRIMARY domain; keep the www redirect on.")
pdf.step(5, "Wait for SSL (padlock). Test https://ababeeltvm.com on phone + desktop.")
pdf.note("DNS ownership", "You must be able to edit DNS at the registrar - keep that login handy, Meta domain verification (Phase 13) also needs one TXT record there.")

# ---------------- PHASE 11 ----------------
pdf.phase("Phase 11", "Remove the password page")
pdf.step(1, "Only after Phases 1-10: Online Store -> Preferences.")
pdf.step(2, "Under 'Password protection', disable the password page and Save.")
pdf.step(3, "Open ababeeltvm.com in a private window - the real homepage must load with no password wall.")
pdf.note("Why so strict", "Meta ad clicks to a password page are wasted money and can get the ad account flagged for poor destination experience. Password stays ON while building, OFF before the first rupee of ad spend.")

# ---------------- PHASE 12 ----------------
pdf.phase("Phase 12", "Facebook & Instagram channel + Pixel (Maximum)")
pdf.step(1, "Shopify Admin -> Sales channels -> search 'Facebook & Instagram' (by Meta) -> install if missing.")
pdf.step(2, "Open the channel -> Connect: personal Facebook account with admin rights to the Business Portfolio.")
pdf.step(3, "Connect, in order: Business Portfolio -> Facebook Page -> Instagram account @ababeelfashions2024 -> Ad account -> Pixel/Dataset (create new only if none exists; prefer the pixel your current campaigns already use).")
pdf.step(4, "Settings -> Data sharing settings -> enable -> choose MAXIMUM -> Confirm the pixel.")
pdf.step(5, "Maximum = Pixel (browser) + Conversions API (server-to-server) + Meta's newest ad tech; server events cannot be blocked by ad blockers and carry hashed customer details for better matching.")
pdf.step(6, "Verify the catalogue: the channel syncs products to Meta Commerce Manager; open Commerce Manager -> Data Sources -> catalogue and confirm items are 'Active'.")
pdf.step(7, "Fix any disapproved products (missing image, bad title, missing price) until the catalogue is green.")
pdf.note("Privacy note", "Enhanced/Maximum shares customer name, email, phone, location with Meta for matching. Your Privacy policy (Phase 6) must mention this. That is the trade for best ad performance.")

# ---------------- PHASE 13 ----------------
pdf.phase("Phase 13", "Verify ababeeltvm.com in Meta")
pdf.step(1, "business.facebook.com -> Settings (Business Settings) -> Brand safety -> Domains -> Add.")
pdf.step(2, "Enter ababeeltvm.com; Meta offers DNS-verification (recommended): copy the TXT record value.")
pdf.step(3, "At your registrar add the TXT record for @ (or _meta / verification subdomain as instructed).")
pdf.step(4, "Click 'Verify' in Meta (propagation can take minutes). A green 'Verified' badge must appear.")
pdf.step(5, "Verified domain = you can configure link behaviour, protect your events from other ad accounts, and use certain Aggregated Event features.")

# ---------------- PHASE 14 ----------------
pdf.phase("Phase 14", "Test the purchase funnel (before any ads)")
pdf.step(1, "Meta -> Events Manager -> your pixel -> 'Test events' (leave the tab open).")
pdf.step(2, "On a phone, open ababeeltvm.com inside the Instagram in-app browser (tap your own profile link from IG) - that is where ad traffic will arrive.")
pdf.step(3, "Browse home -> tap a product -> you should see PageView then ViewContent in Test events.")
pdf.step(4, "Pick a size, Add to cart -> AddToCart appears; open cart -> InitiateCheckout when checkout starts.")
pdf.step(5, "Complete a real COD test order with your own address -> Purchase appears with a value in INR.")
pdf.step(6, "If the gateway test mode exists, complete one prepaid test order too.")
pdf.step(7, "Confirm each event shows ONCE (deduplicated) - Pixel + CAPI pairs are normal and Meta merges them.")
pdf.step(8, "Check the order email/SMS arrived and the order shows correctly in Shopify Admin.")
pdf.h2("Done when")
pdf.check("PageView, ViewContent, AddToCart, InitiateCheckout, Purchase all visible in Test events")
pdf.check("Purchase carries INR value + content IDs")
pdf.check("No duplicate raw events")

# ---------------- PHASE 15 ----------------
pdf.phase("Phase 15", "Mobile & speed check")
pdf.bullet("Test on Android Chrome, iPhone Safari, and Instagram in-app browser.")
pdf.bullet("Homepage loads in under ~3 seconds on 4G; no horizontal scroll anywhere.")
pdf.bullet("Menu, search, product page, size select, Add to cart, cart drawer, checkout - all one-thumb friendly.")
pdf.bullet("WhatsApp button visible on every page; tap opens wa.me/917012045854 with a prefilled message.")
pdf.bullet("No full-screen popups over products; newsletter capture only as a footer block or gentle bar.")
pdf.bullet("Images compressed; avoid extra apps - every app adds script weight and slows the mobile funnel Meta sends you.")
pdf.note("Where ad money dies", "90%+ of your traffic will be mobile Instagram users. A product page that feels slow or confusing on a phone turns paid clicks into bounce.")

# ---------------- PHASE 16 ----------------
pdf.phase("Phase 16", "Master launch checklist - NO ADS BEFORE THIS")
pdf.check("Fixed theme published; Home page shows hero + sections")
pdf.check("404 template is the maroon 'wrong turn' page (working, but only for bad URLs)")
pdf.check("All menu links open real collections/pages")
pdf.check("10-20 products live with photos, sizes, stock, prices")
pdf.check("for-front collection filled and showing on homepage")
pdf.check("Policies published and linked in footer + checkout")
pdf.check("Shipping zones cover India; rates match your promise")
pdf.check("COD + UPI both tested with real orders")
pdf.check("ababeeltvm.com connected, primary, SSL padlock on")
pdf.check("Password page disabled")
pdf.check("Facebook & Instagram channel connected (Page + IG + ad account)")
pdf.check("Data sharing = Maximum, one pixel only")
pdf.check("Domain verified in Meta Business Settings")
pdf.check("Catalogue active in Commerce Manager")
pdf.check("Test events: full funnel incl. Purchase with INR value")
pdf.check("Mobile funnel tested in Instagram in-app browser")
pdf.p("Only when every box is ticked, move to Phase 17.", 10, MAROON, True)

# ---------------- PHASE 17 ----------------
pdf.phase("Phase 17", "Meta Ads - launch structure")
pdf.h2("Campaign 1 - Sales (website purchases)")
pdf.bullet("Objective: Sales. Conversion location: Website. Optimise for: Purchase.")
pdf.bullet("Advantage+ campaign budget (CBO). Start budget: Rs.1,000-2,000/day (pick what is comfortable; consistency beats size).")
pdf.bullet("Ad set A: Broad India, women 20-55, no interests - let the pixel learn.")
pdf.bullet("Ad set B: Kerala + metro cities (Mumbai, Bengaluru, Chennai, Hyderabad, Delhi NCR) if budget allows.")
pdf.bullet("Placements: Advantage+ (automatic) - includes IG Reels/Stories/Feed where your audience lives.")
pdf.h2("Campaign 2 - WhatsApp leads (custom tailoring)")
pdf.bullet("Objective: Engagement -> messaging apps -> WhatsApp.")
pdf.bullet("Ad: 'Get a kurti stitched to your measurements' with 3 process steps + price-from.")
pdf.bullet("Audience: Kerala first; tailoring is trust-local.")
pdf.h2("Campaign 3 - Retargeting (start after ~2 weeks of traffic)")
pdf.bullet("Audiences: 30-day site visitors, AddToCart 30d, IG/FB engagers 90d; exclude 30d purchasers.")
pdf.bullet("Offer angle: free shipping threshold reminder, new-drop alert, or 'still thinking?' with exchange promise.")
pdf.h2("Creative rules (fashion, India)")
pdf.bullet("First 2 seconds: the outfit, full look, real model or flat-lay - not a logo.")
pdf.bullet("Show price + 'COD available' + 'All-India delivery' ON the creative.")
pdf.bullet("Formats: 4:5 feed images, 9:16 reels video (15-30 s), carousel of the drop.")
pdf.bullet("Primary text formula: hook line (occasion/fabric) + benefit (modest fit, breathable fabric) + CTA (Shop now, COD available).")
pdf.bullet("Refresh creatives every 2-3 weeks; reuse your best Instagram posts as ads.")
pdf.h2("Optimisation rules")
pdf.bullet("Do not edit a campaign for the first 72 hours (learning phase).")
pdf.bullet("Judge on cost per purchase and ROAS, not on likes.")
pdf.bullet("Kill an ad set after ~3x your target cost per purchase with zero sales.")
pdf.bullet("Scale a winner +20% budget every 2-3 days, never double overnight.")

# ---------------- PHASE 18 ----------------
pdf.phase("Phase 18", "Weekly routine after launch")
pdf.bullet("Mon: check Ads Manager - cost per purchase, ROAS, frequency; pause tired ad sets.")
pdf.bullet("Tue: post 3-4 IG pieces this week (reel + carousel + story poll); reuse as ads later.")
pdf.bullet("Wed: add new arrivals to new-arrivals + for-front; refresh homepage promo banner weekly.")
pdf.bullet("Thu: reply to every comment/DM; WhatsApp enquiries within business hours; log size questions -> they become size-guide updates.")
pdf.bullet("Fri: check catalogue health in Commerce Manager; fix disapprovals.")
pdf.bullet("Sat: fulfil + dispatch; update tracking; send WhatsApp 'shipped' notes (reviews follow shipped orders).")
pdf.bullet("Sun: 20-min review: best seller, worst bounce page, one fix for next week.")

# ---------------- APPENDIX A ----------------
pdf.phase("Appendix A", "What is inside the fixed theme package")
pdf.table(
    ["Folder / file", "What it does"],
    [
        ["templates/index.json", "RESTORED homepage template (the missing file that caused the 404 problem)"],
        ["templates/404.json + sections/main-404.liquid", "Proper branded 404 page"],
        ["layout/theme.liquid", "Base layout: fonts, meta tags, cart drawer, mobile menu wiring"],
        ["sections/", "hero, header, footer, featured-collection, value-props, shop-categories, brand-story, promo-banner, instagram-showcase, newsletter, cart-drawer, main-* templates"],
        ["config/settings_schema.json", "Theme settings: brand colours, WhatsApp, phone, address, Instagram URL"],
        ["assets/", "CSS (base/advanced/commerce), theme.js (menu, drawer, reveal), demo images"],
        ["locales/en.default.json", "English-only labels"],
    ],
    [55, 127],
)
pdf.p("The same package also ships cart, product, collection, search, cart and page templates - a complete Shopify 2.0 theme, not a homepage shell.", 9)

# ---------------- APPENDIX B ----------------
pdf.phase("Appendix B", "Handles & links cheat-sheet")
pdf.table(
    ["Type", "Name", "Handle / URL"],
    [
        ["Collection", "For Front", "for-front"],
        ["Collection", "New arrivals", "new-arrivals"],
        ["Collection", "Women's ethnic wear", "womens-ethnic-wear"],
        ["Collection", "Kids' wear", "kids-wear"],
        ["Collection", "Wedding collection", "wedding-collection"],
        ["Collection", "Sale", "sale"],
        ["Page", "About", "about"],
        ["Page", "Contact", "contact"],
        ["Page", "Size guide", "size-guide"],
        ["Page", "Custom tailoring", "custom-tailoring"],
        ["Link", "WhatsApp chat", "https://wa.me/917012045854"],
        ["Link", "Instagram", "https://www.instagram.com/ababeelfashions2024/"],
    ],
    [30, 60, 92],
)

# ---------------- APPENDIX C ----------------
pdf.phase("Appendix C", "What the 404 bug was (and the fix)")
pdf.p("Your Shopify export contained templates/404.json holding the HOMEPAGE sections, and had no templates/index.json at all. Without an index template Shopify has no homepage, so previews and the editor fell back to the 404 template.", 9.5)
pdf.p("The fixed package:", 9.5, bold=True)
pdf.bullet("Adds a proper templates/index.json carrying your saved hero image, hero text, and the 'for-front' featured collection exactly as you configured them.")
pdf.bullet("Restores templates/404.json to a real 404 page (the maroon 'That page took a wrong turn' design you saw).")
pdf.bullet("Keeps every advanced section and the mobile/responsive behaviour.")
pdf.p("If the editor ever opens showing '404 page' at the top again, it is only the template selector - switch it to 'Home page' as in Phase 1 step 5.", 9.5)

# ---------------- APPENDIX D ----------------
pdf.phase("Appendix D", "Troubleshooting")
pdf.table(
    ["Symptom", "Fix"],
    [
        ["Store shows 'Will be opening soon'", "Password still on: Phase 11"],
        ["Editor shows 404 artwork instead of homepage", "Template selector at top says '404 page' - switch to 'Home page'"],
        ["Menu link opens empty page", "Collection/page handle differs from Appendix B - fix handle"],
        ["No events in Meta Test events", "Check channel connected + pixel selected + data sharing enabled; clear cache; retest"],
        ["Purchase missing but PageView works", "Finish a FULL test order; Purchase fires on the thank-you page only"],
        ["Catalogue items disapproved", "Commerce Manager -> fix image/title/price; resync"],
        ["Domain shows 'SSL pending' > 48 hrs", "Check A/CNAME records at registrar; re-verify in Shopify"],
        ["Checkout has no COD option", "Settings -> Payments -> manual payments -> enable COD"],
        ["Ads spend but zero purchases", "Check funnel test (Phase 14) first; then creative + offer, not settings"],
    ],
    [62, 120],
)

# ---------------- APPENDIX E ----------------
pdf.phase("Appendix E", "Key links & logins to keep handy")
pdf.bullet("Shopify admin: https://i6iaut-f6.myshopify.com/admin (your store's admin URL)")
pdf.bullet("Meta Business Suite: https://business.facebook.com")
pdf.bullet("Ads Manager: https://adsmanager.facebook.com")
pdf.bullet("Events Manager: https://business.facebook.com/events_manager2")
pdf.bullet("Commerce Manager (catalogue): https://business.facebook.com/commerce")
pdf.bullet("Domain registrar DNS console (for A / CNAME / TXT records)")
pdf.bullet("Instagram: https://www.instagram.com/ababeelfashions2024/")
pdf.bullet("WhatsApp click-to-chat: https://wa.me/917012045854")
pdf.ln(4)
pdf.note("Final word", "Build in order, test on a phone, then advertise. The website is the engine; Meta ads are fuel. Fuel on a broken engine is how budgets burn. You now have the engine manual - go launch.")

OUT = "deliverables/Ababeel-Fashions-Launch-Guide-Final.pdf"
pdf.output(OUT)
print("PAGES:", pdf.pages_count, "->", OUT)
