# Murano Vidraçaria — Fechamento de Varanda (Torre B)

Visualizador 3D + landing page para apresentação na assembleia da Torre B.

## Memorial Descritivo

Fechamento em sistema de vidro deslizante e pivotante para o vão da varanda dos apartamentos da Torre B, conforme **ABNT NBR 16259/14**. O vão é reto e retangular (sem curvas). O trilho é fixado internamente na mureta. As 4 folhas móveis deslizam e pivotam a 90°, recolhendo-se na **parede esquerda** (lado oposto à churrasqueira, à direita).

## Especificações dos Materiais

| Item | Especificação |
|---|---|
| Vão | ~1930 mm (L) × ~1460 mm (A) |
| Formato | Reto e retangular |
| Perfis e trilhos | Alumínio, Branco RAL 9003B |
| Folhas | Exatamente 4 folhas móveis |
| Vidro | Laminado 10 mm (5+5), incolor, com vedação UV |
| Fixação do trilho | Interna na mureta, parafusos 1/4 x 70 |
| Abertura | Deslizante e pivotante 90°, recolhe à esquerda |
| Norma | ABNT NBR 16259/14 |
| Preço / prazo / contato | [A CONFIRMAR] |

## Stack

HTML5, Tailwind CSS (CDN), Three.js + OrbitControls (CDN). Sem build.

## Como rodar (Live Server)

1. Abra a pasta `murano-vidracaria/` no VS Code.
2. Instale a extensão **Live Server** (Ritwick Dey).
3. Clique com o botão direito em `index.html` → **Open with Live Server**.
4. Acesse `http://127.0.0.1:5500`.

## Estrutura

```
index.html
js/scene3d.js   # cena Three.js
js/main.js      # UI e inicialização
assets/{images,videos,docs}
```
