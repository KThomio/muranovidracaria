# 🎯 SPEC DE EXECUÇÃO CIRÚRGICA V2: DEPLOY VERCEL + PIPELINE HÍBRIDO CAD 3D (PERFIS REAIS) & KEYFRAMES IA GENERATIVA

> **PROTOCOLO MULTI-MODELO ATIVO:**
> Planejado pelo **Modelo Forte (Arquiteto)** para execução imediata pelo **Modelo Rápido/Barato (Gemini Flash)** com a skill `superpowers` ativa.

---

## 🛡️ REGRAS INVIOLÁVEIS PARA O MODELO EXECUTOR
1. **Ative a skill `superpowers`** antes de iniciar.
2. **PROIBIDO OMITIR CÓDIGO:** Nunca use `// resto do código` ou placeholders incompletos.
3. **ZERO ALUCINAÇÃO:** Mantenha todos os dados verificados da Murano Vidraçaria (`(15) 99159-8438`, `@muranovidros2`, CNPJ `64.581.884/0001-72`, `R. Cervantes, 237 - Vila Assis, Sorocaba - SP`).
4. **FIDELIDADE ESTRITA À PRANCHA TÉCNICA (`MURANO_3D_TECHNICAL_CONTEXT.md` + Prancha Oficial):**
   - Vão do sistema: `1900 mm` (L) × `860 mm` (A).
   - Veneziana fixa à direita: `150 mm` × `860 mm` (Perfil `VZ 060-P064` com aletas ventiladas reais a cada `30 mm`).
   - Folhas móveis: `4 folhas` de `427.75 mm` × `660 mm`, vidro **Laminado Incolor 10 mm (5+5)** (transparente cristalino real, NÃO colorido de ciano neon).
   - Perfis de alumínio: **Preto Fosco RAL 9005**, com canal/rasgo em **U** real nos trilhos superior/inferior, escovas de vedação `5x6`, perfis leito e pinos/pivôs cilíndricos de inox/latão a `30 mm` da borda.
   - Guarda-Corpo Inferior (`GC-VARANDA`): `1930 mm` de largura total com 3 módulos de `610 mm` (`V1 | V2 | V1`) e vidro laminado incolor 8mm abaixo da mureta/corrimão.

---

## 🚀 TAREFA 1: Promover Nova LP para a Raiz (`index.html`) e Atualizar Vercel (Git Push)

A Vercel serve o arquivo `index.html` da raiz do repositório (`https://github.com/KThomio/muranovidracaria.git`).
1. Copie todo o conteúdo de `clients/murano-vidracaria/lp/index.html` para `clients/murano-vidracaria/index.html` ajustando os caminhos relativos:
   - Substitua `../assets/` por `assets/`
   - Substitua `../js/motion-scroll.js` por `js/motion-scroll.js`
2. Mantenha `lp/index.html` sincronizado para referência modular do pacote.
3. Certifique-se de que o `.gitignore` de `clients/murano-vidracaria/` **NÃO bloqueie** `assets/images/*` nem `assets/videos/preview_animacao.mp4` (pois a Vercel precisa desses arquivos no repositório Git para exibi-los no site publicado!), bloqueando apenas arquivos `.blend`, `.blend1`, `__pycache__` e `node_modules`.

---

## 🏗️ TAREFA 2: Modelagem CAD de Precisão dos Perfis Reais + Keyframes 1080p p/ IA Generativa (`blender_pipeline/`)

Reescreva `blender_pipeline/build_scene_v2.py` e `blender_pipeline/render_fast_preview.py` para abandonar os "cubos lisos genéricos" e construir a geometria técnica real em **Full HD (`1920x1080`)**:

### 2.1. Geometria Real dos Perfis e Componentes em `build_scene_v2.py`
1. **Trilhos Superior e Inferior em Perfil "U" Usinado (`TRILHO_INF` e `TRILHO_SUP`):**
   - Em vez de um cubo maciço cego, construa o trilho (`1900mm` comp × `45mm` prof × `60mm` alt) composto por base + 2 abas laterais formantando o **canal interno em U** de `24mm` de abertura onde o perfil leito corre, mais 2 frisos de **Escova de Vedação 5x6** na borda interna.
   - No lado esquerdo (`x = 15mm .. 160mm`), modele a abertura visual do **Alojamento/Rasgo de Saída** e os **4 Pivôs/Discos de Estacionamento** cilíndricos em latão/inox (`radius = 6mm`, espaçados de `30mm` eixo a eixo a partir de `x = 30mm`).
2. **Perfis Leito (`FOLHA_XX_LEITO_SUP` e `INF`) + Pinos de Giro:**
   - Perfil que abraça a base e o topo do vidro de `10mm`, com chanfro chanfrado (`Bevel 1.5mm`) e pino pivô cilíndrico visível a `30mm` da extremidade esquerda de cada folha.
3. **Veneziana Fixa `VZ 060-P064` com Aletas 3D Reais (`VENEZIANA_REF`):**
   - Na posição `x = 1900mm - 75mm` (`150mm` de largura), substitua o cubo liso por molduras laterais de alumínio + **aletas horizontais 3D reais** inclinadas a `35°` a cada `30mm` de altura (respeitando a ventilação permanente da Norma NBR 13.303 descrita na prancha!).
4. **Contexto Arquitetônico Realista da Varanda (em 3D real, sem foto 2D torta):**
   - Modele o vão real da varanda em alvenaria arquitetônica texturizada (`Paredes Laterais`, `Viga Superior`, `Mureta Central` sob o trilho inferior) e, abaixo da mureta, o **Guarda-Corpo `GC-VARANDA`** com os 3 módulos de `610mm` (`V1 | V2 | V1`) em perfil preto e vidro laminado incolor.
   - No fundo externo (através do vidro), crie uma iluminação de céu diurno/entardecer suave (`Nishita Sky / HDRI Procedural Suave`) para que o **Vidro Laminado Incolor 5+5 (`IOR 1.52`, `Roughness 0.005`, `Base Color (0.97, 0.99, 0.98)`)** seja **100% transparente e cristalino**, com reflexo natural de vidro de verdade e apenas a lapidação da borda de `10mm` levemente esverdeada como vidro real.

### 2.2. Geração dos 3 Keyframes Master em 1080p (Cycles Raytracing) + Vídeo 1080p
Atualize `blender_pipeline/render_fast_preview.py` para:
- Resolução Full HD `1920x1080`.
- Quando chamado com `--keyframes`, renderizar no motor **CYCLES** (`samples = 64` + Denoising) e salvar na pasta `clients/murano-vidracaria/motion/keyframes_ia/`:
  1. `keyframe_01_fechado.png` (Frame 1: As 4 folhas alinhadas fechando o vão + veneziana fixa à direita).
  2. `keyframe_02_deslizando_giro.png` (Frame 110: Folha 01 aberta a 90° no alojamento esquerdo, Folha 02 iniciando giro no pivô e Folhas 03/04 deslizando no trilho U).
  3. `keyframe_03_aberto_total.png` (Frame 240: Todas as 4 folhas recolhidas e empilhadas a 90° à esquerda com espaçamento de 30mm eixo a eixo + vão livre).
- Em seguida, renderizar a animação completa `assets/videos/preview_animacao.mp4` (240 frames, `gopsize = 1`, H.264) para que o site na Vercel já exiba a nova cena 3D realista imediatamente!

### 2.3. Criar o Guia Prático de Geração no Kling AI / Runway (`motion/GUIA_IA_GENERATIVA_VIDEO.md`)
Crie o arquivo `clients/murano-vidracaria/motion/GUIA_IA_GENERATIVA_VIDEO.md` contendo:
- O passo a passo exato de como subir `keyframe_01_fechado.png` como **Start Frame** e `keyframe_02_deslizando_giro.png` / `keyframe_03_aberto_total.png` como **End Frame** no **Kling AI 1.6 (Modo Pro - First/Last Frame)** ou **Runway Gen-3 Alpha**.
- Os prompts técnicos em inglês (otimizados para arquitetura fotorrealista 8K) que preservam a geometria dos perfis pretos RAL 9005 e a transparência do vidro laminado.
- O comando FFmpeg pronto de 1 linha para quando o Diretor baixar o MP4 do Kling/Runway converter para All-Intra (`-g 1`) e substituir `assets/videos/preview_animacao.mp4`.

---

## ✅ TAREFA 3: Execução, QA, Commit & Push para a Vercel
1. Rode o build e o QA do Blender (`build_scene_v2.py` e `run_qa_scene_v2.py`).
2. Rode o render dos 3 keyframes Cycles 1080p (`--keyframes`) e o render do vídeo `preview_animacao.mp4`.
3. No diretório `clients/murano-vidracaria`, execute `git add`, `git commit` e `git push origin main` para publicar a atualização na Vercel.
4. Atualize o `STATE.md` (< 40 linhas).
