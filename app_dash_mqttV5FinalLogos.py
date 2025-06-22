# IMPORTS E CONFIGURAÇÃO INICIAL
import json
import os
from dash import Dash, dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import folium
from folium import Marker, Icon, PolyLine
from geopy.distance import geodesic
from branca.element import Figure
import datetime

data_file = "dados_esps.json"
esp_categorias_file = "esp_categorias.json"
incident_log = []

esp_categorias = {}
if os.path.exists(esp_categorias_file):
    try:
        with open(esp_categorias_file, "r") as f:
            esp_categorias = json.load(f)
    except:
        esp_categorias = {}

# ACCESS POINTS E ESTAÇÕES
access_points = [
    {"nome": "AP-1", "coord": (-23.5995, -46.7152), "bssid": "DE:96:70:F0:75:E1"},
    {"nome": "AP-2", "coord": (-23.6050, -46.7140), "bssid": "02:9B:CD:05:1E:BE"},
    {"nome": "AP-3", "coord": (-23.6120, -46.7135), "bssid": "68:D4:0C:D5:2D:9F"},
    {"nome": "AP-4", "coord": (-23.6225, -46.7136), "bssid": "DE:96:70:F0:75:E4"},
    {"nome": "AP-5", "coord": (-23.6375, -46.7120), "bssid": "DE:96:70:F0:75:E5"},
]

locations = [
    ("São Paulo-Morumbi", (-23.5981, -46.7160)),
    ("Jardim Guedala", (-23.6017, -46.7145)),
    ("Morumbi", (-23.6095, -46.7132)),
    ("Paraisópolis", (-23.6175, -46.7142)),
    ("Américo Maurano", (-23.6260, -46.7138)),
    ("Vila Andrade", (-23.6331, -46.7135)),
    ("Jardim Jussara", (-23.6410, -46.7115)),
]

# POSIÇÃO DO TREM (SIMULADO)
def calcular_posicao_trem(n):
    segmento = n % (len(locations) - 1)
    progresso = (n % 5) / 5.0
    _, inicio = locations[segmento]
    _, fim = locations[segmento + 1]
    lat = inicio[0] + (fim[0] - inicio[0]) * progresso
    lon = inicio[1] + (fim[1] - inicio[1]) * progresso
    return (lat, lon)

# MAPA COM INCIDENTE E ESP MAIS PRÓXIMO
def gerar_mapa(esps, n, incidente_id):
    fig = Figure(width=700, height=500)
    mapa = folium.Map(location=locations[0][1], zoom_start=15, tiles="CartoDB positron")
    fig.add_child(mapa)

    PolyLine([coord for _, coord in locations], color="gold", weight=5).add_to(mapa)

    for nome, coord in locations:
        Marker(coord, tooltip=nome, icon=Icon(color="red", icon="train", prefix='fa')).add_to(mapa)

    for ap in access_points:
        Marker(ap["coord"], tooltip=ap["nome"], icon=Icon(color="blue", icon="wifi", prefix="fa")).add_to(mapa)

    for esp in esps:
        categoria = esp.get("categoria", "desconhecida")
        Marker(
            esp["ap"]["coord"],
            tooltip=f"{esp['client_id']} ({categoria})\nAP: {esp['ap']['nome']}\nÚltima: {esp['last_seen_formatado']}",
            icon=Icon(color="green", icon="microchip", prefix="fa")
        ).add_to(mapa)

    lat, lon = calcular_posicao_trem(n)
    Marker([lat, lon], tooltip="🚇 Vagão em movimento",
           icon=Icon(color="green", icon="subway", prefix="fa")).add_to(mapa)

    incidente = next((i for i in incident_log if i["id"] == incidente_id), None)
    if incidente:
        incidente_coord = (lat, lon) if incidente["local"] == "trem" else dict(locations)[incidente["local"]]
        folium.Marker(
            incidente_coord,
            tooltip=f"📍 Incidente: {incidente['local']} ({incidente['categoria']})",
            icon=Icon(color="orange", icon="exclamation-triangle", prefix="fa")
        ).add_to(mapa)

        esps_categoria = [e for e in esps if e.get("categoria") == incidente["categoria"]]
        if esps_categoria:
            mais_proximo = min(
                esps_categoria,
                key=lambda esp: geodesic(esp["ap"]["coord"], incidente_coord).meters
            )
            distancia_metros = geodesic(mais_proximo["ap"]["coord"], incidente_coord).meters
            velocidade_mps = 1.2  # m/s (simulado)
            tempo_minutos = round(distancia_metros / velocidade_mps / 60, 1)

            folium.Marker(
                mais_proximo["ap"]["coord"],
                tooltip=(
                    f"🆘 {mais_proximo['client_id']} ({mais_proximo['categoria']})\n"
                    f"Distância: {int(distancia_metros)} m\n"
                    f"Estimativa de chegada: {tempo_minutos} min"
                ),
                icon=Icon(color="darkred", icon="user-shield", prefix="fa")
            ).add_to(mapa)
        else:
            folium.Marker(
                incidente_coord,
                tooltip=f"🚫 Nenhum dispositivo da categoria '{incidente['categoria']}' disponível nas proximidades",
                icon=Icon(color="gray", icon="ban", prefix="fa")
            ).add_to(mapa)

    mapa.save("map.html")
    with open("map.html", "r", encoding="utf-8") as f:
        html_data = f.read()

    return html.Iframe(srcDoc=html_data, width="100%", height="520")

# DASH APP
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "ESP32 MQTT Monitor"

app.layout = dbc.Container([
    html.Div([
        dbc.Row([
            dbc.Col(html.Img(src="/assets/metro_logo.png", height="60px"), width=6, style={"textAlign": "left"}),
            dbc.Col(html.Img(src="/assets/fei_logo.png", height="60px"), width=6, style={"textAlign": "right"})
        ], align="center", justify="between", className="mb-4"),
        html.H2("Sistema de Tratativa de Incidentes", style={"textAlign": "center", "marginBottom": "30px"}),
        html.H4("🚨 Reportar Incidente"),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id="local_incidente",
                    options=[{"label": nome, "value": nome} for nome, _ in locations] + [{"label": "🚇 Vagão em movimento", "value": "trem"}],
                    placeholder="Local do incidente"
                )
            ], width=6),
            dbc.Col([
                dcc.Dropdown(
                    id="categoria_incidente",
                    options=[
                        {"label": "Manutenção", "value": "manutencao"},
                        {"label": "Segurança", "value": "seguranca"}
                    ],
                    placeholder="Categoria do incidente"
                )
            ], width=4),
            dbc.Col([
                dbc.Button("Enviar Incidente", id="botao_incidente", color="danger")
            ], width=2)
        ]),
        html.Div(id="mensagem_incidente", style={"marginTop": "10px"})
    ]),
    html.Br(),
    html.Div([
        html.H5("📝 Incidentes registrados"),
        dcc.Dropdown(id="incidente_selecionado", placeholder="Selecione um incidente")
    ]),
    html.Hr(),
    html.H2("📍 Dispositivos ESP32 em Tempo Real"),
    dcc.Interval(id="interval", interval=10000, n_intervals=0),
    html.Div(id="mapa"),
    html.Hr(),
    html.Div(id="lista_esps"),
    html.Hr(),
    html.H4("🛠️ Categorizar Dispositivos"),
    html.Div(id="categorias_esp_ui"),
    html.Hr(),
    html.Div(id="tabela_ap_detalhes")
], fluid=True)

# CALLBACK: REGISTRO DE INCIDENTE
@app.callback(
    Output("mensagem_incidente", "children"),
    Output("incidente_selecionado", "options"),
    Input("botao_incidente", "n_clicks"),
    State("local_incidente", "value"),
    State("categoria_incidente", "value"),
    prevent_initial_call=True
)
def reportar_incidente(n_clicks, local, categoria):
    if local and categoria:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        incidente_id = f"{local}_{categoria}_{timestamp}"
        incident_log.append({
            "id": incidente_id,
            "local": local,
            "categoria": categoria,
            "hora": timestamp
        })
        options = [{"label": f"{i['local']} ({i['categoria']}) - {i['hora']}", "value": i['id']} for i in incident_log]
        return html.Div(f"✅ Incidente registrado em: {local} ({categoria})", style={"color": "green"}), options
    return html.Div("⚠️ Selecione local e categoria antes de enviar.", style={"color": "orange"}), []

# CALLBACK: ATUALIZA MAPA E INTERFACE
@app.callback(
    Output("mapa", "children"),
    Output("lista_esps", "children"),
    Output("tabela_ap_detalhes", "children"),
    Output("categorias_esp_ui", "children"),
    Input("interval", "n_intervals"),
    State("incidente_selecionado", "value")
)
def atualizar(n, incidente_id):
    esps_ativos, esps_historico = [], []
    agora = datetime.datetime.now()
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            try:
                all_esps = json.load(f)
                for esp in all_esps:
                    last_seen = datetime.datetime.strptime(esp["last_seen"], "%Y-%m-%d %H:%M:%S")
                    delta = (agora - last_seen).total_seconds()
                    esp["last_seen_formatado"] = last_seen.strftime("%d/%m/%Y %H:%M:%S")
                    esp["categoria"] = esp_categorias.get(esp["client_id"], "não definida")
                    esps_historico.append(esp)
                    if delta < 300:
                        esps_ativos.append(esp)
            except:
                pass

    mapa = gerar_mapa(esps_ativos, n, incidente_id)

    lista_conectados = html.Div([
        html.H4("✅ Conectados no momento (últimos 5 minutos):"),
        html.Ul([
            html.Li(f"{esp['client_id']} ({esp['categoria']}) — {esp['last_seen_formatado']}")
            for esp in esps_ativos
        ]) if esps_ativos else html.P("⚠️ Nenhum dispositivo conectado agora.", style={"color": "gray"})
    ])

    lista_historico = html.Div([
        html.H4("📜 Histórico de ESPs:"),
        html.Ul([
            html.Li(f"{esp['client_id']} ({esp['categoria']}) — {esp['last_seen_formatado']}")
            for esp in esps_historico
        ])
    ])

    categoria_ui = html.Div([
        html.H5("🧩 Categorizar ESPs"),
        html.Div([
            dbc.Row([
                dbc.Col(html.Div(esp["client_id"]), width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id={"type": "esp_categoria", "index": esp["client_id"]},
                        options=[
                            {"label": "Manutenção", "value": "manutencao"},
                            {"label": "Segurança", "value": "seguranca"}
                        ],
                        value=esp_categorias.get(esp["client_id"], None),
                        placeholder="Selecionar categoria"
                    ),
                    width=5
                )
            ], style={"marginBottom": "5px"})
            for esp in esps_historico
        ])
    ])

    tabela = html.Div([
        html.H4("📶 Access Points:"),
        html.Ul([
            html.Li(f"{ap['nome']} — BSSID: {ap['bssid']} — Local: {ap['coord']}")
            for ap in access_points
        ])
    ])

    return mapa, html.Div([lista_conectados, html.Hr(), lista_historico]), tabela, categoria_ui

# CALLBACK: SALVA CATEGORIAS (PERSISTENTE)
@app.callback(
    Input({"type": "esp_categoria", "index": ALL}, "value"),
    State({"type": "esp_categoria", "index": ALL}, "id"),
    prevent_initial_call=True
)
def salvar_categorias(valores, ids):
    mudou = False
    for val, id_obj in zip(valores, ids):
        if val and esp_categorias.get(id_obj["index"]) != val:
            esp_categorias[id_obj["index"]] = val
            mudou = True
    if mudou:
        with open(esp_categorias_file, "w") as f:
            json.dump(esp_categorias, f, indent=2)

# RODAR APP
if __name__ == "__main__":
    app.run(debug=True, port=8050)
