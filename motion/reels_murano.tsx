import { Composition } from 'remotion';
import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';

// Cena 1: A Dor das Sacadas Convencionais
const Scene1Problem: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 12 } });
  const opacity = interpolate(frame, [0, 15], [0, 1]);

  return (
    <div style={{ flex: 1, backgroundColor: '#050811', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', padding: '60px', fontFamily: 'Space Grotesk, sans-serif' }}>
      <span style={{ color: '#ef4444', fontSize: '28px', textTransform: 'uppercase', letterSpacing: '4px', fontWeight: 700, marginBottom: '20px' }}>
        O Erro Que Todos Cometem
      </span>
      <h1 style={{ color: '#ffffff', fontSize: '64px', fontWeight: 800, textAlign: 'center', transform: `scale(${scale})`, opacity, lineHeight: 1.15 }}>
        Sua sacada faz barulho ou trava ao abrir?
      </h1>
      <p style={{ color: '#94a3b8', fontSize: '32px', textAlign: 'center', marginTop: '30px', maxWidth: '800px', fontFamily: 'Inter, sans-serif' }}>
        90% das sacadas usam roldanas plásticas frágeis que quebram com o vento.
      </p>
    </div>
  );
};

// Cena 2: A Solução de Alta Engenharia Murano
const Scene2Solution: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const translateY = interpolate(frame, [0, 20], [60, 0]);
  const opacity = interpolate(frame, [0, 20], [0, 1]);

  return (
    <div style={{ flex: 1, backgroundColor: '#050811', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', padding: '60px', fontFamily: 'Space Grotesk, sans-serif' }}>
      <span style={{ color: '#00F0FF', fontSize: '28px', textTransform: 'uppercase', letterSpacing: '4px', fontWeight: 700, marginBottom: '20px' }}>
        Engenharia Murano Vidraçaria
      </span>
      <h1 style={{ color: '#ffffff', fontSize: '68px', fontWeight: 800, textAlign: 'center', opacity, transform: `translateY(${translateY}px)`, lineHeight: 1.1 }}>
        Sistema 100% Sem Rolamentos.
      </h1>
      <div style={{ display: 'flex', gap: '20px', marginTop: '40px' }}>
        <div style={{ padding: '20px 30px', borderRadius: '16px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(0,240,255,0.3)', color: '#00F0FF', fontSize: '26px', fontWeight: 600 }}>
          ✓ Norma ABNT NBR 16259
        </div>
        <div style={{ padding: '20px 30px', borderRadius: '16px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(224,169,109,0.3)', color: '#E0A96D', fontSize: '26px', fontWeight: 600 }}>
          ✓ Garantia Vitalícia
        </div>
      </div>
    </div>
  );
};

export const MuranoReelsVideo: React.FC = () => {
  return (
    <Composition
      id="MuranoReels"
      component={Scene1Problem}
      durationInFrames={180} // 6 segundos a 30fps
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
