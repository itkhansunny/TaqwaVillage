document.addEventListener('DOMContentLoaded', () => {
  // Photo Carousel Controls
  const prevBtn = document.getElementById('carouselPrevBtn');
  const nextBtn = document.getElementById('carouselNextBtn');
  const track = document.getElementById('photoCarouselTrack');
  if (track && prevBtn && nextBtn) {
    prevBtn.addEventListener('click', () => {
      track.scrollBy({ left: -260, behavior: 'smooth' });
    });
    nextBtn.addEventListener('click', () => {
      track.scrollBy({ left: 260, behavior: 'smooth' });
    });
  }

  const pause = document.getElementById('homeSliderPause');
  if (!pause) return;
  let paused = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function sync() {
    if (!window.swiperInstance) return;
    if (paused) window.swiperInstance.autoplay.stop();
    else window.swiperInstance.autoplay.start();
    pause.setAttribute('aria-pressed', String(paused));
    pause.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow');
    pause.innerHTML = `<i data-lucide="${paused ? 'play' : 'pause'}"></i>`;
    window.lucide?.createIcons();
  }
  pause.addEventListener('click', () => { paused = !paused; sync(); });
  sync();
});
