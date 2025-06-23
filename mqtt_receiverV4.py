import json
import datetime
import paho.mqtt.client as mqtt

# Caminho do arquivo JSON onde os dados serão salvos
data_file = "dados_esps.json"

# Dicionário completo dos Access Points com nomes descritivos
access_points_detalhados = {
    "DE:96:70:F0:75:E1": {
        "id": "AP-1",
        "nome": "São Paulo-Morumbi e Jardim Guedala",
        "coord": (-23.5995, -46.7152),
        "bssid": "DE:96:70:F0:75:E1"
    },
    "02:9B:CD:05:1E:BE": {
        "id": "AP-2",
        "nome": "Jardim Guedala e Morumbi",
        "coord": (-23.6050, -46.7140),
        "bssid": "02:9B:CD:05:1E:BE"
    },
    "68:D4:0C:D5:2D:9F": {
        "id": "AP-3",
        "nome": "Morumbi e Paraisópolis",
        "coord": (-23.6120, -46.7135),
        "bssid": "68:D4:0C:D5:2D:9F"
    },
    "DE:96:70:F0:75:E4": {
        "id": "AP-4",
        "nome": "Paraisópolis e Américo Maurano",
        "coord": (-23.6225, -46.7136),
        "bssid": "DE:96:70:F0:75:E4"
    },
    "DE:96:70:F0:75:E5": {
        "id": "AP-5",
        "nome": "Vila Andrade e Jardim Jussara",
        "coord": (-23.6375, -46.7120),
        "bssid": "DE:96:70:F0:75:E5"
    },
}

# Mapeamento de nomes dos dispositivos
nome_dispositivos = {
    "ESP32C6_1": "Agente_1",
    "ESP32C6_2": "Agente_2",
    "ESP32C6_3": "Agente_3",
    "ESP32C6_4": "Agente_4",
    # Adicione mais conforme necessário
}

connected_esps = []

def on_message(client, userdata, message):
    global connected_esps
    payload = message.payload.decode()
    print("📡 MQTT RECEBIDO:", payload)

    if "|" in payload:
        client_id_raw, bssid = payload.split("|", 1)
        client_id = nome_dispositivos.get(client_id_raw, client_id_raw)

        ap_info = access_points_detalhados.get(bssid)
        if not ap_info:
            print("❌ BSSID desconhecido:", bssid)
            return

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Atualiza ou adiciona novo ESP
        found = False
        for esp in connected_esps:
            if esp["client_id"] == client_id:
                esp["ap"] = ap_info
                esp["last_seen"] = current_time
                found = True
                break

        if not found:
            connected_esps.append({
                "client_id": client_id,
                "ap": ap_info,
                "last_seen": current_time
            })

        # Salva no arquivo JSON
        with open(data_file, "w") as f:
            json.dump(connected_esps, f, indent=2)

        print(f"✅ Atualizado: {client_id} em {ap_info['id']} às {current_time}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("esp32/bssid")
client.loop_forever()
