# 📡 Estudo Sobre Rede Sem Fio Aplicada na Geolocalização de Agentes Circulantes

> Projeto de TCC apresentado ao Centro Universitário FEI — Engenharia Elétrica  
> Foco: Geolocalização indoor via Wi-Fi 6 usando ESP32-C6 no Metrô de São Paulo

---

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

## 📁 Estrutura do Projeto

```
📂 TCC_Geolocalizacao_Metro
├── 📜 README.md
├── 📄 TCC MASTER BLASTER PRINCIPAL.docx     <- Monografia
├── 📄 Apresentação_TCC_Metro_VF.pptx        <- Slides finais
├── 📄 tccfinal1_1.ino                        <- Código embarcado no ESP32-C6
├── 📄 mqtt_receiverV2.py                    <- Servidor MQTT para coleta dos dados
├── 📄 app_dash_mqttV5FinalLogos.py          <- Dashboard Python com mapa e incidentes
├── 📄 dados_esps.json                        <- Dados dos dispositivos (gerado em runtime)
├── 📄 esp_categorias.json                    <- Categorização dos dispositivos (opcional)
├── 📄 LICENSE                                <- Licença do projeto
├── 📄 METROFEI.pbix                          <- Relatório Power BI com visualização dos dados
```

---

## 🚀 Como Executar

### 📟 Código do Microcontrolador (ESP32-C6)

- Utiliza Wi-Fi Scan para identificar BSSID e RSSI dos APs
- Envia via MQTT no formato:  
  ```
  client_id|bssid
  ```
- Tópico utilizado: `esp32/bssid`

### 🧠 Backend MQTT (coleta dos dados)

```bash
python mqtt_receiverV2.py
```

Coleta os dados dos dispositivos conectados e salva no arquivo `dados_esps.json`.

### 🖥️ Executar o Dashboard

```bash
python app_dash_mqttV5FinalLogos.py
```

Acesse via navegador: [http://localhost:8050](http://localhost:8050)

---

## 🗺️ Funcionalidades

- Mapeamento de agentes por zona Wi-Fi (sem coordenadas GPS)
- Interface com mapa em tempo real (linha do Metrô e agentes)
- Registro e categorização de incidentes
- Identificação automática do agente mais próximo
- Estimativa de tempo de resposta
- LGPD Compliance: uso ético dos dados de localização
- Visualização adicional com **Power BI** para análises mais ricas e interativas

---

## ⚙️ Tecnologias e Ferramentas

| Categoria          | Ferramenta                          |
|--------------------|-------------------------------------|
| **Hardware**        | ESP32-C6, OLED, Li-Ion, Boost       |
| **Software embarcado** | ESP-IDF, C/C++ (Arduino)         |
| **Backend**         | Python, MQTT (Mosquitto)            |
| **Dashboard**       | Python Dash, Folium, Streamlit      |
| **Visualização extra** | Power BI, Elipse E3             |

---

## ✅ Resultados

- Funcionamento estável em ambiente indoor
- Interface funcional para agentes e operadores
- Autonomia estimada: **~11 horas**
- Baixo custo unitário
- Código modular e expansível

---

## 🔐 Considerações Éticas e LGPD

- Dados coletados apenas para fins operacionais
- Consentimento e transparência priorizados
- Conformidade com a **Lei Geral de Proteção de Dados (LGPD)**

---

## 📄 Licença

Este projeto está licenciado sob os termos da [Licença MIT](https://opensource.org/licenses/MIT). Veja o arquivo [`LICENSE`](./LICENSE) para mais detalhes.

---

## 📬 Contato

📧 Prof. Marco Antônio Assis de Melo — marco.melo@fei.edu.br  
📫 Contribuições: via Pull Request ou Issues neste repositório

---
