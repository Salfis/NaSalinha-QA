# Desafio QA: Ecossistema NaSalinha (Comp Júnior)

Este repositório contém o ambiente de homologação do projeto **NaSalinha**, um sistema de check-in gamificado.

> Nota de Liderança (Gestão 2026.1)
Este ambiente foi preparado especificamente para o treinamento de novos Analistas de Quality Assurance. O sistema contém **inconsistências propositais** para testar sua capacidade de auditoria, configuração de ambiente e reporte de bugs.


## Créditos de Desenvolvimento
O projeto original foi desenvolvido por **Lucas Henrique Lopes Costa** (Ex-Trainee da Comp Júnior) como parte de sua trilha de capacitação técnica. 
A manutenção atual e a coordenação deste desafio são de responsabilidade da **Diretoria de Projetos**.

---

## O Objetivo do Treinamento
Sua missão como trainee de QA é atuar como a última linha de defesa antes do "deploy" em produção:
1. **Mapear Bugs:** Encontrar falhas de segurança, erros de pontuação e problemas de interface.
2. **Configuração de Infra:** Garantir que todos os serviços externos estejam integrados corretamente.
3. **Validar Regras de Negócio:** Garantir que permissões de usuário (Admin vs Trainee) e cálculos de ranking estejam íntegros.

---

## Tecnologias Utilizadas
* **Backend:** Node.js, Express, Prisma ORM.
* **Frontend:** React 18, TailwindCSS.
* **Banco de Dados:** PostgreSQL (via Docker).
* **Serviços:** Cloudinary (Imagens) e Nodemailer/Mailtrap (E-mails).

---

## Como Executar o Projeto

### 1. Preparação
Certifique-se de ter o **Docker** e **Git** instalados.

### 2. Configuração de Variáveis (O Primeiro Desafio)
Vá até a pasta `/backend`, copie o arquivo `.env.example` para um novo arquivo `.env`.

>important Configuração de Chaves Obrigatória
Para que o sistema funcione, você deve criar suas próprias contas (gratuitas) nos serviços abaixo:
* **E-mails:** Utilize o [Mailtrap](https://mailtrap.io/) (Sandbox).
* **Fotos:** Utilize o [Cloudinary](https://cloudinary.com/).

Preencha as credenciais no seu `.env`. Identificar se o erro é de **configuração** ou de **código** faz parte do seu teste!


### 3. Execução com Docker
Na raiz do projeto, suba os containers:
```bash
docker-compose up --build
```

Rode o comando para executar as migrations e seeders do backend:

```bash
docker-compose exec backend npx prisma migrate dev --name init
docker-compose exec backend npx prisma db seed
```
FRONTEND_URL=http://localhost:3000

## Níveis de Usuário

- **Admin** - Acesso total ao sistema, gerenciamento de temporadas
- **Membro** - Check-ins, visualização de ranking
- **Trainee** - Check-ins e pontuação

## Principais Endpoints

- **Auth**: `/api/auth/register`, `/api/auth/login`
- **Users**: `/api/users` (CRUD completo)
- **Check-ins**: `/api/checkins` (CRUD completo)
- **Rankings**: `/api/rankings`
- **Seasons**: `/api/seasons` (CRUD completo - Admin only)

## Estrutura do Banco de Dados

### Entidades Principais

1. **Users** - Dados dos usuários (nome, email, senha hash, role)
2. **CheckIns** - Registros de check-in com foto
3. **Seasons** - Temporadas de competição
4. **Points** - Pontuação dos usuários

### Relacionamentos

- User → CheckIns (1:N)
- Season → CheckIns (1:N)
- User → Points → Season (N:N através de Points)

## Segurança

- Senhas criptografadas com bcrypt
- Autenticação JWT com refresh tokens
- Rate limiting para prevenir abuso
- Validação de dados com Joi
- Headers de segurança com Helmet
- CORS configurado adequadamente

## Sistema de E-mails

- Confirmação de cadastro
- Recuperação de senha

# Quality Assurance

Durante a trilha de QA, esse desafio permitirá desenvolver competências e a validar os conhecimentos na área. Vou encontrar inconsistências, avaliar o funcionamento do sistema, validar as 3 funções principais e registrar problemas encontrados.

## Escopo dos Testes

1- **Autenticação JWT:** Verificar a validação de usuários, o acesso indevido de usuários a informações protegidas e possíveis falhas relacionadas às permissões de cada perfil.
2- **Check-in por foto:** Testar a interface do Check-in, comportamento diante de envios incompletos ou arquivos incompatíveis, persistência de check-in e a transmissão de informações entre telas.
3-**Sistema de pontos:** Validar se a pontuação fornecida é a correta em todos os casos, checar por valores não usuais, persistência da pontuação entre telas e em casos de exclusão de check-ins/ pontuação entre temporadas.

## Ferramentas

- **Docker:** Executar o ambiente local do sistema.
- **Chrome DevTools:** Verificar requisições da API, respostas, status HTTP e comportamento da interface.
- **Postman:** Testar chamadas à API e validar suas respostas.
- **GitHub:** Hospedar o repositório, compartilhar arquivos e realizar versionamento.
- **GitHub Issues:** Registrar e acompanhar os problemas encontrados durante o QA.
- **GitHub Projects:** Organizar casos de teste, tarefas e o andamento do trabalho.

## Tipos de Teste

- **Testes Funcionais:** Verificar se as funcionalidades do sistema apresentam o comportamento esperado de acordo com suas regras.
- **Testes de UI:** Verificar se os elementos da interface, como botões, formulários, mensagens e navegação, funcionam corretamente.
- **Testes de API:** Realizar chamadas diretamente aos endpoints da API para verificar respostas, status HTTP, dados retornados, autenticação e permissões.
- **Testes de Regressão:** Reexecutar testes após alterações ou correções para verificar se funcionalidades que já funcionavam continuam funcionando corretamente.

## Organização dos Testes

- **GitHub Projects:** Organização e acompanhamento dos casos de teste e tarefas do projeto.
- **GitHub Issues:** Registro e acompanhamento dos bugs encontrados durante os testes.
- **Postman:** Execução dos testes de API utilizando a coleção que já foi disponibilizada em `docs/postman_NaSalinha.json`.
