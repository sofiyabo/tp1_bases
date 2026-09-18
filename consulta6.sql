SELECT c.nombre                     AS cliente,
       c.email,
       COUNT(DISTINCT r.id_reserva) AS reservas_completadas,
       COALESCE(SUM(i.cantidad * i.precio_unitario), 0) AS consumo_total
FROM Cliente c
JOIN Reserva r           ON r.id_cliente = c.id_cliente
                        AND r.estado = 'completada'
LEFT JOIN PedidoMesa pm  ON pm.id_reserva = r.id_reserva
LEFT JOIN ItemPedido i   ON i.id_pedido = pm.id_pedido
GROUP BY c.id_cliente, c.nombre, c.email
HAVING COUNT(DISTINCT r.id_reserva) >= 2
ORDER BY consumo_total DESC;