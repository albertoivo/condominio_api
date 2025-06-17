----------
-- user --
----------

-- Criação da tabela users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

-- Criação de índices adicionais
CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_users_email ON users(email);

-- Comentários para documentar a tabela
COMMENT ON TABLE users IS 'Tabela de usuários do sistema';
COMMENT ON COLUMN users.id IS 'Identificador único do usuário (chave primária)';
COMMENT ON COLUMN users.name IS 'Nome completo do usuário';
COMMENT ON COLUMN users.email IS 'Email do usuário (único)';

-- Exemplo de inserção de dados
INSERT INTO users (name, email) VALUES 
    ('João Silva', 'joao@email.com'),
    ('Maria Santos', 'maria@email.com'),
    ('Pedro Oliveira', 'pedro@email.com');


----------------
-- CONDOMINIO --
----------------

-- Criação da tabela condominios
CREATE TABLE condominios (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Criação de índices adicionais
CREATE INDEX idx_condominio_name ON condominios(name);

-- Comentários para documentar a tabela
COMMENT ON TABLE condominios IS 'Tabela de Condominios do sistema';
COMMENT ON COLUMN condominios.id IS 'Identificador único do condominio (chave primária)';
COMMENT ON COLUMN condominios.name IS 'Nome completo do condominio';

-- Exemplo de inserção de dados
INSERT INTO condominios (name) VALUES 
    ('Castelfidardo'),
    ('Van Gogh');