# Casos de Teste — NaSalinha

Planejamento dos testes das 3 áreas core do sistema: Autenticação JWT, Check-in por foto e Sistema de pontos. Os casos foram escritos a partir do documento de requisitos e do que observei na exploração (`qa/exploracao.md`).

Para cada requisito foram definidos 2 casos de teste, e para cada área existe pelo menos um caso Funcional, um de API e um de Regressão.

## Organização

- **ID:** CT-AUTH (Autenticação), CT-CHK (Check-in), CT-PTS (Pontos e Ranking), CT-REG (Regressão), CT-EXTRA (casos extras encontrados durante a execução, com a label `casos-extras`).
- **Tipo:** Funcional (pela interface), API (pelo Postman) ou Regressão.
- **Positivo/Negativo:** positivo valida o fluxo esperado; negativo valida entradas inválidas ou ações que o sistema deve bloquear.
- **Situação:** Não executado, Pass, Fail ou Bloqueado.

## Ambiente

- Frontend: http://localhost:3000
- API: http://localhost:5001/api
- Usuários do seed (senha `senha123`):
  - admin@nasalinha.com — ADMIN
  - lucas@example.com — MEMBER
  - maria@example.com — MEMBER
  - pedro@example.com — TRAINEE
- Temporada ativa do seed: Temporada 2025.1, com 10 pontos por check-in.
- Arquivos de teste: foto-valida-1.jpg, foto-valida-2.png, arquivo.pdf e foto-grande.jpg (maior que 5 MB).
- Nas requisições protegidas da API, enviar o header `Authorization: Bearer <accessToken>`.

## Rastreabilidade

- RF-01 — Cadastro e verificação: CT-AUTH-01, CT-AUTH-02
- RF-02 — Restrição de login: CT-AUTH-03, CT-AUTH-04
- RF-03 — Controle de níveis (RBAC): CT-AUTH-05, CT-AUTH-06
- RNF-01 — Segurança de dados: CT-AUTH-07, CT-AUTH-08
- RF-04 — Registro de atividade: CT-CHK-01, CT-CHK-02
- RF-05 — Fluxo de status do check-in: CT-CHK-03, CT-CHK-04
- RF-06 — Restrição de propriedade: CT-CHK-05, CT-CHK-06
- RNF-02 — Integridade de arquivos: CT-CHK-07, CT-CHK-08
- RF-07 — Atribuição de pontos: CT-PTS-01, CT-PTS-02
- RF-08 — Consistência de saldo: CT-PTS-03, CT-PTS-04
- RF-09 — Regras de ranking: CT-PTS-05, CT-PTS-06

Total: 22 casos de requisito + 3 de regressão.

---

## Autenticação JWT

### CT-AUTH-01 — Cadastro com código de verificação e conta PENDENTE

- Requisito: RF-01
- Tipo: Funcional (positivo)
- Prioridade: Alta

**Pré-condições:**
Mailtrap configurado e e-mail ainda não cadastrado no sistema.

**Procedimento:**

1. Acessar a tela de cadastro (/register).
2. Preencher nome, e-mail e senha válidos.
3. Clicar em "Cadastrar".
4. Abrir a caixa de entrada do Mailtrap.

**Dados de teste:**
Nome: Teste QA | E-mail: qa.cadastro01@mail.com | Senha: senha123

**Resultado esperado:**
O cadastro deve ser concluído e o sistema deve levar o usuário para uma etapa de verificação.
Um e-mail com um código de verificação único deve chegar no Mailtrap.
A conta deve ser criada com status PENDENTE.

**Situação:** Fail.

**Resultado Obtido:**
Após clicar em "Criar Conta", o sistema exibiu a mensagem "Cadastro realizado com sucesso!" e redirecionou para `http://localhost:3000/login`.
Não foi oferecida nenhuma etapa de verificação.
A requisição POST /api/auth/register retornou 201 com accessToken e refreshToken. Logo, a conta já foi autenticada assim que cadastrada.
O data.user na resposta da requisição retornou nome, e-mail, role MEMBER e data de criação, sem nada indicando o status PENDENTE nem nada do tipo.
O e-mail que se recebe pelo mailtrap é de boas vindas. Sem código de verificação.

**EVIDÊNCIAS:** CT-AUTH-01-apos-cadastro.png, CT-AUTH-01-email-mailtrap.png, CT-AUTH-01-formulario.png, CT-AUTH-01-rede-register.png

Bug: #31

**Observação:**
Na exploração, o e-mail recebido foi apenas de boas-vindas, sem código (ver RF-01 em exploracao.md).

---

### CT-AUTH-02 — Cadastro pela API com perfil ADMIN

- Requisito: RF-01 / RF-03
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
API em execução.

**Procedimento:**

1. Enviar `POST /api/auth/register` com o corpo abaixo.
2. Verificar o status HTTP e o campo `role` retornado.

**Dados de teste:**

```json
{ "name": "Invasor QA", "email": "qa.invasor@mail.com", "password": "senha123", "role": "ADMIN" }
```

**Resultado esperado:**
O sistema não deve permitir que um usuário crie uma conta ADMIN pelo cadastro público.
A requisição deve ser recusada (400) ou o usuário deve ser criado com o perfil padrão (MEMBER), ignorando o campo `role`.

**Situação:** Não executado.

---

### CT-AUTH-03 — Login de conta não verificada pela interface

- Requisito: RF-02
- Tipo: Funcional (negativo)
- Prioridade: Alta

**Pré-condições:**
Conta criada no CT-AUTH-01, sem o código de verificação confirmado.

**Procedimento:**

1. Acessar a tela de login (/login).
2. Informar o e-mail e a senha da conta não verificada.
3. Clicar em "Entrar".

**Dados de teste:**
qa.cadastro01@mail.com / senha123

**Resultado esperado:**
O sistema deve bloquear o acesso ao dashboard e apresentar a mensagem: "Por favor, verifique sua conta para continuar".

**Situação:** Fail.

**Resultado Obtido:**
Ao realizar o login com a conta sem fazer nenhum tipo de verificação prévia, o usuário recebe um toast do sistema: "Login realizado com sucesso", e é
redirecionado para `/dashboard`. Nenhuma mensagem sobre verificação foi exibida.
Dashboard carregou as informações corretamente.
A requisição POST `/api/auth/login` retornou 200 com `accessToken` e `refreshToken`.

Evidêncas: CT-AUTH-03-forumulario.png, CT-AUTH-03-apos-login.png, CT-AUTH-03-rede-login.png

Bug: #32

**Observação:**
Na exploração foi possível acessar o dashboard sem nenhuma confirmação (ver RF-02 em exploracao.md).

---

### CT-AUTH-04 — Login de conta não verificada pela API

- Requisito: RF-02
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Conta cadastrada e não verificada.

**Procedimento:**

1. Enviar `POST /api/auth/login` com as credenciais da conta não verificada.
2. Verificar o status HTTP, a mensagem e se a resposta traz algum token.

**Dados de teste:**

```json
{ "email": "qa.cadastro01@mail.com", "password": "senha123" }
```

**Resultado esperado:**
A API deve retornar 401 (ou 403) com a mensagem "Por favor, verifique sua conta para continuar".
Nenhum `accessToken` ou `refreshToken` deve ser retornado.

**Situação:** Não executado.

---

### CT-AUTH-05 — MEMBER tentando acessar endpoints de Temporadas

- Requisito: RF-03
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Token de lucas@example.com (MEMBER) e ID de uma temporada existente.

**Procedimento:**

1. Fazer login como MEMBER e copiar o `accessToken`.
2. Enviar `POST /api/seasons` com o token do MEMBER.
3. Enviar `PATCH /api/seasons/{id}/toggle-active` com o token do MEMBER.
4. Conferir a lista de temporadas com `GET /api/seasons`.

**Dados de teste:**

```json
{
  "name": "Temporada Teste",
  "startDate": "2026-01-01",
  "endDate": "2026-06-30",
  "pointsPerCheckIn": 999
}
```

**Resultado esperado:**
As duas requisições devem retornar 403.
Nenhuma temporada deve ser criada ou alterada.

**Situação:** Não executado.

**Observação:**
Na exploração, a interface redirecionou MEMBER e TRAINEE para o dashboard, mas isso não garante que o backend bloqueie as requisições (ver RF-03 em exploracao.md).

---

### CT-AUTH-06 — Usuário comum alterando o perfil de outro usuário

- Requisito: RF-03
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Token de lucas@example.com (MEMBER) e ID de maria@example.com.

**Procedimento:**

1. Fazer login como Lucas.
2. Enviar `PUT /api/users/{id-da-maria}` com o corpo abaixo.
3. Repetir usando o ID do próprio Lucas.
4. Consultar o perfil dos dois usuários.

**Dados de teste:**

```json
{ "role": "ADMIN" }
```

**Resultado esperado:**
As duas requisições devem retornar 403, já que só um ADMIN pode alterar perfis de acesso.
Lucas e Maria devem continuar como MEMBER.

**Situação:** Não executado.

---

### CT-AUTH-07 — Senha salva com hash no banco

- Requisito: RNF-01
- Tipo: API (positivo)
- Prioridade: Média

**Pré-condições:**
Acesso de leitura ao PostgreSQL pelo container.

**Procedimento:**

1. Cadastrar um usuário novo via `POST /api/auth/register` com a senha senha123.
2. Consultar o campo password desse usuário no banco.
3. Verificar se alguma resposta da API devolve o campo password.

**Resultado esperado:**
A senha não deve estar salva em texto puro: o valor deve ser um hash bcrypt (prefixo $2b$ e 60 caracteres).
Nenhuma resposta da API deve expor o campo password.

**Situação:** Não executado.

---

### CT-AUTH-08 — Redefinição de senha

- Requisito: RNF-01
- Tipo: Funcional (positivo)
- Prioridade: Média

**Pré-condições:**
Usuário maria@example.com existente e Mailtrap configurado.

**Procedimento:**

1. Acessar "Esqueci minha senha" (/forgot-password) e informar maria@example.com.
2. Abrir o e-mail no Mailtrap e seguir o link de redefinição.
3. Definir a nova senha novaSenha123.
4. Fazer login com a nova senha.
5. Tentar login com a senha antiga (senha123).
6. Consultar o campo password no banco.

**Resultado esperado:**
O login com a nova senha deve funcionar e o login com a senha antiga deve ser recusado.
O hash salvo no banco deve ter mudado e continuar no formato bcrypt.

**Situação:** Fail.

**Resultado Obtido:**
A solicitação de recuperação de senha para `maria@example.com` foi enviada e o e-mail chegou no mailtrap com o link para a redefinição da senha.
Após definir a nova senha: `novaSenha123`, o sistema exibiu o toast: "Senha redefinida com sucesso!" e a requisição `POST reset-password` retornou 200
Mesmo assim o login com a nova senha foi recusado (401, "Credenciais Inválidas), e o login com a senha antiga (senha123) continuou fucionando com o código 200 na requisição de login.
Conclusão: Senha não é alterada, mesmo apóis a mensagem de sucesso.

**Evidências:** CT-AUTH-08-email.png, CT-AUTH-08-esqueci-senha.png, CT-AUTH-08-login-senha-antiga.png, CT-AUTH-08-login-senha-nova.png, CT-AUTH-08-reset-senha-rede.png

Bug: #37

---

## Check-in por foto

### CT-CHK-01 — Check-in com imagem válida

- Requisito: RF-04
- Tipo: Funcional (positivo)
- Prioridade: Alta

**Pré-condições:**
Logado como pedro@example.com, Temporada 2025.1 ativa, Pedro sem check-in no dia e Cloudinary configurado.

**Procedimento:**

1. Acessar o dashboard.
2. Selecionar foto-valida-1.jpg.
3. Clicar no botão de check-in.
4. Conferir a lista de check-ins recentes.

**Resultado esperado:**
O sistema deve mostrar uma mensagem de sucesso.
O check-in deve aparecer na lista com a foto, a data do dia e o nome do usuário, associado à temporada ativa (Temporada 2025.1).

**Situação:** Pass.

**Resultado obtido:**
Feito login como Pedro, o check-in com `testeJPG.jpeg` exibiu o toast "Check-in realizado com sucesso!".
Os cars passsaram de 0 para 1 check-in e de 0 para 10 pontos.
O novo check-in apareceu em "Atividade Recente" com a foto enviada, o nome Pedro Costa e a data/hora atual.
A requisição POST/api/checkins retornou 201, e o check-in na temporada ativa que nesse caso é a 2025.1.
photoUrl era de uma imagem hospedada no Cloudinary.

**Observação:** o check-in foi criado com o status APPROVED direto e 10 pontos ja caíram imediatamente, sem avaliação de nenhum ADMIN.

**Evidências:** CT-CHK-01-antes.png, CT-CHK-01-apos-checkin.png, CT-CHK-01-modal.png, CT-CHK-01-rede-post.png

---

### CT-CHK-02 — Segundo check-in no dia e foto repetida

- Requisito: RF-04
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Pedro já fez um check-in no dia (CT-CHK-01).

**Procedimento:**

1. Enviar `POST /api/checkins` (form-data, campo photo) com foto-valida-2.png.
2. Enviar `POST /api/checkins` de novo com a mesma foto-valida-1.jpg.
3. Consultar `GET /api/checkins/my-checkins`.

**Resultado esperado:**
O passo 1 deve ser recusado (400 ou 409) com uma mensagem sobre o limite diário.
O passo 2 deve ser recusado com uma mensagem de foto já enviada.
Pedro deve continuar com apenas um check-in no dia.

**Situação:** Não executado.

---

### CT-CHK-03 — Status inicial do check-in

- Requisito: RF-05
- Tipo: Funcional (positivo)
- Prioridade: Alta

**Pré-condições:**
Logado como maria@example.com, sem check-in no dia.

**Procedimento:**

1. Realizar um check-in pelo dashboard com uma imagem válida.
2. Conferir o status mostrado no card do check-in.

**Resultado esperado:**
O check-in deve aparecer como "Pendente" e só mudar para "Aprovado" depois da avaliação de um ADMIN.

**Situação:** Fail

**Resultado obtido:**
O check-in realizado no CT-CHK-01 (Pedro, TRAINEE) foi criado diretamente com status “Aprovado”, sem passar por “Pendente”. A requisição POST /api/checkins retornou 201 com "status": "APPROVED" e "points": 10, e os pontos foram creditados no mesmo instante, sem avaliação de um ADMIM. Logado como ADMIN, não tem na interface nenhuma opção para aprovar ou rejeitar check-ins, o card exibe só o status e o botão de excluir.

**Observação:** executado com a evidência do CT-CHK-01, usando os dados do Pedro, ao invés dos dados da Maria, pois o comportamento verificado acontece igualmente
independente do usuário.

**Evidências:** CT-CHK-01-apos-checkin.png, CT-CHK-01-rede-post.png, CT-CHK-03-check-in-adm.png
Bug: #34

---

### CT-CHK-04 — Usuário comum alterando o status de um check-in

- Requisito: RF-05
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
ID de um check-in PENDENTE e tokens de MEMBER e de ADMIN.

**Procedimento:**

1. Com o token do MEMBER, enviar `PUT /api/checkins/{id}` com `{ "status": "APPROVED" }`.
2. Com o token do ADMIN, enviar a mesma requisição.
3. Consultar `GET /api/checkins/{id}`.

**Resultado esperado:**
A requisição do MEMBER deve retornar 403 e o status deve continuar PENDENTE.
A requisição do ADMIN deve retornar 200 e o status deve mudar para APPROVED.

**Situação:** Não executado.

---

### CT-CHK-05 — Visualizar check-in de outro usuário

- Requisito: RF-06
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Lucas e Maria com pelo menos um check-in cada, token do Lucas e ID de um check-in da Maria.

**Procedimento:**

1. Com o token do Lucas, enviar `GET /api/checkins/{id-checkin-da-maria}`.
2. Com o token do Lucas, enviar `GET /api/checkins`.

**Resultado esperado:**
O passo 1 deve retornar 403 (ou 404), sem os dados do check-in da Maria.
A lista do passo 2 não deve trazer check-ins de outros usuários.

**Situação:** Não executado.

---

### CT-CHK-06 — Excluir check-in de outro usuário pela interface

- Requisito: RF-06
- Tipo: Funcional (negativo)
- Prioridade: Alta

**Pré-condições:**
Logado como lucas@example.com e com check-ins de outros usuários cadastrados.

**Procedimento:**

1. Acessar o dashboard.
2. Procurar check-ins de outros usuários na tela.
3. Verificar se aparecem opções de editar ou excluir nesses check-ins.

**Resultado esperado:**
O usuário não deve conseguir editar ou excluir check-ins que não são dele. Esses botões não devem aparecer para check-ins de outros usuários.

**Situação:** fail.

**Resultado obtido:**
Logado como Lucas, a seção “Atividade Recente” exibiu 3 check-ins (1 de Maria Santos e 2 de Lucas Silva), todos com data, pontuação e status “Aprovado”. Nenhum card exibiu botão de editar ou excluir, e não tem nenhuma ação oculta ao clicar. Porém, o usuário consegue vizualizar check-ins que não pertencem a seu próprio ID, violando a RF-06.
Quando se entra como admin, os mesmos cards exibem o botão de excluir, confirmando que a opção existe e é restrita ao ADMIN, sem problemas.

**Observação:**
A requisição `/api/checkins` retorna a um usuário qualquer os check-ins de todos os usuários, que vem com e-mail e ID.

**Evidências:** CT-CHK-06-dashboard-lucas.png, CT-CHK-06-dashboard-admin.png, CT-CHK-06-rede-checkin.png

Bug: #

### CT-CHK-07 — Envio de arquivo inválido

- Requisito: RNF-02 / RF-04
- Tipo: API (negativo)
- Prioridade: Média

**Pré-condições:**
Token válido e acesso ao container do backend.

**Procedimento:**

1. Listar a pasta de uploads: `docker-compose exec backend ls uploads/`.
2. Enviar `POST /api/checkins` com arquivo.pdf.
3. Enviar `POST /api/checkins` com foto-grande.jpg.
4. Listar a pasta uploads/ de novo.
5. Acompanhar os logs do backend.

**Resultado esperado:**
Os dois envios devem retornar 400 com uma mensagem clara (tipo de arquivo não permitido / arquivo muito grande), e não 500.
A pasta uploads/ deve continuar igual à do passo 1.

**Situação:** Não executado.

---

### CT-CHK-08 — Arquivo temporário após falha no envio para a nuvem

- Requisito: RNF-02
- Tipo: API (negativo)
- Prioridade: Média

**Pré-condições:**
Credencial do Cloudinary alterada de propósito no .env (voltar ao normal depois) e container reiniciado.

**Procedimento:**

1. Listar a pasta uploads/ no container do backend.
2. Enviar `POST /api/checkins` com uma imagem válida.
3. Listar a pasta uploads/ de novo.
4. Restaurar a credencial correta, fazer um check-in válido e listar uploads/.

**Resultado esperado:**
O erro do passo 2 deve ser tratado com uma mensagem amigável.
Nenhum arquivo novo deve ficar na pasta uploads/, nem no caso de falha nem no de sucesso.

**Situação:** Não executado.

---

## Sistema de pontos

### CT-PTS-01 — Pontos somados após check-in aprovado

- Requisito: RF-07
- Tipo: Funcional (positivo)
- Prioridade: Alta

**Pré-condições:**
Pedro sem check-in no dia e pontuação atual dele anotada no ranking (X).

**Procedimento:**

1. Logado como Pedro, realizar um check-in.
2. Logado como ADMIN, aprovar o check-in.
3. Logado como Pedro, acessar o ranking (/ranking).

**Resultado esperado:**
A pontuação do Pedro deve ser X + 10.
A posição no ranking deve refletir o novo total sem nenhuma ação manual.

**Situação:** Pass.

**Resultado Obtido:**

Depois do check-in, a pontuação do Pedro aumentou de 0 para 10 (Ganhou 10 pontos). No ranking, consultado como ADMIN(Pedro como trainee não possui acesso, então o passo 3 foi adaptado), Pedro aparece com 10 pontos, 1 check-in, na 3ª posição, sem nenhuma ação manual.
Ordem do ranking: Lucas (20), Maria (10), Pedro (10). Pedro empata com Maria e aparece depois dela; As outras posições são definidas pelo seed do próprio projeto.

**OBSERVAÇÃO:**
Não é possível executar o segundo passo de aprovação do check-in com o ADMIN, já que não existe fluxo de aprovação e o check-in já é criado aprovado.
Esse problema já é mencionado no bug #34 (RF-05).

**Evidências:** CT-PTS-01-dashboard-pedro-antes.png, CT-PTS-01-dashboard-pedro-depois.png, CT-PTS-01-ranking-admin-depois.png

### CT-PTS-02 — Check-in rejeitado não soma pontos

- Requisito: RF-07 / RF-05
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Token de ADMIN e um usuário com check-in PENDENTE.

**Procedimento:**

1. Enviar `GET /api/rankings` e anotar o totalPoints do usuário (X).
2. Como ADMIN, enviar `PUT /api/checkins/{id}` com `{ "status": "REJECTED" }`.
3. Enviar `GET /api/rankings` de novo.

**Resultado esperado:**
O totalPoints do usuário deve continuar X. Check-in rejeitado não deve contar pontos.

**Situação:** Não executado.

---

### CT-PTS-03 — Exclusão de check-in pela API

- Requisito: RF-08
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Usuário com um check-in aprovado (10 pontos) e token de ADMIN.

**Procedimento:**

1. Enviar `GET /api/rankings` e anotar totalPoints (X) e checkInsCount (N) do usuário.
2. Como ADMIN, enviar `DELETE /api/checkins/{id}`.
3. Enviar `GET /api/rankings` de novo.

**Resultado esperado:**
A exclusão deve retornar 200.
O totalPoints deve passar para X − 10 e o checkInsCount para N − 1.

**Situação:** Não executado.

---

### CT-PTS-04 — Ranking na tela após exclusão de check-in

- Requisito: RF-08
- Tipo: Funcional (negativo)
- Prioridade: Média

**Pré-condições:**
Mesmo cenário do CT-PTS-03, feito pela interface.

**Procedimento:**

1. Acessar o ranking e anotar pontos e posição do usuário.
2. Como ADMIN, excluir o check-in desse usuário pelo dashboard.
3. Recarregar o ranking.

**Resultado esperado:**
Os pontos mostrados devem diminuir 10.
A posição deve ser recalculada se outro usuário passar a ter mais pontos.

**Situação:** Fail.

**Resultado obtido:**
Logado como ADMIN, os dois check-ins de lucas foram excluídos pelo dashboard. Os cards foram removidos da aba "Atividade Recente", porém o ranking continuou a mostrar o lucas com 2- pontos 2 check-ins, mesmo depois de recarregar a página.
No Dashboard do Lucas, o número de check-ins passou a mostrar 0, como deveria, porém os pontos continuaram em 20.
`DELETE /checkins` retornou `200` e `GET /rankings` continuou a mostrar os mesmos `totalPoints` e `checkInsCount`

**Evidências:** CT-PTS-04-dashboard-lucas.png, CT-PTS-04-exclusao.png, CT-PTS-04-ranking-antes.png, CT-PTS-04-ranking-depois.png

Bug: #36

### CT-PTS-05 — Ordem do ranking

- Requisito: RF-09
- Tipo: API (positivo)
- Prioridade: Média

**Pré-condições:**
Pelo menos 3 usuários com pontuações diferentes na temporada ativa.

**Procedimento:**

1. Enviar `GET /api/rankings`.
2. Comparar o totalPoints de cada item com o do item seguinte.
3. Abrir o ranking na interface e comparar a ordem com a da API.

**Resultado esperado:**
A API deve retornar 200 com os usuários em ordem decrescente de pontuação.
A interface deve mostrar a mesma ordem.

**Situação:** Não executado.

---

### CT-PTS-06 — Check-ins com intervalo menor que 24 horas

- Requisito: RF-09
- Tipo: Funcional (negativo)
- Prioridade: Alta

**Pré-condições:**
Usuário com um check-in feito há menos de 24 horas, incluindo o caso de virada de dia (ex.: 23h50 e 00h10).

**Procedimento:**

1. Logado como esse usuário, tentar um novo check-in pelo dashboard com outra imagem.
2. Conferir a mensagem exibida e o ranking.

**Resultado esperado:**
O sistema deve recusar o check-in e informar o intervalo mínimo.
A pontuação do usuário não deve mudar.

**Situação:** Fail.

**Resultado obtido:**
Logado como Pedro, com um check-in feito 3 minutos antes, um novo check-in com outra imagem foi aceito. O sistema exibiu o toast “Check-in realizado com sucesso!” e os cards passaram de 1 para 2 check-ins e de 10 para 20 pontos.
A requisição POST checkins retornou 201. Nenhuma mensagem sobre intervalo mínimo foi exibida.

**Evidências:** CT-PTS-06-pedro-antes.png, CT-PTS-06-pedro-apos-check-in.png
Bug: #35

---

## Testes de regressão

Simulação: um bug reportado foi corrigido. Para cada área, estes são os testes que eu repetiria para garantir que a correção não quebrou outras partes do sistema.

### CT-REG-01 — Autenticação: correção do login sem verificação

- Requisito: RF-02
- Tipo: Regressão

**Cenário simulado:**
O bug "usuário não verificado consegue fazer login" foi corrigido.

**Fluxo principal:**
Cadastro → recebimento do código → verificação → login → acesso ao dashboard.

**Testes que devem ser repetidos:**

- CT-AUTH-01: a correção mexe no status da conta definido no cadastro.
- CT-AUTH-03: confirma a correção na interface.
- CT-AUTH-04: confirma a correção na API.
- CT-AUTH-05: o controle de acesso (RBAC) precisa continuar funcionando.
- CT-AUTH-07: o hash da senha não pode ter sido afetado.
- CT-AUTH-08: o login depois da redefinição de senha usa o mesmo fluxo.
- Login dos usuários já existentes (seed) deve continuar funcionando.

**Situação:** Não executado.

---

### CT-REG-02 — Check-in: correção do status inicial PENDENTE

- Requisito: RF-05
- Tipo: Regressão

**Cenário simulado:**
O bug "check-in é criado já aprovado" foi corrigido.

**Fluxo principal:**
Envio da foto → check-in PENDENTE → aprovação do ADMIN → pontos somados.

**Testes que devem ser repetidos:**

- CT-CHK-01: a criação de check-in continua funcionando.
- CT-CHK-03: confirma a correção.
- CT-CHK-04: a aprovação pelo ADMIN passa a ser obrigatória.
- CT-PTS-01: os pontos só devem ser somados depois da aprovação.
- CT-PTS-02: check-in rejeitado continua sem somar pontos.
- CT-PTS-05: o ranking continua consistente.
- Os status (Pendente, Aprovado e Rejeitado) continuam aparecendo certo no dashboard.

**Situação:** Não executado.

---

### CT-REG-03 — Pontos: correção da subtração ao excluir check-in

- Requisito: RF-08
- Tipo: Regressão

**Cenário simulado:**
O bug "excluir check-in não tira os pontos do usuário" foi corrigido.

**Fluxo principal:**
Check-in aprovado → pontos somados → exclusão → pontos subtraídos → ranking atualizado.

**Testes que devem ser repetidos:**

- CT-PTS-01: a soma de pontos não pode ter sido afetada.
- CT-PTS-03: confirma a correção na API.
- CT-PTS-04: confirma a correção na interface.
- CT-PTS-05: a ordem do ranking continua correta.
- CT-CHK-01: a criação de check-in continua funcionando.
- CT-CHK-04: alterar e excluir check-in continua restrito ao ADMIN.
- Excluir um check-in rejeitado não deve tirar pontos, já que eles nunca foram somados.
- O saldo do usuário nunca deve ficar negativo.

**Situação:** Não executado.

---

## Casos extras

Cenários encontrados durante a execução que não estavam no planejamento. Cada um recebe a label `casos-extras` e deve ter um bug report ligado a ele.

- CT-EXTRA-01 — (preencher durante a execução)
