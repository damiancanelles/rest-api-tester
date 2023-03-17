CREATE DATABASE FastAPI;
GO

USE FastAPI;
GO

CREATE TABLE apps
(
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE requests
(
    id INT IDENTITY(1,1) PRIMARY KEY,
    created_date DATETIME DEFAULT GETUTCDATE(),
    frecuency NVARCHAR(50),
    name NVARCHAR(255),
    description NVARCHAR(MAX),
    url NVARCHAR(1000),
    body NVARCHAR(MAX),
    search_params NVARCHAR(MAX),
    owner_id INT NOT NULL,

    CONSTRAINT FK_requests_apps FOREIGN KEY (owner_id) REFERENCES apps(id)
);

CREATE TABLE tests
(
    id INT IDENTITY(1,1) PRIMARY KEY,
    passed BIT,
    created_date DATETIME DEFAULT GETUTCDATE(),
    request_id INT NOT NULL,

    CONSTRAINT FK_tests_requests FOREIGN KEY (request_id) REFERENCES requests(id)
);