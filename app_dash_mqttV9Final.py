# IMPORTS E CONFIGURAÇÃO INICIAL
import json
import os
import math
from dash import Dash, dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import folium
from folium import Marker, Icon, PolyLine, Map, DivIcon
from geopy.distance import geodesic
from branca.element import Figure
import datetime

import random  # Adicionado para deslocamento de marcadores

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
    {
        "id": "AP-1",
        "nome": "São Paulo-Morumbi e Jardim Guedala",
        "coord": (-23.5995, -46.7152),
        "bssid": "DE:96:70:F0:75:E1"
    },
    {
        "id": "AP-2",
        "nome": "Jardim Guedala e Morumbi",
        "coord": (-23.6050, -46.7140),
        "bssid": "02:9B:CD:05:1E:BE"
    },
    {
        "id": "AP-3",
        "nome": "Morumbi e Paraisópolis",
        "coord": (-23.6120, -46.7135),
        "bssid": "68:D4:0C:D5:2D:9F"
    },
    {
        "id": "AP-4",
        "nome": "Paraisópolis e Américo Maurano",
        "coord": (-23.6225, -46.7136),
        "bssid": "DE:96:70:F0:75:E4"
    },
    {
        "id": "AP-5",
        "nome": "Vila Andrade e Jardim Jussara",
        "coord": (-23.6375, -46.7120),
        "bssid": "DE:96:70:F0:75:E5"
    },
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

def deslocar_coord(coord, index, total):
    offset = 0.001
    if total % 2 == 1:
        base_index = index - total // 2
    else:
        base_index = index - (total // 2 - 0.5)
    deslocamento = base_index * offset
    return (coord[0], coord[1] + deslocamento)

# MAPA COM INCIDENTE E ESP MAIS PRÓXIMO
def gerar_mapa(esps, n, incidente_id):
    media_lat = sum(coord[0] for _, coord in locations) / len(locations)
    media_lon = sum(coord[1] for _, coord in locations) / len(locations)

    fig = Figure(width=700, height=500)
    mapa = folium.Map(
        location=(media_lat, media_lon),
        zoom_start=14,
        tiles="CartoDB positron",
        zoom_control=True,
        scrollWheelZoom=False,
        dragging=False
    )
    fig.add_child(mapa)

    PolyLine([coord for _, coord in locations], color="gold", weight=5).add_to(mapa)

    elementos = []
    for nome, coord in locations:
        elementos.append((coord, {
            "tooltip": nome,
            "icon": Icon(color="red", icon="train", prefix='fa')
        }))
        folium.Marker(
            location=(coord[0] + 0.001, coord[1] + 0.001),
            icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 12px; color: black; text-align: left; font-weight: bold;">{nome}</div>'
            )
        ).add_to(mapa)

    for ap in access_points:
        elementos.append((ap["coord"], {
            "tooltip": ap["id"],
            "icon": Icon(color="blue", icon="wifi", prefix="fa")
        }))
        folium.Marker(
            location=(ap["coord"][0] + 0.001, ap["coord"][1] + 0.001),
            icon=DivIcon(
                icon_size=(150, 36),
                icon_anchor=(0, 0),
                html=f'<div style="font-size: 12px; color: black; text-align: left; font-weight: bold;">{ap["id"]}</div>'
            )
        ).add_to(mapa)

    for esp in esps:
        categoria = esp.get("categoria", "desconhecida")
        coord = esp["ap"]["coord"]
        tooltip = f"{esp['client_id']} ({categoria})\nAP: {esp['ap']['nome']}\nÚltima: {esp['last_seen_formatado']}"
        icon = Icon(color="green", icon="microchip", prefix="fa")
        elementos.append((coord, {"tooltip": tooltip, "icon": icon}))

    trem_coord = calcular_posicao_trem(n)
    elementos.append((trem_coord, {
        "tooltip": "🚇 Trem em movimento",
        "icon": Icon(color="green", icon="subway", prefix="fa")
    }))

    incidente = next((i for i in incident_log if i["id"] == incidente_id), None)
    if incidente:
        incidente_coord = trem_coord if incidente["local"] == "trem" else dict(locations)[incidente["local"]]

        # Remover marcador original no local do incidente
        elementos = [e for e in elementos if tuple(e[0]) != tuple(incidente_coord)]

        # Adicionar marcador de incidente
        elementos.append((incidente_coord, {
            "tooltip": f"📍 Incidente: {incidente['local']} ({incidente['categoria']})",
            "icon": Icon(color="orange", icon="exclamation-triangle", prefix="fa")
        }))

        esps_categoria = [e for e in esps if e.get("categoria") == incidente["categoria"]]
        if esps_categoria:
            mais_proximo = min(
                esps_categoria,
                key=lambda esp: geodesic(esp["ap"]["coord"], incidente_coord).meters
            )
            distancia_metros = geodesic(mais_proximo["ap"]["coord"], incidente_coord).meters
            velocidade_mps = 1.2
            tempo_minutos = round(distancia_metros / velocidade_mps / 60, 1)

            tooltip = (
                f"🚘 {mais_proximo['client_id']} ({mais_proximo['categoria']})\n"
                f"Distância: {int(distancia_metros)} m\n"
                f"Estimativa de chegada: {tempo_minutos} min"
            )

            # Remover marcador original do ESP mais próximo
            elementos = [e for e in elementos if tuple(e[0]) != tuple(mais_proximo["ap"]["coord"])]

            # Adicionar marcador destacado do ESP mais próximo
            elementos.append((mais_proximo["ap"]["coord"], {
                "tooltip": tooltip,
                "icon": Icon(color="darkred", icon="user-shield", prefix="fa")
            }))
        else:
            tooltip = f"❌ Nenhum dispositivo da categoria '{incidente['categoria']}' disponível nas proximidades"
            elementos.append((incidente_coord, {
                "tooltip": tooltip,
                "icon": Icon(color="gray", icon="ban", prefix="fa")
            }))

    # Agrupar por coordenada e aplicar deslocamento
    coord_map = {}
    for coord, dados in elementos:
        key = tuple(coord)
        if key not in coord_map:
            coord_map[key] = []
        coord_map[key].append(dados)

    for coord, grupo in coord_map.items():
        total = len(grupo)
        for i, dados in enumerate(grupo):
            deslocada = deslocar_coord(coord, i, total)
            Marker(
                deslocada,
                tooltip=dados["tooltip"],
                icon=dados["icon"]
            ).add_to(mapa)

    mapa.save("map.html")
    with open("map.html", "r", encoding="utf-8") as f:
        html_data = f.read()

    return html.Iframe(srcDoc=html_data, width="100%", height="585")

# DASH APP
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Monitor de Agentes"

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
    dcc.Interval(id="interval", interval=10000, n_intervals=0),
    dcc.Store(id="mostrar_esps_store", data=False),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Div(id="mapa"),
                dbc.Button(
                    id="botao_mostrar_esps",
                    color="secondary",
                    size="sm",
                    style={"marginTop": "10px", "marginBottom": "10px"},
                    children="👁️ Mostrar todos os dispositivos"
                )
            ]),
            width=6,
            style={"height": "100%", "overflow": "hidden"}
        ),
        dbc.Col([
            html.Div(id="lista_esps"),
            html.Hr(),
            html.H4("🛠️ Categorizar Dispositivos"),
            html.Div(id="categorias_esp_ui"),
            html.Hr(),
            dbc.Button(
                "📶 Mostrar Access Points",
                id="toggle_ap_detalhes",
                color="info",
                size="sm",
                style={"marginBottom": "10px"}
            ),
            dbc.Collapse(
                html.Div(id="tabela_ap_detalhes"),
                id="collapse_ap_detalhes",
                is_open=False
            )
        ], width=6, style={"maxHeight": "85vh", "overflowY": "auto"})
    ])
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
    State("mostrar_esps_store", "data"),
    State("incidente_selecionado", "value")
)
def atualizar(n, mostrar_esps_clicks, incidente_id):
    mostrar_todos_esps = mostrar_esps_clicks and mostrar_esps_clicks > 0

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
                    esp["delta"] = delta
                    esp["status"] = "conectado" if delta < 60 else esp["last_seen_formatado"]
                    esps_historico.append(esp)
                    if delta < 300:
                        esps_ativos.append(esp)
            except:
                pass

    incidente = next((i for i in incident_log if i["id"] == incidente_id), None)

    # Decidir quais ESPs mostrar no mapa
    if mostrar_todos_esps:
        esps_para_mapa = esps_ativos
    elif incidente:
        esps_para_mapa = [e for e in esps_ativos if e.get("categoria") == incidente["categoria"]]
    else:
        esps_para_mapa = []

    mapa = gerar_mapa(esps_para_mapa, n, incidente_id)

    lista_unificada = html.Div([
        html.H4("📡 Lista de Dispositivos"),
        html.Ul([
            html.Li(
                html.Span([
                    html.Strong(esp["client_id"]),
                    f" ({esp['categoria']}) — AP: {esp['ap']['nome']} — ",
                    html.Span("🟢 CONECTADO", style={"color": "green"}) if esp["status"] == "conectado"
                    else html.Span(f"Última: {esp['status']}", style={"color": "gray"})
                ])
            ) for esp in esps_historico
        ]) if esps_historico else html.P("⚠️ Nenhum dispositivo registrado.", style={"color": "gray"})
    ])

    categoria_ui = html.Div([
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
            html.Li(f"{ap['id']} — {ap['nome']} — BSSID: {ap['bssid']}")
            for ap in access_points
        ])
    ])

    return mapa, lista_unificada, tabela, categoria_ui

# CALLBACK: SALVA CATEGORIAS (PERSISTENTE)
@app.callback(
    Output("collapse_ap_detalhes", "is_open"),
    Input("toggle_ap_detalhes", "n_clicks"),
    State("collapse_ap_detalhes", "is_open"),
    prevent_initial_call=True
)
def toggle_collapse_ap(n_clicks, is_open):
    return not is_open

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

#CALLBACK: BOTAO DE MOSTRAR E DESMOSTRAR DISPOSITIVOS
@app.callback(
    Output("mostrar_esps_store", "data"),
    Input("botao_mostrar_esps", "n_clicks"),
    State("mostrar_esps_store", "data"),
    prevent_initial_call=True
)
def alternar_modo_mostragem(n_clicks, estado_atual):
    return not estado_atual

@app.callback(
    Output("botao_mostrar_esps", "children"),
    Input("mostrar_esps_store", "data")
)
def atualizar_texto_botao(estado):
    if estado:
        return "🙈 Ocultar dispositivos (modo incidente)"
    return "👁️ Mostrar todos os dispositivos"


# RODAR APP
if __name__ == "__main__":
    app.run(debug=True, port=8050)
