SELECT p.nombre                     AS plato,
       cp.nombre                    AS categoria,
       p.disponible,
       COALESCE(SUM(i.cantidad), 0) AS unidades_vendidas,
       MAX(ped.fecha_hora)          AS ultima_venta
FROM Plato p
JOIN CategoriaPlato cp ON cp.id_categoria = p.id_categoria
LEFT JOIN ItemPedido i ON i.id_plato = p.id_plato
LEFT JOIN Pedido ped   ON ped.id_pedido = i.id_pedido
                      AND ped.estado <> 'cancelado'
GROUP BY p.id_plato, p.nombre, cp.nombre, p.disponible
HAVING MAX(ped.fecha_hora) IS NULL
    OR MAX(ped.fecha_hora) < DATE '2026-09-15' - INTERVAL '7 days'
ORDER BY unidades_vendidas;