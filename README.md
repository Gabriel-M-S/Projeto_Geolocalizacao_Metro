# 📡 Estudo Sobre Rede Sem Fio Aplicada na Geolocalização de Agentes Circulantes

> Projeto de TCC apresentado ao Centro Universitário FEI — Engenharia Elétrica  
> Foco: Geolocalização indoor via Wi-Fi 6 usando ESP32-C6 no Metrô de São Paulo

## 👥 Autores

- Erich Ramos Borges  
- Gabriel Marques Silva  
- Otavio Meves Ribeiro  
- Robert Rivera M. da Silva  
- Vinícius Henrique Souza de Melo  
- Weslley Silva Santos  

**Orientador:** Prof. Marco Antônio Assis de Melo

---

## 📚 Descrição

Este projeto propõe o desenvolvimento de um sistema de geolocalização em tempo real de agentes operacionais no Metrô de São Paulo, utilizando:

- Microcontroladores ESP32-C6
- Rede Wi-Fi 6 já existente no Metrô
- Visualização via Dashboards Python (Dash + Folium)
- Comunicação via protocolo MQTT

Ao invés de coordenadas exatas, o sistema identifica **zonas de proximidade** com base no RSSI (Received Signal Strength Indicator) dos APs mapeados.

---

📟 Código do Microcontrolador (ESP32-C6)
Utiliza Wi-Fi Scan para identificar BSSID e RSSI dos APs

Envia via MQTT no formato client_id|bssid no tópico esp32/bssid

🖥️ Executar o Dashboard
bash
Copiar
Editar
python app_dash_mqttV5FinalLogos.py
Acesse via navegador em http://localhost:8050

🧠 Backend MQTT (coleta)
bash
Copiar
Editar
python mqtt_receiverV2.py
Coleta os dados enviados pelos dispositivos e armazena em dados_esps.json.

🗺️ Funcionalidades
Mapeamento de agentes por zona Wi-Fi (sem coordenadas GPS)

Interface com mapa em tempo real (linha do Metrô e agentes)

Registro e categorização de incidentes

Identificação automática do agente mais próximo

Estimativa de tempo de resposta

LGPD Compliance: uso ético dos dados de localização

⚙️ Tecnologias e Ferramentas
Categoria	Ferramenta
Hardware	ESP32-C6, OLED, Li-Ion, Boost
Software embarcado	ESP-IDF, C/C++ (Arduino)
Backend	Python, MQTT (Mosquitto)
Dashboard	Python Dash, Folium, Streamlit
Visualização extra	Power BI, Elipse E3

✅ Resultados
Funcionamento estável em ambiente indoor

Interface funcional para agentes e operadores

Autonomia estimada: ~11 horas

Baixo custo unitário

Código modular e expansível

🔐 Considerações Éticas e LGPD
Dados só coletados para fins operacionais

Consentimento e transparência priorizados

Conformidade com a Lei Geral de Proteção de Dados (LGPD)

