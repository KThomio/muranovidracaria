# Contexto Técnico e Documental - Sacada Murano (Pipeline 3D / VFX)

Este arquivo é a fonte de verdade técnica do sistema de envidraçamento da Sacada Murano. O seu objetivo é prescrever a modelagem 3D, rigging e animação (VFX), delimitando estritamente o que é conhecimento documentado, matemática derivada, e o que é hipótese não comprovada.

---

## 1. CONTEXTO DO PROJETO
- **Projeto:** Sacada Murano — sistema de envidraçamento para a Vidraçaria Murano.
- **Local de referência:** Condomínio Parque Vida (Estrada do Luiz Fernando Andrade Pannunzio, Vila Rica — Sorocaba/SP).
- **Sistema:** Kit Sacada Sem Rolamento — AL Indústria.
- **Conceito Mecânico:** Slide & Turn (Deslize e Giro).
- **Objetivo Final:** Visualização técnica/VFX convincente do sistema. Utilizaremos fotografia real da sacada como backplate, reconstruindo no Blender 3D apenas os perfis, trilhos, folhas de vidro, veneziana fixa e cinemática de abertura (sem reconstruir a arquitetura envolvente da sacada).

### Componentes Identificados
- Perfil Ancoragem
- Perfil Trilho S (Superior) e Perfil Trilho I (Inferior)
- Perfil Leito
- Discos/elementos de segurança e Pivôs de estacionamento
- Componentes POM e Buchas de latão
- Escovas 5x6
- Veneziana VZ 060-P064

---

## 2. TABELA DE PARÂMETROS E CLASSIFICAÇÃO

### 2.1. Dados Documentados (Oficiais)
Informações retiradas diretamente do manual técnico (`manual-kit-sacada.pdf`), plantas e catálogos:
- **VÃO_LARGURA:** 1900 mm
- **VÃO_ALTURA:** 860 mm
- **VENEZIANA_LARGURA:** 150 mm
- **QUANTIDADE_FOLHAS_MÓVEIS:** 4
- **ESPESSURA_VIDRO:** 10 mm (Laminado 5+5)
- **FOLGA_LATERAL_TOTAL:** 30 mm (15 mm de cada lado)
- **FOLGA_POR_JUNCAO:** 3 mm (+3 mm de dilatação/folga entre os perfis leito/vidros)
- **DISTANCIA_EIXOS:** 30 mm (A distância centro-a-centro entre os eixos de rotação no momento do empilhamento/estacionamento).
- **OFFSET_PIVO_X:** 30 mm. (Conforme "Página 4 - DISTÂNCIA DO DISCO DE SEGURANÇA (ALOJAMENTO)", a cota de 30mm marca a distância exata da borda do perfil até o centro do primeiro disco/pivô).

### 2.2. Dados Derivados (Matemáticos)
- **ALTURA_VIDRO:** 660 mm. A regra documental dita `VÃO_MENOR - 200 mm`. Logo, 860 - 200 = 660 mm.
- **LARGURA_FOLHA:** 427,75 mm. Cálculo: (1900 - 150 - 30 - (3 * 3)) / 4 = 427,75 mm.
- **PARKING_OFFSET:** 30 mm. Uma vez que o pivot fica a 30mm da borda, e a primeira folha encosta no limite do trilho, o primeiro pivot estaciona exatamente a 30mm da origem.
- **OFFSET_PIVO_Y:** Assumido geometricamente como ~5 mm (centro de simetria do vidro de 10 mm). Contudo, é uma hipótese/derivada geométrica.

### 2.3. Hipóteses e Desconhecidos
Parâmetros que **não** constam da documentação e que devem permanecer como variáveis ajustáveis provisórias (`_HIPOTESE`) no código 3D.
- **ALOJAMENTO_LARGURA:** Desconhecido (dimensões da abertura de escape da roldana).
- **ALOJAMENTO_PROFUNDIDADE:** Desconhecido.
- **ALOJAMENTO_OFFSET:** Desconhecido.

---

## 3. CONFLITOS RESOLVIDOS

### 429 mm vs 427,75 mm
- **429 mm:** Referência aproximada encontrada na planta `WhatsApp Image 2026-10-04 at 13.41.26 (1).jpeg`.
- **427,75 mm:** Valor matematicamente derivado a partir das cotas de 1900, 150, 30 e 3×3.
- **Para a pipeline paramétrica atual:** usar **427,75 mm**.

### 710 mm vs 660 mm
- **710 mm:** Valor encontrado na mesma planta de referência.
- **660 mm:** Resultado da regra documental do manual (`VÃO_MENOR - 200 mm`).
- **Para a pipeline atual:** usar **660 mm**.

### A Regra dos 30 mm
Não interpretar como distância livre entre vidros. É a distância **eixo → eixo**.

---

## 4. COMPREENSÃO MECÂNICA E CINEMÁTICA

### 4.1. A Sequência de Movimento (Slide & Turn)
Interpretação para o Script de Animação 3D:
1. Direção: direita → esquerda.
2. Empilhamento: canto esquerdo. A veneziana permanece fixa no lado direito.
3. Ciclo de Folha: folha desliza horizontalmente → chega à região do alojamento → pivô entra no rasgo → rotaciona 90° → empilha.

### 4.2. Restrições do Alojamento
A documentação mostra rasgos para a passagem do articulador. Porém, as dimensões exatas não estão documentadas. Estes parâmetros permanecem ajustáveis e não se deve inventar medidas oficiais. O modelo 3D atual serve para reconstrução paramétrica + VFX, e não como projeto executivo de usinagem.

---

## REGRAS PARA AGENTES FUTUROS

Todo o trabalho futuro de agentes robóticos ou programadores sobre o script `build_sacada.py` está condicionado às seguintes diretrizes:

1. Nunca alterar valores documentados sem justificativa explícita.
2. Nunca transformar hipótese em fato.
3. Toda nova medida deve ser classificada como DOCUMENTADA, DERIVADA ou HIPÓTESE.
4. Quando houver conflito entre referências, não escolher silenciosamente; registrar o conflito.
5. Não esconder colisões mecânicas simplesmente deslocando peças.
6. Não alterar dimensões oficiais apenas para fazer a animação funcionar.
7. Parâmetros desconhecidos devem permanecer configuráveis.
8. O modelo VFX não deve ser apresentado como projeto executivo.
9. O teste de 30 mm deve medir centro de eixo contra centro de eixo.
10. A origem do pivô deve depender de um parâmetro, nunca de um valor mágico enterrado no código.

