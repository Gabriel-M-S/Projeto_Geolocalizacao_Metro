// ===== Bibliotecas utilizadas =====
#include <Wire.h>                // Comunicação I2C
#include <Adafruit_GFX.h>        // Biblioteca gráfica genérica para displays
#include <Adafruit_SSD1306.h>    // Biblioteca específica para displays OLED SSD1306
#include <WiFi.h>                // Conexão Wi-Fi no ESP32
#include <PubSubClient.h>        // Cliente MQTT
#include <Preferences.h>         // Armazenamento não volátil (NVS)

// ===== Configurações do OLED =====
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 32
#define OLED_ADDR 0x3C            // Endereço I2C do display
#define SDA_PIN 8                 // Pino SDA do I2C
#define SCL_PIN 9                 // Pino SCL do I2C

// ===== Sensores e LEDs =====
#define BATT_PIN 0                // Pino para leitura de tensão da bateria
#define LED1_PIN 15
#define LED2_PIN 23
#define VOLTAGE_MIN 1.3           // Tensão mínima (0%)
#define VOLTAGE_MAX 2.2           // Tensão máxima (100%)

// Cria objeto para o display OLED
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ===== Configuração Wi-Fi e MQTT =====
String ssid = "CASA BO";         // SSID padrão (pode ser sobrescrito pelas preferências salvas)
String password = "casabo3731";  // Senha padrão
const char* mqtt_server = "192.168.189.232";  // Endereço do servidor MQTT
const int mqtt_port = 1883;                   

WiFiClient espClient;            // Cliente Wi-Fi
PubSubClient client(espClient);  // Cliente MQTT

// ===== Preferências salvas no NVS =====
Preferences prefs;               
String mqtt_client_id = "ESP32C6_2";

// ===== Controle de tempo =====
unsigned long lastScan = 0;
const unsigned long scanInterval = 10000; // Intervalo de 10s para envio de dados

// ===== SETUP =====
void setup() {
  Serial.begin(115200);
  delay(1000);

  // Inicializa I2C e OLED
  Wire.begin(SDA_PIN, SCL_PIN);
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  display.clearDisplay();

  // Carrega dados salvos (ID, SSID, senha) da memória persistente
  prefs.begin("mqtt", false);
  String idStr = prefs.getString("client_id", "0");
  mqtt_client_id = "ESP32C6_" + idStr;
  ssid = prefs.getString("ssid", ssid);
  password = prefs.getString("password", password);
  prefs.end();

  // Configura LEDs como saída
  pinMode(LED1_PIN, OUTPUT);
  pinMode(LED2_PIN, OUTPUT);
  digitalWrite(LED1_PIN, HIGH);
  digitalWrite(LED2_PIN, HIGH);

  // Mostra SSID e senha carregados
  Serial.printf("SSID carregado: \"%s\"\n", ssid.c_str());
  Serial.printf("Senha carregada: \"%s\"\n", password.c_str());

  // Configura conexão com o servidor MQTT
  client.setServer(mqtt_server, mqtt_port);

  // Conecta ao melhor ponto de acesso
  connectToBestAP();
}

// ===== LOOP PRINCIPAL =====
void loop() {
  // Permite entrar no modo configuração via comando serial "config"
  if (Serial.available()) {
    String entrada = Serial.readStringUntil('\n');
    entrada.trim();
    if (entrada == "config") {
      entrarModoConfiguracao();
      return;
    }
  }

  // Reconexão Wi-Fi/MQTT se necessário
  if (WiFi.status() != WL_CONNECTED) connectToBestAP();
  if (!client.connected()) connectToMQTT();
  client.loop();

  // Leitura do nível da bateria
  int raw = analogRead(BATT_PIN);
  float voltage = (raw / 4095.0) * 3.3;  // Converte leitura ADC para tensão
  float percent = (voltage - VOLTAGE_MIN) / (VOLTAGE_MAX - VOLTAGE_MIN) * 100.0;
  percent = constrain(percent, 0.0, 100.0);

  // Mostra status no display
  drawStatus(percent);

  // Envia dados a cada intervalo definido
  if (millis() - lastScan > scanInterval) {
    lastScan = millis();
    connectToBestAP();               // Reconecta se necessário
    sendBSSIDViaMQTT();               // Envia BSSID via MQTT
    sendBatteryViaMQTT((int)percent); // Envia nível da bateria via MQTT
  }

  delay(1000);
}

// ===== Modo de configuração serial =====
void entrarModoConfiguracao() {
  String id = "";
  String newSsid = "";
  String newPass = "";

  // Solicita novo ID
  Serial.println("Digite novo ID (apenas número):");
  while (id.length() == 0) {
    if (Serial.available()) {
      id = Serial.readStringUntil('\n');
      id.trim();
    }
  }

  // Solicita novo SSID
  Serial.println("Digite novo SSID:");
  while (newSsid.length() == 0) {
    if (Serial.available()) {
      newSsid = Serial.readStringUntil('\n');
      newSsid.trim();
    }
  }

  // Solicita nova senha
  Serial.println("Digite nova senha:");
  while (newPass.length() == 0) {
    if (Serial.available()) {
      newPass = Serial.readStringUntil('\n');
      newPass.trim();
    }
  }

  // Salva no NVS
  prefs.begin("mqtt", false);
  prefs.putString("client_id", id);
  prefs.putString("ssid", newSsid);
  prefs.putString("password", newPass);
  prefs.end();

  Serial.println("Configuração salva. Reiniciando...");
  delay(500);
  ESP.restart();
}

// ===== Atualiza display com informações =====
void drawStatus(int percent) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.printf("ID: %s\n", mqtt_client_id.c_str());
  display.printf("Bateria: %d%%", percent);
  display.display();
}

// ===== Seleciona e conecta ao melhor ponto de acesso =====
void connectToBestAP() {
  int numNetworks = WiFi.scanNetworks();
  if (numNetworks == 0) {
    Serial.println("Nenhuma rede WiFi encontrada.");
    return;
  }

  int bestSignal = -100;
  String bestBSSID;
  for (int i = 0; i < numNetworks; i++) {
    if (WiFi.SSID(i) == ssid && WiFi.RSSI(i) > bestSignal) {
      bestSignal = WiFi.RSSI(i);
      bestBSSID = WiFi.BSSIDstr(i);
    }
  }

  if (bestSignal == -100) {
    Serial.println("SSID desejado não encontrado.");
    return;
  }

  // Evita reconectar se já está na melhor rede
  if (WiFi.status() == WL_CONNECTED && WiFi.BSSIDstr() == bestBSSID) {
    Serial.println("Já conectado à melhor rede.");
    return;
  }

  // Conexão
  Serial.printf("Conectando a SSID: %s\n", ssid.c_str());
  WiFi.disconnect(true);
  WiFi.begin(ssid.c_str(), password.c_str());

  int timeout = 15;
  while (WiFi.status() != WL_CONNECTED && timeout-- > 0) {
    delay(1000);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWi-Fi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFalha ao conectar.");
  }
}

// ===== Conecta ao broker MQTT =====
void connectToMQTT() {
  for (int i = 0; i < 5 && !client.connected(); i++) {
    client.connect(mqtt_client_id.c_str());
    delay(3000);
  }
}

// ===== Envia BSSID via MQTT =====
void sendBSSIDViaMQTT() {
  if (WiFi.status() == WL_CONNECTED && client.connected()) {
    String payload = mqtt_client_id + "|" + WiFi.BSSIDstr();
    client.publish("esp32/bssid", payload.c_str());
  }
}

// ===== Envia nível da bateria via MQTT =====
void sendBatteryViaMQTT(int percent) {
  if (WiFi.status() == WL_CONNECTED && client.connected()) {
    String payload = mqtt_client_id + "|" + String(percent);
    client.publish("esp32/battery", payload.c_str());
  }
}
