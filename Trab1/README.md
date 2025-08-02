# Trabalho 1 - Redes de Computadores (DCC042)

Este repositório contém duas versões de um servidor socket em Python, implementadas como parte dos exercícios da disciplina de Redes de Computadores (DCC042).

## 🎯 Objetivo

Desenvolver duas versões de um servidor multithread para lidar com conexões de clientes, explorando diferentes abordagens de gerenciamento de threads.

---

## 📁 Estrutura do Projeto

```
Trab1/
├── echo_A/
│   ├── client_A.py
│   └── server_A.py
├── echo_B/
│   ├── client_B.py
│   └── server_B.py
```

---

## 🧪 Exercícios

### ✅ Exercício (a) – Thread por cliente

**Arquivo:** `echo_A/server_A.py`

**Descrição:**  
O servidor aceita conexões indefinidamente. A cada nova conexão de cliente, uma **nova thread** é criada para tratar exclusivamente daquela conexão.  
Quando a conexão é encerrada, a thread termina automaticamente, liberando os recursos utilizados.

**Características:**
- Criação dinâmica de threads por cliente.
- Uso de `threading.Thread` para atender cada cliente separadamente.
- Liberação automática de recursos ao fim da conexão.

---

### ✅ Exercício (b) – Pool fixo de 10 threads

**Arquivo:** `echo_B/server_B.py`

**Descrição:**  
O servidor cria **exatamente 10 threads** na inicialização. Cada uma dessas threads fica responsável por tratar uma conexão de cliente.  
Se todas as threads estiverem ocupadas, novas conexões são rejeitadas com uma mensagem ao cliente.

**Características:**
- Threads fixas definidas por `MAX_THREADS = 10`.
- Controle do número de conexões simultâneas via variável `active_threads`.
- Uso de `Lock` (`active_threads_lock`) para evitar condições de corrida.
- Melhora no controle de recursos do sistema.

---

## ▶️ Execução

### 🔧 Requisitos
- Python 3.x

### 🖥️ Como executar

#### Versão A
```bash
cd Trab1/echo_A
python server_A.py  # Em um terminal
python client_A.py  # Em outro terminal
```

#### Versão B
```bash
cd Trab1/echo_B
python server_B.py  # Em um terminal
python client_B.py  # Em outro terminal
```

---

## 💡 Observações

- Ambas as versões utilizam TCP (`socket.SOCK_STREAM`).
- O cliente simplesmente envia mensagens ao servidor e recebe eco (echo) de volta.
- O código pode ser adaptado facilmente para testar concorrência com múltiplos clientes.
