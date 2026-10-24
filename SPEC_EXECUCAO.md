# SPEC_EXECUCAO.md — Murano Vidraçaria (V3: Design Taste Frontend + HyperFrames + Blindagem SEO/GEO/Security/LGPD)

> **PROTOCOLO DE ROTEAMENTO (`model-router`):**
> - **Arquiteto (Planejador):** Gemini 4 Argon (Concluído — decisões travadas via `/grill-me`).
> - **Executor Recomendado:** **Gemini Flash** (ou modelo rápido equivalente) com a skill `superpowers` ativada.
> - **Regra de Ouro (`superpowers`):** É **TERMINANTEMENTE PROIBIDO** usar `// resto do código`, `<!-- ... -->` ou omitir blocos. Preserve 100% da codificação UTF-8 (acentuação perfeita em português) e sincronize tanto `lp/index.html` quanto `index.html` na raiz do repositório.

---

## 1. Contexto & Dados Reais Verificados (Zero Hallucination)
- **Razão Social (Controladora LGPD):** `Murano Vidraçaria Sorocaba Ltda`
- **Nome Fantasia:** `Murano Vidraçaria`
- **CNPJ:** `64.581.884/0001-72`
- **Responsável / Contato Oficial:** `Caroline Oliveira`
- **E-mail Oficial:** `muranovidracaria@gmail.com`
- **WhatsApp Oficial:** `(15) 99159-8438` (Link: `https://wa.me/5515991598438`)
- **Instagram Oficial:** `@muranovidros2` (`https://www.instagram.com/muranovidros2/`)
- **Endereço Físico:** `R. Cervantes, 237 - Vila Assis, Sorocaba - SP, 18025-174`
- **Avaliação Google:** `4.9 / 5.0` (`34 avaliações verificadas`)
- **Normas Técnicas Verificadas (Ficha Técnica Real):**
  - **ABNT NBR 16259/2014:** Sistema de envidraçamento articulado de ambientes (proteção contra intempéries, vento, chuva e ruído; nota técnica legal: sistemas articulados de sacada destinam-se à proteção e conforto térmico/acústico, não assegurando estanqueidade hermética total de fachada cortina).
  - **ABNT NBR 13.303:** Ventilação permanente obrigatória via Veneziana `VZ 060-P064` (espaçamento mínimo de 30mm para exaustão de gases e circulação contínua de ar).

---

## 2. Tarefa 1 — Design Taste Frontend (`design-taste-frontend`) em `lp/index.html` e `index.html`
Elevar a estética de toda a Landing Page para padrão de **Estúdio de Arquitetura / Boutique High-Ticket (Zero Cara de IA)**:
1. **Textura Óptica SVG Film Grain:**
   - Adicionar um overlay fixo (`position: fixed; inset: 0; pointer-events: none; z-index: 45; opacity: 0.028;`) com filtro `<svg>` fractalNoise sutil para eliminar o aspecto chapado digital em fundos escuros (`#030914`).
2. **Bordas Hairline Especulares & Crosshairs de Engenharia (`+`):**
   - Criar classes utilitárias `.cad-crosshair` que posicionam pequenos marcadores técnicos `+` (`#1CC8D8` com `opacity: 0.45`) nos cantos dos cards principais e do palco 3D.
3. **Indexação Editorial Numerada (Swiss Grid):**
   - Atualizar os cabeçalhos de seção com numeração técnica em `JetBrains Mono`:
     - `[ 01 // PORTFÓLIO DE ESPECIALIDADES ]` na seção `#solucoes`
     - `[ 02 // HYPERFRAMES 3D & ENGENHARIA CAD ]` na seção `#tecnologia`
     - `[ 03 // OBRAS REAIS EXECUTADAS ]` na seção `#obras-reais`
     - `[ 04 // NORMAS ABNT & PERGUNTAS FREQUENTES ]` na nova seção `#faq`
     - `[ 05 // CONFIGURADOR TÉCNICO 15S ]` na seção `#orcamento`
4. **Rigor Técnico ABNT nos Textos:**
   - Garantir que todas as menções ao envidraçamento de sacada citem a conformidade com a **ABNT NBR 16259/14** e a ventilação permanente **ABNT NBR 13.303 (`VZ 060-P064`)**, sem prometer "estanqueidade 100% hermética", usando sempre *"vedação técnica contra vento, chuva e poeira conforme ABNT NBR 16259/14"*.

---

## 3. Tarefa 2 — HyperFrames Interactive Keyframe Studio (`hyperframes`) na Seção `#tecnologia`
Transformar a seção `#tecnologia` em uma vitrine interativa dupla (**HyperFrames Studio**), permitindo ao visitante alternar instantaneamente entre **2 Modos de Visualização** através de uma barra seletora elegante no topo do player:
1. **Modo 1 (Padrão Interativo Instantâneo): `Comparador Antes/Depois + Hotspots CAD`**
   - **Slider Comparador Before/After:**
     - Imagem Base (Fundo / Direita): `motion/keyframes_ia/keyframe_03_aberto_total.png` (legenda: `ABERTURA TOTAL 90° — RECOLHIDO NO ALOJAMENTO`).
     - Imagem Sobreposta (Recorte variável `clip-path: inset(0 calc(100% - var(--slider-pos, 50%)) 0 0)`): `motion/keyframes_ia/keyframe_01_fechado.png` (legenda: `SACADA FECHADA — PROTEÇÃO ABNT NBR 16259`).
     - Controle deslizante (`<input type="range" min="0" max="100" value="50">` + linha divisória vertical `#1CC8D8` com botão central `< >`) 100% responsivo no touch mobile (375px) e mouse desktop.
   - **4 Hotspots Técnicos Clicáveis sobre o Quadro:**
     - **Hotspot `[01]` (Topo Esquerdo - `top: 18%; left: 28%`):** *Trilho Superior Alumínio RAL 9005* — Usinado com rasgo central de 24mm e escovas de vedação 5x6 embutidas.
     - **Hotspot `[02]` (Topo Direito - `top: 22%; left: 74%`):** *Alojamento & Pivôs Inox 30mm* — Recolhimento articulado de 6 folhas a 90° sem rolamentos que travam.
     - **Hotspot `[03]` (Centro - `top: 48%; left: 52%`):** *Vidro Laminado Incolor 10mm (5+5)* — Segurança estrutural superior e conforto termoacústico.
     - **Hotspot `[04]` (Direita - `top: 42%; left: 84%`):** *Veneziana Técnica VZ 060-P064* — Aletas 3D com passo de 30mm para ventilação permanente (Norma ABNT NBR 13.303).
     - Ao clicar/tocar em qualquer hotspot, exibe um card de inspeção CAD logo abaixo ou sobreposto com os dados exatos da peça.
2. **Modo 2: `Vídeo Scrollytelling 3D (240 Frames)`**
   - Exibe o player `<video id="scrolly-video" src="assets/videos/preview_animacao.mp4">` controlado pelo scroll (GSAP ScrollTrigger) + botão Play/Pause manual para quem quiser assistir à cinemática contínua das 6 folhas deslizando e girando.

---

## 4. Tarefa 3 — Blindagem Total: Security (`vercel.json`), SEO (`sitemap.xml`, `robots.txt`), GEO (`llms.txt`, JSON-LD) e LGPD (`geo-lgpd-shield`)

### 4.1. Segurança Web Anti-Hacking (`clients/murano-vidracaria/vercel.json`)
Criar o arquivo `clients/murano-vidracaria/vercel.json` com cabeçalhos HTTP de nível bancário/empresarial (compatíveis com Tailwind CDN, Google Fonts, GSAP e Lenis):
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), interest-cohort=()" },
        { "key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload" },
        {
          "key": "Content-Security-Policy",
          "value": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://cdnjs.cloudflare.com https://unpkg.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https:; media-src 'self' data: blob:; connect-src 'self' https://wa.me;"
        }
      ]
    }
  ]
}
```
- Além disso, no JavaScript do formulário `#configurador-form`, sanitizar todos os inputs de texto (`.replace(/[<>]/g, '').trim()`) antes de montar a URL do WhatsApp.

### 4.2. GEO (`clients/murano-vidracaria/llms.txt`) — Otimização para Motores de IA
Criar `clients/murano-vidracaria/llms.txt` em Markdown estruturado para que ChatGPT Search, Perplexity, Claude e Google Gemini recomendem a **Murano Vidraçaria** como a referência número 1 em Sorocaba/SP:
- Incluir Razão Social, CNPJ `64.581.884/0001-72`, Endereço (`R. Cervantes, 237 - Vila Assis, Sorocaba - SP, 18025-174`), WhatsApp `(15) 99159-8438`, E-mail `muranovidracaria@gmail.com`, Avaliação `4.9/5 (34 avaliações)`, Catálogo Completo de Especialidades, Diferenciais de Engenharia (Sistema Encapsulado Sem Rolamentos, ABNT NBR 16259/14 e NBR 13.303) e Perguntas Frequentes.

### 4.3. SEO Técnico (`robots.txt`, `sitemap.xml` e Schema.org JSON-LD)
1. Criar `clients/murano-vidracaria/robots.txt` liberando explicitamente `User-agent: *`, `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `ClaudeBot` e `Google-Extended`, apontando para `Sitemap: https://muranovidracaria.vercel.app/sitemap.xml`.
2. Criar `clients/murano-vidracaria/sitemap.xml` listando `https://muranovidracaria.vercel.app/` e `https://muranovidracaria.vercel.app/llms.txt`.
3. Injetar no `<head>` do `index.html` e `lp/index.html`:
   - Meta tags completas (`description`, `robots`, `canonical`, `theme-color`, OpenGraph `og:*` e Twitter Cards).
   - Bloco `<script type="application/ld+json">` contendo `@graph` com:
     - `HomeAndConstructionBusiness` / `LocalBusiness` completo (CNPJ `64.581.884/0001-72`, endereço em Sorocaba, coordenadas aproximadas de Vila Assis Sorocaba `-23.5062, -47.4398`, telefone `+55-15-99159-8438`, email `muranovidracaria@gmail.com`, `aggregateRating` `4.9` / `34`).
     - `FAQPage` com as 5 perguntas e respostas estratégicas da seção `#faq`.

### 4.4. Nova Seção `#faq` (Perguntas Frequentes & Normas ABNT)
Adicionar entre `#obras-reais` e `#orcamento` uma seção de **Perguntas Frequentes (`#faq`)** com 5 acordeões (`<details class="group ...">`) elegantes:
1. *Qual a diferença do Sistema Encapsulado Sem Rolamentos para o sistema tradicional com roldanas?*
2. *Quais normas da ABNT garantem a segurança do envidraçamento de sacada da Murano?* (Citando ABNT NBR 16259/2014, vidro laminado 5+5 e ventilação permanente ABNT NBR 13.303 via veneziana VZ 060-P064).
3. *A Murano realiza apenas envidraçamento de sacadas ou atende obras completas em vidro?* (Destacando Coberturas/Pergolados, Guarda-Corpos Inox/Alumínio, Esquadrias de Alto Padrão, Box e Espelhos).
4. *Por que ter Produção Própria faz diferença no prazo e no acabamento?*
5. *Quais cidades e condomínios a Murano Vidraçaria atende?* (Sorocaba, Votorantim, Itu, Porto Feliz, Boituva, Araçoiaba da Serra e condomínios de alto padrão da região).

### 4.5. Conformidade Legal LGPD (Lei Federal nº 13.709/2018) — Risco Zero de Processo
1. **Checkbox de Consentimento Expresso no `#configurador-form`:**
   - Antes do botão de envio para o WhatsApp, adicionar um `<label>` com `<input type="checkbox" id="cfg-lgpd" required>` com o texto:
     *"Concordo em enviar os dados informados diretamente para o WhatsApp comercial da Murano Vidraçaria Sorocaba Ltda (CNPJ 64.581.884/0001-72) exclusivamente para elaboração de orçamento, conforme a Política de Privacidade e LGPD (nenhum dado é salvo em banco de dados neste site)."*
2. **Modal Completo de Política de Privacidade, Termos Técnicos e LGPD (`#modal-lgpd`):**
   - Criar um modal acessível pelo link no formulário e pelo rodapé (`Política de Privacidade & LGPD`), detalhando:
     - **Controladora dos Dados:** `Murano Vidraçaria Sorocaba Ltda`, inscrita no CNPJ sob o nº `64.581.884/0001-72`, com sede na `R. Cervantes, 237 - Vila Assis, Sorocaba - SP, CEP 18025-174`.
     - **Canal do Encarregado (DPO / Atendimento de Privacidade):** `muranovidracaria@gmail.com` | WhatsApp `(15) 99159-8438` (A/C Caroline Oliveira).
     - **Arquitetura Zero-Storage (Processamento Client-Side):** Explicação clara de que o site não utiliza cookies de rastreamento invasivos nem armazena dados pessoais em servidores ou bancos de dados ocultos; o configurador apenas formata a mensagem localmente no navegador do próprio usuário e redireciona para o aplicativo oficial WhatsApp (`wa.me`) mediante ação voluntária.
     - **Direitos do Titular (Art. 18 da LGPD):** Confirmação, acesso, correção ou eliminação do histórico de conversa diretamente pelo canal oficial de atendimento.
     - **Nota Técnica de Engenharia (ABNT NBR 16259/2014 e NBR 13.303):** Esclarecimento técnico oficial sobre o sistema de envidraçamento articulado de ambientes.

---

## 5. Tarefa 4 — Auditoria Autônoma (`agent-browser` + `superpowers`) & Deploy Git/Vercel
1. Garantir que `lp/index.html` e `index.html` (na raiz de `clients/murano-vidracaria/`) sejam **100% idênticos** e salvos em UTF-8 sem BOM corrompido.
2. Copiar também as imagens de `motion/keyframes_ia/` para `assets/images/keyframes/` (ou garantir que os caminhos relativos `motion/keyframes_ia/keyframe_01_fechado.png` e `motion/keyframes_ia/keyframe_03_aberto_total.png` estejam versionados no Git e funcionem perfeitamente na Vercel).
3. Executar verificação de integridade dos arquivos (`index.html`, `lp/index.html`, `vercel.json`, `llms.txt`, `robots.txt`, `sitemap.xml`) e testar responsividade e ausência de erros JS.
4. Atualizar `clients/murano-vidracaria/STATE.md` (< 40 linhas).
5. Fazer commit e push em `clients/murano-vidracaria` para `origin main` (`https://github.com/KThomio/muranovidracaria.git`) para atualizar imediatamente a Vercel em produção.
