SELECT TO_CHAR(r.fecha, 'YYYY-MM')                          AS mes,
       COUNT(*)                                             AS reservas,
       COUNT(*) FILTER (WHERE r.estado = 'completada')      AS completadas,
       COUNT(*) FILTER (WHERE r.estado = 'cancelada')       AS canceladas,
       ROUND(100.0 * COUNT(*) FILTER (WHERE r.estado = 'cancelada')
             / COUNT(*), 2)                                 AS porcentaje_cancelacion,
       ROUND(AVG(r.cantidad_personas), 2)                   AS promedio_personas
FROM Reserva r
GROUP BY mes
ORDER BY mes;