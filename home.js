document.addEventListener('DOMContentLoaded', () => {
  const pause = document.getElementById('homeSliderPause');
  if (!pause) return;
  let paused = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function sync() {
    if (!swiperInstance) return;
    if (paused) swiperInstance.autoplay.stop();
    else swiperInstance.autoplay.start();
    pause.setAttribute('aria-pressed', String(paused));
    pause.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow');
    pause.innerHTML = `<i data-lucide="${paused ? 'play' : 'pause'}"></i>`;
    window.lucide?.createIcons();
  }
  pause.addEventListener('click', () => { paused = !paused; sync(); });
  sync();
});
