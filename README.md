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
- Armazenamento estruturado em banco de dados relacional

Ao invés de coordenadas exatas, o sistema identifica **zonas de proximidade** com base no RSSI (Received Signal Strength Indicator) dos APs mapeados.

---

## 📁 Estrutura do Projeto

```
📂 TCC_Geolocalizacao_Metro
├── 📜 README.md                              <- Documentação do projeto
├── 📄 LICENSE                                <- Licença MIT
├── 📄 TCC GEOLOCALIZACAO.docx                <- Monografia completa
├── 📄 Apresentação_TCC_Metro_VF.pptx         <- Apresentação final
├── 📄 METROFEI.pbix                          <- Relatório Power BI
├── 📄 Query_Criacao_Banco_de_Dados.sql       <- Script de criação do banco de dados
├── 📄 tccfinal.ino                           <- Código embarcado no ESP32-C6
├── 📄 mqtt_receiverV4.py                     <- Backend MQTT atualizado
├── 📄 app_dash_mqttV9Final.py                <- Dashboard Python com visualização e integração ao banco
└── 📄 dados_esps.json                        <- Gerado automaticamente em tempo de execução
```

---

## 🗃️ Banco de Dados

A estrutura do banco de dados é composta por três tabelas principais:

### 🧩 Modelo Relacional

![Modelo ER do Banco de Dados](./ff1a5eba-a619-48ea-85c6-a4135e2ece46.png)

### 🏗️ Tabelas

- **BASE_GEOLOCALIZACAO**  
  Armazena os dados de localização recebidos dos dispositivos.

- **DEPARA_BSSID_ESTACAO**  
  Faz a correspondência entre BSSID (AP) e o nome da estação.

- **ESTACAO_COORDENADAS**  
  Guarda as coordenadas (latitude/longitude) vinculadas a cada estação.

### 📜 Script de Criação

O script SQL `Query_Criacao_Banco_de_Dados.sql` permite a criação de toda a estrutura relacional, incluindo as chaves e relacionamentos.

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
python mqtt_receiverV4.py
```

Salva os dados recebidos no arquivo JSON e/ou insere no banco de dados, conforme a configuração.

### 🖥️ Executar o Dashboard

```bash
python app_dash_mqttV9Final.py
```

Acesse via navegador: [http://localhost:8050](http://localhost:8050)

---

## 🗺️ Funcionalidades

- Mapeamento de agentes por zona Wi-Fi (sem coordenadas GPS)
- Interface com mapa em tempo real
- Registro e categorização de incidentes
- Estimativa de tempo de resposta
- LGPD Compliance: uso ético dos dados
- Armazenamento estruturado e persistente em banco relacional
- Relatórios com Power BI

---

## ⚙️ Tecnologias e Ferramentas

| Categoria              | Ferramenta                          |
|------------------------|-------------------------------------|
| **Hardware**           | ESP32-C6, OLED, Li-Ion, Boost       |
| **Software embarcado** | ESP-IDF, C/C++ (Arduino)            |
| **Backend**            | Python, MQTT (Mosquitto)            |
| **Dashboard**          | Python Dash, Folium, Streamlit      |
| **Banco de dados**     | SQL (PostgreSQL ou SQLite)          |
| **Visualização extra** | Power BI, Elipse E3                 |

---

## ✅ Resultados

- Funcionamento estável em ambiente indoor
- Interface funcional com banco de dados
- Visualização em tempo real com Dash
- Análises em Power BI
- Autonomia estimada: **~11 horas**
- Código modular, expansível e documentado

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
