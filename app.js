/**
 * Taqwa Village Ltd. - Main Application Logic
 * Implements wireframe layout behaviors, Swiper slider, modals, language switching, and interactive elements.
 */

// Global State
let currentLanguage = 'bn';
let isMuted = true;
let swiperInstance = null;

// Translation dictionary for Bangla & English
const translations = {
  bn: {
    offer_badge: "OFFER",
    top_offer_text: "পূর্বাচল প্রজেক্টে সীমিত সময়ের প্রি-বুকিং অফার! রিসোর্ট শেয়ার ও কটেজে আকর্ষণীয় ক্যাশব্যাক সুবিধা।",
    offer_ends: "অফার শেষ হতে বাকি:",
    motto_tag: "নৈতিক লাইফস্টাইল ডেস্টিনেশন",
    slogan_heading: "\"চলুন একসাথে সুন্দর ভবিষ্যৎ গড়ি\"",
    slogan_sub: "বাংলাদেশের প্রথম নৈতিক ও পরিবারভিত্তিক ইকো ভিলেজ প্রজেক্ট",
    book_now_btn: "Book Now",
    site_visit: "সাইট ভিজিট",
    nav_home: "হোম",
    nav_about: "আমাদের সম্পর্কে",
    nav_project: "প্রকল্প",
    nav_facilities: "সুবিধা ও প্যাকেজ",
    nav_gallery: "গ্যালারি",
    nav_contact: "যোগাযোগ",
    follow_us: "কানেক্ট থাকুন:",
    visit_site_btn: "সাইট পরিদর্শনের আবেদন"
  },
  en: {
    offer_badge: "OFFER",
    top_offer_text: "Limited Time Pre-Booking Offer at Purbachal Project! Attractive cashback on Resort Shares & Luxury Cottages.",
    offer_ends: "Offer ends in:",
    motto_tag: "Ethical Lifestyle Destination",
    slogan_heading: "\"Let Us Build A Beautiful Future Together\"",
    slogan_sub: "Bangladesh's First Ethical & Family-Oriented Eco Village Project",
    book_now_btn: "Book Now",
    site_visit: "Site Visit",
    nav_home: "Home",
    nav_about: "About Us",
    nav_project: "Project",
    nav_facilities: "Amenities & Packages",
    nav_gallery: "Gallery",
    nav_contact: "Contact",
    follow_us: "Connect with us:",
    visit_site_btn: "Schedule Site Visit"
  }
};

// Initialize DOM elements when ready
document.addEventListener('DOMContentLoaded', () => {
  // Render Lucide icons
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Initialize Swiper
  initSwiper();

  // Setup mobile navigation
  setupMobileNav();

  // Setup countdown timer
  startCountdown();
});

// Swiper Initialization
function initSwiper() {
  if (typeof Swiper !== 'undefined' && document.querySelector('.mySwiper')) {
    swiperInstance = new Swiper('.mySwiper', {
      loop: true,
      autoplay: {
        delay: 4500,
        disableOnInteraction: false,
      },
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
      navigation: {
        nextEl: '#sliderNextBtn',
        prevEl: '#sliderPrevBtn',
      },
      effect: 'fade',
      fadeEffect: {
        crossFade: true
      },
      speed: 800,
    });
  }
}

// Mobile Menu Toggle
function setupMobileNav() {
  const menuBtn = document.getElementById('mobileMenuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
      menuBtn.setAttribute('aria-expanded', String(!mobileMenu.classList.contains('hidden')));
    });

    // Close when clicking links
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
        menuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }
}

// Language Switcher
function toggleLanguage() {
  currentLanguage = currentLanguage === 'bn' ? 'en' : 'bn';
  const label = document.getElementById('langLabel');
  if (label) {
    label.textContent = currentLanguage === 'bn' ? 'English' : 'বাংলা';
  }

  document.documentElement.lang = currentLanguage;

  // Update translatable elements
  const dict = translations[currentLanguage];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  showToast(currentLanguage === 'bn' ? 'বাংলা ভাষা নির্বাচন করা হয়েছে' : 'Language switched to English');
}

// Booking Modal Controls
function openBookingModal(interestType = 'site_visit') {
  const modal = document.getElementById('bookingModal');
  const interestSelect = document.getElementById('bookInterest');
  if (interestSelect) {
    if (interestType === 'cottage') interestSelect.value = 'cottage';
    else if (interestType === 'resort') interestSelect.value = 'resort_investment';
    else if (interestType === 'investment') interestSelect.value = 'resort_investment';
    else if (interestType === 'family_dayout') interestSelect.value = 'family_dayout';
    else interestSelect.value = 'site_visit';
  }
  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}

function closeBookingModal() {
  const modal = document.getElementById('bookingModal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
}

// Handle Booking Form Submission
function handleBookingSubmit(event) {
  event.preventDefault();

  const name = document.getElementById('userName').value.trim();
  const phone = document.getElementById('userPhone').value.trim();
  const email = document.getElementById('userEmail').value.trim();
  const interest = document.getElementById('bookInterest').value;
  const date = document.getElementById('userDate').value;
  const message = document.getElementById('userMessage').value.trim();

  // Create WhatsApp confirmation message
  const interestLabel = {
    site_visit: 'সাইট ভিজিট (পূর্বাচল প্রজেক্ট)',
    cottage: 'ফ্লোটিং ডুপ্লেক্স কটেজ বুকিং',
    resort_investment: 'রিসোর্ট শেয়ারহোল্ডার ও ইনভেস্টমেন্ট',
    family_dayout: 'পারিবারিক ডে-আউট'
  }[interest] || interest;

  const waText = encodeURIComponent(
    `আসসালামু আলাইকুম Taqwa Village,\nআমি আপনাদের প্রজেক্টে আগ্রহী।\n\nনাম: ${name}\nমোবাইল: ${phone}\nইমেইল: ${email || '—'}\nআগ্রহ: ${interestLabel}\nসম্ভাব্য তারিখ: ${date || 'শীঘ্রই'}\nমন্তব্য: ${message || 'নাই'}`
  );

  window.open(`https://wa.me/8801335145110?text=${waText}`, '_blank', 'noopener,noreferrer');
  showToast('হোয়াটসঅ্যাপে বার্তাটি পাঠিয়ে আপনার আবেদন সম্পন্ন করুন।');

}

// Video Showcase Interactions
function playShowcaseVideo() {
  openVideoModal();
}

function openVideoModal() {
  const modal = document.getElementById('videoModal');
  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}

function closeVideoModal() {
  const modal = document.getElementById('videoModal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
}

function toggleVideoMute() {
  isMuted = !isMuted;
  const muteBtn = document.getElementById('muteBtn');
  if (muteBtn) {
    muteBtn.innerHTML = isMuted
      ? '<i data-lucide="volume-x" class="w-4 h-4"></i>'
      : '<i data-lucide="volume-2" class="w-4 h-4"></i>';
    if (window.lucide) window.lucide.createIcons();
  }
  showToast(isMuted ? 'সাউন্ড মিউট করা হয়েছে' : 'সাউন্ড আনমিউট করা হয়েছে');
}

function changeVideoChapter(chapterNum) {
  const thumbnail = document.getElementById('videoThumbnail');
  const chapters = {
    1: {
      img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80',
      title: '১. সাইট ড্রোন ভিউ'
    },
    2: {
      img: 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=1200&q=80',
      title: '২. কটেজ ও লেক আর্কিটেকচার'
    },
    3: {
      img: 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1200&q=80',
      title: '৩. পারিবারিক ও অর্গানিক জোন'
    }
  };

  if (thumbnail && chapters[chapterNum]) {
    thumbnail.src = chapters[chapterNum].img;
    showToast(`অধ্যায় পরিবর্তিত হয়েছে: ${chapters[chapterNum].title}`);
  }
}

// Lightbox for slider
function openLightbox(imgSrc, caption) {
  const modal = document.getElementById('lightboxModal');
  const img = document.getElementById('lightboxImg');
  const cap = document.getElementById('lightboxCaption');
  if (modal && img) {
    img.src = imgSrc;
    if (cap) cap.textContent = caption || '';
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}

function closeLightbox() {
  const modal = document.getElementById('lightboxModal');
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
}

// Masterplan tab switch
function switchTab(tab) {
  const slider = document.getElementById('slider-section');
  if (slider) {
    slider.scrollIntoView({ behavior: 'smooth' });
    showToast('মাস্টারপ্ল্যান ও গ্যালারি সেকশন প্রদর্শন করা হচ্ছে');
  }
}

// Toast Notification
function showToast(message) {
  const toast = document.getElementById('toast');
  const toastMsg = document.getElementById('toastMsg');
  if (toast && toastMsg) {
    toastMsg.textContent = message;
    toast.classList.remove('translate-y-24', 'opacity-0');
    toast.classList.add('translate-y-0', 'opacity-100');

    setTimeout(() => {
      toast.classList.remove('translate-y-0', 'opacity-100');
      toast.classList.add('translate-y-24', 'opacity-0');
    }, 3500);
  }
}

// Countdown Timer for Offer Tag
function startCountdown() {
  const countdownEl = document.getElementById('countdown');
  if (!countdownEl) return;

  let totalSeconds = 14 * 86400 + 8 * 3600 + 32 * 60; // 14 days 8 hrs 32 mins

  setInterval(() => {
    if (totalSeconds <= 0) return;
    totalSeconds--;

    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);

    countdownEl.textContent = `${days}দ ${hours.toString().padStart(2, '0')}ঘ ${minutes.toString().padStart(2, '0')}মি`;
  }, 1000);
}

// Close modals on Escape key
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeBookingModal();
    closeVideoModal();
    closeLightbox();
  }
});


Object.assign(translations.bn, {
  hero_title: 'প্রকৃতির কাছে, আপনজনের সাথে।', hero_description: 'শহরের ব্যস্ততা পেরিয়ে সবুজের মাঝে একটুখানি প্রশান্তি। তাকওয়া ভিলেজে আবিষ্কার করুন প্রকৃতি, পারিবারিক আনন্দ ও নৈতিক জীবনযাপনের এক অনন্য সমন্বয়।', explore: 'প্রকল্প ঘুরে দেখুন', hero_location: 'পূর্বাচল সেক্টর ৩০ সংলগ্ন, উলুখোলা', image_note: 'লাইফস্টাইলের অনুপ্রেরণামূলক ছবি', visual_caption: 'ব্যস্ততার বাইরে, ভালো থাকার ঠিকানা।', value_nature: 'সবুজে ঘেরা পরিবেশ', value_family: 'পরিবারের জন্য পরিকল্পিত', value_ethics: 'নৈতিক জীবনযাপনের ভাবনা', our_story: 'আমাদের গল্প', discover_title: 'আপনার নতুন অভিজ্ঞতার শুরু', discover_description: 'কটেজ, রিসোর্ট ও সবুজ প্রকৃতি — এক ঠিকানায়।'
});
Object.assign(translations.en, {
  hero_title: 'Closer to nature. Closer to each other.', hero_description: 'Leave the city bustle behind for a moment of calm. Discover a thoughtful blend of nature, family experiences and ethical living at Taqwa Village.', explore: 'Explore the project', hero_location: 'Near Purbachal Sector 30, Ulukhola', image_note: 'Lifestyle inspiration image', visual_caption: 'A place to slow down and feel at home.', value_nature: 'Surrounded by greenery', value_family: 'Designed for families', value_ethics: 'Thoughtful, ethical living', our_story: 'Our story', discover_title: 'Your next chapter begins here', discover_description: 'Cottages, resort experiences and nature, together.'
});

// Keep dialogs accessible to keyboard users and restore their starting position.
document.addEventListener('DOMContentLoaded', () => {
  let returnFocus = null;
  const dialogs = [...document.querySelectorAll('[role="dialog"]')];
  const focusable = modal => [...modal.querySelectorAll('button, a[href], input, select, textarea, [tabindex="0"]')].filter(el => el.getClientRects().length);
  dialogs.forEach(modal => {
    let wasOpen = false;
    new MutationObserver(() => {
      const isOpen = !modal.classList.contains('hidden');
      if (isOpen === wasOpen) return;
      wasOpen = isOpen;
      if (isOpen) {
        returnFocus = document.activeElement;
        focusable(modal)[0]?.focus();
      } else if (!dialogs.some(el => !el.classList.contains('hidden'))) {
        returnFocus?.focus();
      }
    }).observe(modal, { attributes: true, attributeFilter: ['class'] });
    modal.addEventListener('keydown', event => {
      if (event.key !== 'Tab') return;
      const items = focusable(modal);
      const first = items[0], last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    });
    modal.addEventListener('click', event => {
      if (event.target !== modal) return;
      if (modal.id === 'bookingModal') closeBookingModal();
      if (modal.id === 'videoModal') closeVideoModal();
    });
  });
  document.querySelectorAll('img').forEach(img => { if (img.fetchPriority !== 'high') img.loading = 'lazy'; });
  const dateInput = document.getElementById('userDate');
  const now = new Date();
  if (dateInput) dateInput.min = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
});


/* =========================================================
   TAQWA VILLAGE - ENHANCED IMAGE SLIDER & INTERACTIVE LOGIC
   ========================================================= */

let currentFallbackSlide = 0;
let fallbackInterval = null;

function setupEnhancedSlider() {
  const swiperEl = document.querySelector('.mySwiper');
  if (!swiperEl) return;

  function tryHookSwiper() {
    if (typeof Swiper !== 'undefined' && swiperInstance) {
      try {
        swiperInstance.on('slideChange', function() {
          const idx = this.realIndex;
          updateSliderThumbnails(idx);
          updateSliderCounter(idx);
        });
        return true;
      } catch (e) {
        console.warn(e);
      }
    }
    return false;
  }

  // If Swiper instance is available, hook it
  if (!tryHookSwiper()) {
    let retries = 0;
    const checkTimer = setInterval(() => {
      retries++;
      if (tryHookSwiper() || retries > 15) {
        clearInterval(checkTimer);
        if (!swiperInstance) setupCustomFallback();
      }
    }, 200);
  }

  // Bind thumbnail buttons
  document.querySelectorAll('.sketch-slider-thumb').forEach((thumb, i) => {
    thumb.addEventListener('click', () => {
      goToHomeSlide(i);
    });
  });
}

function updateSliderThumbnails(idx) {
  document.querySelectorAll('.sketch-slider-thumb').forEach((thumb, i) => {
    thumb.classList.toggle('active', i === idx);
  });
}

function updateSliderCounter(idx) {
  const counter = document.getElementById('sliderCounter');
  if (counter) {
    const total = 6;
    counter.textContent = `${String(idx + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`;
  }
}

window.goToHomeSlide = function(idx) {
  if (swiperInstance && swiperInstance.slideToLoop) {
    swiperInstance.slideToLoop(idx, 600);
  } else if (typeof window.showCustomSlide === 'function') {
    window.showCustomSlide(idx);
  }
  updateSliderThumbnails(idx);
  updateSliderCounter(idx);
};

function setupCustomFallback() {
  const slides = document.querySelectorAll('.mySwiper .swiper-slide');
  if (!slides.length) return;

  window.showCustomSlide = function(index) {
    currentFallbackSlide = (index + slides.length) % slides.length;
    slides.forEach((s, i) => {
      s.style.display = i === currentFallbackSlide ? 'block' : 'none';
      s.style.opacity = i === currentFallbackSlide ? '1' : '0';
      s.style.transition = 'opacity 0.6s ease';
    });
    updateSliderThumbnails(currentFallbackSlide);
    updateSliderCounter(currentFallbackSlide);
  };

  window.showCustomSlide(0);

  const prevBtn = document.getElementById('sliderPrevBtn');
  const nextBtn = document.getElementById('sliderNextBtn');
  if (prevBtn) prevBtn.onclick = () => window.showCustomSlide(currentFallbackSlide - 1);
  if (nextBtn) nextBtn.onclick = () => window.showCustomSlide(currentFallbackSlide + 1);

  fallbackInterval = setInterval(() => {
    window.showCustomSlide(currentFallbackSlide + 1);
  }, 4500);

  const container = document.querySelector('.mySwiper');
  if (container) {
    container.addEventListener('mouseenter', () => clearInterval(fallbackInterval));
    container.addEventListener('mouseleave', () => {
      clearInterval(fallbackInterval);
      fallbackInterval = setInterval(() => window.showCustomSlide(currentFallbackSlide + 1), 4500);
    });
  }
}

// 5-Zone Master Plan Explorer Data & Switcher
const homeZoneData = {
  zone1: {
    title_bn: 'জোন ১: লেকভিউ ও ফ্লোটিং ডুপ্লেক্স কটেজ',
    title_en: 'Zone 1: Lakeview & Floating Duplex Cottages',
    badge_bn: 'এক্সক্লুসিভ ওয়াটারফ্রন্ট ভিলা',
    badge_en: 'Exclusive Waterfront Villas',
    img: 'https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=1200&q=85',
    desc_bn: 'স্বচ্ছ লেকের শান্ত পানির ওপর স্থাপিত আধুনিক ফ্লোটিং ডুপ্লেক্স কটেজ। প্রাকৃতিক দৃশ্য উপভোগের সঙ্গে সম্পূর্ণ পারিবারিক প্রাইভেসি নিশ্চিত।',
    desc_en: 'Architecturally crafted luxury floating duplex cottages built over clear lake water, offering serene panoramic views and absolute family privacy.',
    features_bn: ['প্রাইভেট লেকভিউ ডেক ও ব্যালকনি', '১০০% সাউন্ডপ্রুফ ও পরিবেশবান্ধব উপাদান', '২৪ ঘণ্টা বাটলার ও রুম সার্ভিস', 'সুপরিসর মাস্টার বেড ও কিচেন স্পেস'],
    features_en: ['Private lakefront deck & balcony', '100% soundproof eco-materials', '24/7 dedicated butler & room service', 'Spacious master bed & kitchenette']
  },
  zone2: {
    title_bn: 'জোন ২: ৫-স্টার ইকো রিসোর্ট ও হোটেল সুইটস',
    title_en: 'Zone 2: 5-Star Eco Resort & Hotel Suites',
    badge_bn: 'লাক্সারি হসপিটালিটি ও কনফারেন্স',
    badge_en: 'Luxury Hospitality & Banquet',
    img: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1200&q=85',
    desc_bn: 'আন্তর্জাতিক মানের আধুনিক রিসোর্ট কমপ্লেক্স, ফ্যামিলি সুইটস, এক্সিকিউটিভ লাউঞ্জ ও আন্তর্জাতিক কনফারেন্স অডিটোরিয়াম।',
    desc_en: 'An international standard resort complex with lavish suites, executive lounge and corporate conference auditorium.',
    features_bn: ['ইনফিনিটি সুইমিং পুল', '১০০০ আসনবিশিষ্ট আন্তর্জাতিক কনভেনশন হল', 'মাল্টি-কুইজিন হালাল ডাইনিং', 'ফিটনেস ও স্টিম স্পা কর্নার'],
    features_en: ['Infinity swimming pool', '1000-seat convention hall', 'Multi-cuisine halal dining', 'Fitness & steam spa center']
  },
  zone3: {
    title_bn: 'জোন ৩: কেন্দ্রীয় জামে মসজিদ ও ইসলামিক কালচারাল হাব',
    title_en: 'Zone 3: Central Grand Mosque & Cultural Hub',
    badge_bn: 'আধ্যাত্মিক প্রশান্তি ও নৈতিক বিকাশ',
    badge_en: 'Spiritual Peace & Ethical Learning',
    img: 'https://images.unsplash.com/photo-1564769625905-50e93615e769?auto=format&fit=crop&w=1200&q=85',
    desc_bn: 'দৃষ্টিনন্দন ঐতিহ্যবাহী ইসলামিক স্থাপত্যে নির্মিত কেন্দ্রীয় জামে মসজিদ, যেখানে থাকবে সমৃদ্ধ লাইব্রেরি ও কোরআন স্টাডি সার্কেল।',
    desc_en: 'A magnificent traditionally inspired Grand Jame Mosque with a comprehensive Islamic reference library and community gathering spaces.',
    features_bn: ['একসাথে ৩,০০০ মুসল্লির জামাত', 'নারী ও শিশুদের পৃথক এবাদতখানা', 'সমৃদ্ধ ইসলামি রিসার্চ লাইব্রেরি', 'পবিত্র কুরআন লার্নিং সেন্টার'],
    features_en: ['Capacity for 3,000 worshippers', 'Separate prayer area for women', 'Islamic research library', 'Quran learning center']
  },
  zone4: {
    title_bn: 'জোন ৪: ১০০% অর্গানিক ফার্ম ও ফিশিং লেক',
    title_en: 'Zone 4: 100% Organic Farm & Fishing Lake',
    badge_bn: 'বিষমুক্ত প্রকৃতি ও জীবন্ত খামার',
    badge_en: 'Pesticide-Free Agro & Fisheries',
    img: 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1200&q=85',
    desc_bn: 'প্রকল্পের নিজস্ব খামারে উৎপাদিত বিষমুক্ত টাটকা শাকসবজি, দেশি মাছ চাষ, ফলের বাগান এবং খাঁটি দুধ ও মধু উৎপাদন কেন্দ্র।',
    desc_en: 'A sustainable organic farming ecosystem producing pure vegetables, native fish varieties, fruit orchards, dairy, and natural honey.',
    features_bn: ['সম্পূর্ণ বিষমুক্ত খাদ্য উৎপাদন', 'পারিবারিক ফিশিং ও বোট রাইডিং', 'শিশুদের অ্যাগ্রো-ট্যুরিজম অভিজ্ঞতা', 'ফার্ম-টু-টেবিল ফ্রেশ ডাইনিং'],
    features_en: ['100% pesticide-free produce', 'Family recreational fishing', 'Children agro-tourism learning', 'Farm-to-table dining fresh daily']
  },
  zone5: {
    title_bn: 'জোন ৫: চিলড্রেনস অ্যাডভেঞ্চার পার্ক ও ওয়াটার জোন',
    title_en: 'Zone 5: Kids Adventure Park & Water Splash',
    badge_bn: 'সুস্থ পারিবারিক বিনোদন ও ক্রীড়া',
    badge_en: 'Healthy Family Fun & Adventure',
    img: 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=85',
    desc_bn: 'শিশুদের শারীরিক ও মানসিক বিকাশে আধুনিক ও নিরাপদ রাইডস, আলাদা স্প্ল্যাশ ওয়াটার পার্ক, ট্র্যাম্পোলিন এবং সাইক্লিং ট্রেইল।',
    desc_en: 'Exciting open-air play areas with safe rides, dedicated splash park, trampolines and cycling pathways for children.',
    features_bn: ['আন্তর্জাতিক মানসম্পন্ন নিরাপদ রাইডস', 'মহিলা ও শিশুদের পৃথক স্প্ল্যাশ পুল', 'প্রকৃতি পর্যবেক্ষণ ও ক্যাম্পিং জোন', '২৪ ঘণ্টা প্রশিক্ষিত সুপারভাইজার'],
    features_en: ['Child-safe international rides', 'Separate women & kids water splash', 'Nature watching & camping grounds', 'Trained supervisors on duty']
  }
};

let activeZoneKey = 'zone1';

window.switchHomeZone = function(zoneKey) {
  activeZoneKey = zoneKey;
  const data = homeZoneData[zoneKey];
  if (!data) return;

  document.querySelectorAll('.zone-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.zone === zoneKey);
  });

  const imgEl = document.getElementById('zoneImg');
  const badgeEl = document.getElementById('zoneBadge');
  const titleEl = document.getElementById('zoneTitle');
  const descEl = document.getElementById('zoneDesc');
  const featEl = document.getElementById('zoneFeatures');

  if (imgEl) {
    imgEl.style.opacity = '0';
    setTimeout(() => {
      imgEl.src = data.img;
      imgEl.style.opacity = '1';
    }, 150);
  }
  if (badgeEl) badgeEl.textContent = currentLanguage === 'en' ? data.badge_en : data.badge_bn;
  if (titleEl) titleEl.textContent = currentLanguage === 'en' ? data.title_en : data.title_bn;
  if (descEl) descEl.textContent = currentLanguage === 'en' ? data.desc_en : data.desc_bn;

  if (featEl) {
    const list = currentLanguage === 'en' ? data.features_en : data.features_bn;
    featEl.innerHTML = list.map(item => `<li><i data-lucide="check-circle-2"></i> <span>${item}</span></li>`).join('');
    if (window.lucide) window.lucide.createIcons();
  }
};

// Halal Investment Calculator
const homeCalcTiers = {
  tier1: {
    amount: '৳ ২,৫০,০০০',
    amount_en: 'BDT 2,50,000',
    title_bn: '১টি রিসোর্ট শেয়ার',
    title_en: '1 Resort Ownership Share',
    dividend_bn: '৳ ৩২,৫০০ - ৳ ৪০,০০০ (১৩-১৬%)',
    dividend_en: 'BDT 32,500 - 40,000 (13-16%)',
    stay_bn: '৭ রাত / বছর (সম্পূর্ণ ফ্রি)',
    stay_en: '7 Nights / Year (Complimentary)',
    gain_bn: '৳ ৪,০০,০০০+ (৫ বছরে আনুমানিক)',
    gain_en: 'BDT 4,00,000+ (Est. 5 Yr Growth)',
    deed_bn: 'নিবন্ধিত শেয়ার সার্টিফিকেট ও মুদারাবা পার্টনারশিপ',
    deed_en: 'Registered Share Certificate & Mudarabah Deed',
    interestVal: 'resort_investment'
  },
  tier2: {
    amount: '৳ ৫,০০,০০০',
    amount_en: 'BDT 5,00,000',
    title_bn: '২টি রিসোর্ট শেয়ার',
    title_en: '2 Resort Ownership Shares',
    dividend_bn: '৳ ৬৫,০০০ - ৳ ৮০,০০০ (১৩-১৬%)',
    dividend_en: 'BDT 65,000 - 80,000 (13-16%)',
    stay_bn: '১৫ রাত / বছর (সম্পূর্ণ ফ্রি)',
    stay_en: '15 Nights / Year (Complimentary)',
    gain_bn: '৳ ৮,৫০,০০০+ (৫ বছরে আনুমানিক)',
    gain_en: 'BDT 8,50,000+ (Est. 5 Yr Growth)',
    deed_bn: 'নিবন্ধিত শেয়ার সার্টিফিকেট ও ভিআইপি মেম্বারশিপ',
    deed_en: 'Registered Share Certificate & VIP Membership',
    interestVal: 'resort_investment'
  },
  tier4: {
    amount: '৳ ১০,০০,০০০',
    amount_en: 'BDT 10,00,000',
    title_bn: '৪টি এক্সিকিউটিভ শেয়ার',
    title_en: '4 Executive Ownership Shares',
    dividend_bn: '৳ ১,৩৫,০০০ - ৳ ১,৬৫,০০০ (১৩.৫-১৬.৫%)',
    dividend_en: 'BDT 1,35,000 - 1,65,000 (13.5-16.5%)',
    stay_bn: '৩০ রাত / বছর (সম্পূর্ণ ফ্রি)',
    stay_en: '30 Nights / Year (Complimentary)',
    gain_bn: '৳ ১৮,০০,০০০+ (৫ বছরে আনুমানিক)',
    gain_en: 'BDT 18,00,000+ (Est. 5 Yr Growth)',
    deed_bn: 'প্রিমিয়াম শেয়ারহোল্ডার ক্লাব মেম্বারশিপ ও চুক্তি',
    deed_en: 'Premium Shareholder Club Access & Deed',
    interestVal: 'resort_investment'
  },
  cottage: {
    amount: '৳ ৫৫,০০,০০০',
    amount_en: 'BDT 55,00,000',
    title_bn: 'প্রেসিডেনশিয়াল ফ্লোটিং কটেজ',
    title_en: 'Presidential Floating Cottage',
    dividend_bn: '৳ ৭,২০,০০০ - ৳ ৮,৮০,০০০ (বাৎসরিক ভাড়া আয়)',
    dividend_en: 'BDT 7,20,000 - 8,80,000 (Annual Rental Yield)',
    stay_bn: 'আজীবন আনলিমিটেড পারিবারিক এক্সেস',
    stay_en: 'Lifetime Unlimited Family Access',
    gain_bn: '৳ ৯০,০০,০০০+ (৫ বছরে সম্ভাব্য বাজারমূল্য)',
    gain_en: 'BDT 90,00,000+ (Est. 5 Yr Property Value)',
    deed_bn: 'শতভাগ সাফ-কবলা দলিল ও ভূমিস্বত্ব হস্তান্তর',
    deed_en: '100% Sub-Kabla Deed & Permanent Land Title',
    interestVal: 'cottage'
  }
};

let activeCalcTier = 'tier1';

window.switchCalcTier = function(tierKey) {
  activeCalcTier = tierKey;
  const data = homeCalcTiers[tierKey];
  if (!data) return;

  document.querySelectorAll('.calc-tier-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tier === tierKey);
  });

  const isEn = currentLanguage === 'en';
  const amtEl = document.getElementById('calcAmount');
  const divEl = document.getElementById('calcDividend');
  const stayEl = document.getElementById('calcStay');
  const gainEl = document.getElementById('calcGain');
  const deedEl = document.getElementById('calcDeed');

  if (amtEl) amtEl.textContent = isEn ? data.amount_en : data.amount;
  if (divEl) divEl.textContent = isEn ? data.dividend_en : data.dividend_bn;
  if (stayEl) stayEl.textContent = isEn ? data.stay_en : data.stay_bn;
  if (gainEl) gainEl.textContent = isEn ? data.gain_en : data.gain_bn;
  if (deedEl) deedEl.textContent = isEn ? data.deed_en : data.deed_bn;
};

window.bookSelectedTier = function() {
  const data = homeCalcTiers[activeCalcTier];
  if (data) {
    openBookingModal(data.interestVal);
  } else {
    openBookingModal('resort_investment');
  }
};

// Hook initialization when page is ready
document.addEventListener('DOMContentLoaded', () => {
  setupEnhancedSlider();
  switchHomeZone('zone1');
  switchCalcTier('tier1');
});
