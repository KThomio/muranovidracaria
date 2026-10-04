---
name: workflow-website
description: Executa o ciclo operacional completo da agência (Discovery > Strategy > Build > Review > QA).
---

# Workflow: Website Client

Este workflow automatiza o ciclo de vida de desenvolvimento de um projeto para cliente. Como IA executora, siga rigorosamente os passos abaixo em ordem.

## PASSO 1: DISCOVERY & STRATEGY (Persona: Architect)
1. Ative a regra **architect** (se já não estiver ativa) e revise o briefing fornecido pelo Diretor (usuário).
2. Analise os requisitos, a arquitetura necessária e a stack mais enxuta possível.
3. **AÇÃO OBRIGATÓRIA:** Crie o arquivo `docs/blueprint.md` detalhando o escopo, estrutura de seções, CTAs e as restrições técnicas.
4. **BLOQUEIO DE EXECUÇÃO:** Pare imediatamente após criar o `blueprint.md`. Pergunte ao Diretor: *"O blueprint foi gerado em docs/blueprint.md. Aprova a estratégia para iniciarmos a construção?"* **Não escreva nenhuma linha de código do projeto até receber a confirmação.**

## PASSO 2: BUILD (Persona: Builder)
1. Após a aprovação do Diretor, ative a regra **builder**.
2. Leia atentamente o `docs/blueprint.md`.
3. (Opcional) Ative as skills `frontend` e `web-design` para garantir aderência aos padrões premium.
4. Crie/edite os arquivos HTML, CSS e JS rigorosamente conforme o plano, mantendo a simplicidade e estruturação de pastas da Agency.
5. Ao terminar, informe ao Diretor que a construção base está concluída.

## PASSO 3: REVIEW (Persona: Reviewer)
1. Ative a regra **reviewer**.
2. (Opcional) Ative as skills `seo` e `security`.
3. Audite todo o código gerado no Passo 2 procurando falhas de semântica, contraste, tags fechadas, vazamento de chaves e links não seguros.
4. Se encontrar erros, corrija-os (ou oriente-se a voltar para a persona Builder para corrigir).
5. Gere um sumário das correções aplicadas.

## PASSO 4: QA (Persona: QA)
1. Ative a regra **qa**.
2. Revise os requisitos de usabilidade: limites de viewport, comportamentos de links (target="_blank"), validação de formulários.
3. Informe os resultados finais ao Diretor, garantindo que o console está limpo e não há bugs óbvios.

## PASSO 5: SALES & DEPLOY
1. (Opcional) Puxe a skill `sales-demo` para auxiliar o Diretor em como apresentar o produto final ao cliente.
2. Aguarde instruções para o deploy final do Diretor.
