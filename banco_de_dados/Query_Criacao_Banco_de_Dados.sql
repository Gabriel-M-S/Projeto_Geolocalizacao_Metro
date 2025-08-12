-- Tabela principal de geolocalização
CREATE TABLE informacoes_geolocalizacao (
    id INT IDENTITY(1,1) PRIMARY KEY,
    data_hora DATETIME NOT NULL,
    id_dispositivo INT NOT NULL,
    id_esp_bssid INT NOT NULL,
    id_tipo INT NOT NULL
);
GO

-- Estoque de dispositivos
CREATE TABLE estoque_dispositivos (
    id_dispositivo INT PRIMARY KEY,
    numero_serial INT NOT NULL,
    status_ativo BIT NOT NULL
);
GO

-- Tabela de BSSID e estações
CREATE TABLE bssid_estacoes (
    id_esp_bssid INT IDENTITY(1,1) PRIMARY KEY,
    nome_estacao NVARCHAR(100) NOT NULL,
    latitude NVARCHAR(50),
    longitude NVARCHAR(50)
);
GO

-- Tipo de funcionário
CREATE TABLE tipo_de_funcionario (
    id_tipo INT IDENTITY(1,1) PRIMARY KEY,
    tipo_funcionario NVARCHAR(50) NOT NULL
);
GO

-- Restrições de chave estrangeira
ALTER TABLE informacoes_geolocalizacao
    ADD CONSTRAINT FK_informacoes_dispositivo
    FOREIGN KEY (id_dispositivo) REFERENCES estoque_dispositivos(id_dispositivo);
GO

ALTER TABLE informacoes_geolocalizacao
    ADD CONSTRAINT FK_informacoes_bssid
    FOREIGN KEY (id_esp_bssid) REFERENCES bssid_estacoes(id_esp_bssid);
GO

ALTER TABLE informacoes_geolocalizacao
    ADD CONSTRAINT FK_informacoes_tipo
    FOREIGN KEY (id_tipo) REFERENCES tipo_de_funcionario(id_tipo);
GO
