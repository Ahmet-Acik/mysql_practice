"""
MySQL Practice Project - REST API
Simple REST API using Flask to interact with the MySQL database.
"""

import sys
import os
from typing import Optional, Dict, Any, List
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


class DatabaseAPI:
    """REST API for database operations."""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for all routes
        self.db: Optional[MySQLConnection] = None
        self.setup_routes()
    
    def get_db(self) -> Optional[MySQLConnection]:
        """Get database connection."""
        if not self.db:
            self.db = MySQLConnection()
            if not self.db.connect():
                return None
        return self.db
    
    def setup_routes(self):
        """Setup API routes."""
        
        @self.app.route('/')
        def index():
            """API documentation page."""
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>MySQL Practice API</title>
                <style>
                    body { 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                        margin: 40px; line-height: 1.6; background: #f8f9fa; color: #333;
                    }
                    .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    .endpoint { 
                        background: linear-gradient(135deg, #f4f4f4, #ffffff); 
                        padding: 15px; margin: 10px 0; border-radius: 8px; 
                        border-left: 4px solid #61affe; transition: all 0.3s ease;
                        cursor: pointer;
                    }
                    .endpoint:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
                    .method { color: #fff; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-right: 10px; }
                    .get { background: linear-gradient(135deg, #61affe, #4a9eff); }
                    .post { background: linear-gradient(135deg, #49cc90, #3eb878); }
                    .put { background: linear-gradient(135deg, #fca130, #e8941a); }
                    .delete { background: linear-gradient(135deg, #f93e3e, #e02d2d); }
                    h1 { color: #2c3e50; text-align: center; margin-bottom: 10px; font-size: 2.5em; }
                    h2 { color: #34495e; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-top: 30px; }
                    .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; font-size: 1.2em; }
                    code { background: #ecf0f1; padding: 4px 8px; border-radius: 4px; font-family: 'Monaco', 'Consolas', monospace; }
                    a { color: #3498db; text-decoration: none; font-weight: 500; }
                    a:hover { color: #2980b9; text-decoration: underline; }
                    .try-btn { 
                        background: linear-gradient(135deg, #3498db, #2980b9); 
                        color: white; padding: 5px 10px; border-radius: 4px; 
                        font-size: 11px; margin-left: 10px; text-decoration: none;
                        display: inline-block; transition: all 0.3s ease;
                    }
                    .try-btn:hover { background: linear-gradient(135deg, #2980b9, #1f6391); transform: scale(1.05); }
                    .examples { background: #e8f6f3; padding: 20px; border-radius: 8px; margin: 20px 0; }
                    .live-data { color: #27ae60; font-weight: bold; }
                    .status-indicator { display: inline-block; width: 10px; height: 10px; background: #27ae60; border-radius: 50%; margin-right: 8px; animation: pulse 2s infinite; }
                    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🗄️ MySQL Practice API</h1>
                    <p class="subtitle"><span class="status-indicator"></span>Live RESTful API for MySQL Practice Database</p>
                    
                    <h2>📊 Database Statistics</h2>
                    <div class="endpoint" onclick="window.open('/api/stats', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/stats</code> - Get database statistics
                        <a href="/api/stats" target="_blank" class="try-btn">Try it →</a>
                    </div>
                    
                    <h2>👥 Customers</h2>
                    <div class="endpoint" onclick="window.open('/api/customers?limit=5', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/customers</code> - List all customers
                        <a href="/api/customers?limit=5" target="_blank" class="try-btn">Try it →</a>
                    </div>
                    <div class="endpoint" onclick="window.open('/api/customers/1', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/customers/{id}</code> - Get customer by ID
                        <a href="/api/customers/1" target="_blank" class="try-btn">Try ID=1 →</a>
                    </div>
                    <div class="endpoint" onclick="window.open('/api/customers/1/orders', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/customers/{id}/orders</code> - Get customer orders
                        <a href="/api/customers/1/orders" target="_blank" class="try-btn">Try ID=1 →</a>
                    </div>
                    
                    <h2>🛍️ Products</h2>
                    <div class="endpoint" onclick="window.open('/api/products?limit=10', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/products</code> - List all products
                        <a href="/api/products?limit=10" target="_blank" class="try-btn">Try it →</a>
                    </div>
                    <div class="endpoint" onclick="window.open('/api/products/1', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/products/{id}</code> - Get product by ID
                        <a href="/api/products/1" target="_blank" class="try-btn">Try ID=1 →</a>
                    </div>
                    <div class="endpoint" onclick="window.open('/api/products/category/Electronics', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/products/category/{category}</code> - Get products by category
                        <a href="/api/products/category/Electronics" target="_blank" class="try-btn">Try Electronics →</a>
                    </div>
                    
                    <h2>📦 Orders</h2>
                    <div class="endpoint" onclick="window.open('/api/orders', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/orders</code> - List recent orders
                        <a href="/api/orders" target="_blank" class="try-btn">Try it →</a>
                    </div>
                    <div class="endpoint" onclick="window.open('/api/orders/1', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/orders/{id}</code> - Get order details
                        <a href="/api/orders/1" target="_blank" class="try-btn">Try ID=1 →</a>
                    </div>
                    
                    <h2>📈 Analytics</h2>
                    <div class="endpoint" onclick="window.open('/api/analytics/sales-by-month', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/analytics/sales-by-month</code> - Monthly sales data
                        <a href="/api/analytics/sales-by-month" target="_blank" class="try-btn">Try it →</a>
                    </div>
                    <div class="endpoint" onclick="window.open('/api/analytics/top-products?limit=5', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/analytics/top-products</code> - Best selling products
                        <a href="/api/analytics/top-products?limit=5" target="_blank" class="try-btn">Top 5 →</a>
                    </div>
                    <div class="endpoint" onclick="window.open('/api/analytics/customer-segments', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/analytics/customer-segments</code> - Customer segmentation
                        <a href="/api/analytics/customer-segments" target="_blank" class="try-btn">Try it →</a>
                    </div>
                    
                    <h2>🔍 Search</h2>
                    <div class="endpoint" onclick="window.open('/api/search/customers?q=John', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/search/customers?q={query}</code> - Search customers
                        <a href="/api/search/customers?q=John" target="_blank" class="try-btn">Search "John" →</a>
                    </div>
                    <div class="endpoint" onclick="window.open('/api/search/products?q=shirt', '_blank')">
                        <span class="method get">GET</span> 
                        <code>/api/search/products?q={query}</code> - Search products
                        <a href="/api/search/products?q=shirt" target="_blank" class="try-btn">Search "shirt" →</a>
                    </div>
                    
                    <div class="examples">
                        <h2>🎯 Quick Test Links</h2>
                        <p>Click any of these links to test the API instantly:</p>
                        <ul>
                            <li><a href="/api/stats" target="_blank"><strong>📊 Database Overview</strong></a> - See current stats</li>
                            <li><a href="/api/customers?limit=3" target="_blank"><strong>👥 First 3 Customers</strong></a> - Sample customer data</li>
                            <li><a href="/api/products?limit=5" target="_blank"><strong>🛍️ First 5 Products</strong></a> - Product catalog</li>
                            <li><a href="/api/analytics/top-products?limit=3" target="_blank"><strong>📈 Top 3 Products</strong></a> - Best sellers</li>
                            <li><a href="/api/analytics/sales-by-month" target="_blank"><strong>📊 Monthly Sales</strong></a> - Revenue analytics</li>
                            <li><a href="/api/search/customers?q=John" target="_blank"><strong>🔍 Search Example</strong></a> - Find customers named "John"</li>
                        </ul>
                        
                        <h3>💡 Pro Tips:</h3>
                        <ul>
                            <li>All endpoints return JSON data</li>
                            <li>Use <code>?limit=N</code> for pagination</li>
                            <li>Search is case-insensitive</li>
                            <li>Click any endpoint above to test it</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1;">
                        <p>🚀 <strong>API Status:</strong> <span class="live-data">Live & Ready</span></p>
                        <p>💻 Built with Flask • 🗄️ Powered by MySQL • 🎨 Interactive Documentation</p>
                    </div>
                </div>
                
                <script>
                    // Add click functionality to prevent event bubbling on buttons
                    document.querySelectorAll('.try-btn').forEach(btn => {
                        btn.addEventListener('click', (e) => {
                            e.stopPropagation();
                        });
                    });
                </script>
            </body>
            </html>
            """
            return html
        
        @self.app.route('/api/stats')
        def get_stats():
            """Get database statistics."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                stats = {}
                
                # Table counts
                tables = ['customers', 'products', 'categories', 'orders', 'order_items']
                for table in tables:
                    result = db.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                    stats[f"{table}_count"] = result[0]['count'] if result else 0
                
                # Recent activity
                recent_orders = db.execute_query(
                    "SELECT COUNT(*) as count FROM orders WHERE order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)"
                )
                stats['recent_orders_30_days'] = recent_orders[0]['count'] if recent_orders else 0
                
                # Total revenue
                revenue = db.execute_query("SELECT SUM(total_amount) as total FROM orders")
                stats['total_revenue'] = float(revenue[0]['total']) if revenue and revenue[0]['total'] else 0
                
                return jsonify(stats)
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/customers')
        def get_customers():
            """Get customers with pagination."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                limit = request.args.get('limit', 50, type=int)
                offset = request.args.get('offset', 0, type=int)
                
                query = """
                SELECT customer_id, first_name, last_name, email, city, state
                FROM customers
                ORDER BY customer_id
                LIMIT %s OFFSET %s
                """
                
                customers = db.execute_query(query, (limit, offset))
                
                # Get total count
                count_result = db.execute_query("SELECT COUNT(*) as total FROM customers")
                total = count_result[0]['total'] if count_result else 0
                
                return jsonify({
                    "customers": customers or [],
                    "total": total,
                    "limit": limit,
                    "offset": offset
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/customers/<int:customer_id>')
        def get_customer(customer_id: int):
            """Get customer by ID."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query = """
                SELECT customer_id, first_name, last_name, email, phone, 
                       address, city, state, zip_code
                FROM customers
                WHERE customer_id = %s
                """
                
                result = db.execute_query(query, (customer_id,))
                
                if not result:
                    return jsonify({"error": "Customer not found"}), 404
                
                return jsonify(result[0])
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/customers/<int:customer_id>/orders')
        def get_customer_orders(customer_id: int):
            """Get orders for a customer."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query = """
                SELECT o.order_id, o.order_date, o.status, o.total_amount,
                       COUNT(oi.order_item_id) as item_count
                FROM orders o
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.customer_id = %s
                GROUP BY o.order_id, o.order_date, o.status, o.total_amount
                ORDER BY o.order_date DESC
                """
                
                orders = db.execute_query(query, (customer_id,))
                
                return jsonify({"orders": orders or []})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/products')
        def get_products():
            """Get products with pagination."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                limit = request.args.get('limit', 50, type=int)
                offset = request.args.get('offset', 0, type=int)
                category = request.args.get('category')
                
                base_query = """
                SELECT p.product_id, p.product_name, p.price, p.stock_quantity,
                       p.sku, c.category_name
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                """
                
                if category:
                    query = base_query + " WHERE c.category_name = %s ORDER BY p.product_name LIMIT %s OFFSET %s"
                    products = db.execute_query(query, (category, limit, offset))
                    
                    count_query = "SELECT COUNT(*) as total FROM products p JOIN categories c ON p.category_id = c.category_id WHERE c.category_name = %s"
                    count_result = db.execute_query(count_query, (category,))
                else:
                    query = base_query + " ORDER BY p.product_name LIMIT %s OFFSET %s"
                    products = db.execute_query(query, (limit, offset))
                    
                    count_result = db.execute_query("SELECT COUNT(*) as total FROM products")
                
                total = count_result[0]['total'] if count_result else 0
                
                return jsonify({
                    "products": products or [],
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "category": category
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/products/<int:product_id>')
        def get_product(product_id: int):
            """Get product by ID."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query = """
                SELECT p.product_id, p.product_name, p.description, p.price, p.stock_quantity,
                       p.sku, c.category_name, c.category_id
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                WHERE p.product_id = %s
                """
                
                result = db.execute_query(query, (product_id,))
                
                if not result:
                    return jsonify({"error": "Product not found"}), 404
                
                return jsonify(result[0])
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/products/category/<string:category>')
        def get_products_by_category(category: str):
            """Get products by category."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                limit = request.args.get('limit', 50, type=int)
                offset = request.args.get('offset', 0, type=int)
                
                query = """
                SELECT p.product_id, p.product_name, p.price, p.stock_quantity,
                       p.sku, c.category_name
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                WHERE c.category_name = %s
                ORDER BY p.product_name
                LIMIT %s OFFSET %s
                """
                
                products = db.execute_query(query, (category, limit, offset))
                
                count_query = """
                SELECT COUNT(*) as total 
                FROM products p 
                JOIN categories c ON p.category_id = c.category_id 
                WHERE c.category_name = %s
                """
                count_result = db.execute_query(count_query, (category,))
                total = count_result[0]['total'] if count_result else 0
                
                return jsonify({
                    "products": products or [],
                    "category": category,
                    "total": total,
                    "limit": limit,
                    "offset": offset
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/orders')
        def get_orders():
            """Get recent orders."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                limit = request.args.get('limit', 20, type=int)
                offset = request.args.get('offset', 0, type=int)
                
                query = """
                SELECT o.order_id, o.order_date, o.status, o.total_amount,
                       c.first_name, c.last_name, c.email,
                       COUNT(oi.order_item_id) as item_count
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                GROUP BY o.order_id, o.order_date, o.status, o.total_amount,
                         c.first_name, c.last_name, c.email
                ORDER BY o.order_date DESC
                LIMIT %s OFFSET %s
                """
                
                orders = db.execute_query(query, (limit, offset))
                
                count_result = db.execute_query("SELECT COUNT(*) as total FROM orders")
                total = count_result[0]['total'] if count_result else 0
                
                return jsonify({
                    "orders": orders or [],
                    "total": total,
                    "limit": limit,
                    "offset": offset
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/orders/<int:order_id>')
        def get_order(order_id: int):
            """Get order details."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                # Get order info
                order_query = """
                SELECT o.order_id, o.order_date, o.status, o.total_amount,
                       c.customer_id, c.first_name, c.last_name, c.email
                FROM orders o
                JOIN customers c ON o.customer_id = c.customer_id
                WHERE o.order_id = %s
                """
                
                order_result = db.execute_query(order_query, (order_id,))
                
                if not order_result:
                    return jsonify({"error": "Order not found"}), 404
                
                order = order_result[0]
                
                # Get order items
                items_query = """
                SELECT oi.order_item_id, oi.quantity, oi.unit_price, oi.total_price,
                       p.product_id, p.product_name, p.sku, c.category_name
                FROM order_items oi
                JOIN products p ON oi.product_id = p.product_id
                JOIN categories c ON p.category_id = c.category_id
                WHERE oi.order_id = %s
                ORDER BY oi.order_item_id
                """
                
                items = db.execute_query(items_query, (order_id,))
                
                order['items'] = items or []
                
                return jsonify(order)
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/analytics/sales-by-month')
        def get_sales_by_month():
            """Get monthly sales analytics."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query = """
                SELECT 
                    DATE_FORMAT(order_date, '%Y-%m') as month,
                    COUNT(DISTINCT order_id) as order_count,
                    COUNT(DISTINCT customer_id) as customer_count,
                    SUM(total_amount) as total_revenue,
                    AVG(total_amount) as avg_order_value
                FROM orders
                GROUP BY DATE_FORMAT(order_date, '%Y-%m')
                ORDER BY month DESC
                LIMIT 12
                """
                
                sales_data = db.execute_query(query)
                
                return jsonify({"monthly_sales": sales_data or []})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/analytics/top-products')
        def get_top_products():
            """Get best selling products."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                limit = request.args.get('limit', 10, type=int)
                
                query = """
                SELECT 
                    p.product_name,
                    c.category_name,
                    p.price,
                    SUM(oi.quantity) as total_sold,
                    SUM(oi.total_price) as total_revenue,
                    COUNT(DISTINCT oi.order_id) as order_count
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                JOIN order_items oi ON p.product_id = oi.product_id
                GROUP BY p.product_id, p.product_name, c.category_name, p.price
                ORDER BY total_sold DESC
                LIMIT %s
                """
                
                top_products = db.execute_query(query, (limit,))
                
                return jsonify({"top_products": top_products or []})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/analytics/customer-segments')
        def get_customer_segments():
            """Get customer segmentation analytics."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query = """
                SELECT 
                    CASE 
                        WHEN total_spent >= 1000 THEN 'VIP'
                        WHEN total_spent >= 500 THEN 'Premium'
                        WHEN total_spent >= 100 THEN 'Regular'
                        ELSE 'New'
                    END as segment,
                    COUNT(*) as customer_count,
                    AVG(total_spent) as avg_spent,
                    SUM(total_spent) as total_revenue,
                    AVG(order_count) as avg_orders
                FROM (
                    SELECT 
                        c.customer_id,
                        COALESCE(SUM(o.total_amount), 0) as total_spent,
                        COUNT(o.order_id) as order_count
                    FROM customers c
                    LEFT JOIN orders o ON c.customer_id = o.customer_id
                    GROUP BY c.customer_id
                ) customer_stats
                GROUP BY 
                    CASE 
                        WHEN total_spent >= 1000 THEN 'VIP'
                        WHEN total_spent >= 500 THEN 'Premium'
                        WHEN total_spent >= 100 THEN 'Regular'
                        ELSE 'New'
                    END
                ORDER BY 
                    CASE segment
                        WHEN 'VIP' THEN 1
                        WHEN 'Premium' THEN 2
                        WHEN 'Regular' THEN 3
                        WHEN 'New' THEN 4
                    END
                """
                
                segments = db.execute_query(query)
                
                return jsonify({"customer_segments": segments or []})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/search/customers')
        def search_customers():
            """Search customers by name or email."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query_param = request.args.get('q', '').strip()
                if not query_param:
                    return jsonify({"error": "Query parameter 'q' is required"}), 400
                
                search_query = """
                SELECT customer_id, first_name, last_name, email, city, state
                FROM customers
                WHERE first_name LIKE %s 
                   OR last_name LIKE %s 
                   OR email LIKE %s
                   OR CONCAT(first_name, ' ', last_name) LIKE %s
                ORDER BY last_name, first_name
                LIMIT 20
                """
                
                search_term = f"%{query_param}%"
                results = db.execute_query(search_query, (search_term, search_term, search_term, search_term))
                
                return jsonify({"customers": results or [], "query": query_param})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/search/products')
        def search_products():
            """Search products by name or description."""
            db = self.get_db()
            if not db:
                return jsonify({"error": "Database connection failed"}), 500
            
            try:
                query_param = request.args.get('q', '').strip()
                if not query_param:
                    return jsonify({"error": "Query parameter 'q' is required"}), 400
                
                search_query = """
                SELECT p.product_id, p.product_name, p.price, p.stock_quantity,
                       p.sku, c.category_name
                FROM products p
                JOIN categories c ON p.category_id = c.category_id
                WHERE p.product_name LIKE %s 
                   OR p.description LIKE %s
                   OR p.sku LIKE %s
                ORDER BY p.product_name
                LIMIT 20
                """
                
                search_term = f"%{query_param}%"
                results = db.execute_query(search_query, (search_term, search_term, search_term))
                
                return jsonify({"products": results or [], "query": query_param})
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Endpoint not found"}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({"error": "Internal server error"}), 500
    
    def run(self, host='127.0.0.1', port=5000, debug=True):
        """Run the API server."""
        print(f"🚀 Starting MySQL Practice API...")
        print(f"📍 Server running at: http://{host}:{port}")
        print(f"📖 API Documentation: http://{host}:{port}")
        print(f"🔍 Example: http://{host}:{port}/api/stats")
        
        self.app.run(host=host, port=port, debug=debug)


def main():
    """Start the API server."""
    print("🌐 MySQL Practice REST API")
    print("=" * 30)
    
    try:
        # Test database connection first
        db = MySQLConnection()
        if not db.connect():
            print("❌ Failed to connect to database. Please check your configuration.")
            print("Make sure MySQL is running and .env file is configured correctly.")
            return
        db.disconnect()
        print("✅ Database connection successful")
        
        # Start API server
        api = DatabaseAPI()
        api.run(host='0.0.0.0', port=5002, debug=True)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except ImportError:
        print("❌ Flask not installed. Install with: pip install flask flask-cors")
    except Exception as e:
        print(f"❌ Error starting server: {e}")


if __name__ == "__main__":
    main()
