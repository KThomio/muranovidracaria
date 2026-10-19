# PROTOCOLOS DE COMUNICAÇÃO DA AGÊNCIA (MURANO 3D)

## 1. AUTORIDADE DOS AGENTES (Matriz de Permissões)
O sistema opera baseado na separação de responsabilidades (Separation of Concerns). Subagentes não cruzam escopos:

- **DOCUMENTATION (`doc_auditor`)**: Leitura. Autoridade sobre o documento técnico base e PDFs.
- **RESEARCH (`researcher`)**: Leitura/Busca. Autoridade sobre dados externos, mas submisso à documentação oficial existente do projeto (não substitui parâmetros).
- **GEOMETRY (`geo_auditor`)**: Leitura. Autoridade sobre as abstrações matemáticas, deduções, e validação lógica dos transforms.
- **BUILDER (`blender_builder`)**: Escrita. Autoridade sobre a manipulação do código `blender_pipeline/build_sacada.py` e da API `bpy`.
- **DEBUGGER (`blender_debugger`)**: Escrita*. Autoridade sobre a análise de causa-raiz usando o método de Funil de Diagnóstico. Altera código *somente* para correções precisas.
- **QA (`blender_qa`)**: Leitura. Autoridade objetiva sobre os resultados e execuções no terminal. Reporta PASS/FAIL sem alterar código.
- **VISUAL QA (`visual_qa`)**: Leitura. Autoridade estética. Pode discordar de geometria, mas deve emitir um status de CONFLITO se a métrica técnica foi seguida.
- **ORCHESTRATOR**: Gerente. Decide o avanço de estado. Modifica os arquivos de controle `.agents`.

---

## 2. PROTOCOLO DE EVIDÊNCIAS
Toda nova descoberta extraída (em arquivos, imagens ou na web) precisa usar o formato padrão:

```text
ID: [ex: MURANO-015]
TIPO: [DOCUMENTADO | DERIVADO | HIPOTESE | DESCONHECIDO | CONFLITO]
FONTE: [ex: manual-kit-sacada.pdf (Pag 4)]
LOCAL: [ex: Canto inferior direito]
DADO: [A cota extraída, ex: Distância entre centros = 30mm]
CONFIANÇA: [Alta/Média/Baixa - com motivo]
OBSERVAÇÃO: [Contexto extra útil para o Builder ou Geo]
```

---

## 3. PROTOCOLO DE HANDOFF
Ao finalizar a tarefa e retornar a comunicação ao Orchestrator ou transferir responsabilidade a outro agente, o agente DEVE encerrar sua resposta com o seguinte bloco:

```text
INPUT: [Resumo do que você recebeu para fazer]
DECISIONS: [Principais arquiteturas ou abordagens que você assumiu]
EVIDENCE: [Lista de evidências criadas/usadas usando o formato acima]
UNKNOWN: [O que você descobriu que não tem resposta]
CONFLICTS: [Qualquer colisão encontrada na física ou regra de negócios]
OUTPUT: [A conclusão, log, código ou matriz gerada]
NEXT_ACTION: [Recomendação clara para o próximo agente ou Orchestrator]
```
