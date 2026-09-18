SELECT p.nombre                  AS plato,
       p.precio_actual,
       MIN(i.precio_unitario)    AS precio_minimo_historico,
       MAX(i.precio_unitario)    AS precio_maximo_historico,
       ROUND(100.0 * (p.precio_actual - MIN(i.precio_unitario))
             / MIN(i.precio_unitario), 2) AS aumento_pct
FROM Plato p
JOIN ItemPedido i ON i.id_plato = p.id_plato
GROUP BY p.id_plato, p.nombre, p.precio_actual
HAVING MIN(i.precio_unitario) < MAX(i.precio_unitario)
ORDER BY aumento_pct DESC
LIMIT 10;