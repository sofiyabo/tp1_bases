SELECT cp.nombre                           AS categoria,
       COUNT(DISTINCT p.id_plato)          AS platos_distintos_vendidos,
       SUM(i.cantidad)                     AS unidades_vendidas,
       SUM(i.cantidad * i.precio_unitario) AS facturacion,
       ROUND(100.0 * SUM(i.cantidad * i.precio_unitario)
             / SUM(SUM(i.cantidad * i.precio_unitario)) OVER (), 2) AS porcentaje
FROM ItemPedido i
JOIN Pedido ped        ON ped.id_pedido = i.id_pedido
JOIN Plato p           ON p.id_plato = i.id_plato
JOIN CategoriaPlato cp ON cp.id_categoria = p.id_categoria
WHERE ped.estado <> 'cancelado'
GROUP BY cp.id_categoria, cp.nombre
ORDER BY facturacion DESC;
