import json
import datetime
import paho.mqtt.client as mqtt

data_file = "dados_esps.json"

access_points = {
    "DE:96:70:F0:75:E1": "AP-1",
    "02:9B:CD:05:1E:BE": "AP-2",
    "68:D4:0C:D5:2D:9F": "AP-3",
    "DE:96:70:F0:75:E4": "AP-4",
    "36:80:80:0C:C5:E1": "AP-5",
}

coord_lookup = {
    "AP-1": (-23.5995, -46.7152),
    "AP-2": (-23.6050, -46.7140),
    "AP-3": (-23.6120, -46.7135),
    "AP-4": (-23.6225, -46.7136),
    "AP-5": (-23.6375, -46.7120),
}

connected_esps = []

def on_message(client, userdata, message):
    global connected_esps
    payload = message.payload.decode()
    print("📡 MQTT RECEBIDO:", payload)

    if "|" in payload:
        client_id, bssid = payload.split("|", 1)
        ap_name = access_points.get(bssid)
        if not ap_name:
            print("❌ BSSID desconhecido:", bssid)
            return

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ap_info = {"nome": ap_name, "bssid": bssid, "coord": coord_lookup[ap_name]}

        # Atualiza ou adiciona ESP
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

        # Salva no arquivo
        with open(data_file, "w") as f:
            json.dump(connected_esps, f, indent=2)

# Setup MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("esp32/bssid")
client.loop_forever()
