// Shared progressive enhancements for the connected static pages.
(() => {
  const storageKey = 'taqwa-language';
  const originalToggle = window.toggleLanguage;
  function applyPageLanguage() {
    document.querySelectorAll('[data-bn][data-en]').forEach(element => {
      element.textContent = element.dataset[currentLanguage];
    });
    document.querySelectorAll('[data-i18n]').forEach(element => {
      const text = translations[currentLanguage][element.dataset.i18n];
      if (text) element.textContent = text;
    });
    document.documentElement.lang = currentLanguage;
    const label = document.getElementById('langLabel');
    if (label) label.textContent = currentLanguage === 'bn' ? 'English' : 'বাংলা';
    try { localStorage.setItem(storageKey, currentLanguage); } catch { /* Storage is optional. */ }
  }
  window.toggleLanguage = () => { originalToggle(); applyPageLanguage(); };

  document.addEventListener('DOMContentLoaded', () => {
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved === 'en' || saved === 'bn') currentLanguage = saved;
    } catch { /* File previews can restrict local storage. */ }
    applyPageLanguage();

    document.querySelectorAll('[data-filter]').forEach(button => {
      button.addEventListener('click', () => {
        document.querySelectorAll('[data-filter]').forEach(other => other.setAttribute('aria-pressed', String(other === button)));
        let visible = 0;
        document.querySelectorAll('[data-gallery-image]').forEach(tile => {
          tile.hidden = button.dataset.filter !== 'all' && tile.dataset.category !== button.dataset.filter;
          if (!tile.hidden) visible++;
        });
        document.getElementById('gallery-status').textContent = currentLanguage === 'en' ? `${visible} images shown` : `${visible}টি ছবি দেখানো হচ্ছে`;
      });
    });
    document.querySelectorAll('[data-gallery-image]').forEach(button => {
      button.addEventListener('click', () => openLightbox(button.querySelector('img').src, button.querySelector('.gallery-caption > span').textContent));
    });

    const form = document.getElementById('inquiryForm');
    if (!form) return;
    const interest = document.getElementById('inquiryInterest');
    const requested = new URLSearchParams(location.search).get('interest');
    if ([...interest.options].some(option => option.value === requested)) interest.value = requested;
    const date = document.getElementById('inquiryDate');
    const now = new Date();
    date.min = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
    const result = document.getElementById('inquiryResult');
    form.addEventListener('input', () => { result.hidden = true; result.replaceChildren(); });
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const values = new FormData(form);
      if (!values.get('name').trim()) {
        document.getElementById('inquiryName').focus();
        return;
      }
      const message = `Hello Taqwa Village, I would like more information.\n\nName: ${values.get('name').trim()}\nPhone: ${values.get('phone').trim()}\nEmail: ${values.get('email').trim() || 'Not provided'}\nInterest: ${interest.selectedOptions[0].dataset.en}\nPreferred date: ${values.get('date') || 'To be discussed'}\nMessage: ${values.get('message').trim() || 'Please contact me with details.'}`;
      const text = document.createElement('p');
      text.textContent = currentLanguage === 'en' ? 'Your message is ready. Open WhatsApp, review it and send it to complete your inquiry.' : 'আপনার বার্তা প্রস্তুত। হোয়াটসঅ্যাপে খুলে যাচাই করে পাঠান।';
      const preview = document.createElement('pre');
      preview.className = 'message-preview';
      preview.textContent = message;
      const send = document.createElement('a');
      send.className = 'primary-button';
      send.textContent = currentLanguage === 'en' ? 'Continue to WhatsApp ↗' : 'হোয়াটসঅ্যাপে যান ↗';
      send.href = `https://wa.me/8801335145110?text=${encodeURIComponent(message)}`;
      send.target = '_blank';
      send.rel = 'noopener noreferrer';
      result.replaceChildren(text, preview, send);
      result.hidden = false;
      send.focus();
    });
  });
})();
