# Relatório de Testes — NaSalinha

**Projeto:** NaSalinha (sistema de check-in gamificado)
**Responsável:** Analista de QA (trilha de QA — Comp Júnior)
**Período de execução:** outubro a novembro de 2026
**Versão testada:** branch `main` do repositório original do NaSalinha
**Documentos de base:** [`Requisitos.md`](./Requisitos.md), [`casos-de-teste.md`](./casos-de-teste.md), [`exploracao.md`](./exploracao.md)

---

## 1. Resumo

Foram planejados **25 casos de teste** e foram encontrados durante os testes **3 casos-extra** para as 3 áreas Core do sistema (Autenticação JWT, Check-in por foto e Sistema de pontos).

Dos **25 casos executados**, **6 passaram** e **19 falharam** (24% de aprovação). Foram criados **15 bug reports**, **7 críticos**.

**Conclusão:** o sistema **não está apto para produção**. Qualquer pessoa consegue se cadastrar como administrador, e uma pessoa que não é admin consegue se promover para um, é possível fazer login com uma conta não verificada, e o saldo é inconsistente quando check-ins são excluídos ou rejeitados, e o check-in não passa por verificação administrativa antes de ser aprovado.

---

## 2. Escopo e ambiente

**Em escopo:**

| Área                        | Requisitos                  |
| --------------------------- | --------------------------- |
| Autenticação JWT            | RF-01, RF-02, RF-03, RNF-01 |
| Check-in por foto           | RF-04, RF-05, RF-06, RNF-02 |
| Sistema de pontos e ranking | RF-07, RF-08, RF-09         |

**Ambiente:**

- Execução local com Docker (backend, frontend e PostgreSQL)
- Frontend: http://localhost:3000 | API: http://localhost:5001/api
- Serviços externos: Cloudinary (imagens) e Mailtrap (e-mails)
- SO: Windows 11 | Navegador: Firefox 158 | Docker 29.8.2
- Dados: seed do projeto (admin, lucas, maria e pedro, com a senha `senha123`)

**Ferramentas:** Postman (API), DevTools do navegador (rede e console), logs do Docker, GitHub Issues (bugs) e GitHub Projects (kanban).

---

## 3. Métricas de execução

### 3.1 Visão geral

| Métrica                                 | Quantidade  |
| --------------------------------------- | ----------- |
| Casos planejados                        | 28          |
| Casos executados                        | 25          |
| Pass                                    | 6           |
| Fail                                    | 19          |
| Bloqueados (não executados)             | 3           |
| Taxa de execução                        | 89% (25/28) |
| Taxa de aprovação (sobre os executados) | 24% (6/25)  |

### 3.2 Por área

| Área                  | Planejados | Executados | Pass  | Fail   | Bloqueados |
| --------------------- | ---------- | ---------- | ----- | ------ | ---------- |
| Autenticação JWT      | 8          | 8          | 2     | 6      | 0          |
| Check-in por foto     | 8          | 8          | 2     | 6      | 0          |
| Sistema de pontos     | 6          | 6          | 2     | 4      | 0          |
| Casos extras (ad-hoc) | 3          | 3          | 0     | 3      | 0          |
| Regressão             | 3          | 0          | 0     | 0      | 3          |
| **Total**             | **28**     | **25**     | **6** | **19** | **3**      |

### 3.3 Por tipo de teste

| Tipo                  | Executados       | Pass | Fail |
| --------------------- | ---------------- | ---- | ---- |
| Funcional (interface) | 9                | 2    | 7    |
| API (Postman)         | 16               | 4    | 12   |
| Regressão             | 0 (3 bloqueados) | —    | —    |

### 3.4 Resultado de cada caso

| ID          | Caso                                                            | Tipo      | Situação  | Bug      |
| ----------- | --------------------------------------------------------------- | --------- | --------- | -------- |
| CT-AUTH-01  | Cadastro com código de verificação e conta PENDENTE             | Funcional | Fail      | #31      |
| CT-AUTH-02  | Cadastro pela API com perfil ADMIN                              | API       | Fail      | #38      |
| CT-AUTH-03  | Login de conta não verificada pela interface                    | Funcional | Fail      | #32      |
| CT-AUTH-04  | Login de conta não verificada pela API                          | API       | Fail      | #32      |
| CT-AUTH-05  | MEMBER tentando acessar endpoints de Temporadas                 | API       | Pass      | —        |
| CT-AUTH-06  | Usuário comum alterando o perfil de outro usuário               | API       | Fail      | #41      |
| CT-AUTH-07  | Senha salva com hash no banco                                   | API       | Pass      | —        |
| CT-AUTH-08  | Redefinição de senha                                            | Funcional | Fail      | #37      |
| CT-CHK-01   | Check-in com imagem válida                                      | Funcional | Pass      | —        |
| CT-CHK-02   | Segundo check-in no dia e foto repetida                         | API       | Fail      | #35      |
| CT-CHK-03   | Status inicial do check-in                                      | Funcional | Fail      | #34      |
| CT-CHK-04   | Usuário comum alterando o status de um check-in                 | API       | Pass      | —        |
| CT-CHK-05   | Visualizar check-in de outro usuário                            | API       | Fail      | #33      |
| CT-CHK-06   | Excluir check-in de outro usuário pela interface                | Funcional | Fail      | #33      |
| CT-CHK-07   | Envio de arquivo inválido                                       | API       | Fail      | #39      |
| CT-CHK-08   | Arquivo temporário após falha no envio para a nuvem             | API       | Fail      | #42      |
| CT-PTS-01   | Pontos somados após check-in aprovado                           | Funcional | Pass\*    | —        |
| CT-PTS-02   | Check-in rejeitado não soma pontos                              | API       | Fail      | #40      |
| CT-PTS-03   | Exclusão de check-in pela API                                   | API       | Fail      | #36      |
| CT-PTS-04   | Ranking na tela após exclusão de check-in                       | Funcional | Fail      | #36      |
| CT-PTS-05   | Ordem do ranking                                                | API       | Pass      | —        |
| CT-PTS-06   | Check-ins com intervalo menor que 24 horas                      | Funcional | Fail      | #35      |
| CT-EXTRA-01 | Coleção do Postman diferente das rotas da API                   | API       | Fail      | #43      |
| CT-EXTRA-02 | Usuário comum vendo o perfil de outro usuário                   | API       | Fail      | #44      |
| CT-EXTRA-03 | ADMIN alterando os pontos de um check-in para um valor inválido | API       | Fail      | #45      |
| CT-REG-01   | Autenticação: correção do login sem verificação                 | Regressão | Bloqueado | #31, #32 |
| CT-REG-02   | Check-in: correção do status inicial PENDENTE                   | Regressão | Bloqueado | #34      |
| CT-REG-03   | Pontos: correção da subtração ao excluir check-in               | Regressão | Bloqueado | #36      |

\* **CT-PTS-01:** os pontos foram somados corretamente, mas o passo de aprovação pelo ADMIN não pôde ser executado, porque o check-in já é criado aprovado (bug #34). O caso deve ser reexecutado por completo quando o #34 for corrigido.

---

## 4. Bugs encontrados

### 4.1 Distribuição por severidade

| Severidade | Definição                                 | Quantidade | %        |
| ---------- | ----------------------------------------- | ---------- | -------- |
| Crítica    | Trava o sistema ou compromete a segurança | 7          | 47%      |
| Maior      | Erro de lógica ou de regra de negócio     | 6          | 40%      |
| Menor      | Erro visual, de texto ou de documentação  | 2          | 13%      |
| **Total**  |                                           | **15**     | **100%** |

### 4.2 Lista de bugs

| Issue                                                   | Título                                                                   | Área         | Severidade | Requisito     |
| ------------------------------------------------------- | ------------------------------------------------------------------------ | ------------ | ---------- | ------------- |
| [#31](https://github.com/salfis/nasalinha-qa/issues/31) | Conta é criada ativa, sem código de verificação e sem status PENDENTE    | Autenticação | Crítica    | RF-01         |
| [#32](https://github.com/salfis/nasalinha-qa/issues/32) | Conta não verificada consegue acessar o Dashboard                        | Autenticação | Crítica    | RF-02         |
| [#37](https://github.com/salfis/nasalinha-qa/issues/37) | Redefinição de senha confirma sucesso, mas a senha não é alterada        | Autenticação | Crítica    | RNF-01        |
| [#38](https://github.com/salfis/nasalinha-qa/issues/38) | API aceita `"role": "ADMIN"` no cadastro público                         | Autenticação | Crítica    | RF-03         |
| [#41](https://github.com/salfis/nasalinha-qa/issues/41) | Rota de atualizar usuário não checa permissão de ADMIN                   | Autenticação | Crítica    | RF-03         |
| [#44](https://github.com/salfis/nasalinha-qa/issues/44) | Usuário comum consegue ver o perfil de qualquer usuário pelo ID          | Autenticação | Crítica    | RF-03         |
| [#33](https://github.com/salfis/nasalinha-qa/issues/33) | Usuário comum visualiza check-ins de outros usuários, com e-mail exposto | Check-in     | Crítica    | RF-06         |
| [#34](https://github.com/salfis/nasalinha-qa/issues/34) | Novo check-in é criado já Aprovado, sem passar por Pendente              | Check-in     | Maior      | RF-05         |
| [#42](https://github.com/salfis/nasalinha-qa/issues/42) | Arquivo temporário fica em `uploads/` quando o envio ao Cloudinary falha | Check-in     | Maior      | RNF-02        |
| [#39](https://github.com/salfis/nasalinha-qa/issues/39) | Envio de arquivo inválido retorna 500 em vez de 400                      | Check-in     | Menor      | RF-04         |
| [#35](https://github.com/salfis/nasalinha-qa/issues/35) | Sistema aceita vários check-ins do mesmo usuário em menos de 24 horas    | Pontos       | Maior      | RF-04 / RF-09 |
| [#36](https://github.com/salfis/nasalinha-qa/issues/36) | Excluir check-in não subtrai os pontos do saldo nem do ranking           | Pontos       | Maior      | RF-08         |
| [#40](https://github.com/salfis/nasalinha-qa/issues/40) | Rejeitar um check-in aprovado não remove os pontos do ranking            | Pontos       | Maior      | RF-07         |
| [#45](https://github.com/salfis/nasalinha-qa/issues/45) | API aceita pontos negativos ao editar um check-in                        | Pontos       | Maior      | RF-07         |
| [#43](https://github.com/salfis/nasalinha-qa/issues/43) | Coleção do Postman tem rotas que não existem na API                      | Documentação | Menor      | —             |

---

## 6. Testes de regressão e re-teste

Os 3 cenários de regressão (CT-REG-01, CT-REG-02 e CT-REG-03) estão descritos em [`casos-de-teste.md`](./casos-de-teste.md#testes-de-regressão). Para cada área, foi listado quais testes devem ser repetidos.

Os casos de regressão estão bloqueados, porque não foi feita nenhuma correção durante os testes.

---

## 7. Ordem de correção sugerida:

1. **#38 e #41:** qualquer pessoa consegue se tornar ADMIN. de longe o risco mais grave do sistema.
2. **#31 e #32:** Sem a verificação de contas se abre um espaço pra criação de contas falsas.
3. **#33 e #44:** Os usuários conseguem ver email e id de outros usuário.
4. **#37:** o usuário acha que trocou a senha, mas a antiga continua valendo.
5. **#34, #35, #36, #40 e #45:** o ranking pode ser manipulado e não reflete os check-ins válidos.
6. **#39, #42 e #43:** tratamento de erros, limpeza de arquivos e documentação.
