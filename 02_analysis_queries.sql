USE ecommerce_customer_analysis;

-- Q1. Total orders and unique customers
SELECT COUNT(*) AS total_orders,
       COUNT(DISTINCT customer_id) AS unique_customers
FROM ecommerce_orders;

-- Q2. Revenue from delivered orders (after discount)
SELECT ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 2) AS delivered_revenue
FROM ecommerce_orders
WHERE order_status = 'Delivered';

-- Q3. Category-wise revenue
SELECT product_category,
       ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 2) AS revenue
FROM ecommerce_orders
WHERE order_status = 'Delivered'
GROUP BY product_category
ORDER BY revenue DESC;

-- Q4. City-wise orders
SELECT city, COUNT(*) AS orders
FROM ecommerce_orders
GROUP BY city
ORDER BY orders DESC;

-- Q5. Payment method usage
SELECT payment_method, COUNT(*) AS order_count
FROM ecommerce_orders
GROUP BY payment_method
ORDER BY order_count DESC;

-- Q6. Monthly revenue
SELECT DATE_FORMAT(order_date, '%Y-%m') AS order_month,
       ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 2) AS revenue
FROM ecommerce_orders
WHERE order_status = 'Delivered'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY order_month;

-- Q7. Repeat customers (more than one delivered order)
SELECT customer_id, COUNT(*) AS delivered_orders
FROM ecommerce_orders
WHERE order_status = 'Delivered'
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY delivered_orders DESC;

-- Q8. Average order value
SELECT ROUND(AVG(order_value), 2) AS average_order_value
FROM (
    SELECT order_id,
           SUM(quantity * unit_price * (1 - discount_pct / 100)) AS order_value
    FROM ecommerce_orders
    WHERE order_status = 'Delivered'
    GROUP BY order_id
) AS order_totals;

-- Q9. Return and cancellation counts
SELECT order_status, COUNT(*) AS total
FROM ecommerce_orders
GROUP BY order_status;
