# **Documento de Requisitos: Projeto NaSalinha**

## **1\. Módulo de Autenticação e Acesso (JWT)**

**RF-01: Cadastro e Verificação**

- O sistema deve permitir o registro via Nome, E-mail e Senha.
- **Fluxo de Ativação:** Após o registro, o sistema deve gerar um **código de verificação** único e enviá-lo ao e-mail do usuário.
- O status inicial da conta deve ser `PENDENTE`.

**RF-02: Restrição de Login**

- O sistema deve **bloquear o acesso** (Login) de qualquer usuário que não tenha confirmado o código de verificação enviado por e-mail.
- **Mensagem de Erro:** Caso o código não tenha sido inserido, o sistema deve retornar: _"Por favor, verifique sua conta para continuar"_.

**RF-03: Controle de Níveis (RBAC)**

- O sistema deve restringir o acesso a endpoints de gestão (Temporadas e Moderação) exclusivamente para usuários com perfil ADMINISTRADOR.

**RNF-01: Segurança de Dados**

- O sistema deve realizar o hashing de senhas antes da persistência no banco de dados.

---

## **2\. Módulo de Check-in (Mídia)**

**RF-04: Registro de Atividade**

- O sistema deve permitir que o usuário realize um check-in mediante o upload de uma imagem.
- O sistema deve associar o check-in à temporada configurada como ativa no momento da requisição.
- O sistema deve permitir a realização de apenas um check-in por dia.
- O sistema deve restringir o envio de uma mesma foto repetidas vezes.

**RF-05: Fluxo de Status do Check-in**

- O sistema deve atribuir o status inicial **PENDENTE** a todo novo check-in realizado.
- O sistema deve permitir que apenas um Administrador altere o status do check-in (Aprovado/Rejeitado).

**RF-06: Restrição de Propriedade**

- O sistema deve impedir que um usuário visualize ou manipule (editar/deletar) check-ins que não pertençam ao seu próprio ID de usuário.

**RNF-02: Integridade de Arquivos**

- O sistema deve garantir que arquivos temporários de upload sejam removidos do servidor após o processamento para o provedor de nuvem.

---toda

## **3\. Módulo de Pontuação e Ranking**

**RF-07: Atribuição de Pontos**

- O sistema deve somar os pontos ao saldo do usuário e atualizar o ranking automaticamente.

**RF-08: Consistência de Saldo**

- O sistema deve realizar a subtração automática dos pontos do saldo total do usuário caso o check-in correspondente seja removido do sistema.

**RF-09: Regras de Ranking**

- O sistema deve exibir o ranking ordenado por pontuação total (decrescente).
- O sistema deve impedir a realização de múltiplos check-ins pelo mesmo usuário em um intervalo inferior a 24 horas.
