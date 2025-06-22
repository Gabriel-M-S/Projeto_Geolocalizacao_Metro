#include <WiFi.h>
#include <PubSubClient.h>

// Configuração do Wi-Fi
const char* ssid = "CASA BO";  // Deixe vazio para conectar ao melhor AP automaticamente
const char* password = "casabo3731";  // Se necessário, defina a senha

// Configuração do MQTT
const char* mqtt_server = "192.168.121.232"; // Substitua pelo IP do seu Mosquitto
const int mqtt_port = 1883; // Porta do Mosquitto
const char* mqtt_client_id = "ESP32C6_1";

WiFiClient espClient;
PubSubClient client(espClient);

// Controle de tempo
unsigned long lastScan = 0;
const unsigned long scanInterval = 10000; // 10 segundos

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println("🔍 Iniciando escaneamento e conexão Wi-Fi...");
    connectToBestAP();

    client.setServer(mqtt_server, mqtt_port);
}

void loop() {
    // Verifica e reconecta Wi-Fi se necessário
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("⚠️ Wi-Fi desconectado! Tentando reconectar...");
        connectToBestAP();
    }

    // Verifica e reconecta MQTT se necessário
    if (!client.connected()) {
        connectToMQTT();
    }

    client.loop();

    // A cada 10s, escaneia e reconecta se necessário + envia MQTT
    if (millis() - lastScan > scanInterval) {
        lastScan = millis();
        connectToBestAP();
        sendBSSIDViaMQTT();
    }
}

// 🔹 Conectar ao melhor AP com SSID alvo
void connectToBestAP() {
    int numNetworks = WiFi.scanNetworks();
    if (numNetworks == 0) {
        Serial.println("⚠️ Nenhuma rede encontrada!");
        return;
    }

    int bestSignal = -100;
    String bestBSSID;

    for (int i = 0; i < numNetworks; i++) {
        String currentSSID = WiFi.SSID(i);
        String currentBSSID = WiFi.BSSIDstr(i);
        int currentRSSI = WiFi.RSSI(i);

        if (currentSSID == ssid) {
            Serial.printf("📶 Encontrado: %s | BSSID: %s | RSSI: %d dBm\n",
                          currentSSID.c_str(), currentBSSID.c_str(), currentRSSI);
            if (currentRSSI > bestSignal) {
                bestSignal = currentRSSI;
                bestBSSID = currentBSSID;
            }
        }
    }

    if (bestSignal == -100) {
        Serial.println("❌ Nenhum ponto de acesso válido encontrado.");
        return;
    }

    // Se já conectado ao melhor AP, não reconecta
    if (WiFi.status() == WL_CONNECTED && WiFi.BSSIDstr() == bestBSSID) {
        Serial.printf("🔗 Já conectado ao AP com melhor sinal (%s).\n", bestBSSID.c_str());
        return;
    }

    // Reconectar ao melhor AP
    WiFi.disconnect();
    Serial.printf("🔄 Reconectando ao BSSID %s...\n", bestBSSID.c_str());
    WiFi.begin(ssid, password);

    int timeout = 15;
    while (WiFi.status() != WL_CONNECTED && timeout > 0) {
        delay(1000);
        Serial.print(".");
        timeout--;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\n✅ Conectado com sucesso!");
        Serial.printf("📡 BSSID: %s | IP: %s\n",
                      WiFi.BSSIDstr().c_str(), WiFi.localIP().toString().c_str());
    } else {
        Serial.println("\n❌ Falha ao conectar.");
    }
}

// 🔹 Conectar ao MQTT
void connectToMQTT() {
    Serial.println("🔌 Tentando conectar ao MQTT...");
    int attempts = 0;

    while (!client.connected() && attempts < 5) {
        if (client.connect(mqtt_client_id)) {
            Serial.println("✅ Conectado ao MQTT!");
            return;
        } else {
            Serial.printf("❌ Falha MQTT (rc=%d), tentando...\n", client.state());
            delay(3000);
            attempts++;
        }
    }

    Serial.println("⚠️ Não foi possível conectar ao MQTT.");
}

// 🔹 Enviar o BSSID atual via MQTT (inclui client_id)
void sendBSSIDViaMQTT() {
    if (WiFi.status() == WL_CONNECTED && client.connected()) {
        String bssid = WiFi.BSSIDstr();
        String payload = String(mqtt_client_id) + "|" + bssid;  // Ex: ESP32C6_Client|DE:96:70:F0:75:E1
        Serial.printf("📤 Publicando no MQTT: %s\n", payload.c_str());
        client.publish("esp32/bssid", payload.c_str());
    } else {
        Serial.println("⚠️ Sem conexão Wi-Fi ou MQTT, não foi possível publicar.");
    }
}
