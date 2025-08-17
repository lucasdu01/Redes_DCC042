import asyncio
import websockets
import json
import threading
import time
from datetime import datetime
from crypto_utils import ChatCrypto

class WebChatServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.clients = {}  # {websocket: {'username': str, 'group': int}}
        # Criptografia para cada grupo
        self.crypto_groups = {
            1: ChatCrypto("g1"),
            2: ChatCrypto("g2"), 
            3: ChatCrypto("g3")
        }
        self.running = False
        
    async def register_client(self, websocket, username, group):
        """
        Registra um novo cliente
        """
        self.clients[websocket] = {'username': username, 'group': group}
        print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] {username} entrou no Grupo {group} (Web)")
        
        # Notifica outros usuários do mesmo grupo
        timestamp = datetime.now().strftime('%H:%M:%S')
        welcome_msg = {
            'type': 'system',
            'message': f"📢 {username} entrou no chat!",
            'timestamp': timestamp,
            'group': group
        }
        await self.broadcast_message(welcome_msg, websocket, group)
        
    async def unregister_client(self, websocket):
        """
        Remove um cliente
        """
        if websocket in self.clients:
            username = self.clients[websocket]['username']
            group = self.clients[websocket]['group']
            del self.clients[websocket]
            
            print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] {username} saiu do Grupo {group} (Web)")
            
            # Notifica outros usuários do mesmo grupo
            timestamp = datetime.now().strftime('%H:%M:%S')
            goodbye_msg = {
                'type': 'system',
                'message': f"📢 {username} saiu do chat!",
                'timestamp': timestamp,
                'group': group
            }
            await self.broadcast_message(goodbye_msg, websocket, group)
    
    async def change_group(self, websocket, new_group):
        """
        Muda um cliente de grupo
        """
        if websocket not in self.clients:
            return False
            
        username = self.clients[websocket]['username']
        old_group = self.clients[websocket]['group']
        
        if new_group not in [1, 2, 3]:
            return False
            
        # Notifica saída do grupo antigo
        timestamp = datetime.now().strftime('%H:%M:%S')
        leave_msg = {
            'type': 'system',
            'message': f"📢 {username} saiu do grupo!",
            'timestamp': timestamp,
            'group': old_group
        }
        await self.broadcast_message(leave_msg, websocket, old_group)
        
        # Atualiza grupo
        self.clients[websocket]['group'] = new_group
        print(f"🔄 {username} mudou do Grupo {old_group} para Grupo {new_group} (Web)")
        
        # Notifica entrada no novo grupo
        join_msg = {
            'type': 'system',
            'message': f"📢 {username} entrou no grupo!",
            'timestamp': timestamp,
            'group': new_group
        }
        await self.broadcast_message(join_msg, websocket, new_group)
        
        return True
    
    async def broadcast_message(self, message, sender_websocket, group):
        """
        Envia mensagem para todos os clientes do grupo
        """
        if not self.clients:
            return
            
        # Lista de clientes para remover (desconectados)
        disconnected_clients = []
        
        for client_websocket, info in self.clients.items():
            # Envia apenas para clientes do mesmo grupo
            if info.get('group', 1) != group:
                continue
                
            # Não envia para o remetente (exceto se for None)
            if sender_websocket is not None and client_websocket == sender_websocket:
                continue
                
            try:
                await client_websocket.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.append(client_websocket)
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                disconnected_clients.append(client_websocket)
        
        # Remove clientes desconectados
        for client in disconnected_clients:
            if client in self.clients:
                await self.unregister_client(client)
    
    async def handle_client(self, websocket):
        """
        Gerencia conexão com um cliente WebSocket
        """
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    message_type = data.get('type')
                    
                    if message_type == 'join':
                        # Cliente quer entrar
                        username = data.get('username', '').strip()
                        group = data.get('group', 1)
                        
                        if username and len(username) >= 2 and group in [1, 2, 3]:
                            await self.register_client(websocket, username, group)
                            response = {
                                'type': 'join_response',
                                'success': True,
                                'group': group
                            }
                        else:
                            response = {
                                'type': 'join_response',
                                'success': False,
                                'error': 'Nome inválido ou grupo inválido'
                            }
                        
                        await websocket.send(json.dumps(response))
                        
                    elif message_type == 'change_group':
                        # Cliente quer trocar de grupo
                        new_group = data.get('group', 1)
                        success = await self.change_group(websocket, new_group)
                        
                        response = {
                            'type': 'change_group_response',
                            'success': success,
                            'group': new_group if success else self.clients.get(websocket, {}).get('group', 1)
                        }
                        await websocket.send(json.dumps(response))
                        
                    elif message_type == 'message':
                        # Mensagem normal do chat
                        if websocket in self.clients:
                            username = self.clients[websocket]['username']
                            group = self.clients[websocket]['group']
                            content = data.get('content', '').strip()
                            
                            if content:
                                timestamp = datetime.now().strftime('%H:%M:%S')
                                chat_message = {
                                    'type': 'message',
                                    'username': username,
                                    'content': content,
                                    'timestamp': timestamp,
                                    'group': group
                                }
                                
                                print(f"💬 [Grupo {group}] [{timestamp}] {username}: {content}")
                                await self.broadcast_message(chat_message, websocket, group)
                                
                    elif message_type == 'get_status':
                        # Cliente quer status do servidor
                        groups = {1: [], 2: [], 3: []}
                        for ws, info in self.clients.items():
                            group_num = info.get('group', 1)
                            groups[group_num].append(info['username'])
                        
                        status = {
                            'type': 'status_response',
                            'total_clients': len(self.clients),
                            'groups': groups
                        }
                        await websocket.send(json.dumps(status))
                        
                except json.JSONDecodeError:
                    print("Mensagem JSON inválida recebida")
                except Exception as e:
                    print(f"Erro ao processar mensagem: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            print(f"Erro na conexão WebSocket: {e}")
        finally:
            await self.unregister_client(websocket)
    
    async def start_server(self):
        """
        Inicia o servidor WebSocket
        """
        self.running = True
        print(f"🌐 Servidor Web Chat iniciado em ws://{self.host}:{self.port}")
        print("🔐 Interface web disponível")
        print("👥 Aguardando conexões web...")
        
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # Executa para sempre

def main():
    server = WebChatServer()
    
    try:
        print("=== SERVIDOR WEB CHAT CRIPTOGRAFADO ===")
        print("Interface web para o chat com grupos")
        print("=====================================\n")
        
        # Inicia o servidor
        asyncio.run(server.start_server())
        
    except KeyboardInterrupt:
        print("\n⚡ Ctrl+C detectado - encerrando servidor...")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
