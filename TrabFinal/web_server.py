import http.server
import socketserver
import os
import threading
import webbrowser
from pathlib import Path

class ChatWebServer:
    def __init__(self, port=8080):
        self.port = port
        self.httpd = None
        
    def start_server(self):
        """
        Inicia o servidor HTTP para servir a interface web
        """
        try:
            # Muda para o diretório do projeto
            project_dir = Path(__file__).parent
            os.chdir(project_dir)
            
            Handler = http.server.SimpleHTTPRequestHandler
            self.httpd = socketserver.TCPServer(("", self.port), Handler)
            
            print(f"🌐 Servidor HTTP iniciado em http://localhost:{self.port}")
            print(f"📱 Interface web disponível em: http://localhost:{self.port}/chat_web.html")
            print("💡 Abra o navegador no endereço acima para usar a interface visual")
            print("🔗 Certifique-se de que o servidor WebSocket está rodando na porta 8765")
            print("-" * 60)
            
            # Abre automaticamente no navegador
            threading.Timer(1.0, lambda: webbrowser.open(f'http://localhost:{self.port}/chat_web.html')).start()
            
            self.httpd.serve_forever()
            
        except Exception as e:
            print(f"❌ Erro ao iniciar servidor HTTP: {e}")
    
    def stop_server(self):
        """
        Para o servidor HTTP
        """
        if self.httpd:
            self.httpd.shutdown()
            print("✅ Servidor HTTP encerrado")

def main():
    print("=== SERVIDOR WEB INTERFACE ===")
    print("Interface visual para o chat criptografado")
    print("================================\n")
    
    server = ChatWebServer()
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\n⚡ Ctrl+C detectado - encerrando servidor...")
        server.stop_server()
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
