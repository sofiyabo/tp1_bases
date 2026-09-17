#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parte V - Carga de datos
Sistema de gestión de reservas y pedidos de un restaurante (Grupo L)

Genera el archivo carga_datos.sql con datos ficticios pero coherentes para
todas las tablas definidas en script.sql.

Uso:
    python3 generar_datos.py                          # genera carga_datos.sql
    python3 generar_datos.py salida.sql               # nombre de archivo alternativo
    python3 generar_datos.py --reservas 20            # exactamente 20 reservas
    python3 generar_datos.py prueba.sql --reservas 5  # combinando ambas opciones

Sin --reservas, la cantidad de reservas depende del día y del turno (~1800).
Fijar un número chico es útil para depurar: se generan menos pedidos de mesa
y el archivo resultante es más fácil de revisar.

La cantidad de pedidos telefónicos y por aplicación se configura con las
variables CANT_PEDIDOS_TELEFONICOS y CANT_PEDIDOS_APLICACION (ver más abajo).

Solo usa la biblioteca estándar de Python 3 (no requiere instalar nada).
La semilla es fija, así que cada ejecución produce exactamente los mismos datos.
"""

import argparse
import random
from datetime import date, datetime, time, timedelta

# ---------------------------------------------------------------------------
# Parámetros generales
# ---------------------------------------------------------------------------
SEMILLA = 312
FECHA_INICIO = date(2026, 9, 1)      # primer día con actividad
FECHA_ACTUAL = date(2026, 9, 15)     # "hoy" dentro del dataset
FECHA_FIN_RESERVAS = date(2026, 9, 30)  # se cargan reservas futuras hasta acá

CANT_CLIENTES = 30
CANT_RESERVAS = 30
CANT_PEDIDOS_TELEFONICOS = 20
CANT_PEDIDOS_APLICACION = 20

TAM_LOTE = 500                       # filas por sentencia INSERT

# Fechas en que el restaurante actualizó su carta de precios.
# Los ítems anteriores a cada fecha usan el precio vigente en ese momento.
ACTUALIZACIONES_PRECIO = [date(2026, 9, 10)]
AUMENTO_POR_ACTUALIZACION = 1.08

random.seed(SEMILLA)

# ---------------------------------------------------------------------------
# Datos de referencia
# ---------------------------------------------------------------------------
NOMBRES = [
    "Sofía", "Martina", "Valentina", "Camila", "Lucía", "Julieta", "Florencia",
    "Agustina", "Micaela", "Paula", "Carolina", "Victoria", "Milagros", "Rocío",
    "Mateo", "Santiago", "Tomás", "Joaquín", "Benjamín", "Nicolás", "Lucas",
    "Martín", "Facundo", "Juan Pablo", "Ignacio", "Federico", "Gonzalo",
    "Ezequiel", "Matías", "Franco", "Diego", "Pablo", "Andrés", "Mariana",
]
APELLIDOS = [
    "González", "Rodríguez", "Gómez", "Fernández", "López", "Díaz", "Martínez",
    "Pérez", "García", "Sánchez", "Romero", "Sosa", "Álvarez", "Torres", "Ruiz",
    "Ramírez", "Flores", "Acosta", "Benítez", "Medina", "Suárez", "Herrera",
    "Aguirre", "Giménez", "Gutiérrez", "Pereyra", "Rojas", "Molina", "Castro",
    "Ortiz", "Silva", "Núñez", "Luna", "Ferrari", "Russo", "Bianchi",
]
DOMINIOS = ["gmail.com", "hotmail.com", "yahoo.com.ar", "outlook.com"]

CALLES = [
    "Av. Santa Fe", "Av. Corrientes", "Av. Cabildo", "Av. Rivadavia", "Gorriti",
    "Honduras", "Thames", "Malabia", "Av. Córdoba", "Guatemala", "Charcas",
    "Paraguay", "Soler", "Fitz Roy", "Arévalo", "Av. Scalabrini Ortiz",
    "Av. Coronel Díaz", "Julián Álvarez", "Gurruchaga", "El Salvador",
]
BARRIOS = ["Palermo", "Villa Crespo", "Recoleta", "Belgrano", "Colegiales", "Almagro"]

CATEGORIAS = [
    "Entradas", "Ensaladas", "Pastas", "Carnes", "Pizzas", "Postres",
    "Bebidas sin alcohol", "Vinos y cervezas",
]

# (nombre, precio_actual en ARS, categoria, disponible)
PLATOS = [
    ("Empanada de carne cortada a cuchillo", 2800, "Entradas", True),
    ("Provoleta a la parrilla", 9500, "Entradas", True),
    ("Rabas a la romana", 14500, "Entradas", True),
    ("Tabla de fiambres y quesos", 18900, "Entradas", True),
    ("Croquetas de jamón", 8200, "Entradas", False),
    ("Burrata con tomates confitados", 12800, "Entradas", True),

    ("Ensalada César", 11500, "Ensaladas", True),
    ("Ensalada caprese", 10200, "Ensaladas", True),
    ("Ensalada de quinoa y vegetales asados", 10900, "Ensaladas", True),
    ("Ensalada mixta", 6500, "Ensaladas", True),

    ("Sorrentinos de jamón y queso", 15800, "Pastas", True),
    ("Ñoquis de papa con salsa bolognesa", 13900, "Pastas", True),
    ("Tallarines al pesto", 13200, "Pastas", True),
    ("Ravioles de verdura con crema", 14600, "Pastas", True),
    ("Lasaña de carne", 16900, "Pastas", True),
    ("Risotto de hongos", 17500, "Pastas", False),

    ("Bife de chorizo con papas fritas", 24900, "Carnes", True),
    ("Ojo de bife con puré rústico", 27800, "Carnes", True),
    ("Milanesa napolitana con fritas", 19500, "Carnes", True),
    ("Pollo grillado con vegetales", 17200, "Carnes", True),
    ("Entraña con chimichurri", 26500, "Carnes", True),
    ("Salmón rosado con verduras", 29900, "Carnes", True),
    ("Matambre a la pizza", 21400, "Carnes", False),

    ("Pizza muzzarella", 13500, "Pizzas", True),
    ("Pizza napolitana", 15200, "Pizzas", True),
    ("Pizza fugazzeta rellena", 16800, "Pizzas", True),
    ("Pizza de jamón y morrones", 16200, "Pizzas", True),
    ("Fainá", 3900, "Pizzas", True),

    ("Flan casero con dulce de leche", 6900, "Postres", True),
    ("Tiramisú", 8400, "Postres", True),
    ("Panqueque con dulce de leche", 7200, "Postres", True),
    ("Volcán de chocolate con helado", 9600, "Postres", True),
    ("Helado artesanal (2 bochas)", 6200, "Postres", True),

    ("Agua mineral 500 ml", 2900, "Bebidas sin alcohol", True),
    ("Gaseosa línea Coca-Cola 500 ml", 3500, "Bebidas sin alcohol", True),
    ("Limonada con menta y jengibre", 5800, "Bebidas sin alcohol", True),
    ("Jugo de naranja exprimido", 5200, "Bebidas sin alcohol", True),
    ("Café espresso", 3200, "Bebidas sin alcohol", True),

    ("Copa de Malbec", 6500, "Vinos y cervezas", True),
    ("Botella de Malbec reserva", 32000, "Vinos y cervezas", True),
    ("Botella de Torrontés", 24500, "Vinos y cervezas", True),
    ("Pinta de cerveza rubia", 6800, "Vinos y cervezas", True),
    ("Pinta de cerveza IPA", 7500, "Vinos y cervezas", True),
]

APLICACIONES = ["PedidosYa", "Rappi", "Uber Eats", "App propia del restaurante"]
PESO_APPS = [50, 30, 12, 8]
PREFIJO_APP = {1: "PY", 2: "RP", 3: "UE", 4: "RL"}

# (numero_mesa, capacidad)
MESAS = ([(n, 2) for n in range(1, 7)] + [(n, 4) for n in range(7, 15)] +
         [(n, 6) for n in range(15, 19)] + [(19, 8), (20, 10)])

TURNOS = {
    "almuerzo": [time(12, 30), time(13, 0), time(13, 30), time(14, 0)],
    "cena": [time(20, 0), time(20, 30), time(21, 0), time(21, 30), time(22, 0)],
}

# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------
def sql_str(valor):
    """Convierte un valor de Python en un literal SQL."""
    if valor is None:
        return "NULL"
    if isinstance(valor, bool):
        return "TRUE" if valor else "FALSE"
    if isinstance(valor, (int, float)):
        return str(valor)
    if isinstance(valor, datetime):
        return "'" + valor.strftime("%Y-%m-%d %H:%M:%S") + "'"
    if isinstance(valor, date):
        return "'" + valor.isoformat() + "'"
    if isinstance(valor, time):
        return "'" + valor.strftime("%H:%M") + "'"
    return "'" + str(valor).replace("'", "''") + "'"


def inserts(tabla, columnas, filas):
    """Genera sentencias INSERT multi-fila en lotes."""
    bloques = []
    for i in range(0, len(filas), TAM_LOTE):
        lote = filas[i:i + TAM_LOTE]
        valores = ",\n".join(
            "    (" + ", ".join(sql_str(v) for v in fila) + ")" for fila in lote
        )
        bloques.append(
            f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES\n{valores};"
        )
    return "\n\n".join(bloques)


def sin_tildes(texto):
    tabla = str.maketrans("áéíóúÁÉÍÓÚñÑü ", "aeiouAEIOUnNu.")
    return texto.translate(tabla).lower()


def telefono_celular():
    return f"11 {random.randint(2000, 6999)}-{random.randint(1000, 9999)}"


def dias_abiertos(desde, hasta):
    """El restaurante abre de martes a domingo (cierra los lunes)."""
    d = desde
    while d <= hasta:
        if d.weekday() != 0:
            yield d
        d += timedelta(days=1)


def precio_vigente(precio_actual, fecha):
    """Precio que tenía un plato en una fecha dada, antes de los aumentos."""
    aumentos_posteriores = sum(1 for f in ACTUALIZACIONES_PRECIO if fecha < f)
    precio = precio_actual / (AUMENTO_POR_ACTUALIZACION ** aumentos_posteriores)
    return round(precio / 50) * 50  # redondeo a múltiplos de $50


def redondear_cuarto_hora(dt):
    minutos = (dt.minute // 15 + 1) * 15
    return dt.replace(minute=0, second=0) + timedelta(minutes=minutos)


# ---------------------------------------------------------------------------
# Generación de entidades
# ---------------------------------------------------------------------------
def generar_clientes():
    clientes, emails = [], set()
    for id_cliente in range(1, CANT_CLIENTES + 1):
        nombre = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        telefono = telefono_celular() if random.random() < 0.95 else None
        email = None
        if random.random() < 0.92:
            base = f"{sin_tildes(nombre)}.{sin_tildes(apellido)}"
            email = f"{base}@{random.choice(DOMINIOS)}"
            n = 2
            while email in emails:
                email = f"{base}{n}@{random.choice(DOMINIOS)}"
                n += 1
            emails.add(email)
        clientes.append((id_cliente, f"{nombre} {apellido}", telefono, email))
    return clientes


PERSONAS_POSIBLES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
PESOS_PERSONAS = [3, 40, 12, 22, 7, 8, 2, 3, 1, 1]


def cantidad_reservas_turno(dia, turno):
    """Cantidad "natural" de reservas para un turno (modo por defecto)."""
    finde = dia.weekday() >= 4  # viernes, sábado, domingo
    if turno == "almuerzo":
        cantidad = random.randint(1, 4) if not finde else random.randint(3, 7)
    else:
        cantidad = random.randint(2, 6) if not finde else random.randint(6, 12)
    if dia > FECHA_ACTUAL:  # a futuro todavía no se reservó todo
        cantidad = max(0, cantidad // 2)
    return cantidad


def peso_turno(dia, turno):
    """Peso relativo de un turno, usado cuando se fija la cantidad total."""
    finde = dia.weekday() >= 4
    peso = (5 if finde else 2.5) if turno == "almuerzo" else (9 if finde else 4)
    return peso / 2 if dia > FECHA_ACTUAL else peso


def crear_reserva(dia, turno, mesas_libres, clientes, pesos_clientes, forzar=False):
    """Crea una reserva en el turno indicado y ocupa su mesa.

    Devuelve None si no hay mesa apta. Con forzar=True, si la cantidad de
    personas sorteada no entra en ninguna mesa libre, se vuelve a sortear
    entre las cantidades que sí entran (así nunca se pierde una reserva).
    """
    personas = random.choices(PERSONAS_POSIBLES, weights=PESOS_PERSONAS)[0]
    aptas = [m for m in mesas_libres if m[1] >= personas]
    if not aptas:
        if not forzar or not mesas_libres:
            return None
        cap_max = max(m[1] for m in mesas_libres)
        opciones = [(p, w) for p, w in zip(PERSONAS_POSIBLES, PESOS_PERSONAS) if p <= cap_max]
        personas = random.choices([p for p, _ in opciones], [w for _, w in opciones])[0]
        aptas = [m for m in mesas_libres if m[1] >= personas]
    cap_min = min(m[1] for m in aptas)  # la mesa más chica que alcanza
    mesa = random.choice([m for m in aptas if m[1] == cap_min])
    mesas_libres.remove(mesa)

    if dia < FECHA_ACTUAL:
        estado = random.choices(["completada", "cancelada"], [85, 15])[0]
    elif dia == FECHA_ACTUAL:
        estado = random.choices(["confirmada", "cancelada"], [90, 10])[0]
    else:
        estado = random.choices(["pendiente", "confirmada", "cancelada"], [35, 55, 10])[0]

    id_cliente = random.choices(clientes, weights=pesos_clientes)[0][0]
    return {
        "fecha": dia, "hora": random.choice(TURNOS[turno]),
        "personas": personas, "estado": estado,
        "mesa": mesa[0], "cliente": id_cliente,
    }


def generar_reservas(clientes, cantidad_total=None):
    """Reservas sin superposición de mesa por turno y con capacidad suficiente.

    cantidad_total=None  -> cantidad variable según el día (comportamiento normal).
    cantidad_total=N     -> se generan exactamente N reservas, repartidas al azar
                            entre los turnos (más peso a cenas y fines de semana).
    """
    # Algunos clientes son habituales: tienen más peso al elegir quién reserva.
    pesos_clientes = [random.choice([1, 1, 1, 2, 3, 8]) for _ in clientes]
    reservas = []

    if cantidad_total is None:
        for dia in dias_abiertos(FECHA_INICIO, FECHA_FIN_RESERVAS):
            for turno in TURNOS:
                cantidad = cantidad_reservas_turno(dia, turno)
                mesas_libres = list(MESAS)
                for _ in range(cantidad):
                    r = crear_reserva(dia, turno, mesas_libres, clientes, pesos_clientes)
                    if r:
                        reservas.append(r)
    else:
        turnos = [(dia, turno) for dia in dias_abiertos(FECHA_INICIO, FECHA_FIN_RESERVAS)
                  for turno in TURNOS]
        maximo = len(turnos) * len(MESAS)
        if cantidad_total < 0 or cantidad_total > maximo:
            raise ValueError(f"La cantidad de reservas debe estar entre 0 y {maximo} "
                             f"({len(turnos)} turnos x {len(MESAS)} mesas).")
        mesas_libres = {t: list(MESAS) for t in turnos}
        pesos = [peso_turno(dia, turno) for dia, turno in turnos]
        while len(reservas) < cantidad_total:
            dia, turno = random.choices(turnos, weights=pesos)[0]
            if not mesas_libres[(dia, turno)]:
                pesos[turnos.index((dia, turno))] = 0  # turno completo
                continue
            reservas.append(crear_reserva(dia, turno, mesas_libres[(dia, turno)],
                                          clientes, pesos_clientes, forzar=True))

    reservas.sort(key=lambda r: (r["fecha"], r["hora"], r["mesa"]))
    for i, r in enumerate(reservas, start=1):
        r["id"] = i
    return reservas


def elegir_items(platos, fecha, personas, canal):
    """Devuelve una lista de (id_plato, cantidad) plausible para el pedido."""
    por_cat = {}
    for p in platos:
        # Los platos hoy no disponibles se dejaron de ofrecer en septiembre.
        if not p["disponible"] and fecha >= date(2026, 9, 1):
            continue
        por_cat.setdefault(p["categoria"], []).append(p)

    elegidos = {}

    def agregar(categoria, cantidad):
        if cantidad <= 0 or categoria not in por_cat:
            return
        plato = random.choices(por_cat[categoria],
                               weights=[p["popularidad"] for p in por_cat[categoria]])[0]
        elegidos[plato["id"]] = elegidos.get(plato["id"], 0) + cantidad

    principales = ["Pastas", "Carnes", "Pizzas", "Ensaladas"]
    pesos_principales = [30, 35, 25, 10] if canal == "mesa" else [25, 20, 45, 10]

    if canal == "mesa":
        if random.random() < 0.55:
            agregar("Entradas", max(1, personas // 2))
        restantes = personas
        while restantes > 0:
            cat = random.choices(principales, pesos_principales)[0]
            if cat == "Pizzas":  # una pizza se comparte entre 2
                agregar(cat, 1)
                restantes -= 2
            else:
                n = min(restantes, random.randint(1, 2))
                agregar(cat, n)
                restantes -= n
        if random.random() < 0.7:
            agregar("Bebidas sin alcohol", random.randint(1, personas))
        if random.random() < 0.5:
            if personas >= 3 and random.random() < 0.5:
                agregar("Vinos y cervezas", max(1, personas // 3))
            else:
                agregar("Vinos y cervezas", random.randint(1, max(1, personas // 2)))
        if random.random() < 0.45:
            agregar("Postres", random.randint(1, personas))
    else:  # delivery: telefónico o aplicación
        for _ in range(random.choices([1, 2, 3], [45, 40, 15])[0]):
            agregar(random.choices(principales, pesos_principales)[0],
                    random.choices([1, 2, 3], [60, 30, 10])[0])
        if random.random() < 0.35:
            agregar("Entradas", random.choice([1, 2, 6, 12]) if random.random() < 0.5 else 1)
        if random.random() < 0.5:
            agregar("Bebidas sin alcohol", random.randint(1, 3))
        if random.random() < 0.15:
            agregar("Vinos y cervezas", 1)
        if random.random() < 0.25:
            agregar("Postres", random.randint(1, 2))

    return list(elegidos.items())


def hora_aleatoria(dia, desde, hasta):
    inicio = datetime.combine(dia, desde)
    fin = datetime.combine(dia, hasta)
    segundos = random.randint(0, int((fin - inicio).total_seconds()))
    return inicio + timedelta(seconds=segundos)


def estado_delivery(fecha_hora, ahora):
    """Estado de un pedido para llevar según cuánto tiempo pasó."""
    if fecha_hora.date() < ahora.date():
        return random.choices(["entregado", "cancelado"], [92, 8])[0]
    minutos = (ahora - fecha_hora).total_seconds() / 60
    if minutos > 60:
        return random.choices(["entregado", "cancelado"], [92, 8])[0]
    if minutos > 35:
        return "listo"
    if minutos > 10:
        return "en_preparacion"
    return "pendiente"


HORARIO_DELIVERY = {"almuerzo": (time(11, 30), time(14, 30)),
                    "cena": (time(19, 30), time(23, 0))}


def meses_desde_inicio(dia):
    return (dia.year - FECHA_INICIO.year) * 12 + dia.month - FECHA_INICIO.month


def cantidad_delivery_turno(dia, turno):
    """Cantidad "natural" de pedidos telefónicos y por app en un turno."""
    finde = dia.weekday() >= 4
    n_tel = random.randint(0, 3) + (2 if finde else 0)
    # Crecimiento gradual del delivery por apps a lo largo de los meses.
    n_app = random.randint(2, 5) + meses_desde_inicio(dia) + (4 if finde else 0)
    if turno == "almuerzo":
        n_app = n_app // 2
    return n_tel, n_app


def peso_delivery_turno(dia, turno, canal):
    """Peso relativo de un turno cuando se fija la cantidad de pedidos."""
    finde = dia.weekday() >= 4
    if canal == "telefonico":
        return 1.5 + (2 if finde else 0)
    peso = 3.5 + meses_desde_inicio(dia) + (4 if finde else 0)
    return peso / 2 if turno == "almuerzo" else peso


def crear_pedido_delivery(canal, dia, turno, ahora, platos, clientes,
                          direcciones, usuarios_app, ids_app_usados):
    """Crea un pedido telefónico o por aplicación. None si es posterior a 'ahora'."""
    desde, hasta = HORARIO_DELIVERY[turno]
    fecha_hora = hora_aleatoria(dia, desde, hasta)
    if fecha_hora > ahora:
        return None
    # El cliente pide para "lo antes posible" o para un horario puntual.
    demora = random.choice([30, 45, 45, 60, 90])
    horario = redondear_cuarto_hora(fecha_hora + timedelta(minutes=demora)).time()
    pedido = {
        "canal": canal, "fecha_hora": fecha_hora, "horario": horario,
        "estado": estado_delivery(fecha_hora, ahora),
        "items": elegir_items(platos, dia, 0, canal),
    }
    if canal == "telefonico":
        cli = random.choice(clientes)
        pedido["telefono"] = cli[2] if cli[2] and random.random() < 0.6 else telefono_celular()
        pedido["direccion"] = random.choice(direcciones)
    else:
        app = random.choices(range(1, len(APLICACIONES) + 1), PESO_APPS)[0]
        id_ext = f"{PREFIJO_APP[app]}-{random.randint(10**7, 10**8 - 1)}"
        while (app, id_ext) in ids_app_usados:
            id_ext = f"{PREFIJO_APP[app]}-{random.randint(10**7, 10**8 - 1)}"
        ids_app_usados.add((app, id_ext))
        pedido["app"] = app
        pedido["id_ext"] = id_ext
        pedido["usuario"] = random.choice(usuarios_app[app])
    return pedido


def generar_pedidos(reservas, platos, clientes):
    ahora = datetime.combine(FECHA_ACTUAL, time(13, 45))  # momento de la "foto"
    pedidos = []

    # --- Pedidos de mesa: uno por cada reserva completada (o en curso hoy) ---
    for r in reservas:
        if r["estado"] == "cancelada":
            continue
        inicio = datetime.combine(r["fecha"], r["hora"])
        if r["estado"] == "completada":
            if random.random() < 0.04:  # algunas reservas no llegaron a pedir
                continue
            estado = "entregado"
        elif r["fecha"] == FECHA_ACTUAL and inicio <= ahora:
            minutos = (ahora - inicio).total_seconds() / 60
            estado = ("entregado" if minutos > 50 else
                      "listo" if minutos > 35 else
                      "en_preparacion" if minutos > 15 else "pendiente")
        else:
            continue  # reserva futura: todavía no generó pedido
        fecha_hora = inicio + timedelta(minutes=random.randint(5, 25),
                                        seconds=random.randint(0, 59))
        if fecha_hora > ahora:
            fecha_hora = ahora - timedelta(minutes=1)
        pedidos.append({
            "canal": "mesa", "fecha_hora": fecha_hora, "horario": r["hora"],
            "estado": estado, "reserva": r["id"],
            "items": elegir_items(platos, r["fecha"], r["personas"], "mesa"),
        })

    # --- Pedidos telefónicos y por aplicación ---
    # Pool de usuarios por aplicación (para que haya usuarios recurrentes).
    usuarios_app = {a: [f"usr_{PREFIJO_APP[a].lower()}_{random.randint(100000, 999999)}"
                        for _ in range(random.randint(60, 140))]
                    for a in range(1, len(APLICACIONES) + 1)}
    ids_app_usados = set()
    # Clientes que llaman por teléfono (a veces con su teléfono registrado).
    direcciones = [f"{random.choice(CALLES)} {random.randint(100, 5800)}"
                   f"{', piso ' + str(random.randint(1, 12)) + ' ' + random.choice('ABCD') if random.random() < 0.5 else ''}"
                   f", {random.choice(BARRIOS)}"
                   for _ in range(90)]

    contexto = (ahora, platos, clientes, direcciones, usuarios_app, ids_app_usados)
    fijos = {"telefonico": CANT_PEDIDOS_TELEFONICOS, "aplicacion": CANT_PEDIDOS_APLICACION}

    # Modo variable: cantidad "natural" por turno para los canales sin número fijo.
    for dia in dias_abiertos(FECHA_INICIO, FECHA_ACTUAL):
        for turno in ("almuerzo", "cena"):
            n_tel, n_app = cantidad_delivery_turno(dia, turno)
            for canal, cantidad in (("telefonico", n_tel), ("aplicacion", n_app)):
                if fijos[canal] is not None:
                    continue
                for _ in range(cantidad):
                    pedido = crear_pedido_delivery(canal, dia, turno, *contexto)
                    if pedido:
                        pedidos.append(pedido)

    # Modo fijo: exactamente N pedidos, repartidos al azar entre los turnos.
    turnos = [(dia, turno) for dia in dias_abiertos(FECHA_INICIO, FECHA_ACTUAL)
              for turno in ("almuerzo", "cena")
              if datetime.combine(dia, HORARIO_DELIVERY[turno][0]) <= ahora]
    for canal, cantidad in fijos.items():
        if cantidad is None:
            continue
        pesos = [peso_delivery_turno(dia, turno, canal) for dia, turno in turnos]
        generados = 0
        while generados < cantidad:
            dia, turno = random.choices(turnos, weights=pesos)[0]
            pedido = crear_pedido_delivery(canal, dia, turno, *contexto)
            if pedido:  # None si el horario sorteado todavía no ocurrió (hoy)
                pedidos.append(pedido)
                generados += 1

    pedidos.sort(key=lambda p: p["fecha_hora"])
    for i, p in enumerate(pedidos, start=1):
        p["id"] = i
    return pedidos


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Genera el script de carga de datos del TP.")
    parser.add_argument("salida", nargs="?", default="carga_datos.sql",
                        help="archivo SQL a generar (por defecto: carga_datos.sql)")
    args = parser.parse_args()
    salida = args.salida
    for nombre, valor in [("CANT_PEDIDOS_TELEFONICOS", CANT_PEDIDOS_TELEFONICOS),
                          ("CANT_PEDIDOS_APLICACION", CANT_PEDIDOS_APLICACION)]:
        if valor is not None and (isinstance(valor, bool) or not isinstance(valor, int) or valor < 0):
            parser.error(f"{nombre} debe ser None o un entero mayor o igual a 0 (vale {valor!r}).")

    categorias = [(i, n) for i, n in enumerate(CATEGORIAS, start=1)]
    id_categoria = {n: i for i, n in categorias}

    platos = []
    for i, (nombre, precio, cat, disp) in enumerate(PLATOS, start=1):
        platos.append({"id": i, "nombre": nombre, "precio": precio,
                       "categoria": cat, "disponible": disp,
                       "popularidad": random.choice([1, 2, 3, 3, 5, 8])})
    precio_actual = {p["id"]: p["precio"] for p in platos}

    clientes = generar_clientes()
    try:
        reservas = generar_reservas(clientes, CANT_RESERVAS)
    except ValueError as error:
        parser.error(str(error))
    pedidos = generar_pedidos(reservas, platos, clientes)

    filas_pedido, filas_mesa, filas_tel, filas_app, filas_items = [], [], [], [], []
    for p in pedidos:
        filas_pedido.append((p["id"], p["fecha_hora"], p["horario"], p["estado"]))
        if p["canal"] == "mesa":
            filas_mesa.append((p["id"], p["reserva"]))
        elif p["canal"] == "telefonico":
            filas_tel.append((p["id"], p["telefono"], p["direccion"]))
        else:
            filas_app.append((p["id"], p["id_ext"], p["usuario"], p["app"]))
        for nro, (id_plato, cant) in enumerate(p["items"], start=1):
            precio = precio_vigente(precio_actual[id_plato], p["fecha_hora"].date())
            filas_items.append((nro, p["id"], cant, f"{precio:.2f}", id_plato))

    secciones = [
        "-- =====================================================================",
        "-- Parte V - Carga de datos (generado automáticamente por generar_datos.py)",
        "-- Sistema de gestión de reservas y pedidos de un restaurante - Grupo L",
        f"-- Período simulado: {FECHA_INICIO} a {FECHA_ACTUAL} "
        f"(reservas futuras hasta {FECHA_FIN_RESERVAS})",
        "-- Requiere haber ejecutado antes script.sql",
        "-- =====================================================================",
        "",
        "BEGIN;",
        "",
        "-- Vacía las tablas para que el script pueda ejecutarse más de una vez",
        "TRUNCATE ItemPedido, PedidoMesa, PedidoTelefonico, PedidoAplicacion, Pedido,",
        "         Reserva, Plato, CategoriaPlato, Cliente, Mesa, Aplicacion",
        "         RESTART IDENTITY CASCADE;",
        "",
        "-- Aplicacion", inserts("Aplicacion", ["id_aplicacion", "nombre"],
                                  [(i, n) for i, n in enumerate(APLICACIONES, start=1)]), "",
        "-- CategoriaPlato", inserts("CategoriaPlato", ["id_categoria", "nombre"], categorias), "",
        "-- Cliente", inserts("Cliente", ["id_cliente", "nombre", "telefono", "email"], clientes), "",
        "-- Mesa", inserts("Mesa", ["numero_mesa", "capacidad"], MESAS), "",
        "-- Plato", inserts("Plato", ["id_plato", "nombre", "precio_actual", "disponible", "id_categoria"],
                            [(p["id"], p["nombre"], f"{p['precio']:.2f}", p["disponible"],
                              id_categoria[p["categoria"]]) for p in platos]), "",
        "-- Reserva", inserts("Reserva", ["id_reserva", "fecha", "hora", "cantidad_personas",
                                          "estado", "numero_mesa", "id_cliente"],
                              [(r["id"], r["fecha"], r["hora"], r["personas"], r["estado"],
                                r["mesa"], r["cliente"]) for r in reservas]), "",
        "-- Pedido", inserts("Pedido", ["id_pedido", "fecha_hora", "horario_solicitado", "estado"],
                             filas_pedido), "",
        "-- PedidoMesa", inserts("PedidoMesa", ["id_pedido", "id_reserva"], filas_mesa), "",
        "-- PedidoTelefonico", inserts("PedidoTelefonico",
                                       ["id_pedido", "telefono_contacto", "direccion_entrega"],
                                       filas_tel), "",
        "-- PedidoAplicacion", inserts("PedidoAplicacion",
                                       ["id_pedido", "id_pedido_app", "id_usuario_app", "id_aplicacion"],
                                       filas_app), "",
        "-- ItemPedido", inserts("ItemPedido",
                                 ["nro_item", "id_pedido", "cantidad", "precio_unitario", "id_plato"],
                                 filas_items), "",
        "-- Como se insertaron ids explícitos, se actualizan las secuencias SERIAL",
        "-- para que los próximos INSERT sin id no generen claves repetidas.",
    ]
    secciones.append("DO $$")
    secciones.append("BEGIN")
    for tabla, col in [("aplicacion", "id_aplicacion"), ("categoriaplato", "id_categoria"),
                       ("cliente", "id_cliente"), ("plato", "id_plato"),
                       ("reserva", "id_reserva"), ("pedido", "id_pedido")]:
        secciones.append(f"    PERFORM setval(pg_get_serial_sequence('{tabla}', '{col}'), "
                         f"(SELECT MAX({col}) FROM {tabla}));")
    secciones.append("END $$;")
    secciones += ["", "COMMIT;", ""]

    with open(salida, "w", encoding="utf-8") as f:
        f.write("\n".join(secciones))

    print(f"Archivo generado: {salida}")
    for nombre, n in [("Aplicacion", len(APLICACIONES)), ("CategoriaPlato", len(categorias)),
                      ("Cliente", len(clientes)), ("Mesa", len(MESAS)), ("Plato", len(platos)),
                      ("Reserva", len(reservas)), ("Pedido", len(filas_pedido)),
                      ("PedidoMesa", len(filas_mesa)), ("PedidoTelefonico", len(filas_tel)),
                      ("PedidoAplicacion", len(filas_app)), ("ItemPedido", len(filas_items))]:
        print(f"  {nombre:<18} {n:>6} filas")


if __name__ == "__main__":
    main()
