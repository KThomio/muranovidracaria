import { createScene } from './scene3d.js';

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('canvas-container');
  const slider = document.getElementById('glazing-slider');
  const btn = document.getElementById('btn-toggle');
  const label = document.getElementById('slider-value');
  if (!container) return;

  const scene = createScene(container);
  let progress = 0;
  let target = 0;
  let raf = null;

  const render = () => {
    scene.setProgress(progress);
    const pct = Math.round(progress * 100);
    if (slider) slider.value = String(pct);
    if (label) label.textContent = pct + '%';
  };

  const tick = () => {
    const diff = target - progress;
    if (Math.abs(diff) < 0.005) {
      progress = target;
      raf = null;
    } else {
      progress += Math.sign(diff) * Math.min(Math.abs(diff), 0.012);
      raf = requestAnimationFrame(tick);
    }
    render();
  };

  const animateTo = (t) => {
    target = t;
    if (!raf) raf = requestAnimationFrame(tick);
  };

  btn?.addEventListener('click', () => animateTo(target > 0.5 ? 0 : 1));

  slider?.addEventListener('input', () => {
    if (raf) { cancelAnimationFrame(raf); raf = null; }
    progress = target = Number(slider.value) / 100;
    render();
  });

  render();
});
