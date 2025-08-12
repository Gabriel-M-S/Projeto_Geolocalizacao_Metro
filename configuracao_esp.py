import serial
import serial.tools.list_ports
import time

# === Lista todas as portas seriais disponíveis no sistema ===
def listar_portas():
    portas = list(serial.tools.list_ports.comports())  # Retorna lista de portas
    for i, porta in enumerate(portas):
        print(f"{i}: {porta.device} - {porta.description}")  # Mostra índice, nome e descrição
    return portas  # Retorna lista para uso posterior

# === Permite ao usuário escolher qual porta serial usar ===
def escolher_porta(portas):
    idx = int(input("Selecione o número da porta serial: "))
    return portas[idx].device  # Retorna o nome da porta escolhida

# === Aguarda até receber uma mensagem específica do ESP via serial ===
def esperar_mensagem(ser, mensagem_esperada, timeout=10):
    """
    Fica lendo a porta serial até encontrar 'mensagem_esperada' 
    ou até estourar o tempo limite (timeout).
    """
    inicio = time.time()
    while time.time() - inicio < timeout:
        if ser.in_waiting:  # Se há dados disponíveis para leitura
            linha = ser.readline().decode(errors='ignore').strip()  # Lê e decodifica
            print("ESP:", linha)  # Mostra a mensagem recebida
            if mensagem_esperada.lower() in linha.lower():  # Compara ignorando maiúsculas/minúsculas
                return True
    return False  # Retorna falso se não recebeu a mensagem no tempo limite

# === Envia as configurações de ID, SSID e senha para o ESP ===
def enviar_dados_configuracao(porta_serial):
    try:
        # Abre a porta serial escolhida com baud rate 115200
        with serial.Serial(porta_serial, 115200, timeout=2) as ser:
            print("Conectado à porta:", porta_serial)
            time.sleep(2)  # Dá tempo para estabilizar a comunicação

            # Envia o comando para entrar no modo de configuração
            print(">> Enviando comando 'config' para o ESP")
            ser.write(b'config\n')  # Envia como bytes
            time.sleep(1)

            # Aguarda o ESP pedir o ID e envia
            if esperar_mensagem(ser, "Digite novo ID"):
                novo_id = input("Novo ID (apenas número): ")
                ser.write((novo_id + '\n').encode())  # Envia com quebra de linha
                time.sleep(1)

            # Aguarda o ESP pedir o SSID e envia
            if esperar_mensagem(ser, "Digite novo SSID"):
                novo_ssid = input("Novo SSID: ")
                ser.write((novo_ssid + '\n').encode())
                time.sleep(1)

            # Aguarda o ESP pedir a senha e envia
            if esperar_mensagem(ser, "Digite nova senha"):
                nova_senha = input("Nova senha: ")
                ser.write((nova_senha + '\n').encode())
                time.sleep(1)

            # Aguarda mensagens finais de confirmação do ESP
            print("\nAguardando confirmação do ESP...\n")
            fim = time.time() + 5
            while time.time() < fim:
                if ser.in_waiting:
                    linha = ser.readline().decode(errors='ignore').strip()
                    print("ESP:", linha)

            print("✅ Configuração finalizada com sucesso!")

    except Exception as e:
        # Captura e exibe erros de comunicação
        print("❌ Erro ao comunicar com o ESP:", e)

# === Função principal ===
def main():
    print("=== CONFIGURADOR SERIAL PARA ESP32 ===\n")
    portas = listar_portas()  # Lista portas disponíveis

    if not portas:  # Se não encontrou nenhuma
        print("Nenhuma porta serial encontrada.")
        return

    porta_escolhida = escolher_porta(portas)  # Usuário escolhe
    enviar_dados_configuracao(porta_escolhida)  # Envia dados para o ESP

# Corrige o nome especial para rodar o script
if __name__ == "__main__":
    main()