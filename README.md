# TCC - Sistema de Geolocalização Indoor com ESP32-C6

Trabalho de Conclusão de Curso — Engenharia Elétrica  
Centro Universitário FEI  
Monitoramento de agentes operacionais no Metrô de São Paulo usando Wi-Fi 6

---

## Autores

Erich Ramos Borges  
Gabriel Marques Silva  
Otavio Meves Ribeiro  
Robert Rivera M. da Silva  
Vinícius Henrique Souza de Melo  
Weslley Silva Santos  

**Orientação:** Prof. Marco Antônio Assis de Melo

---

## Sobre o Projeto

O sistema identifica a posição de agentes dentro de estações do metrô com base na força do sinal (RSSI) dos pontos de acesso Wi-Fi. A localização é aproximada e agrupada por zonas. A comunicação entre dispositivos é feita via MQTT, e os dados são exibidos em um dashboard interativo.

---

## Como Configurar

### 1. Alterar o ID do dispositivo (ESP32-C6)

Abra o arquivo `tccfinal.ino` e localize a linha:

```cpp
const char* mqtt_client_id = "ESP32C6_1"; // Altere para identificar o dispositivo
```


> Esse ID será usado para identificar o agente no dashboard.

---

### 2. Cadastrar novos Access Points e Estações

No arquivo `mqtt_receiverV2.py`, edite os seguintes dicionários:

#### BSSID para nome da estação:

```python
access_points = {
    "DE:96:70:F0:75:E1": "AP-1",
    "02:9B:CD:05:1E:BE": "AP-2",
    ...
}
```

#### Coordenadas da estação:

```python
coord_lookup = {
    "AP-1": (-23.5995, -46.7152),
    "AP-2": (-23.6050, -46.7140),
    ...
}
```

> O nome da estação (ex: `"AP-1"`) deve ser o mesmo nos dois blocos.

---

## 🖥️ Como Executar o Dashboard

1. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

2. **Execute o script**:

```bash
python app_dash_mqttV5FinalLogos.py
```

3. **Acesse o dashboard no navegador**:  
[http://localhost:8050](http://localhost:8050)

---

### 📌 Legenda da Interface

Abaixo, a legenda dos elementos exibidos no mapa da interface:

![image](https://github.com/user-attachments/assets/73997dca-daf9-4b51-ba8c-2ed991d36df3)

**Descrição dos ícones:**
- **Access Point (Wi-Fi)**: marcador azul com símbolo de sinal — representa os pontos de acesso detectados via escaneamento de BSSID.
- **Agente**: marcador vermelho escuro com ícone de pessoa — representa o dispositivo ESP32-C6 carregado por um agente em campo.
- **Incidente**: ícone de alerta amarelo (⚠️) — indica uma ocorrência registrada pelo operador.
- **Estação**: marcador vermelho com símbolo de trem — representa a localização fixa das estações do Metrô.
- **Metrô**: marcador verde com símbolo de trem — representa o vagão em movimento.
  
Esses ícones foram escolhidos para facilitar a visualização e interpretação por parte do operador, contribuindo para decisões rápidas e informadas durante a operação do sistema.

---

## Estrutura de Arquivos

```
.
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt
├── TCC GEOLOCALIZACAO.docx
├── Apresentação_TCC_Metro_VF.pptx
├── METROFEI.pbix
├── Query_Criacao_Banco_de_Dados.sql
├── tccfinal.ino
├── mqtt_receiverV2.py
├── app_dash_mqttV5FinalLogos.py
├── Hardware_Geolocalização.f3z
└── dados_esps.json
```

---

## Tecnologias

- ESP32-C6 com Arduino IDE
- Python 3.10
- Dash, Folium, paho-mqtt
- PostgreSQL ou SQLite
- Power BI

---

## Licença

Distribuído sob a licença MIT. Veja o arquivo [`LICENSE`](LICENSE).

---

## Contato

Prof. Marco Antônio Assis de Melo — marco.melo@fei.edu.br

---
