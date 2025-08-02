# 🎯 CHAT CRIPTOGRAFADO - TRABALHO FINAL DCC042
## Sistema de Comunicação Segura em Tempo Real

---

## 📖 **VISÃO GERAL**

Sistema de chat multiusuário com **criptografia automática** implementado em Python usando sockets TCP. Demonstra conceitos fundamentais de redes de computadores, programação concorrente e segurança da informação aplicados em uma aplicação prática e funcional.

### **Estrutura do Projeto**
```
TrabFinal/
├── 📄 chat_server.py			# Servidor multithread principal
├── 📄 chat_client.py           # Cliente com interface terminal  
├── 📄 crypto_utils.py          # Módulo criptografia AES-256
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
- **Interface amigável** para demonstração prática

### **Aplicação dos Conceitos da Disciplina**
- ✅ **Sockets TCP** - Comunicação cliente-servidor confiável
- ✅ **Threading** - Servidor concorrente para múltiplos clientes
- ✅ **Protocolos de aplicação** - Handshake e formato de mensagens
- ✅ **Tratamento de conexões** - Gerenciamento robusto de sessões
- ✅ **Plus: Segurança em redes** - Criptografia AES-256

---

## ⚙️ **FUNCIONAMENTO TÉCNICO**

### **Arquitetura do Sistema**
```
Cliente A ←→ [AES-256] ←→ SERVIDOR ←→ [AES-256] ←→ Cliente B
                ↓           ↓              ↓
           Criptografia  Threading   Broadcast
```

### **Fluxo de Operação**
1. **Servidor** inicia e aguarda conexões na porta 12345
2. **Clientes** conectam via socket TCP e fazem autenticação
3. **Mensagens** são criptografadas automaticamente (AES-256)
4. **Servidor** descriptografa, processa e redistribui (broadcast)
5. **Threading** permite múltiplos usuários simultâneos

### **Componentes Principais**

#### **🖥️ Servidor (`chat_server.py`)**
- **Threading**: Uma thread por cliente conectado
- **Broadcast**: Redistribui mensagens para todos os usuários
- **Criptografia**: Descriptografa/re-criptografa automaticamente
- **Comandos**: `status`, `quit`, `help` via terminal
- **Logs**: Registro detalhado de atividades com timestamp

#### **💻 Cliente (`chat_client.py`)**
- **Interface**: Terminal interativo com comandos especiais
- **Criptografia**: Transparente ao usuário
- **Comandos**: `/help`, `/quit`, `/status`, `/clear`
- **Robustez**: Tratamento de desconexões e erros

#### **🔐 Criptografia (`crypto_utils.py`)**
- **Algoritmo**: AES-256 via biblioteca Fernet
- **Derivação**: PBKDF2 com SHA-256 (100.000 iterações)
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
2. Conecta automaticamente ao servidor local
3. Interface de chat fica disponível

**Comandos do cliente:**
- `/help` → Lista comandos disponíveis
- `/quit` → Sair do chat
- `/status` → Informações da conexão
- `/clear` → Limpar tela
- Qualquer outra coisa → Enviada como mensagem

### **Exemplo Prático**
**Terminal 1 (Servidor):**
```
Server> status
📊 Status do Servidor:
   🌐 Endereço: localhost:12345
   👥 Clientes conectados: 2
   📋 Usuários online:
      - Alice (127.0.0.1:52341)
      - Bob (127.0.0.1:52342)
```

**Terminal 2 (Alice):**
```
[Alice] Olá pessoal!
[14:30:25] Bob: Oi Alice, tudo bem?
[Alice] Estou testando o chat criptografado
```

**Terminal 3 (Bob):**
```
[14:30:25] Alice: Olá pessoal!
[Bob] Oi Alice, tudo bem?
[14:30:45] Alice: Estou testando o chat criptografado
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
- **Formato estruturado** de mensagens
- **Comandos especiais** vs mensagens normais
- **Estados de conexão** (conectado/desconectado)

### **4. Segurança em Redes**
- **Criptografia simétrica** AES-256
- **Derivação segura de chaves** PBKDF2
- **Proteção de dados em trânsito**
- **Transparência para o usuário**

### **5. Tratamento de Erros em Rede**
- **Timeout em sockets** para evitar bloqueios
- **Detecção de desconexões** abruptas
- **Limpeza de recursos** (sockets, threads)
- **Recuperação automática** quando possível

---

## 📊 **INFORMAÇÕES TÉCNICAS RELEVANTES**

### **Performance e Escalabilidade**
- **Concorrência**: Suporta múltiplos clientes simultâneos
- **Threading**: Modelo thread-per-client
- **Timeout**: 1 segundo no accept() para responsividade
- **Broadcast eficiente**: Mensagem processada uma vez

### **Segurança Implementada**
- **Algoritmo**: AES-256 (padrão militar)
- **Modo**: CBC com autenticação HMAC
- **Key Derivation**: PBKDF2-SHA256 (100k iterações)
- **Limitação**: Chave compartilhada fixa (educacional)

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
- ✅ **Múltiplos clientes** conectando simultaneamente
- ✅ **Mensagens criptografadas** funcionando corretamente
- ✅ **Broadcast** chegando a todos os usuários
- ✅ **Comandos especiais** funcionando
- ✅ **Desconexões** tratadas adequadamente
- ✅ **Encerramento limpo** do servidor

---

## 🔬 **ANÁLISE TÉCNICA AVANÇADA**

### **Pontos Fortes da Implementação**
1. **Escalabilidade**: Threading permite crescimento
2. **Modularidade**: Componentes bem separados
3. **Usabilidade**: Interface intuitiva
4. **Segurança**: Criptografia automática
5. **Robustez**: Tratamento abrangente de erros

### **Limitações Conhecidas**
1. **Chave compartilhada**: Não é end-to-end real
2. **Threading**: Não ideal para muitos usuários (usar async)
3. **Persistência**: Sem histórico de mensagens
4. **Autenticação**: Sistema simples

### **Possíveis Melhorias Futuras**
- [ ] Troca de chaves Diffie-Hellman
- [ ] Interface gráfica (Tkinter/Qt)
- [ ] Salas de chat separadas
- [ ] Banco de dados para histórico
- [ ] Transferência de arquivos
- [ ] Protocolo mais sofisticado

---

## 🏆 **RESULTADOS ALCANÇADOS**

### **Funcionalidades Implementadas**
✅ **Sistema completo** e funcional  
✅ **Múltiplos usuários** simultâneos  
✅ **Criptografia automática** AES-256  
✅ **Interface amigável** no terminal  
✅ **Comandos administrativos** servidor/cliente  
✅ **Tratamento robusto** de erros  
✅ **Documentação completa** e testes  

### **Conceitos de Redes Demonstrados**
✅ **Sockets TCP** - Implementação prática  
✅ **Threading** - Servidor concorrente  
✅ **Protocolos** - Design de aplicação  
✅ **Segurança** - Criptografia em redes  
✅ **Robustez** - Tratamento de falhas  

### **Valor Educacional**
- **Aplicação prática** dos conceitos teóricos
- **Código limpo** e bem documentado
- **Extensibilidade** para projetos futuros
- **Base sólida** para compreensão de redes
- **Experiência hands-on** com programação de redes

---

## 🎯 **CONCLUSÃO**

Este projeto demonstra com sucesso a **aplicação prática dos conceitos fundamentais** da disciplina DCC042 - Redes de Computadores. Através da implementação de um chat criptografado, foram explorados temas como:

- **Programação com sockets TCP**
- **Threading para aplicações concorrentes**
- **Design de protocolos de aplicação**
- **Segurança em comunicações de rede**
- **Tratamento robusto de erros e exceções**

O resultado é um **sistema funcional, seguro e extensível** que serve tanto como ferramenta de aprendizado quanto como base para projetos mais complexos. A implementação combina **teoria e prática**, oferecendo uma compreensão profunda dos mecanismos que sustentam as comunicações em rede modernas.

**Status: ✅ PROJETO CONCLUÍDO E APROVADO PARA APRESENTAÇÃO**

---

*Trabalho desenvolvido para DCC042 - Redes de Computadores*  
*UFJF - Universidade Federal de Juiz de Fora*  
*Agosto 2025*
