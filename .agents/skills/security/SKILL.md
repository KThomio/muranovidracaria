---
name: security
description: Web security, preventing XSS, managing secrets, and HTTPS.
---

# Skill: SeguranÃ§a Web e ProteÃ§Ã£o de Dados

## 1. VisÃ£o Geral
Esta skill estabelece diretrizes de seguranÃ§a defensiva e integridade tÃ©cnica para projetos web desenvolvidos pela AI Agency. Sites profissionais para clientes nÃ£o podem expor credenciais, ser vulnerÃ¡veis a ataques triviais ou vazar dados confidenciais de visitantes.

---

## 2. GestÃ£o de Segredos e API Keys
- **Nenhum Segredo no Frontend PÃºblico:** Chaves privadas de API, tokens de acesso, credenciais de banco de dados ou webhooks confidenciais **NUNCA** devem constar no cÃ³digo HTML, JS ou em repositÃ³rios Git pÃºblicos.
- **FormulÃ¡rios Sem Backend PrÃ³prio:** Ao usar serviÃ§os de envio de formulÃ¡rios (Formspree, Web3Forms, Resend), utilize apenas chaves pÃºblicas destinadas para client-side, com domÃ­nio estritamente restrito nas configuraÃ§Ãµes do serviÃ§o.
- **Git Ignore Proativo:** Assegurar que arquivos sensÃ­veis (`.env`, `.env.local`, chaves `.pem`, senhas de teste) estejam explicitamente no `.gitignore`.

---

## 3. PrevenÃ§Ã£o de XSS (Cross-Site Scripting) & InjeÃ§Ã£o
- **ManipulaÃ§Ã£o Segura do DOM:**
  - Prefira sempre `element.textContent` ou `element.innerText` em vez de `element.innerHTML` ao exibir dados fornecidos pelo usuÃ¡rio.
  - Se for estritamente necessÃ¡rio renderizar HTML dinÃ¢mico vindo de fontes externas, utilize sanitizaÃ§Ã£o rigorosa.
- **ValidaÃ§Ã£o e SanitizaÃ§Ã£o de Entradas:**
  - Todo campo de formulÃ¡rio deve ter validaÃ§Ã£o dupla (validaÃ§Ã£o nativa no browser via HTML5 e tratamento de strings no endpoint de envio).

---

## 4. HTTPS, Mixed Content e Links Externos
1. **HTTPS ObrigatÃ³rio:**
   - Todo site em produÃ§Ã£o deve rodar sob protocolo HTTPS com certificado SSL vÃ¡lido (Cloudflare, Vercel, Netlify ou GitHub Pages fornecem gratuitamente).
2. **EliminaÃ§Ã£o de Mixed Content:**
   - Todos os scripts, folhas de estilo, fontes e imagens externos devem ser carregados via protocolo seguro (`https://`). Nunca referencie recursos via `http://`.
3. **Links Externos Seguros:**
   - Para todo link com `target="_blank"`, adicione obrigatoriamente `rel="noopener noreferrer"`.
   - Isso impede o ataque de *Tabnabbing* (onde a nova aba aberta tem acesso a manipular a pÃ¡gina de origem via `window.opener`).

---

## 5. CabeÃ§alhos de SeguranÃ§a (Security Headers)
Ao configurar o servidor ou arquivo de roteamento da CDN (`_headers`, `vercel.json` ou `netlify.toml`), implemente:
```http
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:;
```

---

## 6. Privacidade e ExposiÃ§Ã£o de Dados
- **LGPD / ProteÃ§Ã£o de Dados:** FormulÃ¡rios devem conter termo de consentimento claro de que os dados serÃ£o utilizados estritamente para contato comercial.
- **Sem Dados SensÃ­veis em URLs:** Nunca passe dados pessoais (telefones, e-mails, senhas) em query strings de URL (`GET`). Utilize requisiÃ§Ãµes `POST` no corpo da requisiÃ§Ã£o.

