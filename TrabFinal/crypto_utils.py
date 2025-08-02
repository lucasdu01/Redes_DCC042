import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class ChatCrypto:
    def __init__(self, password="chat_seguro_2025"):
        """
        Inicializa a criptografia com uma senha padrão
        """
        self.password = password.encode()
        self.salt = b'salt_fixo_para_demo'  # Em produção, use salt aleatório
        self.key = self._derive_key()
        self.cipher = Fernet(self.key)
    
    def _derive_key(self):
        """
        Deriva uma chave criptográfica da senha usando PBKDF2
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key
    
    def encrypt_message(self, message):
        """
        Criptografa uma mensagem
        """
        try:
            encrypted_data = self.cipher.encrypt(message.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            print(f"Erro ao criptografar: {e}")
            return None
    
    def decrypt_message(self, encrypted_message):
        """
        Descriptografa uma mensagem
        """
        try:
            encrypted_data = base64.urlsafe_b64decode(encrypted_message.encode('utf-8'))
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            print(f"Erro ao descriptografar: {e}")
            return None
    
    def test_crypto(self):
        """
        Testa a criptografia com uma mensagem de exemplo
        """
        original = "Mensagem de teste para criptografia!"
        encrypted = self.encrypt_message(original)
        decrypted = self.decrypt_message(encrypted)
        
        print(f"Original: {original}")
        print(f"Criptografado: {encrypted}")
        print(f"Descriptografado: {decrypted}")
        print(f"Teste {'PASSOU' if original == decrypted else 'FALHOU'}")

if __name__ == "__main__":
    # Teste da criptografia
    crypto = ChatCrypto()
    crypto.test_crypto()
