# 🎬 PLANO DE ATUALIZAÇÃO DO RENDER 3D (BLENDER PIPELINE)

## 1. O Diagnóstico do Motion Anterior:
O render anterior sofreu de duas falhas críticas apontadas pelo Diretor:
1. **Falta de Realismo Físico (PBR):** O material do vidro parecia fosco/plástico e o alumínio sem o chanfro e reflexo especular real.
2. **Iluminação Amadora:** Iluminação uniforme sem profundidade, sem contraste dramático de estúdio de arquitetura.

## 2. Ações de Correção Cinemática:
- [ ] **Ajuste de Câmera:** Lente 35mm cinematográfica com Depth of Field (DoF) sutil focado no mecanismo pivotante.
- [ ] **Iluminação de 3 Pontos (High-End):**
  - Key Light: Softbox quente de 45° simulando luz natural da varanda.
  - Rim Light (Luz de Recorte): Ciano sutil a 135° realçando a espessura e bisel do vidro laminado 10mm.
  - Fill Light difusa escura para sombras profundas.
- [ ] **Materiais PBR:**
  - Vidro Laminado: `Transmission: 1.0`, `Roughness: 0.005`, `IOR: 1.52`.
  - Alumínio Estrutural: `Metallic: 0.95`, `Roughness: 0.25` com leve micro-textura anisotrópica.
- [ ] **Movimento Curvado:** Curvas de animação Bezier com aceleração suave e parada amortecida no alojamento esquerdo.
