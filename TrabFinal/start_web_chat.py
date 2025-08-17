import subprocess
import sys
import time
import threading
import os
from pathlib import Path

def run_server(script_name, server_name):
    """
    Executa um servidor em uma thread separada
    """
    try:
        print(f"🚀 Iniciando {server_name}...")
        
        # Executa o script Python
        process = subprocess.Popen([
            sys.executable, script_name
        ], cwd=Path(__file__).parent)
        
        # Aguarda o processo terminar
        process.wait()
        
    except Exception as e:
        print(f"❌ Erro ao executar {server_name}: {e}")

def main():
    print("=" * 60)
    print("🎯 CHAT CRIPTOGRAFADO - INTERFACE WEB COMPLETA")
    print("=" * 60)
    print("🔐 Sistema de chat com múltiplos grupos e interface visual")
    print("📱 Interface web moderna com design responsivo")
    print("🗂️  Suporte a 3 grupos independentes com criptografia")
    print("=" * 60)
    print()
    
    print("📋 INSTRUÇÕES DE USO:")
    print("1. Aguarde ambos os servidores iniciarem")
    print("2. O navegador abrirá automaticamente na interface web")
    print("3. Digite seu nome e escolha um grupo (1, 2 ou 3)")
    print("4. Comece a conversar! Use os botões para trocar de grupo")
    print("5. Abra múltiplas abas/janelas para testar com vários usuários")
    print()
    print("🔧 SERVIDORES NECESSÁRIOS:")
    print("- WebSocket Server (porta 8765) - Comunicação em tempo real")
    print("- HTTP Server (porta 8080) - Interface web")
    print()
    print("⚠️  Para encerrar: Use Ctrl+C neste terminal")
    print("=" * 60)
    print()
    
    try:
        # Verifica se os arquivos existem
        project_dir = Path(__file__).parent
        web_chat_server = project_dir / "web_chat_server.py"
        web_server = project_dir / "web_server.py"
        
        if not web_chat_server.exists():
            print("❌ Arquivo web_chat_server.py não encontrado!")
            return
            
        if not web_server.exists():
            print("❌ Arquivo web_server.py não encontrado!")
            return
        
        # Inicia o servidor WebSocket em uma thread
        websocket_thread = threading.Thread(
            target=run_server, 
            args=("web_chat_server.py", "Servidor WebSocket"),
            daemon=True
        )
        websocket_thread.start()
        
        # Aguarda um pouco para o WebSocket iniciar
        time.sleep(2)
        
        # Inicia o servidor HTTP em uma thread
        http_thread = threading.Thread(
            target=run_server,
            args=("web_server.py", "Servidor HTTP"),
            daemon=True
        )
        http_thread.start()
        
        print("✅ Ambos os servidores foram iniciados!")
        print("🌐 Interface web: http://localhost:8080/chat_web.html")
        print("📡 WebSocket: ws://localhost:8765")
        print()
        print("💡 Dica: Abra múltiplas abas do navegador para testar vários usuários")
        print("🗂️  Teste a troca de grupos para ver o isolamento em ação!")
        print()
        print("⌨️  Pressione Ctrl+C para encerrar todos os servidores...")
        
        # Mantém o programa principal rodando
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Encerrando servidores...")
            
    except KeyboardInterrupt:
        print("\n⚡ Ctrl+C detectado - encerrando...")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    print("👋 Sistema encerrado. Obrigado por usar o Chat Criptografado!")

if __name__ == "__main__":
    main()
