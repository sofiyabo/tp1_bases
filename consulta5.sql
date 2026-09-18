SELECT a.nombre                             AS aplicacion,
       COUNT(DISTINCT pa.id_pedido)         AS pedidos,
       COUNT(DISTINCT pa.id_usuario_app)    AS usuarios_distintos,
       SUM(i.cantidad * i.precio_unitario)  AS facturacion,
       ROUND(SUM(i.cantidad * i.precio_unitario)
             / COUNT(DISTINCT pa.id_pedido), 2) AS ticket_promedio
FROM Aplicacion a
JOIN PedidoAplicacion pa ON pa.id_aplicacion = a.id_aplicacion
JOIN Pedido ped          ON ped.id_pedido = pa.id_pedido
JOIN ItemPedido i        ON i.id_pedido = pa.id_pedido
WHERE ped.estado <> 'cancelado'
GROUP BY a.id_aplicacion, a.nombre
ORDER BY facturacion DESC;