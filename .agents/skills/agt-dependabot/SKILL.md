---
name: agt-dependabot
description: Use when o usuário pedir para revisar, triar, corrigir ou mergear alertas e pull requests do Dependabot no repositório supercalc.
---

# Agt Dependabot

## Visão geral

Triar e resolver os alertas de segurança do Dependabot em `lucasgamadev/supercalc` sem quebrar a `main`.
O fluxo usa `gh` para o GitHub e `npm` para a correção local. Descobrir alertas e PRs dinamicamente; nunca manter lista fixa.

## Contexto fixo do repositório

| Fato | Consequência |
| --- | --- |
| Site estático (HTML/CSS/JS); npm só tem `devDependencies` (Tailwind, ESLint, Prettier) | Vulnerabilidade não atinge o usuário final em produção, mas deve ser corrigida mesmo assim |
| Sem `.github/dependabot.yml` e sem workflow de CI | Não há CI para validar PR: o portão é a validação local (`build`, `lint`, testes Python) |
| Validação local: `npm run build`, `npm run lint`, `tests/run_all_tests.py` (ou `run_tests.cmd`) | Rodar os três após qualquer correção no lock |
| Alertas típicos são de dependências transitivas (`js-yaml`, `brace-expansion`, `smol-toml`, `browserslist`) | Costumam se resolver com `npm audit fix`, sem bump manual |
| `package.json` tem `overrides` (`glob`) | Override pode segurar pacote transitivo; conferir antes de bump manual |

## Contrato

- Nunca commitar nem dar push sem aprovação explícita do usuário (`ok`, `sim`, `aprovar`).
- Mensagens de commit em pt-BR, formato `<prefixo>: <descrição>` (ex.: `chore: corrige vulnerabilidades do npm audit`).
- Nunca editar `package-lock.json` à mão; usar `npm audit fix` ou `npm install <pacote>@<versao>`.
- Merge de PR do bot: um por vez, com prévia e aprovação antes.
- Bump `major`: ler as release notes antes de propor.
- Ao encerrar, avaliar a própria skill e absorver as lacunas da rodada (passo 6).

## Execução

### 1. Levantar alertas e PRs

```bash
gh api repos/lucasgamadev/supercalc/dependabot/alerts?state=open --jq '.[]|"#\(.number) \(.security_advisory.severity) \(.dependency.package.name) patched=\(.security_vulnerability.first_patched_version.identifier)"'
gh pr list --json number,title,author --jq '.[]|"#\(.number) \(.author.login) \(.title)"'
```

Conferir também a visão local, que mostra a cadeia transitiva e o caminho da correção:

```bash
npm audit
```

Alerta sem PR aberto é comum aqui: sem `dependabot.yml`, o bot alerta mas nem sempre abre PR. Verificar se as correções automáticas estão ligadas:

```bash
gh api repos/lucasgamadev/supercalc/automated-security-fixes --jq '"\(.enabled) \(.paused)"'
```

Se estiver desligado, propor ao usuário ativar pela interface do GitHub (Settings > Advanced Security) ou criar `.github/dependabot.yml`. Não criar o arquivo sem pedido explícito.

### 2. Classificar risco

| Classe | Exemplo | Ação |
| --- | --- | --- |
| Transitiva de dev, fix sem bump major | `js-yaml`, `brace-expansion` | `npm audit fix` direto |
| Dev dependency direta, patch/minor | `eslint`, `tailwindcss` | `npm audit fix` ou `npm install <pkg>@latest -D` |
| Major | `eslint` 9 para 10 | Ler release notes e propor com ressalvas |
| Fix que exige mudar `overrides` | `glob` | Expor na prévia; override existe por algum motivo |

Release notes embutidas no PR do bot:

```bash
gh pr view <numero> --json body --jq .body | head -40
```

### 3. Prévia e aprovação

Antes de qualquer alteração, exibir:

```markdown
## 📋 Prévia da rodada Dependabot

| # | Pacote | Severidade | Correção | Risco |
| --- | --- | --- | --- | --- |
| 1 | js-yaml | high | 4.1.1 (audit fix) | baixo |

Plano: npm audit fix → validar → commit `chore: ...`

✅ Aprovar? `ok`, `sim` ou `cancelar`.
```

### 4. Corrigir localmente

Caminho preferido, sem PR do bot:

```bash
npm audit fix
```

O `audit fix` pode deixar pacote para trás mesmo dizendo "fix available": em 2026-01 ele não subiu o `js-yaml` do `@eslint/eslintrc`. Nesse caso, rodar `npm audit` de novo e completar com `npm update <pacote>`, que sobe a transitiva dentro do range declarado pelo pai sem mexer no `package.json`.

Se restarem alertas por exigir bump quebrável, expor o `--force` na prévia em vez de rodar direto: `npm audit fix --force` faz bump major e pode quebrar a toolchain de lint/build.

Conferir o diff do `package.json`: `npm audit fix` não deve alterar versões declaradas; se alterou, revisar antes de seguir.

### 5. Validar

Os três portões, sempre com o lock novo:

```bash
npm run build
npm run lint
python tests/run_all_tests.py
```

Falha em qualquer um: investigar se veio do fix; se não veio, reportar a linha decisiva e parar. Não commitar com portão vermelho sem aval explícito.

Se houver PR do bot em vez de correção local: mergear um por vez com
`gh pr merge <numero> --squash --delete-branch`, depois `git pull --ff-only` e rodar os mesmos três portões localmente.

### 6. Fechamento e auto-avaliação

1. Reconferir os alertas abertos: a contagem caindo é a prova da rodada.
2. Apresentar o resultado e aguardar aprovação para o commit; push só se pedido.
3. Comparar o roteiro com o que a rodada exigiu de fato:
   - regra que não pôde ser cumprida como escrita;
   - passo que faltou ou leu o dado errado.
   Sem lacuna, declarar `Nenhuma lacuna nesta rodada`. Com lacuna, editar esta skill de forma cirúrgica.

## Referência rápida

| Situação | Ação |
| --- | --- |
| Alerta sem PR | `npm audit fix` local; normal neste repo (sem `dependabot.yml`) |
| `npm audit fix` não resolve tudo | Expor o restante e o custo do `--force` na prévia |
| Fix exige mexer em `overrides` | Parar e expor; override é deliberado |
| PR do bot aberto | Mergear um por vez com prévia, validar local depois |
| Major bump | Ler release notes antes de propor |
| Portão local vermelho sem relação com o fix | Reportar e parar; não culpar o bump sem evidência |
| Zero alerta e zero PR | Rodar `npm outdated` e relatar o atraso; não presumir bot travado |

## Erros comuns

- Rodar `npm audit fix --force` sem prévia: faz bump major silencioso na toolchain.
- Editar `package-lock.json` à mão: desincroniza com o `package.json`.
- Commitar sem aprovação explícita.
- Declarar "0 vulnerabilidades" olhando só o `npm audit`: reconferir os alertas no GitHub, que são a fonte oficial da rodada.
- Presumir que o Dependabot abre PR aqui: sem `dependabot.yml`, o normal é alerta sem PR.
- Tratar vulnerabilidade de dev dependency como urgência de produção: o site é estático; o risco real é na máquina de desenvolvimento e na cadeia de build.
