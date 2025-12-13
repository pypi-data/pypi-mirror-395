# Protheus Mapper Plugin

Plugin para geração automática de mapeamentos semânticos a partir do dicionário de dados do Protheus TOTVS.

## Visão Geral

Este plugin lê o dicionário de dados nativo do Protheus (tabelas SX2, SX3, SIX) e gera automaticamente mapeamentos semânticos para o SimpliQ MCP Server.

### Componentes

1. **ProtheusDataDictionary** ([dictionary.py](dictionary.py))
   - Lê metadados das tabelas SX2, SX3, SIX
   - Cache inteligente para otimização
   - Suporte a múltiplas empresas

2. **ProtheusSemanticGenerator** ([generator.py](generator.py))
   - Gera mapeamentos semânticos automaticamente
   - Normaliza nomes (remove acentos, caracteres especiais)
   - Mapeia tipos de dados Protheus → SQL
   - Integra inferência automática de relacionamentos

3. **ProtheusRelationshipInferencer** ([inferencer.py](inferencer.py))
   - Infere relacionamentos automaticamente usando convenções Protheus
   - Detecta FKs baseado em padrões (CLIENTE, FORNECE, PRODUTO, etc.)
   - Valida e deduplicata relacionamentos
   - Gera estatísticas de confiança

4. **ProtheusMapperPlugin** ([protheus_mapper.py](protheus_mapper.py))
   - Plugin MCP principal
   - Expõe ferramentas MCP para mapeamento automático
   - Integra dictionary + generator + inferencer

## Ferramentas MCP Disponíveis

### 1. `auto_map_protheus`

Gera mapeamentos semânticos automaticamente, incluindo entidades e relacionamentos.

**O que é gerado:**
- ✅ Mapeamentos de entidades (tabelas)
- ✅ Relacionamentos inferidos automaticamente
- ✅ Validação e deduplicação de relacionamentos
- ✅ Estatísticas de inferência
- ✅ Progress reporting em tempo real (NEW - Fase 5)

**Performance:**
- ⚡ Cache persistente em disco (acelera chamadas subsequentes)
- 📊 Progress reporting com porcentagem e mensagens detalhadas

**Parâmetros:**
```json
{
  "organization_id": "org-id",
  "connection_id": "conn-id",
  "modules": ["SIGAFIN", "SIGAEST"],  // Opcional
  "companies": ["010", "030"],         // Opcional, default: ["010"]
  "dry_run": false                     // Opcional, default: false
}
```

**Exemplo:**
```javascript
auto_map_protheus({
  organization_id: "my-org",
  connection_id: "protheus-conn",
  modules: ["SIGAFIN"],
  dry_run: true  // Preview antes de criar (mostra entidades + relacionamentos)
})
```

### 2. `list_protheus_modules`

Lista módulos Protheus disponíveis para mapeamento.

**Parâmetros:**
```json
{
  "company": "010"  // Opcional
}
```

**Exemplo:**
```javascript
list_protheus_modules({company: "010"})
```

### 3. `preview_protheus_table`

Visualiza como seria o mapeamento de uma tabela específica.

**Parâmetros:**
```json
{
  "table_alias": "SE1",  // Obrigatório
  "company": "010"       // Opcional
}
```

**Exemplo:**
```javascript
preview_protheus_table({
  table_alias: "SE1",
  company: "010"
})
```

### 4. `list_protheus_tables`

Lista tabelas disponíveis no dicionário de dados.

**Parâmetros:**
```json
{
  "module": "SIGAFIN",  // Opcional - filtra por módulo
  "company": "010"      // Opcional
}
```

**Exemplo:**
```javascript
list_protheus_tables({
  module: "SIGAFIN",
  company: "010"
})
```

### 5. `manage_protheus_cache` (NEW - Fase 5)

Gerencia o cache do dicionário de dados Protheus.

**Ações disponíveis:**
- `stats`: Visualizar estatísticas de cache
- `clear`: Limpar cache (memória e/ou disco)
- `cleanup`: Remover entradas expiradas

**Parâmetros:**
```json
{
  "action": "stats",        // Obrigatório: "stats", "clear", "cleanup"
  "clear_persistent": false // Opcional: para ação "clear"
}
```

**Exemplos:**
```javascript
// Ver estatísticas
manage_protheus_cache({action: "stats"})

// Limpar cache em memória
manage_protheus_cache({action: "clear"})

// Limpar cache em memória E disco
manage_protheus_cache({action: "clear", clear_persistent: true})

// Limpar entradas expiradas
manage_protheus_cache({action: "cleanup"})
```

## Módulos Suportados

| Módulo | Descrição | Prefixos |
|--------|-----------|----------|
| SIGAFIN | Financeiro | SE, SA6 |
| SIGAEST | Estoque | SB, SD3 |
| SIGACOM | Compras | SC, SD1, SA2 |
| SIGAFAT | Faturamento | SC5, SC6, SF2, SA1 |
| SIGAGCT | Gestão de Contratos | CN |
| SIGACTB | Contabilidade | CT |
| SIGAATF | Ativo Fixo | SN |
| SIGAPCP | PCP | SC2, SH |

## Fluxo de Uso

### 1. Listar módulos disponíveis
```javascript
list_protheus_modules()
// Retorna: SIGAFIN, SIGAEST, SIGACOM, etc.
```

### 2. Preview de uma tabela específica
```javascript
preview_protheus_table({table_alias: "SE1"})
// Retorna: visualização do mapeamento para SE1
```

### 3. Mapeamento em DRY RUN (preview)
```javascript
auto_map_protheus({
  organization_id: "my-org",
  connection_id: "conn-id",
  modules: ["SIGAFIN"],
  dry_run: true  // Apenas preview
})
// Retorna: quantos mapeamentos seriam criados
```

### 4. Mapeamento definitivo
```javascript
auto_map_protheus({
  organization_id: "my-org",
  connection_id: "conn-id",
  modules: ["SIGAFIN"],
  dry_run: false  // Cria os mapeamentos
})
// Cria: ~25 mapeamentos do módulo SIGAFIN
```

## Normalização de Nomes

O plugin normaliza automaticamente nomes de campos e tabelas:

| Original | Normalizado |
|----------|-------------|
| "Número do Título" | `numero_do_titulo` |
| "Data de Emissão" | `data_de_emissao` |
| "Títulos a Receber" | `titulos_a_receber` |

Regras:
- Remove acentos
- Converte para minúsculas
- Remove caracteres especiais
- Substitui espaços por underscores

## Mapeamento de Tipos

| Tipo Protheus | Tipo SQL |
|---------------|----------|
| C (Character) | string |
| N (Numeric) | number |
| D (Date) | date |
| L (Logical) | boolean |
| M (Memo) | text |

## Inferência de Relacionamentos

O plugin infere automaticamente relacionamentos entre tabelas usando convenções de nomenclatura do Protheus.

### Padrões Conhecidos

O inferencer reconhece os seguintes padrões de FK:

| Padrão | Campo(s) | Tabela Destino | Exemplo |
|--------|----------|----------------|---------|
| CLIENTE | X_CLIENTE + X_LOJA | SA1 (Clientes) | C7_CLIENTE → SA1 |
| FORNECE | X_FORNECE + X_LOJA | SA2 (Fornecedores) | C7_FORNECE → SA2 |
| PRODUTO | X_COD / X_PRODUTO | SB1 (Produtos) | D1_COD → SB1 |
| FILIAL | X_FILIAL | SM0 (Filiais) | E1_FILIAL → SM0 |
| TPCTO | X_TPCTO | CN1 (Tipos de Contrato) | CN9_TPCTO → CN1 |

### Como Funciona

1. **Análise de Colunas**: Para cada entidade, analisa colunas procurando padrões conhecidos
2. **Validação**: Verifica se a tabela destino existe no conjunto de entidades
3. **Construção de JOIN**: Monta condição de JOIN (simples ou composta)
4. **Deduplicação**: Remove relacionamentos duplicados
5. **Estatísticas**: Gera métricas de confiança e padrões encontrados

### Exemplo de Relacionamento Inferido

**Entrada:** Tabela SC7 (Pedidos de Compra) com campo `C7_FORNECE`

**Saída:**
```json
{
  "concept": "pedidos_compra_fornecedor",
  "type": "relationship",
  "from_table": "SC7010",
  "from_alias": "SC7",
  "to_table": "SA2010",
  "to_alias": "SA2",
  "join_condition": "SC7.C7_FORNECE = SA2.A2_COD AND SC7.C7_LOJA = SA2.A2_LOJA",
  "relationship_type": "many-to-one",
  "description": "Pedidos de Compra → Fornecedor",
  "metadata": {
    "source": "protheus_inference",
    "pattern": "FORNECE",
    "confidence": "high",
    "inferred_from": "C7_FORNECE"
  }
}
```

### Estatísticas de Inferência

Após a geração, o sistema fornece estatísticas:

```json
{
  "total": 15,
  "by_pattern": {
    "FORNECE": 5,
    "CLIENTE": 3,
    "PRODUTO": 7
  },
  "by_confidence": {
    "high": 12,
    "medium": 3
  },
  "by_type": {
    "many-to-one": 15
  }
}
```

### Limitações

- Apenas padrões conhecidos são detectados
- FKs com nomes não convencionais não são inferidos
- Recomenda-se revisão manual dos relacionamentos gerados
- Use `dry_run: true` para preview antes de criar

## Sistema de Cache (NEW - Fase 5)

O plugin implementa um sistema de cache de dois níveis para otimizar performance:

### Cache em Memória (L1)
- **Velocidade:** Extremamente rápido
- **Escopo:** Sessão atual
- **Uso:** Consultas repetidas na mesma execução

### Cache Persistente (L2)
- **Velocidade:** Rápido (leitura de disco)
- **Escopo:** Persiste entre reinicializações
- **Localização:** `.cache/protheus/`
- **TTL:** 24 horas (configurável)
- **Formato:** Arquivos `.pkl` (pickle)

### Gerenciamento de Cache

Use a ferramenta `manage_protheus_cache` para:

```javascript
// Ver estatísticas de cache
manage_protheus_cache({action: "stats"})
// Output: tamanho do cache, entradas válidas/expiradas, localização

// Limpar cache em memória
manage_protheus_cache({action: "clear"})

// Limpar cache completo (memória + disco)
manage_protheus_cache({action: "clear", clear_persistent: true})

// Remover apenas entradas expiradas
manage_protheus_cache({action: "cleanup"})
```

### Performance com Cache

| Operação | Sem Cache | Cache L1 (Memória) | Cache L2 (Disco) |
|----------|-----------|-------------------|------------------|
| get_tables() | ~500ms | ~0.1ms | ~10ms |
| get_columns() | ~300ms | ~0.1ms | ~5ms |
| Mapeamento completo | ~30s | ~5s | ~10s |

## Testes

Execute os testes unitários:

```bash
cd simpliq_server
python -m pytest tests/plugins/test_protheus_mapper.py -v
```

**Cobertura:** 34 testes unitários com mocks de banco de dados

## Estrutura de Arquivos

```
plugins/protheus/
├── __init__.py              # Package exports
├── dictionary.py            # ProtheusDataDictionary
├── generator.py             # ProtheusSemanticGenerator
├── inferencer.py            # ProtheusRelationshipInferencer (NEW - Fase 4)
├── protheus_mapper.py       # ProtheusMapperPlugin (main)
└── README.md                # Esta documentação

tests/plugins/
└── test_protheus_mapper.py  # Unit tests (34 tests)
```

## Metadados Gerados

Cada mapeamento inclui metadados do Protheus:

```json
{
  "concept": "titulos_receber",
  "type": "entity",
  "table": "SE1010",
  "alias": "SE1",
  "columns": {...},
  "metadata": {
    "source": "protheus_dictionary",
    "company": "010",
    "protheus_alias": "SE1",
    "share_mode": "E",
    "primary_key": "E1_FILIAL+E1_PREFIXO+E1_NUM"
  }
}
```

## Limitações e Considerações

### 1. Qualidade dos Mapeamentos
- Mapeamentos gerados automaticamente podem precisar de ajustes
- Recomenda-se usar `dry_run: true` para preview
- Revisão manual de mapeamentos críticos

### 2. Performance
- Cache reduz impacto em leituras repetidas
- Mapeamento de módulos grandes pode demorar
- Considere mapear módulos específicos ao invés de todos

### 3. Relacionamentos
- ✅ **Fase 4 implementada:** Inferência automática de relacionamentos
- Relacionamentos são gerados automaticamente com base em padrões Protheus
- Validação e deduplicação automática
- Estatísticas de confiança disponíveis

## Próximas Fases

- ✅ **Fase 1:** Infraestrutura de plugins (CONCLUÍDA)
- ✅ **Fase 2:** Plugin Protheus Core (CONCLUÍDA)
- ✅ **Fase 3:** Ferramentas MCP (CONCLUÍDA)
- ✅ **Fase 4:** Inferência de relacionamentos (CONCLUÍDA)
- ✅ **Fase 5:** UX/UI enhancements (CONCLUÍDA)
  - Cache persistente implementado
  - Progress reporting em tempo real
  - Gerenciamento de cache via MCP tool
- **Fase 6:** Production readiness (pendente)

## Suporte

Para problemas ou dúvidas:
1. Verifique os logs do servidor MCP
2. Execute testes unitários
3. Consulte [PLUGIN_SYSTEM.md](../../../docs/plugins/PLUGIN_SYSTEM.md)

---

**Autor:** SimpliQ Development Team
**Data:** 2025-11-18
**Versão:** 1.2 (Fase 5 - UX/UI Enhancements)
