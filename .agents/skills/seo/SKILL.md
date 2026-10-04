---
name: seo
description: Technical SEO, meta tags, schema, and sitemap configuration.
---

# Skill: SEO TÃ©cnico e OtimizaÃ§Ã£o OrgÃ¢nica

## 1. VisÃ£o Geral
Esta skill aborda a implementaÃ§Ã£o dos fundamentos essenciais de Search Engine Optimization (SEO) tÃ©cnico e on-page. O foco Ã© garantir que o site seja perfeitamente rastreado, indexado e compreendido pelos motores de busca (Google, Bing), alÃ©m de gerar snippets atraentes e com alta taxa de cliques (CTR) nos compartilhamentos sociais.

---

## 2. Meta Tags Essenciais no `<head>`
Todo projeto web para cliente deve conter a estrutura canÃ´nica completa:

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- SEO BÃ¡sico -->
  <title>Nome da Marca | Proposta de Valor Principal e Cidade/Nicho</title>
  <meta name="description" content="DescriÃ§Ã£o clara de atÃ© 155 caracteres com benefÃ­cio direto, chamada para aÃ§Ã£o e palavra-chave do negÃ³cio.">
  <link rel="canonical" href="https://www.exemplo.com.br/">
  <meta name="robots" content="index, follow">

  <!-- Favicons e Ãcones -->
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">

  <!-- Open Graph / Redes Sociais (WhatsApp, Facebook, LinkedIn) -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.exemplo.com.br/">
  <meta property="og:title" content="TÃ­tulo Atrativo para Compartilhamento">
  <meta property="og:description" content="Resumo objetivo que estimula o clique ao ser compartilhado no WhatsApp.">
  <meta property="og:image" content="https://www.exemplo.com.br/assets/og-image.jpg">
  <meta property="og:locale" content="pt_BR">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="TÃ­tulo Atrativo para Compartilhamento">
  <meta name="twitter:description" content="Resumo objetivo para o Twitter/X.">
  <meta name="twitter:image" content="https://www.exemplo.com.br/assets/og-image.jpg">
</head>
```

---

## 3. Estrutura SemÃ¢ntica e Hierarquia de CabeÃ§alhos (Headings)
- **Regra de Ouro do `<h1>`:** Exatamente **um Ãºnico `<h1>` por pÃ¡gina**, localizado na seÃ§Ã£o Hero, resumindo o serviÃ§o e a localidade/pÃºblico.
- **Hierarquia Linear:** Nunca pular nÃ­veis (`<h1>` seguido de `<h3>` Ã© proibido; sempre use `<h2>` antes de `<h3>`).
- **TÃ­tulos Orientados a BenefÃ­cio e Busca:** Combine termos pesquisados por clientes reais com a soluÃ§Ã£o oferecida.

---

## 4. OtimizaÃ§Ã£o de Assets e Imagens
1. **Atributos `alt` Contextuais:**
   - Descreva o que a imagem retrata incluindo contexto do negÃ³cio (ex: `alt="Dra. Mariana atendendo paciente em consultÃ³rio odontolÃ³gico em Pinheiros"`).
   - Imagens puramente decorativas (formas, linhas, fundos abstratos) devem ter `alt=""` ou ser aplicadas via CSS.
2. **Nomes de Arquivo AmigÃ¡veis:**
   - Evite `IMG_20261001_9823.jpg`. Use `servico-limpeza-industrial-sao-paulo.webp`.

---

## 5. Arquivos de Controle: `robots.txt` e `sitemap.xml`
1. **`robots.txt` PadrÃ£o:**
   ```text
   User-agent: *
   Allow: /

   Sitemap: https://www.exemplo.com.br/sitemap.xml
   ```
2. **`sitemap.xml` Enxuto:**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
     <url>
       <loc>https://www.exemplo.com.br/</loc>
       <lastmod>2026-10-01</lastmod>
       <changefreq>monthly</changefreq>
       <priority>1.0</priority>
     </url>
   </urlset>
   ```

---

## 6. Dados Estruturados (Schema.org / JSON-LD)
Para empresas locais ou prestadores de serviÃ§os, inclua dados estruturados em JSON-LD no rodapÃ© do documento:
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Nome da Empresa",
  "image": "https://www.exemplo.com.br/assets/logo.jpg",
  "telephone": "+55-11-99999-9999",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Rua Exemplo, 123",
    "addressLocality": "SÃ£o Paulo",
    "addressRegion": "SP",
    "postalCode": "01234-567",
    "addressCountry": "BR"
  },
  "url": "https://www.exemplo.com.br"
}
</script>
```

