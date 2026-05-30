/*
BD de demostración para curso:
Construcción y Mantenimiento de Software

Usuario demo:
email: demo@fvncr.org
clave: demo

IMPORTANTE:
Para contraseñas se usa HASH + SALT, no encriptación reversible.
*/

CREATE DATABASE CMSoftwareDemo;
GO

USE CMSoftwareDemo;
GO

IF OBJECT_ID('dbo.Token2FA', 'U') IS NOT NULL DROP TABLE dbo.Token2FA;
IF OBJECT_ID('dbo.Usuario', 'U') IS NOT NULL DROP TABLE dbo.Usuario;
GO

CREATE TABLE dbo.Usuario
(
    id_usuario       INT IDENTITY(1,1) PRIMARY KEY,
    email            NVARCHAR(120) NOT NULL UNIQUE,
    clave_hash       VARBINARY(32) NOT NULL,
    clave_salt       VARBINARY(16) NOT NULL,
    nombre           NVARCHAR(100) NOT NULL,
    celular          NVARCHAR(25) NULL,
    activo              BIT NOT NULL DEFAULT(1),
    intentos_fallidos   INT NOT NULL DEFAULT(0),
    fecha_creacion      DATETIME2(0) NOT NULL DEFAULT SYSDATETIME()
);
GO

CREATE TABLE dbo.Token2FA
(
    id_token         INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario       INT NOT NULL,
    token            NVARCHAR(10) NOT NULL,
    tipo             NVARCHAR(20) NOT NULL, -- LOGIN_2FA / RECUPERACION
    fecha_creacion   DATETIME2(0) NOT NULL DEFAULT SYSDATETIME(),
    fecha_expira     DATETIME2(0) NOT NULL,
    usado            BIT NOT NULL DEFAULT(0),

    CONSTRAINT FK_Token2FA_Usuario
        FOREIGN KEY (id_usuario)
        REFERENCES dbo.Usuario(id_usuario)
);
GO

CREATE INDEX IX_Token2FA_Usuario_Tipo
ON dbo.Token2FA(id_usuario, tipo, usado, fecha_expira);
GO

IF OBJECT_ID('dbo.audit_login', 'U') IS NOT NULL DROP TABLE dbo.audit_login;
GO

CREATE TABLE dbo.audit_login
(
    id_audit         INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario       INT NOT NULL,
    evento           NVARCHAR(30) NOT NULL,  -- LOGIN_OK / LOGIN_FALLIDO / CUENTA_BLOQUEADA
    intentos_fallidos INT NOT NULL,
    fecha            DATETIME2(0) NOT NULL DEFAULT SYSDATETIME(),

    CONSTRAINT FK_AuditLogin_Usuario
        FOREIGN KEY (id_usuario)
        REFERENCES dbo.Usuario(id_usuario)
);
GO

CREATE INDEX IX_AuditLogin_Usuario
ON dbo.audit_login(id_usuario, fecha);
GO

CREATE TRIGGER TR_Usuario_AuditLogin
ON dbo.Usuario
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Login fallido: intentos_fallidos aumentó
    INSERT INTO dbo.audit_login(id_usuario, evento, intentos_fallidos)
    SELECT i.id_usuario,
           CASE WHEN i.activo = 0 AND d.activo = 1 THEN N'CUENTA_BLOQUEADA'
                ELSE N'LOGIN_FALLIDO'
           END,
           i.intentos_fallidos
    FROM inserted i
    INNER JOIN deleted d ON i.id_usuario = d.id_usuario
    WHERE i.intentos_fallidos > d.intentos_fallidos;

    -- Login exitoso: intentos_fallidos se reseteó a 0 desde un valor mayor
    INSERT INTO dbo.audit_login(id_usuario, evento, intentos_fallidos)
    SELECT i.id_usuario, N'LOGIN_OK', 0
    FROM inserted i
    INNER JOIN deleted d ON i.id_usuario = d.id_usuario
    WHERE i.intentos_fallidos = 0
      AND d.intentos_fallidos > 0;
END;
GO

INSERT INTO dbo.Usuario(email, clave_hash, clave_salt, nombre, celular)
VALUES
(
    N'demo@fvncr.org',
    0x59A3273FDB59650E2249C320576B09B2D1B4E98F052B95AC5F0E75C4210784B4,
    0xA1B2C3D4E5F60718293A4B5C6D7E8F90,
    N'Usuario Demo',
    N'8888-8888'
);
GO

SELECT 
    id_usuario,
    email,
    nombre,
    celular,
    activo,
    fecha_creacion
FROM dbo.Usuario;
GO
