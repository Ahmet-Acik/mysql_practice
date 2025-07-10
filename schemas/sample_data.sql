-- Insert sample data for practice

-- Insert categories
INSERT INTO categories (category_name, description) VALUES
('Electronics', 'Electronic devices and accessories'),
('Clothing', 'Apparel and fashion items'),
('Books', 'Books and educational materials'),
('Home & Garden', 'Home improvement and gardening supplies'),
('Sports', 'Sports equipment and accessories');

-- Insert customers
INSERT INTO customers (first_name, last_name, email, phone, address, city, state, zip_code) VALUES
('John', 'Doe', 'john.doe@email.com', '555-0101', '123 Main St', 'New York', 'NY', '10001'),
('Jane', 'Smith', 'jane.smith@email.com', '555-0102', '456 Oak Ave', 'Los Angeles', 'CA', '90210'),
('Mike', 'Johnson', 'mike.johnson@email.com', '555-0103', '789 Pine Rd', 'Chicago', 'IL', '60601'),
('Sarah', 'Wilson', 'sarah.wilson@email.com', '555-0104', '321 Elm St', 'Houston', 'TX', '77001'),
('David', 'Brown', 'david.brown@email.com', '555-0105', '654 Maple Dr', 'Phoenix', 'AZ', '85001'),
('Lisa', 'Davis', 'lisa.davis@email.com', '555-0106', '987 Cedar Ln', 'Philadelphia', 'PA', '19101'),
('Tom', 'Miller', 'tom.miller@email.com', '555-0107', '147 Birch St', 'San Antonio', 'TX', '78201'),
('Emily', 'Garcia', 'emily.garcia@email.com', '555-0108', '258 Spruce Ave', 'San Diego', 'CA', '92101');

-- Insert products
INSERT INTO products (product_name, description, category_id, price, stock_quantity, sku) VALUES
-- Electronics
('Smartphone Pro', 'Latest smartphone with advanced features', 1, 799.99, 50, 'ELEC-001'),
('Laptop Ultra', 'High-performance laptop for professionals', 1, 1299.99, 25, 'ELEC-002'),
('Wireless Headphones', 'Premium wireless headphones with noise cancellation', 1, 199.99, 100, 'ELEC-003'),
('Smart Watch', 'Fitness tracking smart watch', 1, 299.99, 75, 'ELEC-004'),
('Tablet', '10-inch tablet for work and entertainment', 1, 399.99, 40, 'ELEC-005'),

-- Clothing
('Cotton T-Shirt', 'Comfortable cotton t-shirt', 2, 19.99, 200, 'CLOTH-001'),
('Jeans', 'Classic blue jeans', 2, 59.99, 150, 'CLOTH-002'),
('Running Shoes', 'Lightweight running shoes', 2, 89.99, 80, 'CLOTH-003'),
('Winter Jacket', 'Warm winter jacket', 2, 129.99, 60, 'CLOTH-004'),
('Dress Shirt', 'Professional dress shirt', 2, 49.99, 120, 'CLOTH-005'),

-- Books
('Python Programming', 'Complete guide to Python programming', 3, 39.99, 30, 'BOOK-001'),
('Data Science Handbook', 'Comprehensive data science reference', 3, 49.99, 25, 'BOOK-002'),
('Web Development Guide', 'Modern web development techniques', 3, 44.99, 35, 'BOOK-003'),
('Machine Learning Basics', 'Introduction to machine learning', 3, 54.99, 20, 'BOOK-004'),

-- Home & Garden
('Garden Tools Set', 'Complete set of garden tools', 4, 79.99, 45, 'HOME-001'),
('LED Light Bulbs', 'Energy-efficient LED bulbs (4-pack)', 4, 24.99, 200, 'HOME-002'),
('Kitchen Knife Set', 'Professional kitchen knife set', 4, 99.99, 30, 'HOME-003'),
('Plant Pot Set', 'Decorative plant pots (3-pack)', 4, 34.99, 80, 'HOME-004'),

-- Sports
('Basketball', 'Official size basketball', 5, 29.99, 60, 'SPORT-001'),
('Yoga Mat', 'Non-slip yoga mat', 5, 39.99, 100, 'SPORT-002'),
('Dumbbells Set', 'Adjustable dumbbells set', 5, 149.99, 25, 'SPORT-003'),
('Tennis Racket', 'Professional tennis racket', 5, 89.99, 40, 'SPORT-004');

-- Insert orders
INSERT INTO orders (customer_id, order_date, status, total_amount, shipping_address, billing_address) VALUES
(1, '2024-01-15 10:30:00', 'delivered', 859.98, '123 Main St, New York, NY 10001', '123 Main St, New York, NY 10001'),
(2, '2024-01-16 14:20:00', 'shipped', 1299.99, '456 Oak Ave, Los Angeles, CA 90210', '456 Oak Ave, Los Angeles, CA 90210'),
(3, '2024-01-17 09:15:00', 'processing', 249.97, '789 Pine Rd, Chicago, IL 60601', '789 Pine Rd, Chicago, IL 60601'),
(4, '2024-01-18 16:45:00', 'delivered', 399.98, '321 Elm St, Houston, TX 77001', '321 Elm St, Houston, TX 77001'),
(5, '2024-01-19 11:30:00', 'pending', 199.99, '654 Maple Dr, Phoenix, AZ 85001', '654 Maple Dr, Phoenix, AZ 85001'),
(1, '2024-01-20 13:20:00', 'shipped', 79.98, '123 Main St, New York, NY 10001', '123 Main St, New York, NY 10001'),
(6, '2024-01-21 15:10:00', 'delivered', 169.98, '987 Cedar Ln, Philadelphia, PA 19101', '987 Cedar Ln, Philadelphia, PA 19101'),
(7, '2024-01-22 10:05:00', 'processing', 89.99, '147 Birch St, San Antonio, TX 78201', '147 Birch St, San Antonio, TX 78201');

-- Insert order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
-- Order 1 (John Doe)
(1, 1, 1, 799.99),  -- Smartphone Pro
(1, 5, 1, 59.99),   -- Jeans

-- Order 2 (Jane Smith)
(2, 2, 1, 1299.99), -- Laptop Ultra

-- Order 3 (Mike Johnson)
(3, 3, 1, 199.99),  -- Wireless Headphones
(3, 18, 1, 49.98),  -- LED Light Bulbs (2 packs)

-- Order 4 (Sarah Wilson)
(4, 6, 2, 19.99),   -- Cotton T-Shirt (2 pieces)
(4, 15, 1, 39.99),  -- Python Programming book
(4, 19, 10, 34.00), -- Kitchen items

-- Order 5 (David Brown)
(5, 3, 1, 199.99),  -- Wireless Headphones

-- Order 6 (John Doe - second order)
(6, 6, 4, 19.99),   -- Cotton T-Shirt (4 pieces)

-- Order 7 (Lisa Davis)
(7, 8, 1, 89.99),   -- Running Shoes
(7, 20, 2, 39.99),  -- Yoga Mat (2 pieces)

-- Order 8 (Tom Miller)
(8, 22, 1, 89.99);  -- Tennis Racket

-- Display some sample data
SELECT 'Categories:' AS Info;
SELECT * FROM categories;

SELECT 'Customers:' AS Info;
SELECT customer_id, first_name, last_name, email, city, state FROM customers LIMIT 5;

SELECT 'Products:' AS Info;
SELECT product_id, product_name, price, stock_quantity, sku FROM products LIMIT 10;

SELECT 'Orders Summary:' AS Info;
SELECT * FROM order_summary LIMIT 5;
