---
name: frontend
description: Modern, lean frontend practices using HTML, CSS, and vanilla JS.
---

# Skill: Frontend Development Moderno e Enxuto

## 1. VisÃ£o Geral
Esta skill orienta o desenvolvimento de cÃ³digo frontend rÃ¡pido, acessÃ­vel, sustentÃ¡vel e sem complexidade desnecessÃ¡ria. A filosofia central Ã© **aproveitar as capacidades nativas do navegador moderno antes de recorrer a bibliotecas externas**.

---

## 2. PrincÃ­pios de Arquitetura Frontend
- **Zero DependÃªncias Sem Justificativa:** NÃ£o instale pacotes npm, jQuery, frameworks ou bundlers pesados para sites institucionais ou landing pages. HTML5, CSS moderno e Vanilla JS resolvem com perfeiÃ§Ã£o 95% dos projetos de clientes.
- **Respeito Ã  Plataforma:** Use APIs nativas do navegador (`IntersectionObserver`, `fetch`, `CSS Custom Properties`, `dialog`, `<details>/<summary>`).
- **Performance como PadrÃ£o:** Carregamento instantÃ¢neo, peso de pÃ¡gina mÃ­nimo e Core Web Vitals impecÃ¡veis (LCP < 2.0s, INP < 200ms, CLS < 0.1).

---

## 3. HTML SemÃ¢ntico & Acessibilidade
1. **Estrutura de Documento:**
   - Use tags com significado semÃ¢ntico: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`.
   - BotÃµes sÃ£o `<button type="button|submit">`, links de navegaÃ§Ã£o sÃ£o `<a href="...">`. Nunca transforme `<div>` ou `<span>` em botÃµes clicÃ¡veis sem tratamento a11y completo.
2. **FormulÃ¡rios AcessÃ­veis:**
   - Todo input deve ter um `<label for="...">` associado.
   - Utilize tipos adequados (`type="email"`, `type="tel"`, `type="url"`) e atributos Ãºteis (`autocomplete`, `required`, `pattern`, `inputmode="numeric"` para telefones).
3. **MÃ­dia e Assets:**
   - Imagens devem sempre incluir atributos explÃ­citos `width` e `height` para evitar Layout Shift (CLS).
   - Use `loading="lazy"` para imagens fora da viewport inicial.
   - ForneÃ§a textos alternativos (`alt`) descritivos para imagens informativas e `alt=""` para decorativas.

---

## 4. CSS Moderno, Modular e SustentÃ¡vel
1. **Design Tokens com VariÃ¡veis CSS:**
   Centralize variÃ¡veis no `:root`:
   ```css
   :root {
     --color-primary: #0f172a;
     --color-accent: #2563eb;
     --color-bg: #ffffff;
     --color-text: #334155;
     --font-heading: 'Inter', -apple-system, sans-serif;
     --space-md: 1.5rem;
     --radius-md: 0.5rem;
     --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
   }
   ```
2. **Layout com Flexbox e Grid:**
   - Evite floats ou hacks legados. Use CSS Grid para matrizes e Flexbox para fluxos unidirecionais.
3. **Responsividade Fluida:**
   - Use unidades relativas (`rem`, `ch`, `%`, `clamp()`) para tipografia e espaÃ§amentos adaptÃ¡veis.
   - Defina breakpoints padrÃ£o coerentes:
     - Mobile: base
     - Tablet: `@media (min-width: 768px)`
     - Desktop: `@media (min-width: 1024px)`
     - Wide: `@media (min-width: 1280px)`
4. **Sem Overflow Horizontal:**
   - Adicione `box-sizing: border-box` universal.
   - Evite larguras estÃ¡ticas fixas (`width: 500px`) sem `max-width: 100%`.

---

## 5. JavaScript Enxuto (Vanilla JS)
1. **Apenas Quando NecessÃ¡rio:**
   - Se uma animaÃ§Ã£o, dropdown simples ou accordion puder ser feito com CSS puro ou HTML `<details>`, prefira essa soluÃ§Ã£o.
2. **PadrÃµes de Escrita:**
   - Use escopo local (funÃ§Ãµes modulares ou IIFE) para evitar poluiÃ§Ã£o do objeto `window`.
   - Adicione scripts com atributo `defer` no final da tag `<head>` ou antes do fechamento de `</body>`.
   - Delegue eventos no container comum sempre que houver mÃºltiplos itens repetitivos.
3. **Exemplo de Script Enxuto (Menu Mobile & Smooth Scroll):**
   ```javascript
   document.addEventListener('DOMContentLoaded', () => {
     const navToggle = document.querySelector('[data-nav-toggle]');
     const navMenu = document.querySelector('[data-nav-menu]');

     if (navToggle && navMenu) {
       navToggle.addEventListener('click', () => {
         const isOpen = navMenu.classList.toggle('is-open');
         navToggle.setAttribute('aria-expanded', isOpen);
       });
     }
   });
   ```

