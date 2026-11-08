# Casos de Teste — NaSalinha

Planejamento de testes para as 3 áreas Core do sistema. Todos os testes foram planejados em torno da minha navegação pelo frontend, análise do código e leitura do documento de pré-requisitos de funcionamento da aplicação(`/qa/Requisitos.md`).

Para cada um dos requisitos eu especifiquei dois casos de teste, e para cada área existe pelo menos um caso de teste Funcional(frontend), um caso de teste de API e um caso de teste de Regressão.

## Organização:

- **ID:** CT-AUTH define os testes de `Autenticação`, CT-CHK define os testes sobre `Check-in`, CT-PTS vai definir os testes de `Pontos e Ranking`, CT-REG são os casos teste de `Regressão`, CT-EXTRA são os casos de teste que foram definidos durante o projeto e usam a lable `casos-extras`.
- **Tipo:** Funcional (frontend), API (via Postman) ou Regressão.
- **Positivo/Negativo:** testes positivos são testes para validar o cenário esperado, já os testes negativos validam se o sitema permite a entrada inválida ou ação que ele não deveria.
- **Situação:** Não executado, Pass, Fail ou Bloqueado.

## Ambiente

- Frontend: http://localhost:3000
- API: http://localhost:5001/api
- Usuários do seed (senha `senha123`):
  - admin@nasalinha.com — ADMIN
  - lucas@example.com — MEMBER
  - maria@example.com — MEMBER
  - pedro@example.com — TRAINEE
- Temporada ativa no seed: Temporada 2025.1, com 10 pontos por check-in.
- Arquivos para teste: foto-valida-1.jpg, foto-valida-2.png, arquivo.pdf e foto-grande.jpg (maior que 5 MB).
- Nas requisições protegidas da API, adicionar o header `Authorization: Bearer <accessToken>`.

## Rastreabilidade

- RF-01 — Cadastro e verificação do usuário: CT-AUTH-01, CT-AUTH-02
- RF-02 — Restrição de login: CT-AUTH-03, CT-AUTH-04
- RF-03 — Controle de acesso por nível (RBAC): CT-AUTH-05, CT-AUTH-06
- RNF-01 — Segurança dos dados: CT-AUTH-07, CT-AUTH-08
- RF-04 — Registro de atividade: CT-CHK-01, CT-CHK-02
- RF-05 — Fluxo de status do check-in: CT-CHK-03, CT-CHK-04
- RF-06 — Restrição de propriedade: CT-CHK-05, CT-CHK-06
- RNF-02 — Integridade dos arquivos: CT-CHK-07, CT-CHK-08
- RF-07 — Atribuição de pontos: CT-PTS-01, CT-PTS-02
- RF-08 — Consistência do saldo: CT-PTS-03, CT-PTS-04
- RF-09 — Regras do ranking: CT-PTS-05, CT-PTS-06

Total de casos de requisito: 22
Total de casos de regressão: 3

---

## Autenticação JWT

### CT-AUTH-01 — Cadastro com código de verificação e conta PENDENTE

- Requisito: RF-01
- Tipo: Funcional (positivo)
- Prioridade: Alta

**Pré-condições:**
Mailtrap configurado e e-mail ainda não cadastrado no sistema.

**Procedimento:**

1. Vá para a página de cadastro (/register).
2. Digite nome, e-mail e senha.
3. Clique em "Cadastrar".
4. Vá para a caixa de entrada do Mailtrap.

**Dados de teste:**
Nome: Teste QA | E-mail: qa.cadastro01@mail.com | Senha: senha123

**Resultado esperado:**
O cadastro deveria ser concluído e o sistema deveria levar o usuário para a etapa de verificação. Um e-mail com um código único deveria chegar no Mailtrap. A conta deveria ficar registrada com o status PENDENTE.

**Situação:** Fail.

**Resultado obtido:**
Após clicar no botão "Criar Conta", o sistema exibiu a mensagem "Cadastro realizado com sucesso!" e redirecionou para `http://localhost:3000/login`. O sistema não ofereceu nenhuma etapa de verificação. A requisição POST `/api/auth/register` retornou 201 com `accessToken` e `refreshToken`, ou seja, a conta já saiu autenticada logo depois do cadastro. O `data.user` da resposta mostrou nome, e-mail, role MEMBER e data de criação, sem nada indicando status PENDENTE. O e-mail que chegou no Mailtrap é só de boas-vindas, sem nenhum código de verificação.

**Evidências:** CT-AUTH-01-apos-cadastro.png, CT-AUTH-01-email-mailtrap.png, CT-AUTH-01-formulario.png, CT-AUTH-01-rede-register.png

Bug: #31

**Observação:**
Durante a exploração, o e-mail recebido também foi só de boas-vindas, sem nenhum código (ver RF-01 em exploracao.md).

---

### CT-AUTH-02 — Cadastro pela API com perfil ADMIN

- Requisito: RF-03
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
API em execução.

**Procedimento:**

1. Envie a requisição `POST /api/auth/register` com o corpo abaixo.
2. Valide o código de status HTTP e o campo `role` retornado.

**Dados de teste:**

```json
{ "name": "Invasor QA", "email": "qa.invasor@mail.com", "password": "senha123", "role": "ADMIN" }
```

**Resultado esperado:**
A aplicação não deve permitir que alguém se cadastre como ADMIN pelo cadastro público. Ela deve recusar a requisição (400) ou criar o usuário com o perfil padrão (MEMBER), ignorando o campo `role`.

**Situação:** Fail.

**Resultado obtido:**
A aplicação permitiu a criação do perfil com `"role": "ADMIN"` e o status retornado foi `201 Created`, contrariando a regra de negócio da RF-03 em que os endpoints de gestão são restritos a usuários com perfil de ADMINISTRADOR, já que pelo cadastro público, toda pessoa conseguiria acesso de ADMIN.

**Observações:** A alteração do cargo de um usuário não está exatamente prevista nas regras de autenticação mas foi considerada como uma violação da RF-03, já que qualquer usuário consegue obter privilégios de administrador.

**Evidências:** CT-AUTH-02-requisicao-de-registro.png

Bug: #32

---

### CT-AUTH-03 — Login de conta não verificada pela interface

- Requisito: RF-02
- Tipo: Funcional (negativo)
- Prioridade: Alta

**Pré-condições:**
Conta criada no CT-AUTH-01, sem a verificação do código.

**Procedimento:**

1. Vá para a página de login (/login).
2. Digite o e-mail e a senha da conta não verificada.
3. Clique em "Entrar".

**Dados de teste:**
qa.cadastro01@mail.com / senha123

**Resultado esperado:**
O sistema deve negar o acesso ao dashboard e mostrar o aviso: "Por favor, verifique sua conta para continuar".

**Situação:** Fail.

**Resultado obtido:**
Ao fazer login com a conta sem passar por nenhuma verificação, o sistema exibiu o toast "Login realizado com sucesso" e redirecionou o usuário para `/dashboard`. Nenhum aviso sobre verificação foi exibido. O dashboard carregou os dados normalmente. A requisição POST `/api/auth/login` retornou 200 com `accessToken` e `refreshToken`.

**Evidências:** CT-AUTH-03-formulario.png, CT-AUTH-03-apos-login.png, CT-AUTH-03-rede-login.png

Bug: #32

**Observação:**
Durante a exploração também foi possível acessar o dashboard sem nenhuma confirmação (ver RF-02 em exploracao.md).

---

### CT-AUTH-04 — Login de conta não verificada pela API

- Requisito: RF-02
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Conta cadastrada e não verificada.

**Procedimento:**

1. Envie a requisição `POST /api/auth/login` com os dados do usuário não verificado.
2. Verifique o status HTTP, a mensagem e se a resposta traz algum token.

**Dados de teste:**

```json
{ "email": "qa.cadastro01@mail.com", "password": "senha123" }
```

**Resultado esperado:**
A API deve retornar 401 (ou 403) com a mensagem "Por favor, verifique sua conta para continuar". Não deve vir `accessToken` nem `refreshToken` na resposta.

**Situação:** Fail.

**Resultado obtido:**
A API retornou `200 OK` com a mensagem `"Login realizado com sucesso"`. A resposta contém `accessToken` e o `refreshToken`.

**Evidências:** CT-AUTH-04-registrado-usuario-teste.png, CT-AUTH-04-usuario-nao-verificado-login.png.

Bug: #32

---

### CT-AUTH-05 — MEMBER tentando acessar endpoints de Temporadas

- Requisito: RF-03
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Token de lucas@example.com (MEMBER) e ID de uma temporada que já existe.

**Procedimento:**

1. Faça login como MEMBER e copie o `accessToken`.
2. Envie `POST /api/seasons` usando o token do MEMBER.
3. Envie `PATCH /api/seasons/{id}/toggle-active` usando o token do MEMBER.
4. Confira a lista de temporadas com `GET /api/seasons`.

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
As duas requisições devem retornar 403. Nenhuma temporada deve ser criada ou alterada.

**Situação:** Pass.

**Observação:**
Na exploração, a interface redirecionou MEMBER e TRAINEE para o dashboard, mas isso não quer dizer que o backend esteja bloqueando as requisições (ver RF-03 em exploracao.md).

**Resultado obtido:**
As duas requisições retornaram `403 Forbidden`. Nenhuma temporada foi criada ou alterada.

**Evidências:** CT-AUTH-05-atualizacao-temporada-membro.png, CT-AUTH-05-criacao-temporada-membro.png, CT-AUTH-05-todas-as-temporadas-apos-testes.png.

---

### CT-AUTH-06 — Usuário comum alterando o perfil de outro usuário

- Requisito: RF-03
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Token de lucas@example.com (MEMBER) e ID de maria@example.com.

**Procedimento:**

1. Faça login com o Lucas.
2. Envie `PUT /api/users/{id-da-maria}` com o corpo abaixo.
3. Repita usando o ID do próprio Lucas.
4. Confira o perfil dos dois usuários.

**Dados de teste:**

```json
{ "role": "ADMIN" }
```

**Resultado esperado:**
As duas requisições devem retornar 403, já que só um ADMIN pode alterar perfis de acesso. Lucas e Maria devem continuar como MEMBER.

**Situação:** Fail.

**Resultado obtido:**
As duas requisições, feitas com token de MEMBER (usuário lucas), retornaram `200 OK`, após checar o status de ambas as contas com `GET /api/users/me` foi constatado que o perfil foi atualizado para ADMIN.

**Evidências:** CT-AUTH-06-atualizando-usuario-maria-token-membro.png, CT-AUTH-06-atualizando-usuario-lucas-token-membro.png, CT-AUTH-06-obter-perfil-lucas.png, CT-AUTH-06-obter-perfil-maria.png.

Bug: #41

---

### CT-AUTH-07 — Senha salva com hash no banco

- Requisito: RNF-01
- Tipo: API (positivo)
- Prioridade: Média

**Pré-condições:**
Acesso de leitura ao PostgreSQL pelo container.

**Procedimento:**

1. Crie um usuário com a senha senha123 usando `POST /api/auth/register`.
2. Consulte no banco o campo password do usuário criado.
3. Verifique se alguma resposta da API traz o campo password.

**Resultado esperado:**
A senha não pode estar salva em texto puro: deve ser um hash bcrypt (começando com $2b$ e com 60 caracteres). Nenhuma resposta da API deve mostrar o campo password.

**Situação:** Pass.

**Resultado obtido:**
A senha foi salva em hash bcrypt como era esperado (começa com $2b$ e tem 60 caracteres). As respostas da API testadas não mostram o campo password: `POST /api/auth/login` , `GET /api/users/me` , `GET /api/users`, `POST /api/auth/register`.

**Evidências:** CT_AUTH-07-criar-usuario.png, CT-AUTH-07-registro-senha-hash.png, CT-AUTH-07-todas-as-senhas.png.

---

### CT-AUTH-08 — Redefinição de senha

- Requisito: RNF-01
- Tipo: Funcional (positivo)
- Prioridade: Média

**Pré-condições:**
Usuário maria@example.com existente e Mailtrap configurado.

**Procedimento:**

1. Clique em "Esqueci minha senha" (/forgot-password) e informe maria@example.com.
2. Abra o e-mail no Mailtrap e clique no link de redefinição.
3. Defina a nova senha novaSenha123.
4. Faça login usando a nova senha.
5. Tente fazer login com a senha antiga (senha123).
6. Confira a senha no banco de dados.

**Resultado esperado:**
O login com a nova senha deve funcionar e o login com a senha antiga deve falhar. O hash salvo no banco deve ter mudado e continuar no formato bcrypt.

**Situação:** Fail.

**Resultado obtido:**
Foi feito o pedido de redefinição de senha para `maria@example.com` e o e-mail chegou no Mailtrap com o link para redefinir. Depois de definir a nova senha como `novaSenha123`, apareceu o toast "Senha redefinida com sucesso!" e a requisição `POST reset-password` retornou 200. Mesmo assim, o login com a nova senha falhou com 401 e a mensagem "Credenciais inválidas", enquanto o login com a senha antiga (senha123) continuou funcionando normalmente, com 200. Conclusão: a senha não é alterada, mesmo com a mensagem de sucesso.

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

1. Vá para o dashboard.
2. Escolha o arquivo foto-valida-1.jpg.
3. Clique no botão de check-in.
4. Confira a lista dos últimos check-ins.

**Resultado esperado:**
O sistema deve exibir uma mensagem de sucesso. O check-in deve aparecer na lista com a foto, a data atual e o nome do usuário, vinculado à temporada ativa (Temporada 2025.1).

**Situação:** Pass.

**Resultado obtido:**
Logado como Pedro, o check-in com o arquivo `testeJPG.jpeg` mostrou o toast "Check-in realizado com sucesso!". Os cards passaram de 0 para 1 check-in e de 0 para 10 pontos. O check-in apareceu em "Atividade Recente" com a foto, o nome Pedro Costa e a data e hora atuais. A requisição POST `/api/checkins` retornou 201 e o check-in foi registrado na temporada ativa, que nesse caso é a 2025.1. O `photoUrl` era de uma imagem hospedada no Cloudinary.

**Observação:**
O check-in já é criado direto com o status APPROVED e os 10 pontos são creditados na hora, sem nenhuma avaliação de um ADMIN.

**Evidências:** CT-CHK-01-antes.png, CT-CHK-01-apos-checkin.png, CT-CHK-01-modal.png, CT-CHK-01-rede-post.png

---

### CT-CHK-02 — Segundo check-in no dia e foto repetida

- Requisito: RF-04
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Pedro já fez um check-in no dia (CT-CHK-01).

**Procedimento:**

1. Envie `POST /api/checkins` (form-data, campo photo) com a foto foto-valida-2.png.
2. Envie `POST /api/checkins` de novo com a mesma foto-valida-1.jpg.
3. Consulte `GET /api/checkins/my-checkins`.

**Resultado esperado:**
O passo 1 deve ser recusado (400 ou 409) com um aviso de que o limite diário de check-ins foi atingido. O passo 2 deve ser recusado com uma mensagem de que essa foto já foi enviada. O Pedro deve continuar com apenas um check-in no dia.

**Situação:** Fail.

**Resultado obtido:**
O passo 1 foi aceito com status `201 Created` e com a mensagem `"Check-in realizado com sucesso"`. O passo 2 também foi aceito com a mesma mensagem.

**Evidências:** CT_CHK-02-primeiro-check-in-pedro.png, CT-CHK-02-login-pedro.png, CT-CHK-02-segundo-checkin-foto-diferente.png, CT-CHK-02-terceiro-checkin-foto-igual.png.

Bug: #35

---

### CT-CHK-03 — Status inicial do check-in

- Requisito: RF-05
- Tipo: Funcional (positivo)
- Prioridade: Alta

**Pré-condições:**
Logado como maria@example.com, sem check-in no dia.

**Procedimento:**

1. Faça um check-in pelo dashboard com uma imagem válida.
2. Confira o status mostrado no card do check-in.

**Resultado esperado:**
O check-in deve aparecer como "Pendente" e só mudar para "Aprovado" depois da avaliação de um ADMIN.

**Situação:** Fail.

**Resultado obtido:**
O check-in feito no CT-CHK-01 (Pedro, TRAINEE) foi criado direto com o status "Aprovado", sem passar por "Pendente". A requisição POST `/api/checkins` retornou 201 com `"status": "APPROVED"` e `"points": 10`, e os pontos foram creditados na hora, sem aprovação de um ADMIN. Logado como ADMIN, não existe nenhuma opção na interface para aprovar ou rejeitar check-ins, o card só mostra o status e o botão de excluir.

**Observação:**
Executado com a evidência do CT-CHK-01, usando os dados do Pedro no lugar dos da Maria, já que o comportamento não depende do usuário.

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

1. Usando o token do MEMBER, envie `PUT /api/checkins/{id}` com `{ "status": "APPROVED" }`.
2. Usando o token do ADMIN, envie a mesma requisição.
3. Consulte `GET /api/checkins/{id}`.

**Resultado esperado:**
A requisição do MEMBER deve retornar 403 e o status deve continuar PENDENTE. A requisição do ADMIN deve retornar 200 e o status deve mudar para APPROVED.

**Situação:** Pass.

**Resultado obtido:**
A requisição do MEMBER retornou `403 Forbidden` com a mensagem: `Sem permissão para acessar esse recurso` e o status continuou `PENDING`. A requisição do ADMIN retornou `200 OK` e o status mudou para `PENDING` sem problemas. O contrário foi testado também e o status mudou para `APPROVED` porém não foi adicionado às evidências.

**Observação:**
Como todo check-in já é criado como `APPROVED` (bug #34, CT-CHK-03), o check-in foi colocado como PENDING pelo ADMIN antes da execução, com o endpoint `PUT /api/checkins/{id}`.
A coleção do Postman não tem essa requisição, mesmo ela existindo no backend, então foi criada manualmente.

**Evidências:** CT-CHK-04-confirmacao-de-status-apos-tentativa-com-token-MEMBER.png, CT-CHK-04-confirmacao-de-troca-para-pending.png, CT-CHK-04-obtencao-id-checkin-approved.png, CT-CHK-04-troca-de-approved-para-pending-admin.png, CT-CHK-04-usuario-lucas-nao-consegue-alterar-status.png.

---

### CT-CHK-05 — Visualizar check-in de outro usuário

- Requisito: RF-06
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Lucas e Maria com pelo menos um check-in cada, token do Lucas e ID de um check-in da Maria.

**Procedimento:**

1. Com o token do Lucas, envie `GET /api/checkins/{id-checkin-da-maria}`.
2. Com o token do Lucas, envie `GET /api/checkins`.

**Resultado esperado:**
O passo 1 deve retornar 403 (ou 404), sem os dados do check-in da Maria. A lista do passo 2 não deve trazer check-ins de outros usuários.

**Situação:** Fail.

**Resultado obtido:**
O passo 1 retornou `200 OK`, com todos os dados do check-in da Maria. A lista do passo 2 trouxe todos os check-ins de usuários.

**Evidências:** CT-CHK-05-checkin-da-maria-conta-do-lucas.png, CT-CHK-05-checkins-gerais-lucas.png, CT-CHK-05-login-com-lucas.png, CT-CHK-05-pegando-ids-checkin-com-ADM.png.

Bug: #33

### CT-CHK-06 — Excluir check-in de outro usuário pela interface

- Requisito: RF-06
- Tipo: Funcional (negativo)
- Prioridade: Alta

**Pré-condições:**
Logado como lucas@example.com e com check-ins de outros usuários cadastrados.

**Procedimento:**

1. Acesse o dashboard.
2. Procure check-ins de outros usuários na tela.
3. Verifique se aparecem opções de editar ou excluir nesses check-ins.

**Resultado esperado:**
O usuário não deve conseguir editar ou excluir check-ins que não são dele. Esses botões não devem aparecer para check-ins de outros usuários.

**Situação:** Fail.

**Resultado obtido:**
Logado como Lucas, a seção "Atividade Recente" mostrou 3 check-ins (1 da Maria Santos e 2 do Lucas Silva), todos com data, pontuação e status "Aprovado". Nenhum card mostrou botão de editar ou excluir, e não tem nenhuma ação escondida ao clicar. Porém, o usuário consegue visualizar check-ins que não são dele, o que viola a RF-06.
Logado como ADMIN, os mesmos cards mostram o botão de excluir, o que confirma que a opção existe e está restrita ao ADMIN, sem problemas.

**Observação:**
A requisição `/api/checkins` devolve para qualquer usuário os check-ins de todos os usuários, junto com e-mail e ID.

**Evidências:** CT-CHK-06-dashboard-lucas.png, CT-CHK-06-dashboard-admin.png, CT-CHK-06-rede-checkin.png

Bug: #33

---

### CT-CHK-07 — Envio de arquivo inválido

- Requisito: RNF-02 / RF-04
- Tipo: API (negativo)
- Prioridade: Média

**Pré-condições:**
Token válido e acesso ao container do backend.

**Procedimento:**

1. Liste a pasta de uploads: `docker-compose exec backend ls uploads/`.
2. Envie `POST /api/checkins` com arquivo.pdf.
3. Liste a pasta uploads/ de novo.

**Resultado esperado:**
O envio deve retornar 400 com uma mensagem clara (tipo de arquivo não permitido), e não 500. A pasta uploads/ deve continuar igual à do passo 1.

**Situação:** Fail.

**Resultado obtido:**
Ao enviar o arquivo, o status foi `500 Internal Server Error` e retornou uma mensagem clara descrevendo o erro: `Apenas imagens são permitidas`, Ao invés de um erro `4xx`. Por outro lado a pasta uploads continua igual, e o arquivo ainda é recusado.

**Evidências:** CT-CHK-07-login-para-teste.png, CT-CHK-07-teste-envio-PDF.png.

Bug: #39

---

### CT-CHK-08 — Arquivo temporário após falha no envio para a nuvem

- Requisito: RNF-02
- Tipo: API (negativo)
- Prioridade: Média

**Pré-condições:**
Credencial do Cloudinary alterada de propósito no .env (voltar ao normal depois) e container reiniciado.

**Procedimento:**

1. Liste a pasta uploads/ no container do backend.
2. Envie `POST /api/checkins` com uma imagem válida.
3. Liste a pasta uploads/ de novo.
4. Restaure a credencial correta, faça um check-in válido e liste uploads/.

**Resultado esperado:**
O erro do passo 2 deve ser tratado com uma mensagem amigável. Nenhum arquivo novo deve ficar na pasta uploads/, nem no caso de falha nem no de sucesso.

**Situação:** Fail.

**Resultado obtido:**
Com a credencial do Cloudinary alterada no env, `POST /api/checkins` retornou `500 Internal Server Error` com a mensagem "Falha no Upload da Imagem", e o log mostrou "Erro no upload para Cloudinary".
A pasta uploads/, que estava vazia, ficou com o arquivo `photo-1794158396688-40722033.jpg` depois da falha.
Com a credencial restaurada, o check-in válido funcionou e não deixou arquivo novo na pasta.

**Evidências:** CT-CHK-08-uploads-antes.png, CT-CHK-08-resposta-500.png, CT-CHK-08-arquivo-salvo-apos-upload-com-erro.png, CT-CHK-08-checkin-apos-restauracao.png, CT-CHK-08-uploads-apos-restaurar.png.

Bug: #42

---

## Sistema de pontos

### CT-PTS-01 — Pontos somados após check-in aprovado

- Requisito: RF-07
- Tipo: Funcional (positivo)
- Prioridade: Alta

**Pré-condições:**
Pedro sem check-in no dia e pontuação atual dele anotada no ranking (X).

**Procedimento:**

1. Logado como Pedro, faça um check-in.
2. Logado como ADMIN, aprove o check-in.
3. Logado como Pedro, acesse o ranking (/ranking).

**Resultado esperado:**
A pontuação do Pedro deve ser X + 10. A posição no ranking deve refletir o novo total sem nenhuma ação manual.

**Situação:** Pass.

**Resultado obtido:**
Depois do check-in, a pontuação do Pedro foi de 0 para 10 (ganhou 10 pontos). No ranking, consultado como ADMIN (o Pedro, como TRAINEE, não tem acesso, então o passo 3 foi adaptado), o Pedro aparece com 10 pontos e 1 check-in, na 3ª posição, sem nenhuma ação manual.
Ordem do ranking: Lucas (20), Maria (10), Pedro (10). O Pedro empata com a Maria e aparece depois dela. As outras posições vêm do seed do próprio projeto.

**Observação:**
Não foi possível executar o passo 2 (aprovação pelo ADMIN), porque não existe fluxo de aprovação e o check-in já é criado aprovado. Esse problema já está no bug #34 (RF-05).

**Evidências:** CT-PTS-01-dashboard-pedro-antes.png, CT-PTS-01-dashboard-pedro-depois.png, CT-PTS-01-ranking-admin-depois.png

---

### CT-PTS-02 — Check-in rejeitado não soma pontos

- Requisito: RF-07 / RF-05
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Token de ADMIN e um usuário com check-in APPROVED (todo check-in já nasce aprovado, ver bug #34).

**Procedimento:**

1. Enviar `GET /api/rankings` e anote o totalPoints do usuário (X).
2. Como ADMIN, enviar `PUT /api/checkins/{id}` com `{ "status": "REJECTED" }`.
3. Enviar `GET /api/rankings` de novo.

**Resultado esperado:**
O totalPoints do usuário deve passar a ser X − 10, já que um check-in rejeitado não deve contar pontos.

**Situação:** Fail.

**Resultado obtido:** O totalPoints do usuário (`lucas`, 20 pontos) não foi alterado mesmo após mudar o status do check-in para `REJECTED` (continuou com 20 pontos).

**Observações:** O plano anterior para a CT-PTS-02 girava em torno de os check-ins iniciarem pendentes. Considerando o BUG #34, o teste foi modificado, já que iniciam aprovados (`APPROVED`).

**Evidências:** CT-PTS-02-seed-executada.png, CT-PTS-02-id-checkin-lucas.png, CT-PTS-02-pontuacao-lucas-antes.png, CT-PTS-02-status-checkin-lucas-atualizado.png, CT-PTS-02-pontuacao-lucas-depois.png

Bug: #40

---

### CT-PTS-03 — Exclusão de check-in pela API

- Requisito: RF-08
- Tipo: API (negativo)
- Prioridade: Alta

**Pré-condições:**
Usuário com um check-in aprovado (10 pontos) e token de ADMIN (Teste executado a partir da seed).

**Procedimento:**

1. Envie `GET /api/rankings` e anote o totalPoints (X) e o checkInsCount (N) do usuário.
2. Como ADMIN, envie `DELETE /api/checkins/{id}`.
3. Envie `GET /api/rankings` de novo.

**Resultado esperado:**
A exclusão deve retornar 200. O totalPoints deve passar para X − 10 e o checkInsCount para N − 1.

**Situação:** Fail.

**Resultado obtido:**
A exclusão retornou `200 OK`. O totalPoints de lucas continuou como X (20 pontos) ao em vez de X - 10 (10 pontos) e o checkInsCount continuou como N(`2`) e não diminuiu.

**Evidências:** CT-PTS-03-lucas-totalPoints-checkInsCount-antes.png, CT-PTS-03-delete-checkin-lucas.png, CT-PTS-03-lucas-totalPoints-checkInsCount-depois.png.

Bug: 36

---

### CT-PTS-04 — Ranking na tela após exclusão de check-in

- Requisito: RF-08
- Tipo: Funcional (negativo)
- Prioridade: Média

**Pré-condições:**
Mesmo cenário do CT-PTS-03, feito pela interface.

**Procedimento:**

1. Acesse o ranking e anote os pontos e a posição do usuário.
2. Como ADMIN, exclua o check-in desse usuário pelo dashboard.
3. Recarregue o ranking.

**Resultado esperado:**
Os pontos mostrados devem diminuir 10. A posição deve ser recalculada se outro usuário passar a ter mais pontos.

**Situação:** Fail.

**Resultado obtido:**
Logado como ADMIN, os dois check-ins do Lucas foram excluídos pelo dashboard. Os cards sumiram da seção "Atividade Recente", porém o ranking continuou mostrando o Lucas com 20 pontos e 2 check-ins, mesmo depois de recarregar a página.
No dashboard do Lucas, o número de check-ins passou para 0, como deveria, mas os pontos continuaram em 20.
`DELETE /checkins` retornou 200 e `GET /rankings` continuou mostrando os mesmos `totalPoints` e `checkInsCount`.

**Evidências:** CT-PTS-04-dashboard-lucas.png, CT-PTS-04-exclusao.png, CT-PTS-04-ranking-antes.png, CT-PTS-04-ranking-depois.png

Bug: #36

---

### CT-PTS-05 — Ordem do ranking

- Requisito: RF-09
- Tipo: API (positivo)
- Prioridade: Média

**Pré-condições:**
Pelo menos 3 usuários com pontuações diferentes na temporada ativa.

**Procedimento:**

1. Envie `GET /api/rankings`.
2. Compare o totalPoints de cada item com o do item seguinte.
3. Abra o ranking na interface e compare a ordem com a da API.

**Resultado esperado:**
A API deve retornar 200 com os usuários em ordem decrescente de pontuação. A interface deve mostrar a mesma ordem.

**Situação:** Pass.

**Resultado observado:**
Executar a rota `GET /api/rankings` via Postman retornou Status `200 OK`, o corpo da resposta mostra os pontos e a ordem dos usuários, que estão iguais aos mostrados na interface( Ordem decrescente: Lucas (20), Maria (10) e Pedro (0) ).

**Observação:** executado logo após o seed, antes dos outros testes de API.

**Evidências:** CT-PTS-05-interface-rankings.png, CT-PTS-05-resposta-rankings.png

---

### CT-PTS-06 — Check-ins com intervalo menor que 24 horas

- Requisito: RF-09
- Tipo: Funcional (negativo)
- Prioridade: Alta

**Pré-condições:**
Usuário com um check-in feito há menos de 24 horas, incluindo o caso de virada de dia (ex.: 23h50 e 00h10).

**Procedimento:**

1. Logado como esse usuário, tente um novo check-in pelo dashboard com outra imagem.
2. Confira a mensagem exibida e o ranking.

**Resultado esperado:**
O sistema deve recusar o check-in e informar o intervalo mínimo. A pontuação do usuário não deve mudar.

**Situação:** Fail.

**Resultado obtido:**
Logado como Pedro, com um check-in feito 3 minutos antes, um novo check-in com outra imagem foi aceito. O sistema mostrou o toast "Check-in realizado com sucesso!" e os cards passaram de 1 para 2 check-ins e de 10 para 20 pontos. A requisição POST `/api/checkins` retornou 201. Nenhuma mensagem sobre intervalo mínimo apareceu.

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
- O login dos usuários que já existem (seed) deve continuar funcionando.

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
