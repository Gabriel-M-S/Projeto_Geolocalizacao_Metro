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

---

## 📁 Estrutura do Projeto

```
📂 TCC_Geolocalizacao_Metro
├── .gitignore                              <- Ignora arquivos desnecessários no Git
├── README.md                               <- Documentação principal do projeto
├── LICENSE                                 <- Licença MIT
├── requirements.txt                        <- Dependências Python
├── TCC GEOLOCALIZACAO.docx                 <- Monografia final
├── Apresentação_TCC_Metro_VF.pptx          <- Slides da apresentação
├── METROFEI.pbix                           <- Relatório em Power BI
├── Query_Criacao_Banco_de_Dados.sql        <- Script SQL do banco de dados
├── tccfinal.ino                            <- Código embarcado no ESP32-C6
├── mqtt_receiverV4.py                      <- Backend MQTT para recepção de dados
├── app_dash_mqttV9Final.py                 <- Dashboard com mapa e conexão ao banco
└── dados_esps.json                         <- Arquivo gerado com dados de localização
```

---

## 🗃️ Banco de Dados

- **BASE_GEOLOCALIZACAO**: Registro das mensagens recebidas dos dispositivos  
- **DEPARA_BSSID_ESTACAO**: Relaciona BSSID com estações  
- **ESTACAO_COORDENADAS**: Coordenadas das estações para visualização em mapa

Use o script `Query_Criacao_Banco_de_Dados.sql` para criar toda a estrutura.

---

## 🚀 Como Executar

### 📟 ESP32-C6

- Envia mensagens via MQTT no formato `client_id|bssid` para o tópico `esp32/bssid`

### 🧠 Coletor MQTT (Python)

```bash
python mqtt_receiverV4.py
```

Armazena os dados recebidos em arquivo e/ou banco de dados.

### 🖥️ Dashboard

```bash
python app_dash_mqttV9Final.py
```

Interface com mapa, visualização de agentes, incidentes e tempo de resposta.  
Acesse em: [http://localhost:8050](http://localhost:8050)

---

## 🗺️ Funcionalidades

- Visualização em tempo real de agentes por zona Wi-Fi
- Registro e categorização de incidentes
- Cálculo do agente mais próximo
- Análise por Power BI
- Armazenamento em banco relacional
- Conformidade com LGPD

---

## ⚙️ Tecnologias Utilizadas

| Categoria              | Ferramentas                          |
|------------------------|--------------------------------------|
| Hardware               | ESP32-C6, Li-Ion, OLED               |
| Backend MQTT           | Python, paho-mqtt                    |
| Dashboard              | Dash, Folium, Bootstrap              |
| Banco de Dados         | PostgreSQL / SQLite (flexível)       |
| Visualização Analítica | Power BI, Elipse E3                  |

---

## ✅ Resultados

- Sistema funcional em ambiente indoor
- Integração completa com banco de dados
- Interface web responsiva
- Ferramentas de análise em Power BI
- Projeto modular e expansível

---

## 🔐 Ética e LGPD

- Dados anonimizados e com finalidade definida
- Sem rastreamento pessoal
- Em conformidade com a LGPD

---

## 📄 Licença

Este projeto está licenciado sob os termos da [Licença MIT](https://opensource.org/licenses/MIT).  
Consulte o arquivo [`LICENSE`](./LICENSE) para mais informações.

---

## 📬 Contato

📧 Prof. Marco Antônio Assis de Melo — marco.melo@fei.edu.br  
📫 Contribuições: via Pull Request ou Issues

---
