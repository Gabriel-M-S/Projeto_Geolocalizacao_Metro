
/****** Tabela de Dados Enviados pela ESP-C6 ao banco de dados constando informações de id do bssid conectado, data e hora, id do dispositivo esp e id tipo de dispositivo (atrelado a função de segurança e manutenção) ******/

CREATE TABLE [dbo].[BASE_GEOLOCALIZACAO](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_esp_bssid] [varchar](50) NULL,
	[data_hora] [datetime] NULL,
	[id_dispositivo] [int] NULL,
	[id_tipo] [varchar](50) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Tabela De Para com Dados de Nome de Estação Atrelado ao BSSID de cada ESP-C6 ******/

CREATE TABLE [dbo].[DEPARA_BSSID_ESTACAO](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[id_esp_bssid] [varchar](50) NOT NULL,
	[nome_estacao] [varchar](100) NOT NULL,
 CONSTRAINT [PK_DEPARA_BSSID_ESTACAO] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

/****** Tabela De Para com Informações de Latitude e Longitude de Cada uma das Estações ******/


CREATE TABLE [dbo].[ESTACAO_COORDENADAS](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nome_estacao] [varchar](100) NOT NULL,
	[latitude] [float] NOT NULL,
	[longitude] [float] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO


