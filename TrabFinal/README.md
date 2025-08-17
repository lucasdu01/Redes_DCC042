# 🎯 CHAT CRIPTOGRAFADO - TRABALHO FINAL DCC042
## Sistema de Comunicação Segura em Tempo Real com Múltiplos Grupos

---

## 📖 **VISÃO GERAL**

Sistema de chat multiusuário com **criptografia automática** e **múltiplos grupos de conversa** implementado em Python usando sockets TCP. Demonstra conceitos fundamentais de redes de computadores, programação concorrente e segurança da informação aplicados em uma aplicação prática e funcional.

### **Principais Funcionalidades**
- 🔐 **Criptografia automática** AES-256 para todas as mensagens
- 🗂️ **3 grupos de conversa** independentes com chaves distintas
- 👥 **Chat multiusuário** com suporte a múltiplos clientes simultâneos
- 🔄 **Troca dinâmica** entre grupos durante a sessão
- 🛡️ **Isolamento total** entre grupos (mensagens não cruzam)

### **Estrutura do Projeto**
```
TrabFinal/
├── 📄 chat_server.py			# Servidor multithread com suporte a grupos
├── 📄 chat_client.py           # Cliente com seleção e troca de grupos  
├── 📄 crypto_utils.py          # Módulo criptografia AES-256 multigrupo
├── 📄 requirements.txt			# Dependências Python
├── 📄 test_chat.py				# Testes automatizados
└── 📄 README.md				# Esta documentação
```

---

## 🎯 **IDEIA E OBJETIVOS**

### **Conceito Central**
Criar um sistema de comunicação que combine:
- **Comunicação em rede** usando protocolos TCP
- **Programação concorrente** com threading
- **Segurança de dados** através de criptografia simétrica
- **Múltiplos grupos** de conversa com isolamento criptográfico
- **Interface amigável** para demonstração prática

### **Aplicação dos Conceitos da Disciplina**
- ✅ **Sockets TCP** - Comunicação cliente-servidor confiável
- ✅ **Threading** - Servidor concorrente para múltiplos clientes
- ✅ **Protocolos de aplicação** - Handshake, seleção de grupo e formato de mensagens
- ✅ **Tratamento de conexões** - Gerenciamento robusto de sessões
- ✅ **Roteamento de mensagens** - Broadcast seletivo por grupo
- ✅ **Plus: Segurança em redes** - Criptografia AES-256 com chaves independentes

---

## ⚙️ **FUNCIONAMENTO TÉCNICO**

### **Arquitetura do Sistema**
```
        GRUPO 1 (g1)     GRUPO 2 (g2)     GRUPO 3 (g3)
           |                 |                 |
Cliente A ←→ [AES-256] ←→ SERVIDOR ←→ [AES-256] ←→ Cliente D
Cliente B ←→ [AES-256] ←→    ↓    ←→ [AES-256] ←→ Cliente E
Cliente C ←→ [AES-256] ←→ Threading  ←→ [AES-256] ←→ Cliente F
           |              Broadcast             |
       Chave: "g1"         por Grupo       Chave: "g3"
```

### **Fluxo de Operação**
1. **Servidor** inicia e aguarda conexões na porta 12345
2. **Clientes** conectam via socket TCP e fazem autenticação
3. **Seleção de grupo** - Cliente escolhe grupo (1, 2 ou 3) na conexão
4. **Mensagens** são criptografadas com a chave específica do grupo
5. **Servidor** descriptografa, processa e redistribui apenas para o grupo correto
6. **Threading** permite múltiplos usuários simultâneos em todos os grupos
7. **Troca de grupo** - Cliente pode mudar de grupo dinamicamente

### **Componentes Principais**

#### **🖥️ Servidor (`chat_server.py`)**
- **Threading**: Uma thread por cliente conectado
- **Grupos independentes**: Gerencia 3 grupos com chaves criptográficas distintas
- **Broadcast seletivo**: Redistribui mensagens apenas para clientes do mesmo grupo
- **Mudança dinâmica**: Processa solicitações de troca de grupo em tempo real
- **Criptografia**: Descriptografa/re-criptografa com a chave correta de cada grupo
- **Comandos**: `status`, `quit`, `help` via terminal
- **Logs**: Registro detalhado com identificação de grupos

#### **💻 Cliente (`chat_client.py`)**
- **Seleção inicial**: Escolhe grupo (1, 2 ou 3) ao conectar
- **Troca dinâmica**: Comando `/grupo N` para mudar de grupo durante a sessão
- **Interface**: Terminal interativo com comandos especiais expandidos
- **Criptografia**: Transparente ao usuário, ajustada automaticamente por grupo
- **Comandos**: `/help`, `/quit`, `/status`, `/clear`, `/grupo N`
- **Status detalhado**: Mostra grupo atual na visualização de status

#### **🔐 Criptografia (`crypto_utils.py`)**
- **Múltiplas chaves**: Suporte a senhas diferentes por grupo (g1, g2, g3)
- **Algoritmo**: AES-256 via biblioteca Fernet
- **Derivação**: PBKDF2 com SHA-256 (100.000 iterações)
- **Troca dinâmica**: Permite alterar senha/chave em tempo real
- **Encoding**: Base64 para transmissão via socket
- **Testes**: Validação automática incluída

---

## 🚀 **COMO INICIAR E USAR**

### **Pré-requisitos**
```bash
# Instalar dependências
pip install -r requirements.txt
```

### **Passo 1: Iniciar Servidor**
```bash
python chat_server.py
```
**Saída esperada:**
```
🚀 Servidor de Chat Criptografado iniciado em localhost:12345
🔐 Criptografia ativada - todas as mensagens são criptografadas
👥 Aguardando conexões...
💡 Digite 'status' para ver usuários, 'quit' para sair

Server> 
```

**Comandos do servidor:**
- `status` → Mostra usuários conectados
- `quit` ou `exit` → Encerra o servidor
- `help` → Lista comandos
- `Ctrl+C` → Força encerramento

### **Passo 2: Conectar Clientes**
```bash
python chat_client.py
```

**Fluxo de conexão:**
1. Sistema solicita nome de usuário (mín. 2 caracteres)
2. Sistema solicita escolha do grupo (1, 2 ou 3)
3. Conecta automaticamente ao servidor local no grupo escolhido
4. Interface de chat fica disponível

**Comandos do cliente:**
- `/help` → Lista comandos disponíveis
- `/quit` → Sair do chat
- `/status` → Informações da conexão e grupo atual
- `/clear` → Limpar tela
- `/grupo N` → **NOVO**: Trocar para o grupo N (1, 2 ou 3)
- Qualquer outra coisa → Enviada como mensagem

### **Exemplo Prático - Múltiplos Grupos**

**Terminal 1 (Servidor):**
```
Server> status
📊 Status do Servidor:
   🌐 Endereço: localhost:12345
   👥 Clientes conectados: 4
   📋 Usuários online por grupo:
      🗂️  Grupo 1: 2 usuários
         - Alice (127.0.0.1:52341)
         - Bob (127.0.0.1:52342)
      🗂️  Grupo 2: 1 usuários
         - Charlie (127.0.0.1:52343)
      🗂️  Grupo 3: 1 usuários
         - Diana (127.0.0.1:52344)
```

**Terminal 2 (Alice - Grupo 1):**
```
🗂️  Escolha o grupo (1, 2 ou 3): 1
✅ Conectado ao chat como 'Alice'!
🗂️  Grupo atual: 1
[Alice] Olá pessoal do Grupo 1!
[14:30:25] Bob: Oi Alice, só nós aqui no grupo 1!
[Alice] /grupo 2
🔄 Grupo alterado de 1 para 2
[Alice] Agora estou no grupo 2
[14:31:10] Charlie: Bem-vinda ao grupo 2, Alice!
```

**Terminal 3 (Bob - Grupo 1):**
```
🗂️  Escolha o grupo (1, 2 ou 3): 1
[14:30:20] Alice: Olá pessoal do Grupo 1!
[Bob] Oi Alice, só nós aqui no grupo 1!
[14:30:45] 📢 Alice saiu do grupo!
[Bob] Alice foi para outro grupo
```

**Terminal 4 (Charlie - Grupo 2):**
```
🗂️  Escolha o grupo (1, 2 ou 3): 2
[14:31:05] 📢 Alice entrou no grupo!
[14:31:08] Alice: Agora estou no grupo 2
[Charlie] Bem-vinda ao grupo 2, Alice!
```

---

## 🎓 **CONCEITOS DE REDES DEMONSTRADOS**

### **1. Programação com Sockets TCP**
- **Criação de sockets** cliente e servidor
- **Binding e listening** na porta 12345
- **Accept/Connect** para estabelecer conexões
- **Send/Recv** para transmissão de dados
- **Tratamento de exceções** de socket

### **2. Threading e Concorrência**
- **Servidor multithread** - uma thread por cliente
- **Sincronização** de acesso aos dados compartilhados
- **Daemon threads** para limpeza automática
- **Thread safety** no broadcast de mensagens

### **3. Protocolos de Aplicação**
- **Handshake personalizado** para autenticação
- **Seleção de grupo** durante o estabelecimento da conexão
- **Protocolo de mudança de grupo** em tempo real
- **Formato estruturado** de mensagens por grupo
- **Comandos especiais** vs mensagens normais
- **Estados de conexão** (conectado/desconectado/mudando grupo)

### **4. Segurança em Redes**
- **Criptografia simétrica** AES-256 com múltiplas chaves
- **Isolamento criptográfico** entre grupos
- **Derivação segura de chaves** PBKDF2 independente por grupo
- **Proteção de dados em trânsito** com chaves específicas
- **Transparência para o usuário** com segurança robusta

### **5. Tratamento de Erros em Rede**
- **Timeout em sockets** para evitar bloqueios
- **Detecção de desconexões** abruptas
- **Limpeza de recursos** (sockets, threads)
- **Recuperação automática** quando possível

---

## 📊 **INFORMAÇÕES TÉCNICAS RELEVANTES**

### **Performance e Escalabilidade**
- **Concorrência**: Suporta múltiplos clientes simultâneos em 3 grupos
- **Threading**: Modelo thread-per-client com isolamento por grupo
- **Timeout**: 1 segundo no accept() para responsividade
- **Broadcast eficiente**: Mensagem processada uma vez e enviada apenas para o grupo correto

### **Segurança Implementada**
- **Algoritmo**: AES-256 (padrão militar) para cada grupo
- **Modo**: CBC com autenticação HMAC
- **Key Derivation**: PBKDF2-SHA256 (100k iterações)
- **Chaves independentes**: g1, g2, g3 para isolamento total
- **Limitação**: Chaves compartilhadas fixas por grupo (educacional)

### **Robustez do Sistema**
- **Detecção automática** de clientes desconectados
- **Limpeza de recursos** em caso de erro
- **Logs detalhados** para debugging
- **Tratamento gracioso** de Ctrl+C

---

## 🧪 **TESTES E VALIDAÇÃO**

### **Teste da Criptografia**
```bash
python crypto_utils.py
# Saída: "Teste PASSOU - Criptografia funcionando!"
```

### **Teste Completo do Sistema**
```bash
python test_chat.py
# Executa bateria completa de testes automatizados
```

### **Cenários Testados**
- ✅ **Múltiplos clientes** conectando simultaneamente em diferentes grupos
- ✅ **Mensagens criptografadas** funcionando corretamente por grupo
- ✅ **Isolamento entre grupos** - mensagens não cruzam grupos
- ✅ **Broadcast seletivo** chegando apenas aos usuários do mesmo grupo
- ✅ **Troca dinâmica de grupos** funcionando em tempo real
- ✅ **Comandos especiais** funcionando em todos os grupos
- ✅ **Desconexões** tratadas adequadamente
- ✅ **Encerramento limpo** do servidor

---

## 🔬 **ANÁLISE TÉCNICA AVANÇADA**

### **Pontos Fortes da Implementação**
1. **Escalabilidade**: Threading permite crescimento em múltiplos grupos
2. **Modularidade**: Componentes bem separados com suporte a grupos
3. **Usabilidade**: Interface intuitiva com comandos de grupo
4. **Segurança**: Criptografia automática com isolamento por grupo
5. **Flexibilidade**: Troca dinâmica de grupos durante a sessão
6. **Robustez**: Tratamento abrangente de erros

### **Limitações Conhecidas**
1. **Chaves compartilhadas**: Não é end-to-end real por grupo
2. **Threading**: Não ideal para muitos usuários (usar async)
3. **Persistência**: Sem histórico de mensagens por grupo
4. **Autenticação**: Sistema simples sem controle de acesso

### **Possíveis Melhorias Futuras**
- [ ] Troca de chaves Diffie-Hellman por grupo
- [ ] Interface gráfica (Tkinter/Qt) com abas por grupo
- [ ] Grupos privados com senhas personalizadas
- [ ] Banco de dados para histórico por grupo
- [ ] Transferência de arquivos entre grupos
- [ ] Administração avançada de grupos

---

## 🏆 **RESULTADOS ALCANÇADOS**

### **Funcionalidades Implementadas**
✅ **Sistema completo** e funcional com 3 grupos independentes  
✅ **Múltiplos usuários** simultâneos em cada grupo  
✅ **Criptografia automática** AES-256 com chaves distintas por grupo  
✅ **Isolamento total** entre grupos - zero vazamento de dados  
✅ **Troca dinâmica** de grupos durante a sessão  
✅ **Interface amigável** no terminal com comandos expandidos  
✅ **Comandos administrativos** servidor/cliente com suporte a grupos  
✅ **Tratamento robusto** de erros e mudanças de estado  
✅ **Documentação completa** e testes abrangentes  

### **Conceitos de Redes Demonstrados**
✅ **Sockets TCP** - Implementação prática com protocolo estendido  
✅ **Threading** - Servidor concorrente com isolamento por grupo  
✅ **Protocolos** - Design de aplicação com seleção e troca de grupos  
✅ **Roteamento** - Broadcast seletivo por grupo de destino  
✅ **Segurança** - Criptografia em redes com múltiplas chaves  
✅ **Robustez** - Tratamento de falhas e mudanças de estado  

### **Valor Educacional**
- **Aplicação prática** dos conceitos teóricos
- **Código limpo** e bem documentado
- **Extensibilidade** para projetos futuros
- **Base sólida** para compreensão de redes
- **Experiência hands-on** com programação de redes

---

## 🎯 **CONCLUSÃO**

Este projeto demonstra com sucesso a **aplicação prática dos conceitos fundamentais** da disciplina DCC042 - Redes de Computadores. Através da implementação de um chat criptografado com múltiplos grupos, foram explorados temas como:

- **Programação com sockets TCP**
- **Threading para aplicações concorrentes**
- **Design de protocolos de aplicação** com estados complexos
- **Roteamento seletivo** de mensagens por grupo
- **Segurança em comunicações de rede** com isolamento criptográfico
- **Tratamento robusto de erros e exceções**

O resultado é um **sistema funcional, seguro e extensível** que serve tanto como ferramenta de aprendizado quanto como base para projetos mais complexos. A implementação combina **teoria e prática**, oferecendo uma compreensão profunda dos mecanismos que sustentam as comunicações em rede modernas, incluindo conceitos avançados como **isolamento de grupos** e **criptografia multi-chave**.

**Status: ✅ PROJETO CONCLUÍDO E APROVADO PARA APRESENTAÇÃO**

---

*Trabalho desenvolvido para DCC042 - Redes de Computadores*  
*UFJF - Universidade Federal de Juiz de Fora*  
*Agosto 2025*
