# Fact-checked work cards: which projects appear on which pages, and the image + text each card uses there.
# Every image below was checked against its still description. Text sticks to what's in the case studies.

# Default card text: one complete sentence, no truncation.
CARD = {
 "turbotax-three-event-campaign": "Three TurboTax activations, Sneaker Con, Bellevue pickleball and a grand opening, delivered in one week.",
 "chilean-salmon-culinary-event-film": "A multi-day culinary and educational program with chef demos and talks, cut into one 1:42 film.",
 "nuwav-jacket-launch-commercial": "A jacket launch commercial starring Seattle creatives instead of models.",
 "peristera-first-collection-launch": "A first-collection launch film plus five stylized reels, one for each look.",
 "gerard-cycles-brand-film": "A 60-second website hero film for a Kirkland bike brand that hand-builds carbon frames.",
 "jack-s-bbq-commercial-campaign": "A 30-second restaurant commercial built around the pitmaster, the crew and the regulars.",
 "lula-coffee-co-brand-film": "A 30-second brand film for a hot-pink Seattle coffee shop.",
 "zadart-exotic-car-campaign": "A music-video-style promo for two Lamborghinis, with rolling shots and FPV drone.",
 "turbotax-tax-season-promo": "A tax-season street-team promo for TurboTax, filmed run-and-gun by a two-person crew in Renton.",
 "laid-back-allure-weekend-recap": "A recap of Laid Back Allure's R&B event weekend, plus vertical cuts for social.",
 "sarajevo-mariah-the-scientist": "Mariah The Scientist's night at Sarajevo, opening with a luxury rental car feature.",
 "saint-meadow-can-t-complain": "A dark, cinematic official video for Saint Meadow's \"Can't Complain\".",
 "tbg-kam-bino-my-life": "A dark, high-contrast official video for TBG Kam Bino's \"My Life\".",
 "youngcam206-ruthless": "A cinematic, vintage-inspired official video for YoungCam206's \"Ruthless\".",
 "rell-moore-chrome-hearts": "A black-and-white official video shot across Seattle for Rell Moore's \"Chrome Hearts\".",
 "tha-baby-street-runner": "A neon, high-energy official video for Tha Baby, shot at the Washington State Fair.",
 "slotlifebaby-different-time": "A moody, late-night official video for SlotLifeBaby, shot in Tacoma and Spanaway.",
}

# Context-specific angles: (work, context) -> (image, text). Context = niche name, sector slug or service slug.
_A = {}
def _a(work, ctxs, img, text):
    for c in ctxs: _A[(work, c)] = (img, text)

MS = "sarajevo-mariah-the-scientist"
_a(MS, ["automotive", "Luxury Car Rentals", "Automotive Events"], "img/ev-ms-01.jpg",
   "The recap opens on a luxury rental partner's yellow Lamborghini Urus in the alley before Mariah The Scientist's night at Sarajevo.")
_a(MS, ["Brand Activations", "corporate-events"], "img/ev-ms-01.jpg",
   "One recap for several partners: the venue, the artist and a luxury vehicle rental feature, all woven together.")
_a(MS, ["hospitality-nightlife", "Private Events"], "img/ev-ms-06.jpg",
   "A night at Sarajevo, a Belltown nightclub, with Mariah The Scientist performing for a packed room.")
_a(MS, ["music-entertainment", "Concerts & Music Festivals", "Live Entertainment"], "img/ev-ms-h1.jpg",
   "Mariah The Scientist live at Sarajevo: the arrival, the performance and the fan moments, filmed solo.")
_a(MS, ["travel-tourism", "Luxury Experiences"], "img/ev-ms-01.jpg",
   "A luxury night out in Seattle: a Lamborghini Urus arrival, then Mariah The Scientist at Sarajevo.")

TT = "turbotax-three-event-campaign"
_a(TT, ["Pickleball & Racket Sports", "sports-fitness", "Sports Events & Tournaments", "Community Events"], "img/ev-pb-00.jpg",
   "TurboTax's community pickleball day at Bellevue Pickleball Club, one of three activations delivered in a week.")
_a(TT, ["Sporting Events & Sponsorships"], "img/ev-pb-00.jpg",
   "A TurboTax brand activation at a Bellevue pickleball club, with merch, giveaways and players.")
_a(TT, ["Footwear & Sneakers", "Conventions & Trade Shows"], "img/ev-tt-01.jpg",
   "Sneaker Con Seattle for TurboTax: custom sneakers, vendors, collectors and the crowd, with attendee interviews.")
_a(TT, ["Catering Companies"], "img/ev-go-04.jpg",
   "Catering, florals and live violin at the grand opening of TurboTax's new Bellevue location.")
_a(TT, ["Commercial Real Estate", "real-estate-design", "retail-brands", "Luxury Retail"], "img/ev-go-cover.jpg",
   "The grand opening of TurboTax's new Bellevue location, with florals, live violin and a photo station.")
_a(TT, ["Fintech & Financial Services", "corporate-enterprise"], "img/ev-tt.jpg",
   "Three tax-season activations for Intuit's TurboTax, directed by Reelclip and delivered in one week.")

CS = "chilean-salmon-culinary-event-film"
_a(CS, ["Universities & Colleges", "Education & Training", "nonprofit-education-public"], "img/ev-cs-06.jpg",
   "Educational talks and chef demos at the University of Washington and a Seattle hotel venue, cut into one film.")
_a(CS, ["Hotels & Resorts"], "img/ev-cs-01.jpg",
   "A culinary program held at a Seattle hotel venue.")
_a(CS, ["Catering Companies", "Culinary Events", "food-beverage", "Restaurants"], "img/ev-cs-04.jpg",
   "Live chef demonstrations and plated salmon dishes across a multi-day culinary program.")
_a(CS, ["Business Conferences", "corporate-events", "Event Production Companies", "corporate-enterprise"], "img/ev-cs-06.jpg",
   "Talks, interviews and networking across a multi-day program, with audio support for every speaker.")
_a(CS, ["Food Manufacturers"], "img/ev-cs-10.jpg",
   "A promotional and educational film for Chilean salmon, from chef demos to the product itself.")

LU = "lula-coffee-co-brand-film"
_a(LU, ["Interior Design Studios", "real-estate-design"], "img/lula-08.jpg",
   "A space-first film for Lula Coffee Co.: slow, clean frames that let the pink and teal interior do the talking.")
_a(LU, ["Coffee Shops & Cafés", "food-beverage"], "img/lula-06.jpg",
   "A 30-second brand film for Lula Coffee Co.'s pink Seattle cafes and signature drinks.")

ZA = "zadart-exotic-car-campaign"
_a(ZA, ["Car Dealerships", "Automotive Brands", "automotive"], "img/zadart-04.jpg",
   "Rolling, aerial and FPV car cinematography for two Lamborghinis around Seattle.")
_a(ZA, ["Luxury Car Rentals", "Luxury Experiences", "travel-tourism", "luxury-lifestyle"], "img/zadart-01.jpg",
   "A social-first campaign for Zadart's exotic car rentals: two Lamborghinis on the Seattle waterfront.")

GE = "gerard-cycles-brand-film"
_a(GE, ["Manufacturing & Industrial", "industrial-infrastructure"], "img/gerard-cycles.jpg",
   "Hand-built carbon frames from Kirkland: the build process, the product and the ride, in one hero film.")
_a(GE, ["Bicycle Brands", "Cycling & Bicycle Companies", "Sports Equipment", "sports-fitness"], "img/gerard-cycles.jpg",
   "A 60-second website hero film for Gerard Cycles' hand-built carbon road and gravel bikes.")

LA = "laid-back-allure-weekend-recap"
_a(LA, ["Breweries & Distilleries"], "img/ev-la.jpg",
   "The back bar and cocktails at Deadline, filmed for Laid Back Allure's R&B nights.")
_a(LA, ["Community Events", "Live Entertainment", "Event Production Companies"], "img/ev-la.jpg",
   "A weekend of Laid Back Allure events, a brunch, an all-white party and an estate gathering, recapped.")

_a("nuwav-jacket-launch-commercial", ["Influencers & Content Creators"], "img/nuwav.jpg",
   "A launch commercial built around Seattle creatives Kid Steez, Xavier Weeks and D. Hayes.")
_a("peristera-first-collection-launch", ["Startups & Venture-Backed Brands"], "img/peristera.jpg",
   "A launch campaign for an emerging clothing brand's first-ever collection.")
_a("turbotax-tax-season-promo", ["Fintech & Financial Services", "corporate-enterprise", "Brand Activations"], "img/turbotax.jpg",
   "A tax-season street team for Intuit's TurboTax in Renton, filmed by a two-person crew.")

def angle(work, ctxs):
    for c in ctxs or []:
        if (work, c) in _A: return _A[(work, c)]
    return None

# Which projects genuinely fit each niche. Niches not listed show no work section (we don't fake relevance).
NICHE_WORK = {
 "Restaurants": ["jack-s-bbq-commercial-campaign"],
 "Coffee Shops & Cafés": [LU],
 "Catering Companies": [CS, TT],
 "Food Manufacturers": [CS],
 "Culinary Events": [CS],
 "Fashion Designers": ["peristera-first-collection-launch", "nuwav-jacket-launch-commercial"],
 "Footwear & Sneakers": [TT],
 "Lifestyle Brands": ["peristera-first-collection-launch", "nuwav-jacket-launch-commercial"],
 "Car Dealerships": [ZA],
 "Luxury Car Rentals": [ZA, MS],
 "Automotive Brands": [ZA],
 "Automotive Events": [MS],
 "Bicycle Brands": [GE],
 "Startups & Venture-Backed Brands": ["peristera-first-collection-launch"],
 "Fintech & Financial Services": [TT, "turbotax-tax-season-promo"],
 "Business Conferences": [CS],
 "Brand Activations": [TT, "turbotax-tax-season-promo", MS],
 "Experiential Marketing": [TT],
 "Live Entertainment": [MS, LA],
 "Conventions & Trade Shows": [TT],
 "Concerts & Music Festivals": [MS],
 "Community Events": [TT, LA],
 "Event Production Companies": [TT, CS, LA],
 "Music Artists & Record Labels": ["saint-meadow-can-t-complain", "rell-moore-chrome-hearts", "slotlifebaby-different-time", "tha-baby-street-runner"],
 "Influencers & Content Creators": ["nuwav-jacket-launch-commercial"],
 "Pickleball & Racket Sports": [TT],
 "Cycling & Bicycle Companies": [GE],
 "Sports Events & Tournaments": [TT],
 "Sports Equipment": [GE],
 "Sporting Events & Sponsorships": [TT],
 "Education & Training": [CS],
 "Universities & Colleges": [CS],
 "Manufacturing & Industrial": [GE],
 "Luxury Experiences": [ZA],
}

# Fact-checked sector and service lists (override the originals)
SECTOR_WORK = {
 "food-beverage": ["jack-s-bbq-commercial-campaign", LU, CS],
 "fashion-apparel": ["nuwav-jacket-launch-commercial", "peristera-first-collection-launch"],
 "automotive": [ZA, MS],
 "corporate-events": [TT, CS, "turbotax-tax-season-promo"],
 "hospitality-nightlife": [MS, LA, LU, "jack-s-bbq-commercial-campaign"],
 "music-entertainment": ["saint-meadow-can-t-complain", "rell-moore-chrome-hearts", "slotlifebaby-different-time", MS],
 "retail-brands": [TT, GE, "turbotax-tax-season-promo", "peristera-first-collection-launch"],
 "corporate-enterprise": [TT, "turbotax-tax-season-promo", CS],
 "real-estate-design": [],
 "sports-fitness": [TT, GE],
 "health-wellness": [],
 "nonprofit-education-public": [CS],
 "industrial-infrastructure": [GE],
 "travel-tourism": [],
 "luxury-lifestyle": ["peristera-first-collection-launch", "nuwav-jacket-launch-commercial", ZA],
}
SERVICE_WORK = {
 "brand-films": [GE, LU],
 "corporate-video-production": [CS, TT],
 "content-partnerships": [],
}

# When an industry has no directly matching project, show a business hero film that makes sense as a format example.
FALLBACK_BY_SECTOR = {
 "food-beverage": "jack-s-bbq-commercial-campaign", "hospitality-nightlife": "jack-s-bbq-commercial-campaign",
 "luxury-lifestyle": "peristera-first-collection-launch", "fashion-apparel": "peristera-first-collection-launch",
 "retail-brands": TT, "automotive": ZA, "travel-tourism": ZA, "sports-fitness": TT, "corporate-events": TT,
}
FALLBACK_DEFAULT = GE
FALLBACK_TEXT = {
 GE: ("img/gerard-cycles.jpg", "A 60-second website hero film for Gerard Cycles: the same brand-film format we'd build around your business."),
 "jack-s-bbq-commercial-campaign": ("img/jacks-bbq.jpg", "A 30-second commercial for Jack's BBQ, built around the people behind the business: the format we'd bring to yours."),
 "peristera-first-collection-launch": ("img/peristera.jpg", "A launch film and reels for Peristera's first collection, the product-first approach we'd bring to your brand."),
 TT: ("img/ev-go-cover.jpg", "TurboTax's Bellevue grand opening and activations, delivered in one week: the kind of coverage we'd bring to your business."),
 ZA: ("img/zadart-01.jpg", "A social-first promo for Zadart's exotic car rentals, with rolling shots and FPV drone: the energy we'd bring to your brand."),
}
# Music videos that shouldn't lead a business or city page
NO_HERO_ON_BUSINESS = {"slotlifebaby-different-time", "saint-meadow-can-t-complain", "tbg-kam-bino-my-life", "youngcam206-ruthless", "rell-moore-chrome-hearts", "tha-baby-street-runner"}
