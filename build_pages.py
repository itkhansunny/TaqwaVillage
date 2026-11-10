"""
Comprehensive page builder for Taqwa Village Ltd.
Generates rich, detailed, responsive, and bilingual content for all inner pages:
about, projects, cottages, resort, agro, amenities, gallery, investment, booking, contact, privacy, terms.
"""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent
home = (ROOT / 'index.html').read_text(encoding='utf-8')

# Extract shared chrome from homepage
head = home[:home.index('<body')]
chrome = home[home.index('<body'):home.index('<main id="hero-section"')]
chrome = chrome.replace('href="#hero-section"', 'href="#page-content"').replace(' aria-current="page"', '')

# Extract clean footer and address section
footer_start = home.index('<footer')
footer_end = home.index('</footer>', footer_start) + len('</footer>')
footer = home[footer_start:footer_end]

addr_start = home.index('<section id="address-bar"')
addr_end = home.index('</section>', addr_start) + len('</section>')
address = home[addr_start:addr_end].strip()

# Modals (Lead, Price, Booking, Video, Lightbox)
modals = home[home.index('<div id="leadModal"'):home.index('<!-- Custom Scripts')]

def t(bn, en, tag='span', cls=''):
    return f'<{tag} class="{cls}" data-bn="{escape(bn, quote=True)}" data-en="{escape(en, quote=True)}">{escape(bn)}</{tag}>'

def link(url, bn, en, cls='text-button'):
    return f'<a class="{cls}" href="{url}">{t(bn, en)} <span aria-hidden="true">↗</span></a>'

photos = {
    'resort': 'photo-1571896349842-33c89424de2d',
    'cottage': 'photo-1582719508461-905c673771fd',
    'nature': 'photo-1500937386664-56d1dfef3854',
    'pool': 'photo-1566073771259-6a8506099945',
    'mosque': 'photo-1564769625905-50e93615e769',
    'masterplan': 'photo-1506744038136-46273834b3fb',
    'dining': 'photo-1517248135467-4c7edcad34c4',
    'villa': 'photo-1512917774080-9991f1c4c750',
    'park': 'photo-1519331379826-f10be5486c6f',
    'aerial': 'photo-1506744038136-46273834b3fb'
}

def image(key, cls='', eager=False):
    photo_id = photos.get(key, 'photo-1571896349842-33c89424de2d')
    return f'<img class="{cls}" src="https://images.unsplash.com/{photo_id}?auto=format&amp;fit=crop&amp;w=1200&amp;q=85" alt="{key.title()} lifestyle inspiration" {"fetchpriority=high" if eager else "loading=lazy"}>'

def feature(icon, bn, en, body, bodyen):
    return f'<article class="feature-panel"><i data-lucide="{icon}" aria-hidden="true"></i>{t(bn, en, "h3")}{t(body, bodyen, "p")}</article>'

def section(bn, en, content, eyebrow='THE TAQWA EXPERIENCE'):
    return f'<section class="page-section"><span class="eyebrow">{eyebrow}</span>{t(bn, en, "h2")}{content}</section>'

def card(key, title, titleen, desc, descen, url, number):
    return f'<article class="destination-card"><a href="{url}" aria-label="{titleen}">{image(key)}</a><div class="destination-body"><span class="eyebrow">{number} / TAQWA VILLAGE</span>{t(title, titleen, "h3")}{t(desc, descen, "p")}{link(url, "বিস্তারিত দেখুন", "Discover more")}</div></article>'

cards = [
    card('cottage', 'ফ্লোটিং কটেজ', 'Floating cottages', 'জল, সবুজ ও আপনজনের জন্য ব্যক্তিগত প্রাকৃতিক আবাসন।', 'An intimate retreat inspired by water, greenery and time together.', 'cottages.html', '01'),
    card('resort', 'রিসোর্ট ও আতিথেয়তা', 'Resort & hospitality', '৫-স্টার আবাসন, হালাল ডাইনিং ও পরিবারের প্রশান্তিময় ছুটি।', 'A 5-star destination for family escapes, dining and shared leisure.', 'resort.html', '02'),
    card('nature', 'অ্যাগ্রো ও পারিবারিক অভিজ্ঞতা', 'Agro & family experiences', 'প্রকৃতিকে চেনা, বিষমুক্ত বাগান ও শিশুদের প্রাণবন্ত বিনোদন।', 'Discover the outdoors, walk through greenery and nurture curiosity.', 'agro.html', '03')
]

def cta(title_bn="ছবির বাইরে, প্রকল্পটি জানুন কাছ থেকে।", title_en="Go beyond the pictures. Get to know the project.", body_bn="পরিদর্শনের সময়, ফ্রি শাটল বাস ও বর্তমান অগ্রগতি জানতে আমাদের প্রতিনিধিদের সাথে কথা বলুন।", body_en="Talk to our team about visiting times, complimentary shuttle service and current availability."):
    return f'<aside class="page-cta"><div><span class="eyebrow">LET’S PLAN YOUR VISIT</span>{t(title_bn, title_en, "h2")}{t(body_bn, body_en, "p")}</div>{link("booking.html", "ভিজিটের আবেদন করুন", "Plan a visit", "primary-button")}</aside>'

def faq(items):
    return '<div class="faq-list">' + ''.join(f'<details><summary>{t(q, qe)}</summary>{t(a, ae, "p")}</details>' for q, qe, a, ae in items) + '</div>'

pages = {}
def add(slug, bn, en, desc, descen, body, photo=None, parent=None):
    pages[slug] = (bn, en, desc, descen, body, photo, parent)

# ==========================================
# 1. ABOUT US (আমাদের সম্পর্কে)
# ==========================================
about_body = (
    section('আমাদের লক্ষ্য ও রূপকল্প', 'Our Vision & Purpose',
        f'<div class="story-layout"><div>'
        f'{t("তাকওয়া ভিলেজ লিমিটেড (Taqwa Village Ltd.) বাংলাদেশের প্রথম দূরদর্শী নৈতিক ও পরিবারভিত্তিক লাইফস্টাইল ইকো-রিসোর্ট প্রকল্প। ঢাকার অত্যন্ত সন্নিকটে পূর্বাচল ৩০ নম্বর সেক্টর সংলগ্ন উলুখোলা এলাকায় ১০০+ বিঘা নির্মল প্রাকৃতিক পরিবেশজুড়ে গড়ে উঠছে এই অনন্য আবাসন。", "Taqwa Village Ltd. is Bangladesh’s premier ethical, family-first eco-lifestyle and resort sanctuary. Spread across 100+ bighas near Purbachal Sector 30 in Ulukhola, Dhaka, it harmonizes nature, family ethics and modern hospitality.", "p")}'
        f'{t("আমরা বিশ্বাস করি একটি সমৃদ্ধ জীবনধারা কেবল বিলাসিতার প্রদর্শনী নয়; বরং তা হওয়া উচিত মানসিক সুস্থতা, পারিবারিক বন্ধন, আধ্যাত্মিক প্রশান্তি ও টেকসই প্রকৃতির এক অপূর্ব প্রতিফলন। তাই এখানে শিশুদের নিরাপদ বিনোদন, মা-বোনদের সম্পূর্ণ পর্দাঘেরা প্রাইভেসি এবং শতভাগ হালাল পরিবেশ নিশ্চিত করা হয়েছে।", "We believe true luxury is rooted in peace of mind, strong family bonds, spiritual tranquility and sustainable living. That is why Taqwa Village is crafted with complete family privacy, separate amenities for women, and 100% Shariah-guided principles.", "p")}'
        f'{link("projects.html", "আমাদের প্রকল্প জোনগুলো দেখুন", "Explore our project zones")}'
        f'</div><blockquote>{t("“প্রকৃতির কোলে পারিবারিক বন্ধন ও আধ্যাত্মিক প্রশান্তির এক নিরাপদ ঠিকানা।”", "“A serene sanctuary for family bonding and spiritual peace in nature’s lap.”")}</blockquote></div>',
        'ETHICAL FOUNDATION') +
    section('যে ৪টি মৌলিক মূল্যবোধ আমাদের পরিচালনা করে', 'The 4 Guiding Pillars',
        '<div class="feature-grid">' +
        feature('coins', '১০০% সুদমুক্ত শরিয়াহ মডেল', '100% Shariah Compliant', 'দেশের শীর্ষস্থানীয় ইসলামিক স্কলার ও মুফতি বোর্ডের প্রত্যক্ষ তত্ত্বাবধানে সকল আর্থিক ও পরিচালন নীতিমালা শতভাগ সুদমুক্ত ও শরিয়াহসম্মত।', 'All financial investments and operations strictly adhere to authentic Islamic Mudarabah/Musharakah guidelines vetted by prominent scholars.') +
        feature('users', 'পারিবারিক শালীনতা ও সুরক্ষা', 'Family Dignity & Privacy', 'মা-বোনদের জন্য সম্পূর্ণ পৃথক পর্দাঘেরা ইনডোর-আউটডোর সুইমিং পুল, স্পা এবং সার্বক্ষণিক আধুনিক গেটেড সিকিউরিটি প্রটোকল।', 'Private ladies-only swimming pools, family leisure spaces and around-the-clock gated security ensure complete peace of mind.') +
        feature('leaf', 'সবুজ প্রকৃতি ও অর্গানিক জীবন', 'Sustainable Green Sanctuary', '১০০+ বিঘা সবুজে ঘেরা প্রাকৃতিক জলাশয়, নিজস্ব অর্গানিক ফার্ম ও বিষমুক্ত খাদ্যের নিশ্চয়তা যা নগর জীবনের দূষণ থেকে সম্পূর্ণ মুক্ত।', 'Over 100 bighas of verdant lakes, chemical-free agro farms and pristine fresh air, completely away from urban pollution.') +
        feature('badge-check', 'স্থায়ী সম্পদ ও হালাল ডিভিডেন্ড', 'Permanent Deeds & Halal ROI', 'সাফ-কবলা সরকারি জমি রেজিস্ট্রি এবং রিসোর্ট শেয়ারহোল্ডারদের জন্য বাৎসরিক আকর্ষণীয় হালাল মুনাফা ও ফ্রি স্টে সুবিধা।', 'Sub-kabla registered land titles, predictable annual halal dividends, and complimentary family stay nights for investors.') +
        '</div>',
        'CORE VALUES') +
    section('অবস্থান ও কৌশলগত যোগাযোগ', 'Strategic Location & Connectivity',
        f'<div class="detail-split"><article class="info-panel"><span class="eyebrow">ACCESSIBILITY</span>'
        f'{t("ঢাকার প্রবেশদ্বারে সহজ যাতায়াত", "Effortless Access from Key Dhaka Hubs", "h3")}'
        f'{t("কুড়িল বিশ্বরোড থেকে ৩০০ ফুট এক্সপ্রেসওয়ে হয়ে মাত্র ২০ মিনিটে ঢাকা বাইপাস সংলগ্ন উলুখোলায় পৌঁছানো যায়। হযরত শাহজালাল আন্তর্জাতিক বিমানবন্দর ও উত্তরা থেকে ২৫-৩০ মিনিটের ড্রাইভ。", "Just 20 minutes from Kuril Flyover via the 300ft Expressway to Ulukhola. Effortless 25-30 minute drive from Hazrat Shahjalal International Airport and Uttara.", "p")}'
        f'{t("শুক্র ও শনিবার আমাদের বনানী করপোরেট অফিস এবং কুড়িল থেকে বিনামূল্যে এসি শাটল মাইক্রোবাস সার্ভিস চালু রয়েছে।", "Complimentary AC shuttle bus services operate every Friday and Saturday from our Banani corporate office and Kuril.", "p")}'
        f'{link("contact.html", "ম্যাপ ও দিকনির্দেশনা দেখুন", "View map and directions")}'
        f'</article><article class="info-panel"><span class="eyebrow">KEY DISTANCES</span>'
        f'<ul>'
        f'<li>{t("কুড়িল বিশ্বরোড / ৩০০ ফুট: ২০ মিনিট", "Kuril Flyover / 300ft: 20 Minutes")}</li>'
        f'<li>{t("বিমানবন্দর / উত্তরা: ২৫-৩০ মিনিট", "Airport / Uttara: 25-30 Minutes")}</li>'
        f'<li>{t("গুলশান / বনানী: ৩০-৩৫ মিনিট", "Gulshan / Banani: 30-35 Minutes")}</li>'
        f'<li>{t("পূর্বাচল সেক্টর ৩০: সংলগ্ন (০ কিমি)", "Purbachal Sector 30: Adjacent (0 km)")}</li>'
        f'</ul>'
        f'{link("booking.html?interest=site_visit", "সাইট ভিজিট বুক করুন", "Schedule a visit")}'
        f'</article></div>',
        'STRATEGIC CONNECTIVITY') +
    section('সাধারণ জিজ্ঞাসা ও উত্তর', 'Frequently Asked Questions',
        faq([
            ('তাকওয়া ভিলেজ কীভাবে একটি সাধারণ রিসোর্ট থেকে আলাদা?', 'How is Taqwa Village different from regular resorts?', 'তাকওয়া ভিলেজ একটি নৈতিক ও পরিবারভিত্তিক ইকো-ভিলেজ। এখানে রয়েছে সম্পূর্ণ পর্দাঘেরা নারীদের আলাদা বিনোদন ও সুইমিং পুল, কেন্দ্রীয় জামে মসজিদ, ১০০% হালাল খাদ্য সরবরাহ এবং সুদমুক্ত বিনিয়োগ মডেল।', 'Taqwa Village is an ethical, family-first destination featuring segregated pools for women, a central Grand Mosque, 100% halal organic food, and an interest-free Shariah investment framework.'),
            ('প্রকল্পের বর্তমান নির্মাণ অগ্রগতি কেমন?', 'What is the current construction progress?', 'প্রথম ধাপের ভূমি উন্নয়ন ও লেক খনন সম্পন্ন হয়েছে। বর্তমানে ফ্লোটিং কটেজের কাঠামো ও রিসোর্টের ফাউন্ডেশন পাইলিং দ্রুত এগিয়ে চলেছে (ফেজ ১: ৭৮% সম্পন্ন)।', 'Phase 1 earth development and lake excavations are complete. Floating cottage structures and resort piling are progressing rapidly (Phase 1: 78% complete).'),
            ('আমি কি সপরিবারে প্রকল্প সাইট ঘুরে দেখতে পারব?', 'Can I visit the site with my family?', 'জি হ্যাঁ! আমরা প্রতি সপ্তাহে শুক্র ও শনিবার ঢাকা থেকে পরিবারসহ বিনামূল্যে ফ্রি এসি শাটল বাস পরিচালনা করি। হটলাইনে ফোন করে বা বুকিং ফর্ম থেকে সিট বুক করতে পারেন।', 'Yes! We organize free family shuttle trips every Friday and Saturday from Dhaka. You can reserve seats via our hotline or booking form.')
        ]),
        'FAQ')
)
add('about', 'প্রকৃতি ও পরিবারের জন্য, এক সুন্দর নৈতিক ঠিকানা।', 'A Thoughtful Place for Nature, Family & Values.',
    'তাকওয়া ভিলেজের কেন্দ্রে রয়েছে সহজ একটি বিশ্বাস — ভালো থাকার সঙ্গে প্রকৃতি, পরিবার ও আধ্যাত্মিক মূল্যবোধের গভীর সম্পর্ক।',
    'At the heart of Taqwa Village is a profound conviction: true wellbeing flourishes through nature, family harmony and spiritual grounding.',
    about_body, 'nature')

# ==========================================
# 2. ALL PROJECTS (প্রকল্প পরিচিতি)
# ==========================================
projects_body = (
    '<div class="destination-grid">' + ''.join(cards) + '</div>' +
    section('প্রকল্পের ৫টি পরিকল্পিত বিশেষ জোন', 'The 5 Planned Zones of Taqwa Village',
        '<div class="feature-grid">' +
        feature('home', 'জোন ১: ফ্লোটিং ডুপ্লেক্স কটেজ', 'Zone 1: Floating Duplex Cottages', 'লেকের ওপর কাঠের নান্দনিক ডুপ্লেক্স ভিলা, ব্যক্তিগত সান ডেক ও বাটলার সার্ভিস।', 'Luxury waterfront duplex cottages built over the lake with private decks and butler service.') +
        feature('hotel', 'জোন ২: ৫-স্টার ইকো রিসোর্ট ও সুইটস', 'Zone 2: 5-Star Eco Resort & Suites', 'আন্তর্জাতিক মানের লাক্সারি স্যুট, পৃথক সুইমিং পুল, স্পা ও ১০০০ আসনের কনভেনশন হল।', 'World-class suites, segregated swimming pools, wellness spa and 1,000-seat convention facility.') +
        feature('landmark', 'জোন ৩: কেন্দ্রীয় জামে মসজিদ ও লাইব্রেরি', 'Zone 3: Grand Jame Mosque & Library', '৩,০০০ মুসল্লির ধারণক্ষমতাসম্পন্ন দৃষ্টিনন্দন স্থাপত্য, ইসলামিক রিসার্চ সেন্টার ও এবাদতখানা।', 'Grand 3,000 capacity mosque with Islamic research library and dedicated ladies prayer hall.') +
        feature('sprout', 'জোন ৪: ১০০% অর্গানিক ফার্ম ও ফিশিং', 'Zone 4: Organic Agro Farm & Fisheries', 'বিষমুক্ত শাকসবজি খামার, ফলের বাগান, লাইভ দেশি মাছ চাষ ও রিক্রিয়েশনাল ফিশিং ডেক।', 'Chemical-free vegetable greenhouse, fruit orchards, aquaculture and recreational fishing.') +
        feature('tent', 'জোন ৫: কিডস থিম পার্ক ও স্প্ল্যাশ জোন', 'Zone 5: Kids Theme Park & Water Splash', 'শিশুদের জন্য নিরাপদ রাইডস, আলাদা স্প্ল্যাশ ওয়াটার পার্ক, ট্র্যাম্পোলিন ও ক্যাম্পিং গ্রাউন্ড।', 'Child-safe adventure rides, dedicated water splash zone, trampolines and camping spaces.') +
        feature('plane', 'অবকাঠামো ও হেলিপ্যাড সুবিধা', 'Zone 6: Infrastructure & Helipad', '৬০ ফুট ও ৩০ ফুট অভ্যন্তরীণ পাকা সড়ক, সৌরবিদ্যুৎ ব্যাকআপ এবং নিজস্ব হেলিপ্যাড ও ভিআইপি লাউঞ্জ।', '60ft & 30ft paved internal roads, solar energy backup, dedicated helipad and VIP lounge.') +
        '</div>',
        'MASTER PLAN HIGHLIGHTS') +
    section('প্রকল্পের অবকাঠামো ও নির্মাণ মান', 'Engineering & Construction Standards',
        f'<div class="detail-split"><article class="info-panel"><span class="eyebrow">SUSTAINABLE ENGINEERING</span>'
        f'{t("পরিবেশবান্ধব ও দীর্ঘস্থায়ী নির্মাণ শৈলী", "Eco-Friendly & Long-Lasting Engineering", "h3")}'
        f'{t("তাকওয়া ভিলেজের প্রতিটি স্থাপনা উচ্চমানের সয়েল টেস্ট ও আন্তর্জাতিক পরিবেশবান্ধব প্রকৌশল নীতি মেনে নির্মিত হচ্ছে। ফ্লোটিং কটেজগুলোতে ব্যবহৃত হচ্ছে বিশেষ ট্রিটেড টেকসই কাঠ ও ওয়াটারপ্রুফ মেটেরিয়ালস যা বহু দশক অক্ষত থাকে।", "Every structure at Taqwa Village adheres to stringent soil engineering and international green building guidelines. Floating cottages feature specially treated weather-resistant timber and eco-composites.", "p")}'
        f'{link("cottages.html", "ফ্লোটিং কটেজের বিবরণ", "Explore cottage specs")}'
        f'</article><article class="info-panel"><span class="eyebrow">INVESTMENT & OWNERSHIP</span>'
        f'{t("নিরাপদ মালিকানা ও নিয়মিত হালাল ডিভিডেন্ড", "Secure Ownership & Predictable Dividends", "h3")}'
        f'{t("আপনি চাইলে সম্পূর্ণ কটেজের স্থায়ী সাফ-কবলা মালিক হতে পারেন, অথবা রিসোর্ট ফ্র্যাকশনাল শেয়ারহোল্ডার হিসেবে বাৎসরিক ১৩-১৬% হালাল আয়ের অংশীদার হতে পারেন।", "Acquire full permanent ownership of a presidential cottage with sub-kabla registration, or join as a resort fractional shareholder yielding 13-16% annual halal returns.", "p")}'
        f'{link("investment.html", "বিনিয়োগ ও শেয়ারহোল্ডার তথ্য", "Explore investment details")}'
        f'</article></div>',
        'QUALITY ASSURANCE') +
    section('আপনার আগ্রহ অনুযায়ী পরবর্তী পদক্ষেপ', 'Take Your Next Step Today',
        '<div class="feature-grid">' +
        feature('calendar-check', 'সাইট পরিদর্শনের আবেদন', 'Schedule a Site Visit', 'প্রতি শুক্র ও শনিবার আমাদের ফ্রি এসি শাটল মাইক্রোবাসে সপরিবারে প্রকল্প এলাকা ঘুরে দেখুন।', 'Join our complimentary Friday & Saturday family shuttle to experience the site in person.') +
        feature('message-circle', 'হোয়াটসঅ্যাপে সরাসরি পরামর্শ', 'Direct WhatsApp Consultation', 'ইউনিটের মূল্য, সহজ কিস্তির সুযোগ ও বুকিং প্রক্রিয়া সম্পর্কে সিনিয়র কর্মকর্তার সাথে কথা বলুন।', 'Chat directly with senior project consultants about pricing, installments and booking.') +
        feature('trending-up', 'শেয়ারহোল্ডার হিসেবে যুক্ত হোন', 'Become a Shareholder', 'মাত্র ৳ ২,৫০,০০০ থেকে শুরু করে রিসোর্ট শেয়ারের মাধ্যমে আজীবন হালাল আয়ের সুযোগ নিন।', 'Start from BDT 2,50,000 to earn lifetime halal dividends and complimentary resort nights.') +
        '</div>')
)
add('projects', 'এক ঠিকানায়, অনেক রূপান্তরমূলক অভিজ্ঞতা।', 'One Destination. Many Transformative Experiences.',
    'তাকওয়া ভিলেজের প্রস্তাবিত ফ্লোটিং কটেজ, ফাইভ-স্টার রিসোর্ট, জামে মসজিদ ও প্রকৃতিনির্ভর অ্যাগ্রো জোন ঘুরে দেখুন।',
    'Explore the proposed presidential floating cottages, 5-star eco resort, grand mosque and nature-led agro park at Taqwa Village.',
    projects_body, 'masterplan')

# ==========================================
# 3. COTTAGES (ফ্লোটিং ডুপ্লেক্স কটেজ)
# ==========================================
cottages_body = (
    section('জলের ওপর অনন্য স্থাপত্য শৈলী', 'Architectural Splendor Over Clear Waters',
        f'<div class="story-layout"><div>'
        f'{t("প্রেসিডেনশিয়াল ফ্লোটিং ডুপ্লেক্স কটেজ হলো তাকওয়া ভিলেজের সবচেয়ে আকর্ষণীয় সিগনেচার আবাসন। শান্ত প্রাকৃতিক লেকের স্বচ্ছ জলের ওপর আধুনিক ডুপ্লেক্স ডিজাইনে নির্মিত এই কটেজগুলো আপনাকে দেবে মালদ্বীপ বা বালির মতো আন্তর্জাতিক মানের ওয়াটার ভিলা অভিজ্ঞতা।", "The Presidential Floating Duplex Cottages represent the crown jewel of Taqwa Village. Constructed over tranquil lake waters, these duplex villas offer a world-class waterfront living experience reminiscent of top international eco-resorts.", "p")}'
        f'{t("কটেজগুলোতে ব্যবহৃত হয়েছে সাউন্ডপ্রুফ গ্লাস উইন্ডো, প্রাইভেট সান ডেক, সুপরিসর ড্রয়িং-ডাইনিং, আধুনিক হালাল কিচেন এবং নিজস্ব বোট ডকিং স্পেস। পরিবারের সদস্যদের নিয়ে পূর্ণ নিভৃততায় সময় কাটানোর জন্য এটি একটি অনবদ্য ঠিকানা।", "Featuring soundproof panoramic glass, private sun decks, spacious living-dining, modern kitchenettes and private boat docking, it provides the ultimate private family sanctuary.", "p")}'
        f'{link("booking.html?interest=cottage", "কটেজ বুকিং আবেদন করুন", "Inquire for Cottage", "primary-button")}'
        f'</div><blockquote>{t("“লেকের শান্ত জলে ভেসে থাকা কাঠের ডুপ্লেক্স ভিলা—যেখানে প্রতিটি সকাল শুরু হয় প্রকৃতির অপার সৌন্দর্যে।”", "“Timber duplex villas floating serenely over lake waters—where every dawn greets you with unspoiled nature.”")}</blockquote></div>',
        'SIGNATURE WATER VILLAS') +
    section('কটেজের বৈশিষ্ট্য ও স্পেসিফিকেশন', 'Cottage Features & Specifications',
        '<div class="feature-grid">' +
        feature('home', '১৮৫০ বর্গফুটের ডুপ্লেক্স লেআউট', '1,850 Sq Ft Duplex Plan', '৩টি মাস্টার বেডরুম, এটাচড বাথরুম, সুপরিসর লিভিং রুম ও প্যানোরামিক ব্যালকনি।', '3 spacious en-suite master bedrooms, open-concept living area and panoramic lake-facing balconies.') +
        feature('sun', 'ব্যক্তিগত লেক ডেক ও লাউঞ্জ', 'Private Water Deck & Lounge', 'জলের ঠিক ওপরে সানবাথ, ফিশিং ও পরিবারের সাথে বিকেলের চা উপভোগের জন্য নিজস্ব কাঠের ডেক।', 'Overwater timber deck perfect for morning tea, recreational angling, and evening sunset vistas.') +
        feature('shield-check', '১০০% সাউন্ডপ্রুফ ও পরিবেশবান্ধব', 'Soundproof & Eco-Treated Timber', 'বিশেষ ট্রিটেড কাঠ ও ডাবল গ্লেজড গ্লাস যা বাহ্যিক শব্দমুক্ত ও প্রাকৃতিক তাপমাত্রা নিয়ন্ত্রণ করে।', 'Treated anti-rot timber and double-glazed insulated glass ensure complete thermal and acoustic comfort.') +
        feature('bell', '২৪/৭ ডেডিকেটেড বাটলার সার্ভিস', '24/7 Dedicated Butler Service', 'রুমে খাবার সরবরাহ, হাউসকিপিং ও অতিথিদের ব্যক্তিগত চাহিদায় সার্বক্ষণিক সেবাকর্মী।', 'Round-the-clock personalized dining, housekeeping and guest assistance.') +
        feature('ship', 'প্রাইভেট বোট ডকিং প্ল্যাটফর্ম', 'Private Boat Docking Slip', 'কটেজের সামনেই স্পিডবোট বা প্যাডেল বোটে সরাসরি লেকভ্রমণে বের হওয়ার নিজস্ব ঘাট।', 'Direct private boat landing slip for immediate lake boating and kayaking access.') +
        feature('badge-check', 'সাফ-কবলা মালিকানা বা শেয়ার', 'Sub-Kabla Deed or Shareholding', 'পুরো কটেজের স্থায়ী সাফ-কবলা মালিকানা দলিল অথবা ফ্র্যাকশনাল শেয়ারহোল্ডার হওয়ার সুযোগ।', 'Available for full permanent sub-kabla deed registration or fractional profit-sharing shares.') +
        '</div>',
        'SPECIFICATIONS') +
    section('মালিকানা ও বিনিয়োগের বিকল্পসমূহ', 'Ownership & Investment Models',
        f'<div class="detail-split"><article class="info-panel"><span class="eyebrow">FULL UNIT PURCHASE</span>'
        f'{t("সম্পূর্ণ কটেজের স্থায়ী সাফ-কবলা মালিকানা", "Full Unit Permanent Ownership", "h3")}'
        f'{t("মূল্য: ৳ ৫৫,০০,০০০ (সম্পূর্ণ ফার্নিশড ইউনিট)। আপনি পাবেন শতভাগ সাফ-কবলা সরকারি দলিল ও নামজারি। নিজের অবকাশ যাপনের পাশাপাশি আপনি না থাকলে রিসোর্ট ম্যানেজমেন্টের মাধ্যমে ভাড়া দিয়ে বাৎসরিক ৳ ৭-৯ লাখ হালাল আয় করতে পারবেন।", "Price: BDT 55,00,000 (Fully furnished). Includes 100% permanent sub-kabla title registration. Use it for unlimited family holidays or let resort management rent it out to earn BDT 700,000 - 900,000 annually.", "p")}'
        f'{link("booking.html?interest=cottage", "মালিকানা আলোচনা শুরু করুন", "Inquire for ownership")}'
        f'</article><article class="info-panel"><span class="eyebrow">FRACTIONAL SHARE</span>'
        f'{t("ফ্র্যাকশনাল কটেজ শেয়ার সুবিধা", "Fractional Ownership Share", "h3")}'
        f'{t("মূল্য: ৳ ২,৫০,০০০ / শেয়ার। সীমিত বাজেটে কটেজ আয়ের অংশীদার হওয়ার সুবর্ণ সুযোগ। প্রতি বছর নগদ হালাল ডিভিডেন্ড এবং ৭ রাত বিনামূল্যে পরিবারসহ ফ্রি থাকার সুবিধা।", "Price: BDT 2,50,000 per share. An accessible pathway to participate in luxury cottage returns with annual halal dividends and 7 complimentary holiday nights.", "p")}'
        f'{link("investment.html", "শেয়ারহোল্ডার সুবিধা দেখুন", "Explore share benefits")}'
        f'</article></div>',
        'OWNERSHIP OPTIONS') +
    section('কটেজ সম্পর্কিত সাধারণ জিজ্ঞাসা', 'Frequently Asked Questions',
        faq([
            ('কটেজটি কি সারা বছর ব্যবহারের উপযোগী?', 'Is the cottage suitable for year-round living?', 'জি হ্যাঁ! কটেজগুলোতে আধুনিক এসি, হিটিং, নিরবচ্ছিন্ন সোলার ব্যাকআপ বিদ্যুৎ ও উচ্চগতির ওয়াইফাই রয়েছে। ফলে শীত, বর্ষা বা গ্রীষ্ম—যেকোনো মৌসুমে এটি সম্পূর্ণ আরামদায়ক।', 'Yes! All cottages are equipped with climate control, uninterrupted solar power backup, and high-speed Wi-Fi, ensuring supreme comfort in every season.'),
            ('আমি না থাকলে কটেজের দেখভালের দায়িত্ব কার?', 'Who maintains the cottage when I am away?', 'তাকওয়া ভিলেজ রিসোর্ট ম্যানেজমেন্ট সার্বক্ষণিক রক্ষণাবেক্ষণ, সিকিউরিটি ও ল্যান্ডস্কেপিং পরিচালনা করে। ফলে মালিকের কোনো বাড়তি ঝক্কি পোহাতে হয় না।', 'Taqwa Village Resort Management manages 24/7 security, continuous maintenance, and housekeeping, giving owners complete peace of mind.')
        ]),
        'FAQ')
)
add('cottages', 'জলের ওপর ভেসে থাকা, আপন পারিবারিক স্বর্গোদ্যান।', 'Private Luxury Waterfront Duplex Cottages.',
    'স্বচ্ছ লেকের ওপর কাঠের স্থাপত্য, ব্যক্তিগত সান ডেক ও পরিবারের একান্ত নির্জনতার অনন্য প্রকাশ।',
    'Architectural timber duplex water villas over clear lake waters, complete with private decks and absolute family seclusion.',
    cottages_body, 'cottage', 'projects')

# ==========================================
# 4. RESORT (৫-স্টার ইকো রিসোর্ট)
# ==========================================
resort_body = (
    section('আন্তর্জাতিক মানের আতিথেয়তা ও পারিবারিক অবকাশ', 'World-Class Hospitality & Family Leisure',
        f'<div class="story-layout"><div>'
        f'{t("তাকওয়া ভিলেজ ৫-স্টার ইকো রিসোর্ট কমপ্লেক্স আন্তর্জাতিক আতিথেয়তার মান এবং খাঁটি দেশীয় উষ্ণতার এক অনন্য মেলবন্ধন। ঢাকা শহরের কর্মব্যস্ত নাগরিক জীবনের চাপ কাটিয়ে এখানে আপনি পাবেন পাখির কলকাকলি, সবুজ লন ও লেকের মৃদু হাওয়া।", "The 5-Star Eco Resort complex at Taqwa Village combines global hospitality excellence with warm Bangladeshi heritage. Escape urban stress to immerse in lush green lawns, bird songs and gentle lake breezes.", "p")}'
        f'{t("রিসোর্টে রয়েছে আধুনিক ডিলাক্স ও এক্সিকিউটিভ স্যুট, পুরুষ ও নারীদের জন্য সম্পূর্ণ পৃথক আন্তর্জাতিক সুইমিং পুল ও স্পা, স্বাস্থ্যকর হালাল ডাইনিং এবং ১,০০০ আসনবিশিষ্ট আন্তর্জাতিক কনভেনশন সেন্টার।", "The resort offers deluxe and executive suites, dedicated segregated swimming pools and wellness spas for men and women, authentic halal dining, and a 1,000-seat convention hall.", "p")}'
        f'{link("booking.html?interest=resort_investment", "রিসোর্ট বুকিং ও তথ্য আবেদন", "Book or Inquire for Resort", "primary-button")}'
        f'</div><blockquote>{t("“যেখানে প্রতিটি অবকাশ হয়ে ওঠে অর্থবহ, মর্যাদাপূর্ণ ও শারীরিক-মানসিক পুনরুজ্জীবনের ক্ষেত্র।”", "“Where every holiday transforms into meaningful rest, dignity, and wholesome rejuvenation.”")}</blockquote></div>',
        'RESORT EXCELLENCE') +
    section('রিসোর্টের প্রধান সুবিধাসমূহ', 'Signature Resort Amenities',
        '<div class="feature-grid">' +
        feature('hotel', 'লাক্সারি ডিলাক্স ও ফ্যামিলি স্যুট', 'Luxury Deluxe & Family Suites', 'আন্তর্জাতিক পাঁচ তারকা মানের বেডিং, ব্যালকনি ও আধুনিক এন্টারটেইনমেন্ট সুবিধা।', '5-star quality plush bedding, lakeview balconies, high-speed Wi-Fi and modern amenities.') +
        feature('waves', 'পৃথক সুইমিং পুল ও স্টিম বাথ', 'Segregated Pools & Wellness Spas', 'মা-বোনদের জন্য সম্পূর্ণ পর্দাঘেরা সংরক্ষিত ইনডোর পুল এবং পুরুষদের জন্য আলাদা আউটডোর পুল।', 'Strictly private indoor pools for women alongside separate outdoor pools and wellness spas for men.') +
        feature('utensils', 'মাল্টি-কুইজিন হালাল ডাইনিং', 'Multi-Cuisine Halal Dining', 'দেশি, এরাবিক ও কন্টিনেন্টাল খাবারের সমাহার, নিজস্ব ফার্মের খাঁটি অর্গানিক উপাদান দিয়ে প্রস্তুত।', 'Multi-cuisine halal dining prepared with fresh, chemical-free ingredients from our organic farms.') +
        feature('presentation', '১০০০ আসনের আন্তর্জাতিক কনভেনশন', '1,000-Seat Convention & Banquet', 'কর্পোরেট সেমিনার, এজিএম, পারিবারিক বিয়ে ও পুনর্মিলনীর জন্য আধুনিক অডিটোরিয়াম।', 'State-of-the-art acoustics and catering for corporate retreats, AGMs, and grand family celebrations.') +
        feature('activity', 'ফিটনেস ও হেলথ ক্লাব', 'Fitness Center & Health Club', 'আধুনিক জিম সরঞ্জাম, ফিজিওথেরাপি, স্টিম বাথ ও সিনিয়র সিটিজেন সুস্থতা কর্নার।', 'Modern gym equipment, physical therapy, steam sauna, and specialized senior care.') +
        feature('trending-up', 'রিসোর্ট শেয়ারহোল্ডার সুযোগ', 'Resort Shareholder Opportunity', 'শেয়ার ক্রয়ের মাধ্যমে রিসোর্টের পরিচালন মুনাফার অংশীদারিত্ব ও আজীবন হালাল লভ্যাংশ।', 'Acquire fractional shares to earn annual operating profits, capital growth, and free stay nights.') +
        '</div>',
        'AMENITIES') +
    section('রিসোর্ট শেয়ারহোল্ডার প্যাকেজ', 'Resort Ownership Share Packages',
        f'<div class="detail-split"><article class="info-panel"><span class="eyebrow">SHAREHOLDER PROGRAM</span>'
        f'{t("সীমিত সংখ্যক রিসোর্ট শেয়ারে আজীবন আয়", "Lifetime Halal Income via Resort Shares", "h3")}'
        f'{t("তাকওয়া ভিলেজ রিসোর্টের প্রতিটি শেয়ারের মূল্য মাত্র ৳ ২,৫০,০০০। রিসোর্ট পরিচালনার নিট পরিচালন মুনাফা থেকে বাৎসরিক ১৩%-১৬% হারে হালাল ডিভিডেন্ড সরাসরি শেয়ারহোল্ডারদের ব্যাংক একাউন্টে পাঠানো হয়। এছাড়াও প্রতি বছর পরিবারসহ ৭ রাত বিনামূল্যে রিসোর্টে থাকার অধিকার থাকবে।", "Each resort share is valued at BDT 2,50,000. Shareholders receive 13-16% annual halal dividends from net operating income, plus 7 complimentary holiday nights each year.", "p")}'
        f'{link("investment.html", "সম্পূর্ণ ইনভেস্টমেন্ট মডেল দেখুন", "Explore investment framework")}'
        f'</article><article class="info-panel"><span class="eyebrow">CORPORATE & RETREATS</span>'
        f'{t("কর্পোরেট রিট্রিট ও সেমিনার প্যাকেজ", "Corporate Retreats & Group Packages", "h3")}'
        f'{t("আপনার প্রতিষ্ঠানের বার্ষিক সেমিনার, টিম বিল্ডিং ডে-আউট বা স্ট্র্যাটেজিক মিটিংয়ের জন্য তাকওয়া ভিলেজ রিসোর্ট একটি আদর্শ ডেস্টিনেশন। কনফারেন্স হল, মাল্টিমিডিয়া প্রজেক্টর ও বুফে ডাইনিংয়ের সুব্যবস্থা রয়েছে।", "An ideal sanctuary for corporate team-building, executive off-sites, and strategic retreats with comprehensive AV technology, auditoriums and banquet catering.", "p")}'
        f'{link("booking.html?interest=resort_investment", "কর্পোরেট বুকিং ইনকোয়ারি", "Inquire for corporate bookings")}'
        f'</article></div>',
        'PACKAGES') +
    section('সাধারণ জিজ্ঞাসা', 'Frequently Asked Questions',
        faq([
            ('রিসোর্টে কি ডে-ট্যুর বা শুধু খাবারের জন্য যাওয়া যায়?', 'Can I visit the resort for day-dining or day tours?', 'জি হ্যাঁ! আমাদের অর্গানিক রেস্তোরাঁ ও ডে-আউট প্যাকেজ বুক করে আপনি সপরিবারে সকাল থেকে সন্ধ্যা পর্যন্ত রিসোর্টের বিভিন্ন জোন উপভোগ করতে পারেন।', 'Yes! Families can book our day-tour and dining packages to enjoy the resort grounds, pools and organic dining from morning to evening.'),
            ('রিসোর্টের খাবার কি শতভাগ হালাল?', 'Is all food served 100% halal?', 'জি শতভাগ! তাকওয়া ভিলেজের ডাইনিং সম্পূর্ণ হালাল শরিয়াহ নীতিতে পরিচালিত। সকল মাংস জবেহ থেকে শুরু করে প্রক্রিয়াকরণ কঠোরভাবে তদারকি করা হয়।', 'Absolutely. All food preparation follows strict halal standards with organic farm-fresh ingredients and rigorous hygiene supervision.')
        ]),
        'FAQ')
)
add('resort', 'একসঙ্গে ভালো থাকার অবকাশ ও ফাইভ-স্টার আতিথেয়তা।', '5-Star Luxury Eco Resort & Suites.',
    'আন্তর্জাতিক মানের আবাসন, পৃথক পর্দাঘেরা সুইমিং পুল, হালাল ডাইনিং ও ১,০০০ আসনবিশিষ্ট আধুনিক কনভেনশন সেন্টার।',
    'Global hospitality standards, strictly segregated swimming pools, multi-cuisine halal dining and a 1,000-seat convention facility.',
    resort_body, 'resort', 'projects')

# ==========================================
# 5. AGRO & FAMILY PARK (অ্যাগ্রো ও পার্ক)
# ==========================================
agro_body = (
    section('সবুজের মাঝে নতুন কিছু শেখা ও বিশুদ্ধ আনন্দ', 'Nature Education, Pure Food & Family Fun',
        f'<div class="story-layout"><div>'
        f'{t("তাকওয়া ভিলেজ অর্গানিক অ্যাগ্রো ও ফ্যামিলি পার্ক হলো শহুরে শিশুদের প্রকৃতিকে জানার এবং খাঁটি গ্রামীণ মাটির সান্নিধ্য পাওয়ার এক স্বপ্নিল অঙ্গন। কৃত্রিম জীবনের দেয়াল ভেঙে এখানে শিশুরা দেখতে পায় কীভাবে মাটি থেকে গাছ বড় হয়, কীভাবে বিষমুক্ত শাকসবজি উৎপাদিত হয়।", "The Organic Agro & Family Park at Taqwa Village is a vibrant sanctuary where children connect with nature and experience the purity of rural heritage. It bridges urban living with the wonders of soil, agriculture and open-air adventure.", "p")}'
        f'{t("প্রকল্পে রয়েছে বিশাল ফলের বাগান, গ্রিনহাউস, ড্রাগন ও পেয়ারা বাগান, দেশি হাঁস-মুরগি ও গরুর ডেইরি খামার, সুবিশাল ফিশিং লেক এবং আধুনিক শিশুবান্ধব অ্যাডভেঞ্চার রাইডস।", "Featuring extensive fruit orchards, greenhouse farming, dairy farms, sprawling fishing lakes and modern child-safe adventure playgrounds, it offers rich recreational recreation for every age group.", "p")}'
        f'{link("booking.html?interest=family_dayout", "ডে-আউট প্যাকেজ বুক করুন", "Book Day-Out Package", "primary-button")}'
        f'</div><blockquote>{t("“যেখানে শিশুরা প্রকৃতি চেনে, মাটি স্পর্শ করে এবং পুরো পরিবার বিষমুক্ত খাবারের স্বাদ নেয়।”", "“Where children discover nature, touch the earth, and families savor 100% chemical-free harvests.”")}</blockquote></div>',
        'AGRO TOURISM') +
    section('অ্যাগ্রো ও পার্কের প্রধান আকর্ষণসমূহ', 'Signature Park Highlights',
        '<div class="feature-grid">' +
        feature('sprout', '১০০% বিষমুক্ত অর্গানিক বাগান', '100% Chemical-Free Greenhouses', 'কোনো রাসায়নিক কীটনাশক ছাড়াই উৎপাদিত টাটকা শাকসবজি, দেশি শাক ও বিদেশি অর্গানিক ফল।', 'Fresh organic greens, seasonal vegetables and exotic fruits cultivated with zero synthetic pesticides.') +
        feature('fish', 'লেক ফিশিং ও ওয়াটার বোটিং', 'Recreational Fishing & Lake Boating', 'স্বচ্ছ লেকে রুই, কাতলা ও শিং মাছ শিকারের আনন্দ এবং পারিবারিক প্যাডেল বোটিং ও কায়াকিং।', 'Angling native carp in stocked lakes alongside family kayaking and gentle paddle boat excursions.') +
        feature('tent', 'কিডস অ্যাডভেঞ্চার ও থিম পার্ক', 'Kids Adventure & Splash Playground', 'নিরাপদ ক্লাইম্বিং নেট, ট্র্যাম্পোলিন, সুইং, স্লাইড এবং গ্রীষ্মকালীন স্প্ল্যাশ পুল।', 'Child-friendly climbing frames, outdoor trampolines, zip lines and safe shallow splash pools.') +
        feature('apple', 'ফার্ম-টু-টেবিল তাজা খাবার', 'Farm-to-Table Fresh Produce', 'খামার থেকে সরাসরি তোলা তাজা শাকসবজি ও দেশি মাছ দিয়ে তৈরি সুস্বাদু মধ্যাহ্নভোজ।', 'Wholesome buffet dining crafted directly from morning harvests and freshly caught lake fish.') +
        feature('store', 'ইন-হাউস অর্গানিক সুপার শপ', 'In-House Organic Harvest Store', 'প্রকল্পে উৎপাদিত খাঁটি সুন্দরবনের মধু, দেশি ঘি, সরিষার তেল ও ফলমূল ক্রয়ের সুযোগ।', 'Purchase pure raw honey, organic ghee, cold-pressed mustard oil and fresh fruit baskets directly on-site.') +
        feature('footprints', '৩ কিমি ন্যাচারাল ওয়াকিং ট্রেইল', '3 km Scenic Green Pathways', 'লেকের পাড় ঘেঁষে বনায়ন ও ফুলের বাগানের ভেতর দিয়ে হাঁটার স্বাস্থ্যকর পরিবেশ।', 'Shaded walking and jogging tracks bordered by flowering trees and fresh lake breezes.') +
        '</div>',
        'ATTRACTIONS') +
    section('পারিবারিক ডে-আউট ও পিকনিক প্যাকেজ', 'Family Day-Out & Picnic Packages',
        f'<div class="detail-split"><article class="info-panel"><span class="eyebrow">POPULAR PACKAGE</span>'
        f'{t("সম্পূর্ণ দিনের পারিবারিক পিকনিক প্যাকেজ", "Full Day Family Picnic Package", "h3")}'
        f'{t("মূল্য: ৳ ২,৫০০ / জনপ্রতি (শিশুদের জন্য বিশেষ ছাড়)। প্যাকেজে অন্তর্ভুক্ত: সকালের দেশি নাস্তা, খামার ট্যুর, লেকে বোট রাইড, বাচ্চাদের পার্ক এক্সেস, অর্গানিক বুফে লাঞ্চ এবং বিকেলের চা-নাস্তা।", "Price: BDT 2,500 per person (special concession for children). Includes: traditional morning breakfast, guided farm tour, boat ride, theme park access, organic buffet lunch, and afternoon tea.", "p")}'
        f'{link("booking.html?interest=family_dayout", "ডে-আউট বুকিং আবেদন", "Book day excursion")}'
        f'</article><article class="info-panel"><span class="eyebrow">GROUP & INSTITUTION</span>'
        f'{t("স্কুল, মাদ্রাসা ও কর্পোরেট গ্রুপ প্যাকেজ", "Educational & Corporate Day Trips", "h3")}'
        f'{t("৫০ জন বা তার বেশি দলের জন্য রয়েছে বিশেষ ক্যাটারিং ও অ্যাক্টিভিটি সমন্বয় সুবিধা। কৃষি শিক্ষা, পরিবেশ সচেতনতা এবং উন্মুক্ত মাঠে টিম বিল্ডিং গেমসের জন্য আদর্শ।", "Tailored packages for schools, academic institutions and corporate groups of 50+. Includes dedicated agricultural guides, outdoor team sports, and private lawn catering.", "p")}'
        f'{link("contact.html", "গ্রুপ প্যাকেজ আলোচনা করুন", "Discuss group rates")}'
        f'</article></div>',
        'DAY PACKAGES') +
    section('সাধারণ জিজ্ঞাসা', 'Frequently Asked Questions',
        faq([
            ('অ্যাগ্রো পার্ক পরিদর্শনে কি আগাম বুকিং প্রয়োজন?', 'Do we need advance booking for the Agro Park?', 'জি হ্যাঁ! দর্শনার্থীদের পূর্ণ নিরাপত্তা ও মানসম্মত সেবা বজায় রাখার জন্য আমরা সীমিত সংখ্যক অতিথিকে প্রতিদিন প্রবেশাধিকার দিই। তাই আগাম বুকিং জরুরি।', 'Yes! To maintain exclusivity, tranquility and quality catering, daily admissions are limited. Prior reservation is recommended.'),
            ('আমরা কি নিজেদের সাথে খাবার নিয়ে যেতে পারব?', 'Can we bring our own outside food?', 'প্রকল্পের নিজস্ব স্বাস্থ্যকর ও শতভাগ খাঁটি অর্গানিক ফুড কোর্ট রয়েছে। তবে শিশুদের জন্য বিশেষ শিশুখাদ্য সাথে আনার অনুমতি রয়েছে।', 'We provide fresh farm-to-table dining on site. Special infant food or formula is naturally permitted.')
        ]),
        'FAQ')
)
add('agro', 'সবুজের মাঝে নতুন অভিজ্ঞতা, শেখা ও পারিবারিক আনন্দ।', 'Agro Farming, Fresh Harvest & Outdoor Fun.',
    '১০০% বিষমুক্ত বাগান, লেকে রিক্রিয়েশনাল ফিশিং, বাচ্চাদের অ্যাডভেঞ্চার থিম পার্ক ও স্বাস্থ্যকর পারিবারিক ডে-আউট।',
    '100% chemical-free organic farming, stocked fishing lakes, children adventure playgrounds and memorable family day excursions.',
    agro_body, 'nature', 'projects')

# ==========================================
# 6. AMENITIES (সুযোগ-সুবিধা)
# ==========================================
amenities_body = (
    section('একটি স্বয়ংসম্পূর্ণ ইকো-ভিলেজের ১৮+ বিশেষ সুবিধা', '18+ Signature Amenities in One Sanctuary',
        '<div class="feature-grid amenities-grid">' +
        feature('waves', 'পৃথক সুইমিং ও স্পা', 'Segregated Swimming & Spas', 'মহিলা ও পুরুষদের জন্য সম্পূর্ণ আলাদা ও পর্দাঘেরা আন্তর্জাতিক মানের ইনডোর ও আউটডোর সুইমিং পুল।', 'Strictly separate indoor heated pools for women and open-air lap pools for men with steam spas.') +
        feature('landmark', 'কেন্দ্রীয় দৃষ্টিনন্দন জামে মসজিদ', 'Grand Jame Mosque', 'একসাথে ৩,০০০ মুসল্লির জামাত, সমৃদ্ধ ইসলামিক লাইব্রেরি এবং নারী ও শিশুদের জন্য পৃথক ইবাদতখানা।', '3,000 capacity architectural grand mosque featuring Islamic reference library and dedicated ladies hall.') +
        feature('utensils', 'অর্গানিক ফুড কোর্ট ও ক্যাফে', 'Organic Dining & Lake Cafes', 'প্রকল্পের নিজস্ব খামার থেকে সংগৃহীত বিষমুক্ত টাটকা খাদ্য দিয়ে প্রস্তুত শতভাগ খাঁটি হালাল ডাইনিং।', 'Multi-cuisine halal dining prepared with 100% pesticide-free produce from our own agro farms.') +
        feature('tent', 'কিডস থিম ও স্প্ল্যাশ পার্ক', 'Kids Adventure Splash Park', 'শিশুদের শারীরিক বিকাশের জন্য আন্তর্জাতিক মানের নিরাপদ রাইডস, ট্র্যাম্পোলিন ও অগভীর স্প্ল্যাশ পুল।', 'Safe adventure climbing structures, trampolines, gentle zip lines and monitored shallow water splash pads.') +
        feature('ship', 'লেক বোটিং ও ফিশিং ডেক', 'Kayaking & Angling Decks', 'বিশাল লেকে পারিবারিক বোট রাইডিং, প্যাডেল বোটিং ও দেশি রুই-কাতলা মাছ শিকারের বিশেষ সুবিধা।', 'Kayaking and paddle boating on clear waters alongside peaceful angling decks stocked with native fish.') +
        feature('footprints', '৩ কিমি জগিং ও সাইক্লিং ট্রেইল', '3 km Jogging & Cycling Track', 'গাছপালা ও লেকফ্রন্ট ঘেঁষে নির্মিত প্রশস্ত স্বাস্থ্যকর ওয়াকিং ট্রেইল।', 'Paved and shaded jogging pathways bordered by flowering plants and cooling lake breezes.') +
        feature('presentation', 'কনভেনশন হল ও অডিটোরিয়াম', '1,000-Seat Convention Banquet', 'কর্পোরেট সেমিনার, এজিএম, ওয়ার্কশপ ও পারিবারিক উৎসবের জন্য আধুনিক অডিটোরিয়াম।', 'State-of-the-art acoustics, stage lighting and catering for corporate conferences and grand family milestones.') +
        feature('heart-pulse', 'ওয়েলনেস ক্লিনিক ও সিনিয়র কেয়ার', 'Wellness Clinic & Senior Care', '২৪ ঘণ্টা প্রাথমিক স্বাস্থ্যসেবা, জরুরি ফার্স্ট এইড, ফিজিওথেরাপি ও প্রবীণদের স্বাস্থ্য কর্নার।', 'Round-the-clock primary health support, physical therapy, and dedicated senior wellness provisions.') +
        feature('shield-check', '২৪/৭ স্মার্ট গেটেড সিকিউরিটি', '24/7 Gated Smart Security', 'পুরো প্রকল্পজুড়ে সিসিটিভি ক্যামেরা নজরদারি, প্রশিক্ষিত গার্ড এবং ইলেকট্রনিক গেট পাস।', 'Complete perimeter security, smart CCTV monitoring, and strict vehicular gate pass controls.') +
        feature('plane', 'প্রাইভেট হেলিপ্যাড ও লাউঞ্জ', 'Private Helipad & VIP Lounge', 'জরুরি স্বাস্থ্য পরিবহন ও ভিআইপি অতিথিদের দ্রুত ঢাকা ও দেশের বাইরে থেকে যাতায়াতের ব্যবস্থা।', 'Certified on-site helipad for urgent medical transfers and executive VIP arrivals.') +
        feature('sun', 'সোলার পাওয়ার ও গ্রিন এনার্জি', 'Solar Power & 24/7 Backup', 'পরিবেশবান্ধব সৌরবিদ্যুৎ ব্যবস্থা এবং নিরবচ্ছিন্ন ২৪ ঘণ্টা বিদ্যুৎ ও বিশুদ্ধ পানির সরবরাহ।', 'Green solar energy grids and soundproof automated power generators guaranteeing uninterrupted supply.') +
        feature('store', 'অর্গানিক সুপার শপ', 'Organic Harvest Marketplace', 'প্রকল্পের খামারে উৎপাদিত খাঁটি মধু, দেশি ঘি, সরিষার তেল ও মৌসুমি ফল কেনার ইন-হাউস শপ।', 'On-site farm shop providing pure raw honey, cold-pressed mustard oil, and seasonal fresh harvests.') +
        '</div>',
        'FULL AMENITIES DIRECTORY') +
    section('পরিদর্শনের পূর্বে প্রয়োজনীয় তথ্য', 'Good to Know Before Visiting',
        faq([
            ('সব সুবিধা কি বর্তমান পর্যায়ে চালু আছে?', 'Are all amenities currently operational?', 'ফেজ ১ এর আওতায় লেক, অ্যাগ্রো ফার্ম, ডে-আউট পিকনিক জোন ও পাইলট কটেজ চালু রয়েছে। সেন্ট্রাল মসজিদ ও রিসোর্ট কমপ্লেক্সের নির্মাণ কাজ দ্রুত এগিয়ে চলেছে।', 'Under Phase 1, the lake, organic agro farm, day picnic zones and pilot cottages are operational. The grand mosque and resort complex are under active construction.'),
            ('মা-বোনদের পর্দার নিরাপত্তা কীভাবে নিশ্চিত করা হয়?', 'How is women’s modesty and privacy protected?', 'নারীদের জন্য নির্ধারিত প্রতিটি পুল ও অবকাশ জোন চারপাশ থেকে সম্পূর্ণ সুরক্ষিত ও উঁচু সীমানা প্রাচীর দিয়ে ঘেরা। এখানে নারী কর্মী ও নিরাপত্তা সদস্য দ্বারা সেবা দেওয়া হয়।', 'All female wellness and pool areas are completely enclosed with high privacy screens and served exclusively by female staff.'),
            ('সাইট পরিদর্শনে কি বিশেষ কোনো ড্রেসকোড রয়েছে?', 'Is there an expected dress code on site?', 'যেহেতু এটি একটি নৈতিক ও পরিবারভিত্তিক ইকো-ভিলেজ, তাই আমরা সকল অতিথিদের মার্জিত ও শালীন পোশাক পরিধান করার অনুরোধ জানাই।', 'As Taqwa Village is an ethical, family-first sanctuary, all visitors and guests are warmly requested to observe modest and respectful attire.')
        ]),
        'VISITOR INFORMATION')
)
add('amenities', 'প্রতিটি মুহূর্তে, প্রশান্তি ও পারিবারিক পরিপূর্ণতা।', 'Thoughtful Amenities for Every Cherished Moment.',
    'তাকওয়া ভিলেজের ১৮+ আধুনিক সুবিধা: পৃথক সুইমিং পুল, জামে মসজিদ, অর্গানিক ডাইনিং, কিডস পার্ক ও সার্বক্ষণিক নিরাপত্তা।',
    '18+ signature amenities at Taqwa Village: strictly segregated pools, grand mosque, organic dining, children theme park and 24/7 gated security.',
    amenities_body, 'pool')

# ==========================================
# 7. GALLERY (ফটো গ্যালারি)
# ==========================================
gallery_items = [
    ('masterplan', 'stay', 'মাস্টারপ্ল্যান ও পূর্বাচল গ্রিন হাব', 'Aerial Master Plan & 100+ Bigha Hub'),
    ('cottage', 'stay', 'প্রেসিডেনশিয়াল ফ্লোটিং ডুপ্লেক্স কটেজ', 'Presidential Floating Duplex Cottage'),
    ('resort', 'stay', '৫-স্টার ইকো রিসোর্ট ও হোটেল স্যুট', '5-Star Eco Resort & Hotel Suites'),
    ('villa', 'stay', 'লেকভিউ ওয়াটার ভিলা ও সান ডেক', 'Lakeview Waterfront Villa & Sun Deck'),
    ('mosque', 'spiritual', 'কেন্দ্রীয় জামে মসজিদ ও রিসার্চ লাইব্রেরি', 'Grand Jame Mosque & Islamic Library'),
    ('nature', 'nature', '১০০% বিষমুক্ত অর্গানিক ফার্ম ও বাগান', '100% Chemical-Free Organic Farm'),
    ('dining', 'leisure', 'ফার্ম-টু-টেবিল হালাল ডাইনিং ও ক্যাফে', 'Farm-to-Table Halal Dining & Cafe'),
    ('pool', 'leisure', 'পৃথক সংরক্ষিত সুইমিং পুল ও স্পা', 'Segregated Swimming Pool & Spa'),
    ('park', 'leisure', 'শিশুদের অ্যাডভেঞ্চার থিম পার্ক ও রাইডস', 'Kids Adventure Playground & Rides'),
    ('aerial', 'nature', 'পূর্বাচল উলুখোলার মনোরম প্রাকৃতিক জলাশয়', 'Purbachal Ulukhola Serene Lakeview')
]

gallery_markup = (
    '<div class="gallery-filters" role="group" aria-label="Filter gallery">' +
    ''.join(f'<button type="button" data-filter="{key}" aria-pressed="{str(key=="all").lower()}">{t(bn, en)}</button>'
            for key, bn, en in [
                ('all', 'সব ছবি', 'All Images'),
                ('stay', 'কটেজ ও রিসোর্ট', 'Cottages & Resort'),
                ('nature', 'প্রকৃতি ও ফার্ম', 'Nature & Agro'),
                ('spiritual', 'মসজিদ ও আধ্যাত্মিক', 'Mosque & Spiritual'),
                ('leisure', 'অবকাশ ও ডাইনিং', 'Leisure & Dining')
            ]) +
    '</div>' +
    '<div class="gallery-grid">' +
    ''.join(f'<button type="button" class="gallery-tile" data-category="{cat}" data-gallery-image>'
            f'<span class="gallery-photo">{image(key)}<span class="gallery-zoom" aria-hidden="true"><i data-lucide="maximize-2"></i></span></span>'
            f'<span class="gallery-caption">{t(bn, en)}<small>{t("বাস্তব ও পরিকল্পিত স্থিরচিত্র", "Project Lifestyle Visual")}</small></span>'
            f'</button>' for key, cat, bn, en in gallery_items) +
    '</div>' +
    '<p id="gallery-status" class="sr-only" role="status" aria-live="polite"></p>'
)

gallery_body = (
    gallery_markup +
    section('লাইভ ভিডিও ও সোশ্যাল আপডেট', 'Live Video & Social Updates',
        f'<div class="detail-split"><article class="info-panel"><span class="eyebrow">OFFICIAL FACEBOOK</span>'
        f'{t("ফেসবুক পেজে নিয়মিত ড্রোন ভিডিও দেখুন", "Watch Latest Drone Videos on Facebook", "h3")}'
        f'{t("আমাদের অফিশিয়াল ফেসবুক পেজে প্রকল্পের সাম্প্রতিক মাটি ভরাট, লেক খনন ও কটেজ নির্মাণের লাইভ ভিডিও আপডেট প্রকাশিত হয়।", "Visit our official Facebook page for ongoing construction updates, 4K drone footage, and community visitor albums.", "p")}'
        f'{link("https://www.facebook.com/share/1EGtoqgu51/", "অফিসিয়াল ফেসবুক পেজে যান", "Visit Official Facebook")}'
        f'</article><article class="info-panel"><span class="eyebrow">SITE VISITATION</span>'
        f'{t("বাস্তব প্রকল্প এলাকা সরাসরি পরিদর্শন করুন", "Experience the Project Location in Person", "h3")}'
        f'{t("ছবির চেয়েও বাস্তব অনুভূতি অনেক সুন্দর। ঢাকা থেকে পরিবারসহ সরাসরি সাইট পরিদর্শনে অংশ নিন।", "Reality is even more captivating than pictures. Join our complimentary weekend shuttle tours from Dhaka.", "p")}'
        f'{link("booking.html?interest=site_visit", "সাইট ভিজিট বুক করুন", "Schedule a site visit")}'
        f'</article></div>',
        'SEE IN PERSON')
)
add('gallery', 'ছবিতে তাকওয়া ভিলেজের স্বপ্ন ও বাস্তবতা।', 'A Glimpse of the Taqwa Village Vision.',
    'তাকওয়া ভিলেজের মাস্টারপ্ল্যান, ফ্লোটিং কটেজ, ইকো রিসোর্ট, কেন্দ্রীয় মসজিদ ও প্রাকৃতিক জলাশয়ের স্থিরচিত্র গ্যালারি।',
    'Photographic showcase of Taqwa Village: masterplan layout, floating water cottages, eco resort, grand mosque and verdant lakes.',
    gallery_body, 'resort')

# ==========================================
# 8. INVESTMENT (বিনিয়োগ ও শেয়ারহোল্ডার তথ্য)
# ==========================================
investment_body = (
    section('শরিয়াহসম্মত সুদমুক্ত বিনিয়োগ ও নিশ্চিত হালাল মুনাফা', 'Shariah-Compliant Investment & Halal Returns',
        f'<div class="story-layout"><div>'
        f'{t("তাকওয়া ভিলেজ লিমিটেড (Taqwa Village Ltd.) একটি দূরদর্শী রিয়েল এস্টেট ও হসপিটালিটি মেগা প্রকল্প। এখানে প্রতিটি বিনিয়োগ সম্পূর্ণ ইসলামী শরিয়াহর ‘মুদারাবা’ ও ‘মুশারাকা’ নীতি অনুযায়ী পরিচালিত হয়—যেখানে কোনো সুদের (রিবা) সংমিশ্রণ নেই।", "Taqwa Village Ltd. represents a visionary real estate and hospitality sanctuary. Every investment opportunity strictly follows authentic Islamic Mudarabah and Musharakah profit-sharing agreements—100% free from usury (Riba).", "p")}'
        f'{t("বিনিয়োগকারীগণ রিসোর্ট ও কটেজের নিট পরিচালন আয়ের অংশীদার হবেন। এর মাধ্যমে প্রতি বছর বাৎসরিক ১৩% থেকে ১৬% হারে নিশ্চিত হালাল মুনাফা উপার্জনের পাশাপাশি মূল সম্পত্তির দ্রুত ক্যাপিটাল গ্রোথ নিশ্চিত হয়।", "Investors share in the net operational revenues of the resort and cottages, generating 13% to 16% in annual halal dividend payouts while enjoying substantial long-term capital appreciation.", "p")}'
        f'{link("booking.html?interest=resort_investment", "বিনিয়োগ আবেদন ও পরামর্শ", "Consult Investment Team", "primary-button")}'
        f'</div><blockquote>{t("“সুদমুক্ত উপার্জনের আত্মিক প্রশান্তি এবং পরিবারের জন্য আজীবন হালাল সম্পদের নিশ্চয়তা।”", "“The spiritual serenity of usury-free earnings, building generational halal wealth for your family.”")}</blockquote></div>',
        'HALAL WEALTH BUILDING') +
    section('বিনিয়োগ ও শেয়ারহোল্ডার প্যাকেজসমূহ', 'Investment Packages & Tiers',
        '<div class="packages-grid">' +
        '<div class="package-card">' +
        '<h3>১টি রিসোর্ট শেয়ার</h3><div class="package-price">৳ ২,৫০,০০০ <small>/ শেয়ার</small></div>' +
        '<ul class="package-features">' +
        '<li><i data-lucide="check"></i> <strong>১৩% - ১৬% বাৎসরিক হালাল ডিভিডেন্ড</strong></li>' +
        '<li><i data-lucide="check"></i> ৭ রাত প্রতি বছর সম্পূর্ণ ফ্রি রিসোর্ট স্টে</li>' +
        '<li><i data-lucide="check"></i> খাদ্য ও সেবায় ২৫% ভিআইপি ছাড়</li>' +
        '<li><i data-lucide="check"></i> নিবন্ধিত শেয়ার সার্টিফিকেট ও হস্তান্তরযোগ্য</li>' +
        '</ul><button onclick="openBookingModal(\'resort_investment\')" class="primary-button text-xs py-2.5">আবেদন করুন ↗</button></div>' +
        '<div class="package-card highlight">' +
        '<span class="package-card-ribbon">জনপ্রিয় প্যাকেজ</span>' +
        '<h3>২টি রিসোর্ট শেয়ার</h3><div class="package-price">৳ ৫,০০,০০০ <small>/ ২ শেয়ার</small></div>' +
        '<ul class="package-features">' +
        '<li><i data-lucide="check"></i> <strong>১৩% - ১৬% বাৎসরিক হালাল লভ্যাংশ</strong></li>' +
        '<li><i data-lucide="check"></i> ১৫ রাত প্রতি বছর ফ্রি রিসোর্ট থাকার সুবিধা</li>' +
        '<li><i data-lucide="check"></i> ভিআইপি মেম্বারশিপ কার্ড ও লাউঞ্জ এক্সেস</li>' +
        '<li><i data-lucide="check"></i> ব্যাংকিং চ্যানেলে সরাসরি ডিভিডেন্ড প্রাপ্তি</li>' +
        '</ul><button onclick="openBookingModal(\'resort_investment\')" class="primary-button text-xs py-2.5 bg-amber-600 hover:bg-amber-700 text-white">আবেদন করুন ↗</button></div>' +
        '<div class="package-card">' +
        '<h3>৪টি এক্সিকিউটিভ শেয়ার</h3><div class="package-price">৳ ১০,০০,০০০ <small>/ ৪ শেয়ার</small></div>' +
        '<ul class="package-features">' +
        '<li><i data-lucide="check"></i> <strong>১৩.৫% - ১৬.৫% প্রিমিয়াম ডিভিডেন্ড</strong></li>' +
        '<li><i data-lucide="check"></i> ৩০ রাত প্রতি বছর ফ্রি রিসোর্ট ও কটেজ স্টে</li>' +
        '<li><i data-lucide="check"></i> এজিএম-এ ভোটাধিকার ও পলিসি অংশগ্রহণ</li>' +
        '<li><i data-lucide="check"></i> এক্সিকিউটিভ ক্লাব মেম্বারশিপ ও কনভেনশন ছাড়</li>' +
        '</ul><button onclick="openBookingModal(\'resort_investment\')" class="primary-button text-xs py-2.5">আবেদন করুন ↗</button></div>' +
        '<div class="package-card">' +
        '<h3>ফুল ফ্লোটিং কটেজ</h3><div class="package-price">৳ ৫৫,০০,০০০ <small>/ সম্পূর্ণ কটেজ</small></div>' +
        '<ul class="package-features">' +
        '<li><i data-lucide="check"></i> <strong>১০০% সাফ-কবলা সরকারি দলিল ও নামজারি</strong></li>' +
        '<li><i data-lucide="check"></i> বাৎসরিক ৳ ৭-৯ লাখ ভাড়া আয়ের সুযোগ</li>' +
        '<li><i data-lucide="check"></i> আজীবন পরিবারের আনলিমিটেড অবকাশ</li>' +
        '<li><i data-lucide="check"></i> সম্পূর্ণ ফার্নিশড ও অটো-মেইনটেন্যান্স</li>' +
        '</ul><button onclick="openBookingModal(\'cottage\')" class="primary-button text-xs py-2.5">মালিকানা ইনকোয়ারি ↗</button></div>' +
        '</div>',
        'INVESTMENT TIERS') +
    section('আইনি সুরক্ষা ও শরিয়াহ সার্টিফিকেশন', 'Legal Security & Shariah Governance',
        '<div class="feature-grid">' +
        feature('file-text', '১০০% সাফ-কবলা দলিল', 'Registered Sub-Kabla Deeds', 'জমির নিরঙ্কুশ মালিকানা নিশ্চিত করে সরকারি সাব-রেজিস্ট্রি অফিস থেকে সাফ-কবলা দলিল ও নামজারি খতিয়ান প্রদান।', 'Permanent sub-kabla title deeds and official mutation records guarantee unencumbered land ownership.') +
        feature('shield-check', 'শরিয়াহ উপদেষ্টা বোর্ড', 'Independent Shariah Board', 'মুদারাবা নীতিমালার সঠিক প্রয়োগ ও হিসাব নিরীক্ষায় দেশের প্রথিতযশা ইসলামিক ফিন্যান্স স্কলারদের সার্বক্ষণিক নজরদারি।', 'Reputable Islamic finance scholars continuously audit operational contracts to preserve complete Riba-free integrity.') +
        feature('building-2', 'ব্যাংকিং চ্যানেলে স্বচ্ছতা', 'Transparent Banking Audits', 'সকল বিনিয়োগ গ্রহণ ও লভ্যাংশ বিতরণ সরাসরি তফসিলি ব্যাংকিং চ্যানেলের মাধ্যমে এবং বাৎসরিক অডিট রিপোর্ট প্রকাশ।', 'All capital inflows and dividend distributions flow transparently through scheduled banks with chartered audits.') +
        feature('refresh-cw', 'স্থানান্তর ও হস্তান্তরযোগ্য', 'Transferable & Inheritable', 'শেয়ার ও মালিকানা সম্পূর্ণ উত্তরাধিকারযোগ্য এবং যেকোনো সময় কোম্পানির সম্মতি সাপেক্ষে হস্তান্তর করা যায়।', 'All shares and titles are fully inheritable by heirs and can be transferred or sold with company concurrence.') +
        '</div>',
        'LEGAL ASSURANCE') +
    section('বিনিয়োগ প্রক্রিয়ার ৪টি সহজ ধাপ', 'The 4-Step Investment Process',
        f'<div class="timeline-wrap">'
        f'<div class="timeline-step"><span class="timeline-step-badge">ধাপ ১</span><h4>তথ্য ও পরামর্শ</h4><p>আমাদের বনানী অফিসে আসুন বা সাইট ভিজিটে অংশ নিয়ে সরাসরি কর্মকর্তাদের সাথে আলোচনা করুন।</p></div>'
        f'<div class="timeline-step"><span class="timeline-step-badge">ধাপ ২</span><h4>প্যাকেজ নির্বাচন</h4><p>আপনার বাজেট অনুযায়ী ১টি বা ততোধিক শেয়ার অথবা সম্পূর্ণ কটেজ নির্বাচন করুন।</p></div>'
        f'<div class="timeline-step active"><span class="timeline-step-badge">ধাপ ৩</span><h4>আবেদন ও পেমেন্ট</h4><p>কেওয়াইসি ফরম পূরণ করে কোম্পানির অফিশিয়াল ব্যাংক একাউন্টে চেক বা পে-অর্ডারে অর্থ জমা দিন।</p></div>'
        f'<div class="timeline-step"><span class="timeline-step-badge">ধাপ ৪</span><h4>দলিল ও সার্টিফিকেট</h4><p>আইনি চুক্তি স্বাক্ষরপূর্বক মূল শেয়ার সার্টিফিকেট ও মালিকানা দলিল সংগ্রহ করুন।</p></div>'
        f'</div>',
        'HOW IT WORKS') +
    section('সাধারণ বিনিয়োগ জিজ্ঞাসা', 'Investment FAQs',
        faq([
            ('লভ্যাংশ কবে এবং কীভাবে বণ্টন করা হয়?', 'When and how are dividends distributed?', 'প্রতি অর্থবছরের হিসাব ক্লোজিং ও অডিটের পর বার্ষিক সাধারণ সভায় (AGM) ঘোষিত লভ্যাংশ সরাসরি শেয়ারহোল্ডারের ব্যাংক একাউন্টে ট্রান্সফার করা হয়।', 'Following annual financial audit and AGM declaration, dividends are deposited directly into shareholders’ designated bank accounts.'),
            ('প্রবাসীরা (NRB) কি বিদেশ থেকে বিনিয়োগ করতে পারবেন?', 'Can Non-Resident Bangladeshis (NRBs) invest from abroad?', 'জি হ্যাঁ! বিশ্বের যেকোনো দেশ থেকে প্রবাসী বাংলাদেশিরা বৈধ রেমিট্যান্স চ্যানেলে সরাসরি বিনিয়োগ করতে পারেন এবং প্রয়োজনীয় দলিলপত্র কুরিয়ার বা প্রতিনিধির মাধ্যমে সম্পন্ন করা যায়।', 'Yes! NRBs can invest seamlessly via official remittance banking channels from anywhere in the world, with documents processed securely.'),
            ('বিনিয়োগ কি প্রত্যাহার বা বিক্রি করা যায়?', 'Can shares be redeemed or sold?', 'জি হ্যাঁ, নির্দিষ্ট লক-ইন সময়সীমার পর আপনি আপনার শেয়ার অন্য কারও কাছে হস্তান্তর করতে পারেন অথবা কোম্পানির নিজস্ব ক্রয় নীতি অনুযায়ী ফিরিয়ে দিতে পারেন।', 'Yes, following the standard lock-in period, shares may be transferred, sold to third parties, or repurchased under company guidelines.')
        ]),
        'INVESTMENT FAQ')
)
add('investment', 'শরিয়াহসম্মত লাভজনক বিনিয়োগ ও স্থায়ী সম্পদ।', 'Shariah-Compliant Investment & Generational Wealth.',
    'তাকওয়া ভিলেজ কটেজ ও ৫-স্টার রিসোর্ট ফ্র্যাকশনাল শেয়ারের মাধ্যমে বাৎসরিক ১৩-১৬% হালাল আয় ও ফ্রি স্টে সুবিধা।',
    'Earn 13-16% annual halal dividends, capital growth and complimentary resort stay nights through Taqwa Village shares.',
    investment_body, 'resort', 'projects')

# ==========================================
# 9. BOOKING & SITE VISIT (সাইট ভিজিট আবেদন)
# ==========================================
form_markup = (
    '<form id="inquiryForm" class="inquiry-form">' +
    '<div class="form-heading"><span class="eyebrow">YOUR VISIT, YOUR WAY</span>' +
    t('সাইট ভিজিট ও বুকিং ফর্ম', 'Site Visit & Booking Inquiry Form', 'h2') +
    t('আপনার পছন্দের অপশন বেছে নিন। আমাদের সিনিয়র প্রতিনিধি দ্রুত আপনার সাথে যোগাযোগ করবেন।', 'Select your preferred interest below. Our representative will follow up immediately.', 'p') +
    '</div>' +
    f'<label for="inquiryInterest">{t("আগ্রহের ধরন নির্বাচন করুন *", "Select Your Primary Interest *")}</label>' +
    '<select id="inquiryInterest" name="interest">' +
    '<option value="site_visit" data-bn="সাইট ভিজিট (পূর্বাচল উলুখোলা প্রজেক্ট)" data-en="Site Visit (Purbachal Project)">সাইট ভিজিট (পূর্বাচল উলুখোলা প্রজেক্ট)</option>' +
    '<option value="cottage" data-bn="ফ্লোটিং ডুপ্লেক্স কটেজ বুকিং / মালিকানা" data-en="Floating Duplex Cottage Booking / Ownership">ফ্লোটিং ডুপ্লেক্স কটেজ বুকিং / মালিকানা</option>' +
    '<option value="resort_investment" data-bn="রিসোর্ট ফ্র্যাকশনাল শেয়ারহোল্ডার (ইনভেস্টমেন্ট)" data-en="Resort Fractional Shareholder (Investment)">রিসোর্ট ফ্র্যাকশনাল শেয়ারহোল্ডার (ইনভেস্টমেন্ট)</option>' +
    '<option value="family_dayout" data-bn="পারিবারিক ডে-আউট ও পিকনিক স্পট" data-en="Family Day-Out & Picnic Spot">পারিবারিক ডে-আউট ও পিকনিক স্পট</option>' +
    '</select>' +
    '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">' +
    '<div class="form-field"><label for="inquiryName">' + t('আপনার পূর্ণ নাম *', 'Full Name *') + '</label><input id="inquiryName" name="name" type="text" required autocomplete="name" placeholder="মোহাম্মদ রফিকুল ইসলাম"></div>' +
    '<div class="form-field"><label for="inquiryPhone">' + t('মোবাইল নম্বর *', 'Mobile Number *') + '</label><input id="inquiryPhone" name="phone" type="tel" required autocomplete="tel" placeholder="01XXXXXXXXX"></div>' +
    '</div>' +
    '<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">' +
    '<div class="form-field"><label for="inquiryEmail">' + t('ইমেইল ঠিকানা (ঐচ্ছিক)', 'Email Address (Optional)') + '</label><input id="inquiryEmail" name="email" type="email" autocomplete="email" placeholder="name@example.com"></div>' +
    '<div class="form-field"><label for="inquiryDate">' + t('সম্ভাব্য ভিজিটের তারিখ', 'Preferred Visit Date') + '</label><input id="inquiryDate" name="date" type="date"></div>' +
    '</div>' +
    '<div class="form-field full-width"><label for="inquiryMessage">' + t('কোনো নির্দিষ্ট চাহিদা বা প্রশ্ন (ঐচ্ছিক)', 'Questions or Specific Requirements (Optional)') + '</label><textarea id="inquiryMessage" name="message" rows="3" placeholder="সদস্য সংখ্যা, বিশেষ চাহিদা বা প্রশ্ন লিখুন..."></textarea></div>' +
    f'<div class="bg-emerald-50 p-3 rounded-lg border border-emerald-200 text-xs text-emerald-950 mb-3">' +
    f'<i data-lucide="bus" class="w-4 h-4 inline mr-1 text-emerald-700"></i> ' +
    t("প্রতি শুক্র ও শনিবার বনানী ও কুড়িল থেকে বিনামূল্যে এসি শাটল বাস সার্ভিস রয়েছে।", "Complimentary AC shuttle bus service operates every Friday & Saturday from Banani & Kuril.") +
    f'</div>' +
    '<button class="primary-button full-width" type="submit">' + t('আবেদন জমা দিন (হোয়াটসঅ্যাপে নিশ্চিতকরণ)', 'Submit Inquiry (WhatsApp Confirmation)') + ' ↗</button>' +
    '<div id="inquiryResult" class="full-width" role="status" aria-live="polite" hidden></div>' +
    '</form>'
)

booking_body = (
    f'<div class="booking-layout">{form_markup}<aside class="booking-aside"><span class="eyebrow">WHAT HAPPENS NEXT</span>'
    f'{t("পরবর্তী ৩টি সহজ পদক্ষেপ", "Three Simple Next Steps", "h2")}'
    f'<ol class="steps">'
    f'<li>{t("ফর্মটি পূরণ করে সাবমিট করুন।", "Complete the form with your preferences.")}</li>'
    f'<li>{t("স্বয়ংক্রিয়ভাবে প্রস্তুত হওয়া হোয়াটসঅ্যাপ মেসেজটি পাঠান।", "Send the pre-filled WhatsApp message to our hotline.")}</li>'
    f'<li>{t("আমাদের প্রতিনিধি সময় ও ফ্রি শাটল সিট নিশ্চিত করবেন।", "Our team confirms timing and complimentary shuttle seats.")}</li>'
    f'</ol>'
    f'<div class="info-panel">{t("সরাসরি কথা বলতে চান?", "Prefer to Speak Directly?", "h3")}'
    f'<p>{t("হটলাইন নম্বরে সরাসরি কল করে কথা বলুন:", "Call our senior representatives directly:")}</p>'
    f'<a href="tel:+8801335145110" class="text-lg font-bold text-emerald-900 block my-1">+880 1335 145110</a>'
    f'{link("contact.html", "অফিসের ঠিকানা ও গুগল ম্যাপ", "Corporate address & maps")}'
    f'</div>'
    f'{link("privacy.html", "আপনার তথ্য ব্যবহারের নীতিমালা", "Read our privacy commitment")}'
    f'</aside></div>' +
    section('ফ্রি শাটল বাস শিডিউল', 'Free Weekend Shuttle Bus Schedule',
        f'<div class="shuttle-card"><div class="w-12 h-12 rounded-xl bg-emerald-800 text-amber-300 flex items-center justify-center shrink-0"><i data-lucide="bus" class="w-6 h-6"></i></div>'
        f'<div><h4>{t("ঢাকা থেকে পূর্বাচল প্রকল্প সাইট শাটল ট্রিপ", "Dhaka to Purbachal Site Weekend Shuttle")}</h4>'
        f'<p>{t("প্রতি শুক্র ও শনিবার সকাল ৯:৩০ টায় বনানী অফিস এবং সকাল ১০:১৫ টায় কুড়িল বিশ্বরোড থেকে গাড়ি ছাড়ে। দুপুরের মধ্যাহ্নভোজ শেষে বিকেলে পুনরায় ঢাকায় পৌঁছে দেওয়া হয়।", "Departs Banani office at 9:30 AM and Kuril Flyover at 10:15 AM every Friday & Saturday. Returning to Dhaka in the afternoon after lunch.", "p")}</p>'
        f'</div><a href="tel:+8801335145110" class="primary-button text-xs py-2 px-4 whitespace-nowrap">{t("সিট কনফার্ম করুন", "Confirm Seats")} ↗</a></div>',
        'SHUTTLE SERVICE')
)
add('booking', 'চলুন, আপনার পরিবারসহ ভিজিটের পরিকল্পনা করি।', 'Plan Your Family Site Visit.',
    'আপনার পছন্দ ও তারিখ জানান। আমাদের প্রতিনিধির সঙ্গে সময়, সাইট ভিজিট ও পরবর্তী পদক্ষেপ নিশ্চিত করুন।',
    'Share your interest and schedule. Confirm dates, complimentary weekend shuttle seats and project briefings with our team.',
    booking_body)

# ==========================================
# 10. CONTACT (যোগাযোগ ও অবস্থান)
# ==========================================
contact_body = (
    '<div class="contact-grid">' +
    '<article class="feature-panel"><i data-lucide="phone"></i>' + t('সরাসরি কল করুন', 'Call Us Directly', 'h2') + '<a href="tel:+8801335145110" class="text-base font-bold text-emerald-900 block mt-1">+880 1335 145110</a><span class="text-xs text-slate-500 block mt-1">শনি - বৃহস্পতি (১০টা - ৬টা)</span></article>' +
    '<article class="feature-panel"><i data-lucide="mail"></i>' + t('ইমেইল পাঠান', 'Email Support', 'h2') + '<a href="mailto:info@taqwavillage.com" class="text-base font-bold text-emerald-900 block mt-1">info@taqwavillage.com</a><span class="text-xs text-slate-500 block mt-1">২৪ ঘণ্টার মধ্যে উত্তর প্রদান</span></article>' +
    '<article class="feature-panel"><i data-lucide="message-circle"></i>' + t('হোয়াটসঅ্যাপ চ্যাট', 'WhatsApp Chat', 'h2') + '<a href="https://wa.me/8801335145110" target="_blank" class="text-base font-bold text-emerald-900 block mt-1">+880 1335 145110</a>' + link('https://wa.me/8801335145110', 'মেসেজ দিন', 'Message now') + '</article>' +
    '</div>' +
    section('অফিস ও প্রকল্প সাইটের অবস্থান', 'Headquarters & Project Locations',
        f'<div class="detail-split">'
        f'<article class="info-panel"><span class="eyebrow">HEADQUARTERS</span>'
        f'{t("প্রধান করপোরেট অফিস", "Corporate Headquarters", "h3")}'
        f'{t("হাউস #২৬, রোড #৩, বনানী, ঢাকা - ১২১৩, বাংলাদেশ।", "House #26, Road #3, Banani, Dhaka - 1213, Bangladesh.", "p")}'
        f'{t("সাক্ষাতের সময়: শনিবার থেকে বৃহস্পতিবার (সকাল ১০:০০ টা থেকে সন্ধ্যা ৬:০০ টা)। শুক্রবার পূর্বনির্ধারিত সাক্ষাতে খোলা থাকে।", "Visiting Hours: Saturday to Thursday (10:00 AM to 6:00 PM). Fridays open by prior appointment.", "p")}'
        f'{link("https://www.google.com/maps/search/?api=1&query=House+26+Road+3+Banani+Dhaka", "গুগল ম্যাপে বনানী অফিস খুঁজুন", "Locate Banani office on Google Maps")}'
        f'</article>'
        f'<article class="info-panel"><span class="eyebrow">PROJECT LOCATION</span>'
        f'{t("প্রকল্প সাইটের ঠিকানা", "Purbachal Project Site", "h3")}'
        f'{t("রাথুরা, উলুখোলা, পূর্বাচল সেক্টর ৩০ সংলগ্ন, ঢাকা বাইপাস রোড, ঢাকা।", "Rathura, Ulukhola, adjacent to Purbachal Sector 30, Dhaka Bypass, Dhaka.", "p")}'
        f'{t("কুড়িল বিশ্বরোড থেকে ৩০০ ফুট রাস্তা ধরে মাত্র ২০ মিনিটের ড্রাইভ। কাঞ্চন ব্রিজ বা উলুখোলা বাজার হয়ে সহজে প্রবেশযোগ্য।", "Just 20 minutes from Kuril Flyover via the 300ft highway. Easily reachable through Kanchan Bridge or Ulukhola road.", "p")}'
        f'{link("booking.html?interest=site_visit", "সাইট পরিদর্শনের আবেদন", "Request site visit")}'
        f'</article>'
        f'</div>',
        'LOCATIONS & DIRECTIONS') +
    section('সামাজিক যোগাযোগ মাধ্যম', 'Connect on Social Media',
        f'<div class="feature-grid">'
        f'{feature("facebook", "ফেসবুক অফিসিয়াল পেজ", "Official Facebook", "নিয়মিত লাইভ আপডেট, ড্রোন ভিডিও ও প্রকল্পের উন্নয়ন চিত্র দেখুন।", "Follow our verified page for daily construction reels, aerial drone tours and community announcements.")}'
        f'{feature("youtube", "ইউটিউব চ্যানেল", "YouTube Channel", "প্রকল্প পরিচিতি, বিশেষজ্ঞ বক্তব্য ও কটেজ ওয়াকথ্রু ভিডিও।", "Subscribe for in-depth architectural walkthroughs, scholar perspectives and event highlights.")}'
        f'{feature("instagram", "ইনস্টাগ্রাম প্রোফাইল", "Instagram Profile", "প্রকৃতি, লেক ভিউ ও পরিবারের সুন্দর মুহূর্তের ফটো অ্যালবাম।", "Visual moments of nature, peaceful water villas and family living.")}'
        f'</div>',
        'OFFICIAL CHANNELS')
)
add('contact', 'আপনার একটি প্রশ্ন দিয়েই শুরু হোক সুন্দর পরিকল্পনা।', 'Every Great Vision Begins with a Conversation.',
    'তাকওয়া ভিলেজ প্রকল্প, সাইট পরিদর্শন বা বিনিয়োগ সম্পর্কে যেকোনো জিজ্ঞাসা নিয়ে আমাদের সাথে যোগাযোগ করুন।',
    'Get in touch about the masterplan, weekend site visit bookings, or Shariah investment opportunities with our team.',
    contact_body)

# ==========================================
# 11. PRIVACY POLICY (প্রাইভেসি পলিসি)
# ==========================================
privacy_body = (
    '<div class="reading-layout">' +
    section('তথ্যের গোপনীয়তা ও নিরাপত্তা অঙ্গীকার', 'Privacy Commitment',
        t('তাকওয়া ভিলেজ লিমিটেড (Taqwa Village Ltd.) আপনার ব্যক্তিগত তথ্যের সর্বোচ্চ গোপনীয়তা ও সুরক্ষায় প্রতিশ্রুতিবদ্ধ। এই ওয়েবসাইটের মাধ্যমে সংগৃহীত তথ্য কীভাবে ব্যবহৃত ও সংরক্ষিত হয় তা এখানে স্বচ্ছতার সাথে তুলে ধরা হলো।',
          'Taqwa Village Ltd. is committed to upholding your privacy and protecting your personal information. This policy transparently explains how your data is collected, processed, and safeguarded.', 'p')) +
    section('কী ধরনের তথ্য সংগৃহীত হয়', 'Information We Collect',
        t('যখন আপনি আমাদের ওয়েবসাইটের বুকিং ফর্ম, সাইট ভিজিট আবেদন বা যোগাযোগ ফর্ম ব্যবহার করেন, তখন আমরা আপনার নাম, মোবাইল নম্বর, ইমেইল ঠিকানা, পছন্দের পরিদর্শনের তারিখ এবং বিশেষ মন্তব্য গ্রহণ করি। এই ওয়েবসাইট কোনো অনলাইন আর্থিক পেমেন্ট বা সংবেদনশীল কার্ড তথ্য সংগ্রহ করে না।',
          'When you interact with our reservation, inquiry, or contact forms, we collect your name, phone number, email address, preferred appointment date, and personal requirements. We never collect or process credit card details on this website.', 'p')) +
    section('তথ্যের ব্যবহার ও উদ্দেশ্য', 'How Information is Utilized',
        t('সংগৃহীত তথ্যাবলি শুধুমাত্র আপনার সাথে যোগাযোগ স্থাপন, সাইট ভিজিটের সময়সূচি সমন্বয়, প্রকল্পের অগ্রগতি সম্পর্কিত আপডেট প্রদান এবং শেয়ারহোল্ডার সংক্রান্ত প্রাসঙ্গিক তথ্য পাঠানোর উদ্দেশ্যে ব্যবহৃত হয়। আমরা কখনোই কোনো তৃতীয় পক্ষের কাছে আপনার তথ্য বিক্রি বা বিনিময় করি না।',
          'Collected data is utilized strictly to communicate with you, coordinate site visits, deliver project briefings, and respond to shareholder inquiries. We never sell, lease, or monetize your details to third-party marketers.', 'p')) +
    section('হোয়াটসঅ্যাপ ও বহিরাগত সংযোগ', 'WhatsApp & External Services',
        t('ফর্ম সাবমিটের মাধ্যমে তৈরি হওয়া তথ্যগুলো আপনার অনুমতিক্রমে আপনার ব্রাউজার থেকে সরাসরি হোয়াটসঅ্যাপে প্রি-ফিল্ড মেসেজ আকারে প্রস্তুত হয়। তথ্যটি পাঠানোর চূড়ান্ত নিয়ন্ত্রণ সম্পূর্ণ আপনার হাতে থাকে। গুগল ম্যাপস বা ফেসবুকের মতো বহিরাগত সেবা তাদের নিজস্ব নীতিমালায় পরিচালিত হয়।',
          'Form submissions prepare a formatted WhatsApp message in your local browser for your confirmation before sending. Third-party integrations such as Google Maps and Facebook operate under their respective independent terms.', 'p')) +
    section('যোগাযোগ ও তথ্য সংশোধন', 'Contact for Privacy Matters',
        t('আপনার তথ্যের কোনো পরিবর্তন বা প্রত্যাহারের প্রয়োজন হলে আমাদের কমপ্লায়েন্স বিভাগে info@taqwavillage.com অথবা +880 1335 145110 নম্বরে যোগাযোগ করতে পারেন।',
          'To request modification, correction, or deletion of your records, reach out to our team at info@taqwavillage.com or +880 1335 145110.', 'p') +
        link('contact.html', 'যোগাযোগ পেজে যান', 'Go to contact page')) +
    '</div>'
)
add('privacy', 'আপনার তথ্যের পূর্ণ গোপনীয়তা ও নিরাপত্তা।', 'Your Information, Protected and Respected.',
    'তাকওয়া ভিলেজ ওয়েবসাইটের তথ্য সংরক্ষণ, গোপনীয়তা ও ব্যবহার সংক্রান্ত স্পষ্ট এবং স্বচ্ছ নীতিমালা।',
    'Clear, transparent policies regarding data protection, inquiries, and customer confidentiality at Taqwa Village.',
    privacy_body)

# ==========================================
# 12. TERMS OF USE (ব্যবহারের শর্তাবলী)
# ==========================================
terms_body = (
    '<div class="reading-layout">' +
    section('ওয়েবসাইট ব্যবহারের সাধারণ শর্তাবলী', 'Terms of Website Use',
        t('তাকওয়া ভিলেজ লিমিটেডের ওয়েবসাইট ব্যবহারের মাধ্যমে আপনি নিম্নলিখিত শর্তাবলী মেনে নিতে সম্মতি প্রদান করছেন। এই শর্তাবলী বাংলাদেশ সরকারের প্রচলিত রিয়েল এস্টেট আইন ও আইটি নীতিমালা অনুসারে পরিচালিত।',
          'By accessing the Taqwa Village Ltd. website, you agree to comply with the terms set forth herein, governed by the real estate and information technology laws of Bangladesh.', 'p')) +
    section('তথ্য ও উপস্থাপনার প্রকৃতি', 'Informational Nature of Content',
        t('এই ওয়েবসাইটের সমস্ত বিবরণ, নকশা, থ্রিডি রেন্ডার এবং অনুপ্রেরণামূলক ছবি প্রকল্প পরিচিতি ও প্রাথমিক তথ্য প্রদানের উদ্দেশ্যে প্রকাশিত। চূড়ান্ত নির্মাণ, সুযোগ-সুবিধা ও ইউনিট হস্তান্তরের ক্ষেত্রে মূল বিক্রয় চুক্তি ও সরকারি রেজিস্ট্রি দলিলে বর্ণিত শর্তাবলীই চূড়ান্ত হিসেবে গণ্য হবে।',
          'All renderings, masterplans, visual inspirations, and specifications presented are for conceptual and informational purposes. Binding commitments are governed exclusively by executed bilateral contracts and registered deeds.', 'p')) +
    section('বুকিং ও চুক্তি সংক্রান্ত বিধান', 'Booking & Agreement Rules',
        t('ওয়েবসাইটের কোনো ফর্ম পূরণ বা হোয়াটসঅ্যাপে বার্তা প্রেরণ স্বয়ংক্রিয়ভাবে কটেজ ক্রয় বা শেয়ারের চূড়ান্ত মালিকানা নিশ্চিত করে না। প্রাতিষ্ঠানিক ব্যাংকিং চ্যানেলে পেমেন্ট ক্লিয়ারেন্স এবং আনুষ্ঠানিক চুক্তি স্বাক্ষর ব্যতীত কোনো স্বত্ব প্রতিষ্ঠিত হবে না।',
          'Submitting an inquiry or sending a WhatsApp message does not constitute a confirmed deed or legal title. Absolute rights are established only upon formal contract execution and banking clearance.', 'p')) +
    section('মেধাসম্পদ ও স্বত্বাধিকার', 'Intellectual Property Rights',
        t('তাকওয়া ভিলেজের ব্র্যান্ড লোগো, টেক্সট, ডিজাইন, স্থাপত্য নকশা এবং ভিডিও সামগ্রী তাকওয়া ভিলেজ লিমিটেডের নিজস্ব মেধাসম্পদ। অনুমতি ছাড়া বাণিজ্যিক পুনরুৎপাদন কঠোরভাবে নিষিদ্ধ।',
          'All trademarks, logos, architectural layouts, copy, and visual media are the intellectual property of Taqwa Village Ltd. Unauthorized commercial reproduction is strictly prohibited.', 'p')) +
    section('আইনগত এখতিয়ার', 'Governing Jurisdiction',
        t('এই শর্তাবলী এবং এর সাথে সংশ্লিষ্ট যেকোনো বিরোধ বাংলাদেশের সুপ্রিম কোর্ট ও বিজ্ঞ আদালতের বিচারিক এখতিয়ারের অধীনে নিষ্পত্তিযোগ্য হবে।',
          'These terms and any related matters are subject to the exclusive jurisdiction of the judicial courts of Bangladesh.', 'p') +
        link('investment.html', 'বিনিয়োগ শর্তাবলী দেখুন', 'Review investment guidelines')) +
    '</div>'
)
add('terms', 'ওয়েবসাইট ব্যবহারের স্পষ্ট ও সুনির্দিষ্ট শর্তাবলী।', 'Clear and Standard Terms of Website Use.',
    'তাকওয়া ভিলেজ লিমিটেডের ওয়েবসাইট ব্যবহার, তথ্য অনুসন্ধান এবং আইনি বিধানের পূর্ণ বিবরণ।',
    'Complete terms and legal disclosures governing website usage, property inquiries, and service standards.',
    terms_body)

# ==========================================
# BUILD ALL PAGES
# ==========================================
for slug, (bn, en, desc, descen, body, photo, parent) in pages.items():
    pagehead = re.sub(r'<title>.*?</title>', f'<title>{escape(en)} | Taqwa Village</title>', head)
    pagehead = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m[1] + escape(descen, quote=True), pagehead)
    pagehead = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m[1] + escape(en + ' | Taqwa Village', quote=True), pagehead)
    pagehead = pagehead.replace('content="https://taqwavillage.com"', f'content="https://taqwavillage.com/{slug}.html"')
    
    nav = chrome.replace('<body class="', '<body class="inner-page ')
    active = 'projects' if parent == 'projects' else slug
    nav = re.sub(r'<nav\b.*?</nav>', lambda match: match[0].replace(f'href="{active}.html"', f'href="{active}.html" aria-current="page"'), nav, flags=re.S)
    if slug == 'booking':
        nav = nav.replace('class="sketch-book"', 'class="sketch-book" aria-current="page"')
        
    crumbs = link('index.html', 'হোম', 'Home', '')
    if parent:
        crumbs += ' <span aria-hidden="true">/</span> ' + link(parent + '.html', 'প্রকল্প', 'Projects', '')
    crumbs += f' <span aria-hidden="true">/</span> {t(bn, en)}'
    
    hero = f'<div class="page-hero-copy"><span class="eyebrow">TAQWA VILLAGE / {slug.upper()}</span>{t(bn, en, "h1")}{t(desc, descen, "p")}</div>'
    if photo:
        hero += f'<figure class="page-hero-image">{image(photo, eager=True)}<figcaption>{t("বাস্তব ও পরিকল্পিত স্থিরচিত্র", "Project Lifestyle Visual")}</figcaption></figure>'
        
    output = (
        pagehead +
        nav +
        f'<main class="page-shell" id="page-content">'
        f'<nav class="breadcrumbs" aria-label="Breadcrumb">{crumbs}</nav>'
        f'<section class="page-hero {"with-image" if photo else "text-hero"}">{hero}</section>' +
        body +
        (cta() if slug not in ['booking', 'privacy', 'terms'] else '') +
        address +
        '</main>' +
        footer +
        modals +
        '<script src="app.js"></script><script src="pages.js"></script></body></html>'
    )
    (ROOT / (slug + '.html')).write_text(output, encoding='utf-8')

print(f'Successfully updated all {len(pages)} inner pages with rich, comprehensive content and matching styling!')
