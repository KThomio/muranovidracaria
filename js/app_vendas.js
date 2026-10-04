import { init3DScene, toggleGlazing, setGlazingProgress, onGlazingChange } from './motor_vendas.js';

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('canvas-container');
    if(container) init3DScene(container);
    
    const btn = document.getElementById('btn-toggle');
    const slider = document.getElementById('glazing-slider');
    const sliderValueText = document.getElementById('slider-value');
    
    onGlazingChange(({ progress, open }) => {
        if(btn) btn.textContent = open ? 'Fechar Envidraçamento' : 'Abrir Envidraçamento';
        if(slider && document.activeElement !== slider) slider.value = progress;
        if(sliderValueText) sliderValueText.textContent = `${Math.round(progress * 100)}%`;
    });
    
    btn?.addEventListener('click', () => toggleGlazing());
    slider?.addEventListener('input', (e) => setGlazingProgress(e.target.value));
});
