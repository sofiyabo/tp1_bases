SELECT TO_CHAR(ped.fecha_hora, 'YYYY-MM') AS mes,
       CASE WHEN pm.id_pedido IS NOT NULL THEN 'Mesa'
            WHEN pt.id_pedido IS NOT NULL THEN 'Telefónico'
            ELSE 'Aplicación' END         AS canal,
       COUNT(DISTINCT ped.id_pedido)      AS cantidad_pedidos,
       SUM(i.cantidad * i.precio_unitario) AS monto_total,
       ROUND(SUM(i.cantidad * i.precio_unitario)
             / COUNT(DISTINCT ped.id_pedido), 2) AS ticket_promedio
FROM Pedido ped
JOIN ItemPedido i            ON i.id_pedido = ped.id_pedido
LEFT JOIN PedidoMesa pm      ON pm.id_pedido = ped.id_pedido
LEFT JOIN PedidoTelefonico pt ON pt.id_pedido = ped.id_pedido
WHERE ped.estado <> 'cancelado'
GROUP BY mes, canal
ORDER BY mes, canal;