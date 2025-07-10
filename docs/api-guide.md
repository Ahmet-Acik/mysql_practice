# REST API Usage Guide

## 🌐 **How to View and Use the REST API**

The MySQL Practice Project includes a comprehensive REST API built with Flask that provides web access to your database.

### **🚀 Quick Start**

#### **Option 1: Using Docker (Recommended)**
```bash
# 1. Ensure Docker services are running
docker-compose up -d

# 2. Start the API server
docker exec -d mysql_practice_app python api/rest_api.py

# 3. Open your browser and visit:
# http://localhost:5001
```

#### **Option 2: Using CLI**
```bash
# Start API via CLI
docker exec -it mysql_practice_app python cli.py api
```

#### **Option 3: Local Development**
```bash
# Install dependencies
pip install flask flask-cors

# Start API locally (requires local MySQL)
python api/rest_api.py
```

### **📍 API Endpoints**

#### **Main Documentation**
- **🏠 Homepage:** http://localhost:5001
- **📊 Live Stats:** http://localhost:5001/api/stats

#### **📊 Database Statistics**
```bash
GET /api/stats
```
Returns database overview including table counts and metrics.

#### **👥 Customer Endpoints**
```bash
GET /api/customers                    # List all customers (with pagination)
GET /api/customers/{id}               # Get specific customer
GET /api/customers/{id}/orders        # Get customer's orders
GET /api/search/customers?q={query}   # Search customers
```

#### **🛍️ Product Endpoints**
```bash
GET /api/products                     # List all products (with pagination)
GET /api/products/{id}                # Get specific product
GET /api/products/category/{category} # Get products by category
GET /api/search/products?q={query}    # Search products
```

#### **📦 Order Endpoints**
```bash
GET /api/orders                       # List recent orders
GET /api/orders/{id}                  # Get order details
```

#### **📈 Analytics Endpoints**
```bash
GET /api/analytics/sales-by-month     # Monthly sales data
GET /api/analytics/top-products       # Best selling products
GET /api/analytics/customer-segments  # Customer analysis
```

### **🔍 Example API Calls**

#### **Using curl:**
```bash
# Get database statistics
curl http://localhost:5001/api/stats

# Get first 5 customers
curl "http://localhost:5001/api/customers?limit=5"

# Search for customers named "John"
curl "http://localhost:5001/api/search/customers?q=John"

# Get top 10 products
curl "http://localhost:5001/api/analytics/top-products?limit=10"

# Get monthly sales data
curl http://localhost:5001/api/analytics/sales-by-month
```

#### **Using Browser:**
Simply visit these URLs in your browser:
- http://localhost:5001/api/stats
- http://localhost:5001/api/customers?limit=5
- http://localhost:5001/api/products?limit=10
- http://localhost:5001/api/analytics/sales-by-month

### **🎨 Web Interface Features**

The API includes a beautiful web documentation interface with:
- **📋 Complete endpoint documentation**
- **🎯 Interactive examples**
- **🔗 Clickable links** to test endpoints
- **📊 Real-time data display**
- **💻 Professional styling**

### **🔧 Configuration**

#### **Port Configuration**
- **Docker:** API runs on port 5002 inside container, mapped to 5001 on host
- **Local:** API runs on port 5002 by default (can be customized)

#### **Environment Variables**
```bash
DB_HOST=mysql          # Database host
DB_PORT=3306           # Database port
DB_USER=practice_user  # Database user
DB_PASSWORD=practice_password
DB_NAME=practice_db    # Database name
```

### **📱 Response Format**

All API responses are in JSON format:

```json
{
  "customers": [...],
  "total": 150,
  "limit": 20,
  "offset": 0
}
```

### **🛠️ Development & Testing**

#### **Test API Endpoints:**
```bash
# Quick health check
curl http://localhost:5001/api/stats

# Test with parameters
curl "http://localhost:5001/api/customers?limit=3&offset=10"

# Test search functionality
curl "http://localhost:5001/api/search/products?q=laptop"
```

#### **Error Handling:**
The API provides helpful error messages:
```json
{
  "error": "Database connection failed"
}
```

### **🎯 Integration Examples**

#### **JavaScript/Fetch:**
```javascript
// Get database stats
fetch('http://localhost:5001/api/stats')
  .then(response => response.json())
  .then(data => console.log(data));

// Search customers
fetch('http://localhost:5001/api/search/customers?q=John')
  .then(response => response.json())
  .then(data => console.log(data.customers));
```

#### **Python/Requests:**
```python
import requests

# Get database statistics
response = requests.get('http://localhost:5001/api/stats')
stats = response.json()
print(f"Total customers: {stats['customers_count']}")

# Get top products
response = requests.get('http://localhost:5001/api/analytics/top-products')
products = response.json()['top_products']
for product in products:
    print(f"{product['product_name']}: {product['total_sold']} sold")
```

### **🔒 Security Notes**

- API includes CORS headers for web browser access
- All database operations use parameterized queries
- Error handling prevents information disclosure
- Rate limiting should be implemented for production use

### **🚀 Production Deployment**

For production deployment:
1. Use environment variables for configuration
2. Implement authentication/authorization
3. Add rate limiting
4. Use HTTPS
5. Configure proper CORS headers
6. Add logging and monitoring

### **📞 Support**

If you encounter issues:
1. Check that Docker services are running: `docker-compose ps`
2. Verify database connectivity: `docker exec -it mysql_practice_app python cli.py status`
3. Check API logs: `docker logs mysql_practice_app`
4. Ensure port 5001 is not in use by another application
