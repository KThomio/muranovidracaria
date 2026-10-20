/**
 * Murano Vidraçaria — Controlador Cinemático GSAP ScrollTrigger (Scrollytelling 3D)
 * Sincroniza os 240 frames (All-Intra H.264) da Sacada sem Rolamentos com o scroll.
 */
(() => {
    const STAGES = [
        { limit: 0.25, step: '01 / 04', title: 'Folha 01 · Destravamento e Giro 90° no Alojamento' },
        { limit: 0.50, step: '02 / 04', title: 'Folha 02 · Deslize Suave Sem Rolamento & Giro' },
        { limit: 0.75, step: '03 / 04', title: 'Folha 03 · Encaixe Preciso no Perfil Leito' },
        { limit: 1.01, step: '04 / 04', title: 'Folha 04 · Abertura Total do Vão com Veneziana Fixa' }
    ];

    const initMotionScroll = () => {
        if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
            return;
        }
        gsap.registerPlugin(ScrollTrigger);

        const section = document.getElementById('tecnologia');
        const video = document.getElementById('sacada-motion-video');
        const progressBar = document.getElementById('motion-progress-bar');
        const stageStep = document.getElementById('motion-stage-step');
        const stageLabel = document.getElementById('motion-stage-label');
        const progressPct = document.getElementById('motion-progress-pct');

        if (!section || !video) return;

        let targetTime = 0;
        let rafPending = false;

        const updateHUD = (progress) => {
            const clamped = Math.max(0, Math.min(1, progress));
            const pct = Math.round(clamped * 100);

            if (progressBar) {
                progressBar.style.transform = `scaleX(${clamped})`;
            }
            if (progressPct) {
                progressPct.textContent = `${pct}%`;
            }

            const activeStage = STAGES.find((s) => clamped <= s.limit) || STAGES[STAGES.length - 1];
            if (stageStep && stageStep.textContent !== activeStage.step) {
                stageStep.textContent = activeStage.step;
            }
            if (stageLabel && stageLabel.textContent !== activeStage.title) {
                stageLabel.textContent = activeStage.title;
            }
        };

        const renderVideoFrame = () => {
            rafPending = false;
            if (video.readyState >= 2 && Math.abs(video.currentTime - targetTime) > 0.015) {
                try {
                    video.currentTime = targetTime;
                } catch (_) {
                    // Ignora seek enquanto bufferiza
                }
            }
        };

        const setupScrollTrigger = () => {
            const duration = video.duration;
            if (!duration || isNaN(duration)) return;

            // Desbloqueia o decoder de hardware em navegadores mobile/Chromium
            video.pause();
            video.currentTime = 0;

            ScrollTrigger.create({
                trigger: section,
                start: 'top top',
                end: '+=250%',
                pin: true,
                scrub: 0.4,
                anticipatePin: 1,
                invalidateOnRefresh: true,
                onUpdate: (self) => {
                    targetTime = self.progress * Math.max(0, duration - 0.04);
                    updateHUD(self.progress);
                    if (!rafPending) {
                        rafPending = true;
                        requestAnimationFrame(renderVideoFrame);
                    }
                }
            });

            ScrollTrigger.refresh();
        };

        if (video.readyState >= 1 && video.duration) {
            setupScrollTrigger();
        } else {
            video.addEventListener('loadedmetadata', setupScrollTrigger, { once: true });
            video.load();
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMotionScroll);
    } else {
        initMotionScroll();
    }
})();
