#!/usr/bin/env python3
"""
Script de teste automatizado para o Chat Criptografado
Demonstra o funcionamento básico do sistema
"""

import subprocess
import time
import threading
import os
import sys

def test_crypto():
    """Testa o módulo de criptografia"""
    print("🔐 Testando criptografia...")
    result = subprocess.run([sys.executable, "crypto_utils.py"], 
                          capture_output=True, text=True, cwd=".")
    
    if "Teste PASSOU" in result.stdout:
        print("✅ Criptografia funcionando corretamente!")
        return True
    else:
        print("❌ Erro na criptografia:")
        print(result.stdout)
        print(result.stderr)
        return False

def start_server():
    """Inicia o servidor em background"""
    print("🚀 Iniciando servidor...")
    try:
        # Inicia servidor em processo separado
        server_process = subprocess.Popen(
            [sys.executable, "chat_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd="."
        )
        time.sleep(2)  # Aguarda servidor inicializar
        
        if server_process.poll() is None:
            print("✅ Servidor iniciado com sucesso!")
            return server_process
        else:
            print("❌ Falha ao iniciar servidor")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        return None

def check_files():
    """Verifica se todos os arquivos necessários existem"""
    required_files = [
        "chat_server.py",
        "chat_client.py", 
        "crypto_utils.py",
        "requirements.txt",
        "README.md"
    ]
    
    print("📁 Verificando arquivos do projeto...")
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - FALTANDO!")
            all_exist = False
    
    return all_exist

def show_demo_instructions():
    """Mostra instruções para demonstração manual"""
    print("\n" + "="*60)
    print("🎯 INSTRUÇÕES PARA DEMONSTRAÇÃO")
    print("="*60)
    print()
    
    print("1️⃣  SERVIDOR:")
    print("   Terminal 1: python chat_server.py")
    print("   -> Aguarde mensagem 'Servidor iniciado'")
    print()
    
    print("2️⃣  CLIENTES (abra 2-3 terminais):")
    print("   Terminal 2: python chat_client.py")
    print("   Terminal 3: python chat_client.py")
    print("   -> Digite nomes diferentes para cada cliente")
    print()
    
    print("3️⃣  TESTE O CHAT:")
    print("   - Digite mensagens em qualquer cliente")
    print("   - Veja como aparecem criptografadas nos outros")
    print("   - Teste comandos: /help, /status, /quit")
    print()
    
    print("4️⃣  COMANDOS DO SERVIDOR:")
    print("   - Digite 'status' para ver usuários conectados")
    print("   - Digite 'quit' para encerrar servidor")
    print()
    
    print("🔐 PONTOS PARA DESTACAR NA APRESENTAÇÃO:")
    print("   ✅ Múltiplos clientes simultâneos")
    print("   ✅ Mensagens criptografadas automaticamente")
    print("   ✅ Threading no servidor")
    print("   ✅ Interface amigável")
    print("   ✅ Tratamento de desconexões")
    print("   ✅ Comandos administrativos")
    print()

def main():
    print("🧪 TESTE DO CHAT CRIPTOGRAFADO")
    print("="*40)
    print()
    
    # Verifica arquivos
    if not check_files():
        print("❌ Alguns arquivos estão faltando!")
        return False
    
    # Testa criptografia
    if not test_crypto():
        print("❌ Falha no teste de criptografia!")
        return False
    
    print()
    print("✅ TODOS OS TESTES PASSARAM!")
    print("🎯 Sistema pronto para demonstração!")
    
    # Mostra instruções
    show_demo_instructions()
    
    # Opção de iniciar servidor automaticamente
    start_demo = input("Deseja iniciar o servidor agora? (s/N): ").strip().lower()
    
    if start_demo == 's':
        server = start_server()
        if server:
            print("\n🎮 Servidor rodando! Abra outros terminais para clientes.")
            print("💡 Pressione Ctrl+C para encerrar o teste...")
            try:
                # Mantém o script rodando
                server.wait()
            except KeyboardInterrupt:
                print("\n🛑 Encerrando servidor...")
                server.terminate()
                server.wait()
                print("✅ Teste concluído!")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Teste interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
