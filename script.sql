-- Aplicacion
CREATE TABLE Aplicacion (
    id_aplicacion  SERIAL PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL
);

-- CategoriaPlato
CREATE TABLE CategoriaPlato (
    id_categoria  SERIAL PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL UNIQUE -- unique porque no se repiten nombres de las categorias
);

-- Cliente 
CREATE TABLE Cliente (
    id_cliente  SERIAL PRIMARY KEY,
    nombre      VARCHAR(150) NOT NULL,
    telefono    VARCHAR(20),
    email       VARCHAR(150) UNIQUE -- no se repiten mails entre clientes
);

-- Mesa 
CREATE TABLE Mesa (
    numero_mesa  INTEGER PRIMARY KEY,
    capacidad    INTEGER NOT NULL CHECK (capacidad > 0)
);


-- Pedido
CREATE TABLE Pedido (
    id_pedido           SERIAL PRIMARY KEY,
    fecha_hora          TIMESTAMP NOT NULL DEFAULT NOW(),
    horario_solicitado  TIME,
    estado              VARCHAR(20) NOT NULL
        CHECK (estado IN ('pendiente','en_preparacion','listo','entregado','cancelado'))
);


-- Plato: depende de CategoriaPlato
CREATE TABLE Plato (
    id_plato       SERIAL PRIMARY KEY,
    nombre         VARCHAR(150) NOT NULL,
    precio_actual  NUMERIC(10,2) NOT NULL CHECK (precio_actual >= 0),
    disponible     BOOLEAN NOT NULL DEFAULT TRUE,
    id_categoria   INTEGER NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES CategoriaPlato(id_categoria)
);

-- Reserva: depende de Mesa y Cliente
CREATE TABLE Reserva (
    id_reserva         SERIAL PRIMARY KEY,
    fecha              DATE NOT NULL,
    hora               TIME NOT NULL,
    cantidad_personas  INTEGER NOT NULL CHECK (cantidad_personas > 0),
    estado             VARCHAR(20) NOT NULL
        CHECK (estado IN ('pendiente','confirmada','cancelada','completada')),
    numero_mesa        INTEGER NOT NULL,
    id_cliente         INTEGER NOT NULL,
    FOREIGN KEY (numero_mesa) REFERENCES Mesa(numero_mesa),
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);


-- PedidoAplicacion: depende de Pedido y Aplicacion
CREATE TABLE PedidoAplicacion (
    id_pedido       INTEGER PRIMARY KEY,
    id_pedido_app   VARCHAR(100) NOT NULL,
    id_usuario_app  VARCHAR(100) NOT NULL,
    id_aplicacion   INTEGER NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_aplicacion) REFERENCES Aplicacion(id_aplicacion)
);

-- PedidoTelefonico: depende de Pedido 
CREATE TABLE PedidoTelefonico (
    id_pedido          INTEGER PRIMARY KEY,
    telefono_contacto  VARCHAR(20) NOT NULL,
    direccion_entrega  TEXT NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido) ON DELETE CASCADE
);

-- PedidoMesa: depende de Pedido y Reserva 
CREATE TABLE PedidoMesa (
    id_pedido   INTEGER PRIMARY KEY,
    id_reserva  INTEGER NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_reserva) REFERENCES Reserva(id_reserva)
);

-- ItemPedido: depende de Pedido y Plato
CREATE TABLE ItemPedido (
    nro_item         INTEGER NOT NULL,
    id_pedido        INTEGER NOT NULL,
    cantidad         INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario  NUMERIC(10,2) NOT NULL CHECK (precio_unitario >= 0),
    id_plato         INTEGER NOT NULL,
    PRIMARY KEY (nro_item, id_pedido),
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_plato) REFERENCES Plato(id_plato)
);