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

## Topologia do Sistema

O sistema conecta diferentes dispositivos para comunicação remota no metrô, com agentes portando ESP32-C6 que enviam dados via MQTT para um servidor. O servidor processa e armazena essas informações, permitindo que o analista visualize, pelo Dash em Python, o status da linha, a proximidade dos agentes e a ocupação das estações, garantindo geolocalização indoor com atualização constante.

<img width="845" height="580" alt="Arquitetura da Rede" src="https://github.com/user-attachments/assets/e99cb1bd-0f3a-4e33-8176-37be966eff74" />

---

## Como Configurar

### 1. Alterar o ID do dispositivo (ESP32-C6), SSID e senha

Após conectar o ESP32-C6 na USB, execute o programa `configuracao_esp`. Ele abrirá um terminal solicitando que você selecione a porta serial correta conectada a ESP32-C6. Após selecionar a correta, ele perguntará qual o novo ID da ESP32-C6 e será necessário informar ou caso seja mantido o mesmo ID é necessário pressionar enter. Após isso, o mesmo processo ocorrerá para SSID (nome da rede de conexão) e senha.

> Esse ID será usado para identificar o agente no dashboard.
> O SSID identifica o nome da conexão dos Acess Points.
> A senha permitirá o acesso ao Acess Point da rede.

---

### 2. Cadastrar Access Points e Agentes no Backend

No arquivo `mqtt_receiverV2.py`, dois dicionários principais devem ser atualizados:

#### a) `access_points_detalhados`

Dicionário que mapeia cada BSSID (MAC do ponto de acesso) para um nome de estação e suas coordenadas:

```python
access_points_detalhados = {
    "DE:96:70:F0:75:E1": {
        "id": "AP-1",
        "nome": "São Paulo-Morumbi e Jardim Guedala",
        "coord": (-23.5995, -46.7152),
        "bssid": "DE:96:70:F0:75:E1"
    },
    ...
}
```

#### b) `nome_dispositivos`

Converte o `client_id` enviado pelo ESP em um nome mais amigável para exibição:

```python
nome_dispositivos = {
    "ESP32C6_1": "Agente_1",
    "ESP32C6_2": "Agente_2",
    ...
}
```

---

## Como Executar o Dashboard

1. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

2. **Execute o script**:

```bash
python app_dash_mqttV5FinalLogos.py
```

3. **Acesse o dashboard no navegador**:  
[http://[localhost:8050]

---

### 📌 Legenda da Interface

Abaixo, a legenda dos elementos exibidos no mapa da interface:

<img width="713" height="422" alt="Legenda" src="https://github.com/user-attachments/assets/65ad5b6d-a0c8-418c-8e7c-c581ca2ead7e" />

**Descrição dos ícones:**
- **Trem em movimento**: marcador verde com vagão  — representa o trem simulado em movimento.
- **Incidente**: ícone de alerta amarelo (⚠️) — indica uma ocorrência registrada pelo operador.
- **Dispositivo**: Ilustra todos os dispositivos ativos
- **Dispositivo mais próximo**: marcador vermelho escuro com ícone de pessoa — representa o dispositivo ESP32-C6 carregado por um agente em campo.
- **Sem dispositivo disponível**: Marcador que representa a ausência de dispositivos disponíveis.
- **Estação**: marcador vermelho com símbolo de trem — representa a localização fixa das estações do Metrô.


Esses ícones foram escolhidos para facilitar a visualização e interpretação por parte do operador, contribuindo para decisões rápidas e informadas durante a operação do sistema.

---

## 🗃️ Modelo de Banco de Dados

Abaixo está o modelo relacional utilizado para persistência dos dados de geolocalização no sistema:

![image](https://github.com/user-attachments/assets/d3b1c12e-757d-4dfd-864b-0851c2b3e246)


**Descrição das tabelas:**

- **informacoes_geolocalizacao**  
  Guarda os registros principais, contendo data/hora, ID do dispositivo, ID do ponto de acesso (BSSID) e tipo de agente.

- **estoque_dispositivos**  
  Lista os dispositivos cadastrados, com número de série e status de ativação.

- **bssid_estacoes**  
  Tabela com os access points (BSSID), associando-os a nomes de estações e suas coordenadas geográficas (latitude/longitude).

- **tipo_de_funcionario**  
  Define os tipos de agentes (exemplo: segurança, manutenção) para categorização e filtros no dashboard.

---

## Estrutura de Arquivos

```
.
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt
├── TCC GEOLOCALIZACAO.pdf
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
