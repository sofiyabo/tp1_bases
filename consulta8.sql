SELECT m.numero_mesa,
       m.capacidad,
       COUNT(r.id_reserva)                AS reservas,
       ROUND(AVG(r.cantidad_personas), 2) AS promedio_personas,
       ROUND(100.0 * AVG(r.cantidad_personas) / m.capacidad, 2) AS uso_capacidad_pct
FROM Mesa m
LEFT JOIN Reserva r ON r.numero_mesa = m.numero_mesa
                   AND r.estado <> 'cancelada'
GROUP BY m.numero_mesa, m.capacidad
ORDER BY reservas DESC, m.numero_mesa;