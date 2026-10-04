import { init3DScene, toggleGlazing, setGlazingProgress, onGlazingChange } from './render.js';

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('canvas-container');
  if (!container) { console.error('Container 3D não encontrado.'); return; }
  try { 
    init3DScene(container); 
  } catch (err) {
    console.error('Erro ao iniciar o visualizador 3D:', err);
  }
  const btn = document.getElementById('btn-toggle');
  const slider = document.getElementById('glazing-slider');
  
  onGlazingChange(({ progress, open }) => {
    if (btn) btn.textContent = open ? 'Fechar Envidraçamento' : 'Abrir Envidraçamento';
    if (slider && document.activeElement !== slider) slider.value = progress;
  });
  
  btn?.addEventListener('click', () => toggleGlazing());
  slider?.addEventListener('input', (e) => setGlazingProgress(e.target.value));
});
