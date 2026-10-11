"""Generate me/about_business.pdf, the business profile for Cedar & Crumb Bakery.

Run from the repo root:
    python scripts/make_about_pdf.py
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = Path(__file__).resolve().parent.parent / "me" / "about_business.pdf"

CEDAR = colors.HexColor("#2F5D3A")
CRUMB = colors.HexColor("#C8873A")
CREAM = colors.HexColor("#FBF6EE")
INK = colors.HexColor("#2B2B2B")

# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------

ABOUT = (
    "Cedar &amp; Crumb Bakery is an artisan bakery and cafe at 112 Armenia Street in Mar Mikhael, "
    "Beirut. It was founded in 2021 by head baker Rania Haddad and operations lead Karim Nassar, who "
    "wanted to bring back the flavour of the bread they grew up with: slow, honest loaves made from "
    "Lebanese grain. Today we bake every morning for our neighbourhood, for celebrations across the "
    "city, and for a growing list of cafes and restaurants."
)

MISSION = (
    "To bake honest, slow-fermented bread and pastries that bring together Lebanese baking heritage "
    "and European artisan technique, made from heritage wheat grown by small farmers in the Bekaa "
    "Valley, while wasting nothing."
)

VALUE_PROPOSITION = [
    "<b>Milled in-house, every morning.</b> We are the only bakery in Beirut that stone-mills Lebanese "
    "heritage Salamouni wheat on site each day, so our flour is hours old, not months old.",
    "<b>48-hour sourdough.</b> Every sourdough loaf is fermented for 48 hours for deeper flavour and "
    "easier digestion.",
    "<b>Fusion pastries you will not find elsewhere.</b> Signature bakes such as the knefeh croissant "
    "and the pistachio and rose pain suisse.",
    "<b>Direct from six Bekaa family farms.</b> We buy our wheat directly from the farmers at a fair "
    "price agreed before each harvest.",
    "<b>Zero-waste kitchen.</b> Unsold bread is donated every evening to a local food bank or turned "
    "into croutons and bread pudding.",
]

SERVICES = [
    ("Daily bakery &amp; cafe",
     "Walk-in bakery and cafe serving sourdough loaves, man'oushe, croissants, pastries and coffee. "
     "20 indoor seats plus a small terrace."),
    ("Custom celebration cakes",
     "Designed-to-order cakes for birthdays, engagements, baby showers and weddings, created by our "
     "pastry chef Lea Khoury."),
    ("Corporate &amp; event catering",
     "Breakfast boxes and pastry and mezze platters for offices, meetings and private events of 15 "
     "guests or more."),
    ("Baking workshops",
     "Hands-on weekend classes for adults and kids in small groups of up to 10 people, plus private "
     "team-building workshops for companies."),
    ("Bread subscriptions",
     "The Crumb Club weekly subscription for households, and wholesale bread supply for cafes and "
     "restaurants."),
]

MENU = [
    ("Breads", [
        ("Country Sourdough (800 g)", "$6.00"),
        ("Seeded Rye Sourdough", "$7.00"),
        ("Salamouni Whole-Wheat Loaf", "$6.50"),
        ("Olive &amp; Za'atar Fougasse", "$5.00"),
        ("Baguette", "$2.50"),
    ]),
    ("Man'oushe &amp; savoury", [
        ("Za'atar Man'oushe", "$2.50"),
        ("Akkawi Cheese Man'oushe", "$3.50"),
        ("Half Za'atar, Half Cheese Man'oushe", "$3.00"),
        ("Spinach Fatayer (3 pieces)", "$4.00"),
    ]),
    ("Pastries", [
        ("Butter Croissant", "$2.75"),
        ("Knefeh Croissant (signature)", "$4.50"),
        ("Pistachio &amp; Rose Pain Suisse", "$4.00"),
        ("Orange Blossom Brioche", "$3.25"),
        ("Date &amp; Tahini Cookie", "$1.75"),
    ]),
    ("Drinks", [
        ("Espresso", "$2.00"),
        ("Cappuccino", "$3.25"),
        ("Cardamom Latte", "$3.75"),
        ("Fresh Lemonade with Mint", "$3.00"),
    ]),
    ("To take home", [
        ("Stone-milled Salamouni Flour (1 kg)", "$4.00"),
    ]),
]

CAKE_SIZES = [
    ("6-inch round", "8 to 10", "from $45"),
    ("8-inch round", "12 to 16", "from $65"),
    ("10-inch round", "20 to 25", "from $90"),
    ("Tiered wedding cake", "50+", "from $250 (consultation required)"),
]

CAKE_DETAILS = [
    "<b>Flavours:</b> vanilla bean and berries, chocolate hazelnut, pistachio rose, orange blossom "
    "and honey, carrot and walnut.",
    "<b>Notice:</b> at least 72 hours for custom cakes; at least 3 weeks for wedding cakes.",
    "<b>Decorations:</b> custom toppers and hand-piped sugar flowers start at $10 extra. Customers "
    "are welcome to send a reference photo of the design they want.",
    "<b>Deposit:</b> a 50% deposit confirms every custom cake order.",
]

CATERING = [
    ("Breakfast Box", "Butter croissant, za'atar man'oushe, fruit cup and fresh juice", "$12 / person"),
    ("Pastry &amp; Mezze Platter", "Assorted pastries, savoury bakes, labneh, olives and vegetables",
     "$18 / person"),
    ("Coffee Service (add-on)", "Freshly brewed coffee and tea with cups and milk", "$3 / person"),
]

CATERING_NOTES = (
    "Minimum 15 guests and 48 hours' notice. Delivery and setup within Beirut are included for "
    "catering orders. Events of 100 guests or more are priced by custom quote."
)

WORKSHOPS = [
    ("Sourdough 101", "Saturdays, 10:00-13:00", "Adults", "$55"),
    ("Lebanese Breads &amp; Man'oushe", "Sundays, 9:00-12:00", "Adults", "$50"),
    ("Kids' Cookie Decorating", "Saturdays, 15:00-17:00", "Ages 6-12", "$30"),
]

WORKSHOP_NOTES = (
    "Every workshop is limited to 10 participants and includes all ingredients, an apron to keep, "
    "and everything you bake to take home. Private team-building workshops for 6 to 10 people are "
    "available on weekday evenings, priced by quote."
)

SUBSCRIPTIONS = [
    "<b>Crumb Club ($28 / month):</b> one loaf of your choice every week plus a monthly pastry box. "
    "Pickup is free; home delivery within Beirut adds $5 per month. Cancel any time before the next "
    "billing date.",
    "<b>Wholesale:</b> daily bread delivery before 7:00 for cafes, restaurants and hotels in Beirut. "
    "Minimum order of 20 loaves per week. Pricing is by quote after a short consultation with Karim.",
]

TEAM = [
    ("Rania Haddad", "Co-founder &amp; Head Baker",
     "Grew up in Zahle and trained at a pastry school in Lyon. She spent 12 years in bakeries in "
     "France and Beirut and leads all recipe development, including our 48-hour sourdough."),
    ("Karim Nassar", "Co-founder &amp; Operations Director",
     "A former supply-chain engineer who built our partnerships with six family farms in the Bekaa "
     "Valley. He runs the stone mill, logistics and wholesale accounts."),
    ("Lea Khoury", "Pastry Chef &amp; Cake Designer",
     "Designs every custom and wedding cake and is known for her hand-piped sugar flowers."),
    ("Omar Saad", "Workshop Lead &amp; Community Manager",
     "Runs our baking workshops, community events and the Crumb Club."),
]

HOURS = [
    ("Tuesday to Saturday", "7:00 - 19:00"),
    ("Sunday", "8:00 - 15:00"),
    ("Monday", "Closed"),
]

LOCATION_AND_DELIVERY = [
    "<b>Address:</b> 112 Armenia Street, Mar Mikhael, Beirut. Paid public parking is a 2-minute walk "
    "away. Free Wi-Fi for cafe guests.",
    "<b>Delivery:</b> within Beirut only, $4 flat fee, free on orders over $50. Same-day delivery for "
    "orders placed before 14:00. Customers outside Beirut can order ahead and pick up.",
    "<b>How to order:</b> in person, by phone, by email, or through our virtual assistant on our "
    "website. Our team confirms every order by email.",
]

POLICIES = [
    "<b>Payment:</b> cash (USD, or LBP at the daily rate) and all major cards. Bank transfer is "
    "accepted for catering and wholesale.",
    "<b>Custom cake cancellations:</b> the deposit is fully refunded if you cancel at least 72 hours "
    "before pickup; within 72 hours it is non-refundable.",
    "<b>Workshop cancellations:</b> full refund up to 48 hours before the class; after that, your "
    "seat can be moved to another date.",
    "<b>Allergens:</b> our kitchen handles wheat, nuts (pistachio, walnut, hazelnut), sesame, dairy "
    "and eggs. All items are labelled with their allergens.",
    "<b>Gluten-free:</b> we do not offer gluten-free products. Flour is milled on site, so we cannot "
    "prevent cross-contamination.",
    "<b>Vegan options:</b> all sourdough loaves, the za'atar man'oushe, the olive and za'atar "
    "fougasse and the date and tahini cookie are vegan.",
    "<b>Ingredients:</b> none of our products contain pork or alcohol.",
]

FAQ = [
    ("Can I reserve a table?",
     "Seating is first come, first served. Groups of 8 or more can call ahead and we will do our best "
     "to keep a table."),
    ("Can I bring my own cake design?",
     "Yes. Send a reference photo and Lea will confirm whether it is possible and what it will cost."),
    ("Are pets allowed?", "Pets are welcome on the terrace."),
    ("Do you deliver outside Beirut?",
     "Not yet. Customers outside Beirut can order ahead and pick up from the bakery."),
    ("Can I buy your flour?",
     "Yes. Our stone-milled Salamouni flour is sold in 1 kg bags for $4."),
]

CONTACT = [
    ("Email", "hello@cedarandcrumb.example"),
    ("Phone", "+961 1 555 0142"),
    ("Website", "www.cedarandcrumb.example"),
    ("Address", "112 Armenia Street, Mar Mikhael, Beirut, Lebanon"),
]

# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

base = getSampleStyleSheet()
STYLES = {
    "title": ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=28,
                            leading=34, textColor=CEDAR, spaceAfter=6, alignment=TA_CENTER),
    "tagline": ParagraphStyle("tagline", parent=base["Normal"], fontName="Helvetica-Oblique",
                              fontSize=13, textColor=CRUMB, alignment=TA_CENTER, spaceAfter=2),
    "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontSize=9, textColor=colors.grey,
                               alignment=TA_CENTER, spaceAfter=14),
    "h1": ParagraphStyle("h1", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=15,
                         textColor=CEDAR, spaceBefore=14, spaceAfter=6),
    "h2": ParagraphStyle("h2", parent=base["Heading3"], fontName="Helvetica-Bold", fontSize=11,
                         textColor=CRUMB, spaceBefore=8, spaceAfter=3),
    "body": ParagraphStyle("body", parent=base["Normal"], fontSize=10, leading=14.5, textColor=INK,
                           spaceAfter=4),
    "cell": ParagraphStyle("cell", parent=base["Normal"], fontSize=9.5, leading=12.5, textColor=INK),
    "cell_head": ParagraphStyle("cell_head", parent=base["Normal"], fontName="Helvetica-Bold",
                                fontSize=9.5, leading=12.5, textColor=colors.white),
}


def p(text, style="body"):
    return Paragraph(text, STYLES[style])


def bullets(items):
    return ListFlowable(
        [ListItem(p(item), leftIndent=12, bulletColor=CRUMB) for item in items],
        bulletType="bullet", start="•", leftIndent=12,
    )


def table(rows, col_widths, header=None):
    data = []
    if header:
        data.append([p(h, "cell_head") for h in header])
    data.extend([p(c, "cell") for c in row] for row in rows)
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#E2D6C3")),
        ("ROWBACKGROUNDS", (0, 1 if header else 0), (-1, -1), [colors.white, CREAM]),
    ]
    if header:
        style.append(("BACKGROUND", (0, 0), (-1, 0), CEDAR))
    t.setStyle(TableStyle(style))
    return t


def section(title, *flowables):
    """Keep a heading together with the first block under it."""
    first, *rest = flowables
    return [KeepTogether([p(title, "h1"), first]), *rest]


def on_page(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(CEDAR)
    canvas.rect(0, height - 0.6 * cm, width, 0.6 * cm, stroke=0, fill=1)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(2 * cm, 1.2 * cm, "Cedar & Crumb Bakery - Business Profile")
    canvas.drawRightString(width - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build():
    full = A4[0] - 4 * cm
    story = [
        Spacer(1, 0.6 * cm),
        p("Cedar &amp; Crumb Bakery", "title"),
        p("Mountain grains, city mornings.", "tagline"),
        p("Business Profile &middot; Mar Mikhael, Beirut &middot; Established 2021", "subtitle"),
    ]

    story += section("About Us", p(ABOUT))
    story += section("Our Mission", p(MISSION))
    story += section("What Makes Us Different", bullets(VALUE_PROPOSITION))
    story += section(
        "Services",
        table(SERVICES, [5 * cm, full - 5 * cm], header=["Service", "Description"]),
    )

    menu_blocks = []
    for category, items in MENU:
        menu_blocks.append(KeepTogether([p(category, "h2"), table(items, [full - 3 * cm, 3 * cm])]))
    story += section("Menu &amp; Price List", *menu_blocks)

    story += section(
        "Custom Celebration Cakes",
        KeepTogether([
            table(CAKE_SIZES, [5 * cm, 3.5 * cm, full - 8.5 * cm], header=["Size", "Serves", "Price"]),
            Spacer(1, 4),
            bullets(CAKE_DETAILS),
        ]),
    )
    story += section(
        "Corporate &amp; Event Catering",
        table(CATERING, [5 * cm, full - 8 * cm, 3 * cm], header=["Package", "Includes", "Price"]),
        Spacer(1, 4),
        p(CATERING_NOTES),
    )
    story += section(
        "Baking Workshops",
        table(WORKSHOPS, [5.5 * cm, 4.5 * cm, 3 * cm, full - 13 * cm],
              header=["Workshop", "When", "For", "Price"]),
        Spacer(1, 4),
        p(WORKSHOP_NOTES),
    )
    story += section("Subscriptions &amp; Wholesale", bullets(SUBSCRIPTIONS))

    team_blocks = [KeepTogether([p(f"{name} &mdash; {role}", "h2"), p(bio)])
                   for name, role, bio in TEAM]
    story += section("Our Team", *team_blocks)

    story += section(
        "Opening Hours, Location &amp; Delivery",
        table(HOURS, [6 * cm, 4 * cm]),
        Spacer(1, 6),
        bullets(LOCATION_AND_DELIVERY),
    )
    story += section("Policies", bullets(POLICIES))

    faq_blocks = [KeepTogether([p(q, "h2"), p(a)]) for q, a in FAQ]
    story += section("Frequently Asked Questions", *faq_blocks)
    story += section("Contact", table(CONTACT, [3 * cm, full - 3 * cm]))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm,
        title="Cedar & Crumb Bakery - Business Profile", author="Cedar & Crumb Bakery",
    )
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
