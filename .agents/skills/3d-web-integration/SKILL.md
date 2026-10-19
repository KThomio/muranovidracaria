---
name: 3d-web-integration
description: Integração e automação de assets 3D (Blender/GLTF) em ecossistemas web com alta performance (Three.js, GSAP).
---

# Skill: Web 3D & Motion de Alta Conversão

## 1. Visão Geral
Transformar modelos precisos do Blender em experiências interativas web.

## 2. Ecossistema Sugerido
- **Exportação:** Sugira gerar ativos `.glb` ou `.gltf` automatizados via Python (`bpy`). Sugira compressão (draco/gltf-pipeline).
- **Render Interativo:** Use `Three.js` Vanilla ou `@react-three/fiber` (com `drei`).
- **Cinemática:** Use sempre **GSAP (ScrollTrigger)** para animações scroll-bound.

## 3. Regra de Execução
Entregue código modularizado: um script para otimizar o Blender e outro JS para o Canvas com anti-aliasing e responsividade.
