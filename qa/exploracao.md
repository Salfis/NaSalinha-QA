# Exploração do Sistema — NaSalinha

## Testes automatizados existentes

### Frontend

- Framework: Jest + React Testing Library
- Suítes executadas: 9
- Testes executados: 85
- Testes aprovados: 85
- Testes falhos: 0

### RF-01 — Cadastro e verificação

**Comportamento observado:**

**Resultado esperado:**
O sistema deveria enviar um email com um código de verificação único para o usuário.
O status inicial da conta deve ser PENDENTE.

**Resultado observado:**
O usuário recebe um email de boas vindas com um botão para ser redirecionado a página de login, sem código de verificação.

- Cadastro realizado com sucesso.
- E-mail recebido no Mailtrap.
- Sistema redirecionou para a tela de login.
- Nenhuma etapa de código foi mostrada.

**Situação:** Não conforme.

**Próxima verificação:**

- Conferir conteúdo do e-mail.
- Verificar se uma conta não confirmada consegue realizar login.
- Investigar o status inicial da conta.

**Evidências**

- RF-01-email-sem-codigo.png

### RF-02 — Restrição de Login

**Resultado esperado:**
O sistema deve bloquear o login de usuários que não confirmaram o e-mail, apresentando a mensagem ao usuário: "Por favor, verifique sua conta para continuar".

**Resultado observado:**
Após realizar o cadastro, o usuário recebeu apenas um e-mail de boas-vindas, sem código de verificação.

Mesmo sem realizar qualquer confirmação, foi possível autenticar-se e acessar normalmente o dashboard.

**Situação:** Não Conforme.

**Evidências:**

- RF-02-login-sem-verificacao.png

### RF-03 — Controle de Níveis (RBAC)

**Resultado esperado:**
Apenas usuários ADMIN devem acessar funcionalidades
e endpoints de gestão administrativa.

**Resultado observado:**

- ADMIN: acesso permitido à página de Gerenciamento de Temporadas.
- MEMBER: acesso direto à URL resultou em redirecionamento para o dashboard.
- TRAINEE: acesso direto à URL resultou em redirecionamento para o dashboard.

**Situação:** Conforme na interface.
Validação dos endpoints administrativos pendente.

**Observação:**
O redirecionamento demonstra a proteção da rota no frontend, mas não garante que o backend rejeite requisições administrativas de usuários sem permissão.

### RNF-01 — Segurança de Dados

**Resultado esperado:**
O sistema deve realizar o hashing das senhas e armazená-las no banco de dados.

**Procedimento:**
Consulta somente de leitura ao PostgreSQL, verificando o tamanho e o prefixo dos valores armazenados no campo password.

**Resultado observado:**

- 3 registros analisados.
- Todos apresentaram 60 caracteres.
- Todos apresentaram o prefixo $2b$.
- Os valores são compatíveis com hashes bcrypt.

**Situação:** Conforme na amostra analisada.

**Observação:**
A consulta não comprova que todos os fluxos de criação ou alteração de senha estão conformes.
