
# 1) Introdução
O projeto "Chat Criptografado" consiste em um sistema de comunicação segura em tempo real, com múltiplos grupos de conversa, desenvolvido em Python. O objetivo é demonstrar, de forma prática, conceitos fundamentais de redes de computadores, programação concorrente e segurança da informação, aplicados em uma aplicação funcional e didática.

# 2) Problema tratado
O sistema resolve o problema de comunicação segura entre múltiplos usuários, organizados em grupos independentes, garantindo que as mensagens trocadas em cada grupo sejam criptografadas e isoladas das demais. O desafio central é permitir que vários clientes se comuniquem simultaneamente, com confidencialidade, integridade e isolamento entre grupos, utilizando apenas recursos de programação de redes e criptografia simétrica.

# 3) Estruturas de dados e análises
O projeto é composto por três módulos principais:
- **Servidor (`chat_server.py`)**: Gerencia conexões, autenticação, roteamento e broadcast de mensagens por grupo, utilizando threading para suportar múltiplos clientes simultâneos. Mantém um dicionário de clientes conectados e utiliza instâncias separadas de criptografia para cada grupo.
- **Cliente (`chat_client.py`)**: Permite ao usuário escolher e trocar de grupo dinamicamente, envia e recebe mensagens criptografadas, e oferece comandos interativos para facilitar o uso.
- **Criptografia (`crypto_utils.py`)**: Implementa criptografia simétrica AES-256, com derivação de chave via PBKDF2, utilizando uma senha distinta para cada grupo. As mensagens são criptografadas e descriptografadas de forma transparente para o usuário.

O sistema utiliza:
- Sockets TCP para comunicação confiável
- Threading para concorrência
- Broadcast seletivo para isolamento de grupos
- Estruturas de dicionário para gerenciar clientes e grupos

**Análise:**
O modelo thread-per-client garante escalabilidade para um número moderado de usuários. O isolamento criptográfico por grupo impede vazamento de mensagens entre grupos. O uso de chaves fixas por grupo é suficiente para fins educacionais, mas pode ser aprimorado para produção.

# 4) Testes realizados
Foram realizados testes automatizados e manuais:
- **Teste de criptografia:** Execução do módulo `crypto_utils.py` para validar a correta encriptação e decriptação das mensagens.
- **Teste completo:** Execução do script `test_chat.py`, que verifica a existência dos arquivos, inicializa o servidor, conecta múltiplos clientes e simula o envio de mensagens e comandos.
- **Testes manuais:**
	- Conexão simultânea de múltiplos clientes em diferentes grupos
	- Envio e recebimento de mensagens criptografadas
	- Troca dinâmica de grupos durante a sessão
	- Teste de comandos especiais (`/help`, `/status`, `/grupo N`, etc.)
	- Verificação do isolamento entre grupos e tratamento de desconexões

# 5) Conclusões
O projeto atinge plenamente seus objetivos, demonstrando na prática:
- Comunicação segura via sockets TCP
- Concorrência com threading
- Isolamento e segurança de dados com criptografia AES-256
- Roteamento eficiente e broadcast seletivo por grupo
- Interface amigável e comandos interativos

Como limitações, destacam-se o uso de chaves fixas por grupo (não end-to-end), ausência de histórico de mensagens e autenticação simplificada. Como possíveis melhorias, sugerem-se a implementação de troca de chaves Diffie-Hellman, interface gráfica e persistência de mensagens.

# 6) Referências
- Documentação oficial Python: https://docs.python.org/3/
- Documentação da biblioteca cryptography: https://cryptography.io/
- Material da disciplina DCC042 - Redes de Computadores (UFJF)
- RFC 4251: The Secure Shell (SSH) Protocol Architecture
- Tanenbaum, A. S. "Redes de Computadores" (Livro texto)
