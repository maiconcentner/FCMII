SELECT *
FROM sales.products LEFT JOIN
	(SELECT product_id, COUNT(product_id) AS cc 
		FROM sales.funnel
		GROUP BY product_id
		HAVING COUNT(product_id) > 1) AS tab_nova
ON sales.products.product_id = tab_nova.product_id
WHERE cc IS NOT NULL
ORDER BY cc DESC;
