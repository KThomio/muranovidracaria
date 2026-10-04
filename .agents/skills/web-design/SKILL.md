---
name: web-design
description: Design principles and visual identity to avoid generic AI looks.
---

# Skill: Web Design Profissional

## 1. VisÃ£o Geral
Esta skill estabelece os princÃ­pios e critÃ©rios estÃ©ticos para a criaÃ§Ã£o de interfaces web modernas, confiÃ¡veis e com alta taxa de conversÃ£o. O objetivo central Ã© entregar produtos com acabamento refinado de estÃºdio de design, **eliminando totalmente a aparÃªncia genÃ©rica e artificial tÃ­pica de templates gerados por IA**.

---

## 2. PrincÃ­pios de Hierarquia Visual e Tipografia
1. **Escala TipogrÃ¡fica Controlada:**
   - Use uma proporÃ§Ã£o harmÃ´nica (ex: Major Second `1.125` ou Minor Third `1.2`).
   - Evite misturar mais de duas famÃ­lias tipogrÃ¡ficas. O padrÃ£o ideal Ã©:
     - 1 fonte expressiva e moderna para tÃ­tulos (`font-heading`).
     - 1 fonte altamente legÃ­vel com suporte completo a pesos e caracteres para corpo de texto (`font-body`).
   - Diferencie nÃ­veis de informaÃ§Ã£o nÃ£o apenas por tamanho, mas por peso (`font-weight`), cor e espaÃ§amento (`letter-spacing`).
2. **Escaneabilidade do ConteÃºdo:**
   - Textos de parÃ¡grafo nunca devem ultrapassar 65 a 75 caracteres por linha (`max-width: 65ch`) para evitar fadiga visual.
   - Use tÃ­tulos que sintetizem o benefÃ­cio e subtÃ­tulos complementares curtos.

---

## 3. EspaÃ§amento, Ritmo e Layout
1. **Sistema de Grid e EspaÃ§amento Base 4/8px:**
   - Adote mÃºltiplos de 8px (8px, 16px, 24px, 32px, 48px, 64px, 96px, 128px) para margens, paddings e gaps.
   - Respiro visual transmite valor premium. Interfaces amontoadas parecem amadoras.
2. **Alinhamento e ConsistÃªncia:**
   - Mantenha linhas de visÃ£o consistentes. Elementos que pertencem ao mesmo grupo devem compartilhar alinhamentos exatos.

---

## 4. Identidade Visual e Paleta de Cores
1. **Regra 60-30-10:**
   - 60% cor dominante/neutra (fundos limpos, brancos, cinzas suaves ou temas escuros profundos e consistentes).
   - 30% cor secundÃ¡ria de apoio (estruturas de cards, bordas sutis, tipografia secundÃ¡ria).
   - 10% cor de destaque/aÃ§Ã£o (botÃµes primÃ¡rios de conversÃ£o, badges pontuais).
2. **Contraste Intencional:**
   - Garanta contraste acessÃ­vel (mÃ­nimo WCAG AA 4.5:1 para texto normal, 3:1 para textos grandes).
   - Evite fundos com gradientes exagerados ou sombras pesadas e borradas. Use sombras suaves e difusas com baixa opacidade (`rgba(0,0,0, 0.04)` a `0.08)` para criar profundidade natural.

---

## 5. Como Evitar a "AparÃªncia GenÃ©rica de IA"
| âŒ O que Evitar (ClichÃª de IA) | âœ… O que Fazer (Design Profissional) |
| :--- | :--- |
| IlustraÃ§Ãµes 3D genÃ©ricas flutuantes e astronautas roxos | Fotos reais e autÃªnticas do setor do cliente ou Ã­cones vetoriais refinados e monocromÃ¡ticos |
| Gradientes neon roxo/azul cÃ³smico sem motivo | Paleta sÃ³bria alinhada Ã  psicologia do nicho de atuaÃ§Ã£o do cliente |
| Textos vagos como "SoluÃ§Ãµes Inovadoras do Futuro" | Proposta de valor direta: "Aumente seus agendamentos em 35% sem sobrecarregar sua equipe" |
| Efeitos exagerados em tudo (glows, glassmorphism excessivo) | MicrointeraÃ§Ãµes elegantes, bordas sutis (`1px solid var(--border)`), foco total no conteÃºdo |
| BotÃµes idÃªnticos em todas as seÃ§Ãµes | Hierarquia clara: Apenas 1 CTA PrimÃ¡rio por viewport, complementado por CTA SecundÃ¡rio neutro |

---

## 6. UX Focado em ConversÃ£o e Mobile-First
- **Primeira Dobra (Hero Section):** Deve responder em menos de 5 segundos:
  1. O que este negÃ³cio oferece?
  2. Para quem Ã©?
  3. Qual o diferencial imediato?
  4. O que devo fazer agora? (CTA evidente).
- **Provas Sociais CrÃ­veis:** NÃºmeros tangÃ­veis, depoimentos com nomes/cargos/empresas, logos de clientes ou certificaÃ§Ãµes.
- **Mobile First:** Todo componente deve ser desenhado para polegares em telas pequenas antes de expandir para grids de desktop.

