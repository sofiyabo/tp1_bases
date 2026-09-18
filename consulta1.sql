SELECT c.nombre        AS cliente,
       r.fecha,
       r.hora,
       r.cantidad_personas,
       r.numero_mesa,
       m.capacidad     AS capacidad_mesa,
       r.estado
FROM Reserva r
JOIN Cliente c ON c.id_cliente = r.id_cliente
JOIN Mesa m    ON m.numero_mesa = r.numero_mesa
WHERE c.id_cliente = 12
ORDER BY r.fecha DESC, r.hora DESC;