import json
import datetime
import paho.mqtt.client as mqtt

# Arquivo JSON para armazenar dados recebidos dos ESPs
data_file = "dados_esps.json"

# Lista de Access Points (APs) conhecidos com BSSID, nome e coordenadas
access_points_detalhados = {
    "7A:37:16:2B:8D:5D": {"id": "AP-1", "nome": "São Paulo-Morumbi e Jardim Guedala", "coord": (-23.5995, -46.7152)},
    "02:9B:CD:05:1E:BE": {"id": "AP-2", "nome": "Jardim Guedala e Morumbi", "coord": (-23.6050, -46.7140)},
    "68:D4:0C:D5:2D:9F": {"id": "AP-3", "nome": "Morumbi e Paraisópolis", "coord": (-23.6120, -46.7135)},
    "C4:6E:1F:95:82:A7": {"id": "AP-4", "nome": "Paraisópolis e Américo Maurano", "coord": (-23.6225, -46.7136)},
    "58:10:8C:96:6C:76": {"id": "AP-5", "nome": "Vila Andrade e Jardim Jussara", "coord": (-23.6375, -46.7120)},
}

# Mapeia nomes técnicos dos dispositivos ESP para nomes amigáveis
nome_dispositivos = {
    "ESP32C6_1": "Agente_1",
    "ESP32C6_2": "Agente_2",
    "ESP32C6_3": "Agente_3",
    "ESP32C6_4": "Agente_4",
}

# Lista com todos os ESPs conectados (será populada dinamicamente)
connected_esps = []

# 🔹 Função utilitária para buscar um ESP já registrado ou criar um novo
def get_esp(client_id):
    for esp in connected_esps:
        if esp["client_id"] == client_id:
            return esp
    # Se não existir, cria um novo registro
    new_esp = {
        "client_id": client_id,
        "ap": None,          # Access Point atual
        "last_seen": None,   # Última vez que foi visto
        "bateria": None      # Percentual de bateria
    }
    connected_esps.append(new_esp)
    return new_esp

# Função chamada quando uma mensagem MQTT é recebida
def on_message(client, userdata, message):
    global connected_esps
    payload = message.payload.decode()  # Decodifica o conteúdo para string
    topic = message.topic               # Obtém o tópico da mensagem
    print(f"📡 MQTT RECEBIDO ({topic}): {payload}")

    # Data/hora atual formatada
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 🛰️ Tratamento para mensagens de localização (BSSID)
    if topic == "esp32/bssid":
        parts = payload.split("|")
        if len(parts) != 2:
            print("❌ Formato inválido para bssid!")
            return
        client_id_raw, bssid = parts
        # Converte ID técnico em nome amigável, se existir no dicionário
        client_id = nome_dispositivos.get(client_id_raw, client_id_raw)

        # Verifica se o BSSID recebido é conhecido
        ap_info = access_points_detalhados.get(bssid)
        if not ap_info:
            print("❌ BSSID desconhecido:", bssid)
            return

        # Atualiza informações do ESP
        esp = get_esp(client_id)
        esp["ap"] = ap_info
        esp["last_seen"] = current_time
        print(f"✅ {client_id} conectado ao {ap_info['id']} em {current_time}")

    # 🔋 Tratamento para mensagens de bateria
    elif topic == "esp32/battery":
        parts = payload.split("|")
        if len(parts) != 2:
            print("❌ Formato inválido para bateria!")
            return
        client_id_raw, battery_str = parts
        client_id = nome_dispositivos.get(client_id_raw, client_id_raw)

        # Converte o nível de bateria para inteiro
        try:
            battery = int(battery_str)
        except ValueError:
            print("⚠️ Nível de bateria inválido:", battery_str)
            return

        # Atualiza informações do ESP
        esp = get_esp(client_id)
        esp["bateria"] = battery
        esp["last_seen"] = current_time
        print(f"🔋 Bateria atualizada para {client_id}: {battery}%")

    # 💾 Salva os dados atualizados no arquivo JSON
    with open(data_file, "w") as f:
        json.dump(connected_esps, f, indent=2)

# 🔧 Configura e inicia o cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("localhost", 1883)          # Conecta ao broker MQTT local
client.subscribe("esp32/bssid")            # Inscreve para receber mensagens de localização
client.subscribe("esp32/battery")          # Inscreve para receber mensagens de bateria
client.loop_forever()                      # Mantém a conexão ativa e processa mensagens
