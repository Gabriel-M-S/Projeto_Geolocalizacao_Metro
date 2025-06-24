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

## Estrutura de Arquivos

```
.
├── .gitignore                        # Ignora arquivos desnecessários
├── README.md                         # Este arquivo
├── LICENSE                           # Licença MIT
├── requirements.txt                  # Dependências Python
├── TCC GEOLOCALIZACAO.docx           # Relatório final
├── Apresentação_TCC_Metro_VF.pptx    # Slides
├── METROFEI.pbix                     # Relatório Power BI
├── Query_Criacao_Banco_de_Dados.sql  # Script SQL do banco
├── tccfinal.ino                      # Código do ESP32-C6
├── mqtt_receiverV4.py                # Backend que recebe dados por MQTT
├── app_dash_mqttV9Final.py           # Dashboard com mapa e banco de dados
├── Hardware_Geolocalização.f3z       # Esquemático do circuito
└── dados_esps.json                   # Dados gerados em tempo de execução
```

---

## Componentes do Sistema

- **ESP32-C6**: envia BSSID dos APs Wi-Fi via MQTT
- **Python MQTT**: recebe e processa as mensagens
- **Dashboard**: exibe a posição estimada dos agentes
- **Banco de dados SQL**: armazena registros de localização
- **Power BI**: análise dos dados e relatórios

---

## Como Rodar

1. **Receber dados dos ESPs**

```bash
python mqtt_receiverV4.py
```

2. **Executar o dashboard**

```bash
python app_dash_mqttV9Final.py
```

Acesse em: http://localhost:8050

3. **Criar banco de dados (opcional)**

Use o script `Query_Criacao_Banco_de_Dados.sql` com PostgreSQL ou SQLite.

---

## Funcionalidades

- Identificação da estação mais próxima com base no Wi-Fi
- Visualização em tempo real dos agentes
- Registro de incidentes
- Estimativa de tempo de resposta
- Dados salvos localmente e/ou no banco
- Relatórios analíticos com Power BI

---

## Tecnologias

- ESP32-C6 com Arduino IDE
- Python 3.10
- Dash, Folium, paho-mqtt
- PostgreSQL ou SQLite
- Power BI

---

## Licença

Distribuído sob a licença MIT. Veja o arquivo [`LICENSE`](LICENSE) para mais informações.

---

## Contato

Professor orientador: marco.melo@fei.edu.br  
Para dúvidas ou sugestões: crie um Issue neste repositório.
