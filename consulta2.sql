SELECT p.nombre                            AS plato,
       cp.nombre                           AS categoria,
       SUM(i.cantidad)                     AS unidades_vendidas,
       COUNT(DISTINCT i.id_pedido)         AS pedidos_en_que_aparece,
       SUM(i.cantidad * i.precio_unitario) AS facturacion
FROM ItemPedido i
JOIN Pedido ped        ON ped.id_pedido = i.id_pedido
JOIN Plato p           ON p.id_plato = i.id_plato
JOIN CategoriaPlato cp ON cp.id_categoria = p.id_categoria
WHERE ped.estado <> 'cancelado'
GROUP BY p.id_plato, p.nombre, cp.nombre
ORDER BY unidades_vendidas DESC
LIMIT 10;
