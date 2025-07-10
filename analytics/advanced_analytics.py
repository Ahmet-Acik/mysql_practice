"""
MySQL Practice Project - Advanced Analytics
Business intelligence and advanced analytics queries.
"""

import json
import os
import sys
from datetime import datetime
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


class AdvancedAnalytics:
    """Advanced business analytics and reporting."""

    def __init__(self):
        self.db: Optional[MySQLConnection] = None

    def setup(self) -> bool:
        """Setup database connection."""
        try:
            self.db = MySQLConnection()
            return self.db.connect()
        except Exception as e:
            print(f"Failed to setup database connection: {e}")
            return False

    def cleanup(self):
        """Clean up database connection."""
        if self.db:
            self.db.disconnect()

    def _check_connection(self) -> bool:
        """Check if database connection is available."""
        if not self.db:
            print("Error: No database connection")
            return False
        return True

    def customer_lifetime_value_analysis(self):
        """Comprehensive Customer Lifetime Value analysis."""
        print("=== Customer Lifetime Value Analysis ===")

        if not self._check_connection():
            return
        assert self.db is not None

        # CLV with cohort analysis
        clv_query = """
        WITH customer_metrics AS (
            SELECT 
                c.customer_id,
                CONCAT(c.first_name, ' ', c.last_name) as customer_name,
                c.email,
                c.city,
                c.state,
                MIN(o.order_date) as first_order_date,
                MAX(o.order_date) as last_order_date,
                COUNT(DISTINCT o.order_id) as total_orders,
                SUM(o.total_amount) as total_revenue,
                AVG(o.total_amount) as avg_order_value,
                DATEDIFF(MAX(o.order_date), MIN(o.order_date)) + 1 as customer_lifespan_days,
                COUNT(DISTINCT DATE_FORMAT(o.order_date, '%Y-%m')) as active_months
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state
        ),
        clv_calculations AS (
            SELECT 
                *,
                CASE 
                    WHEN customer_lifespan_days > 0 
                    THEN total_revenue / customer_lifespan_days * 365
                    ELSE total_revenue
                END as estimated_annual_value,
                CASE 
                    WHEN active_months > 0 
                    THEN total_revenue / active_months
                    ELSE total_revenue
                END as monthly_value,
                CASE
                    WHEN total_revenue >= 2000 THEN 'VIP'
                    WHEN total_revenue >= 1000 THEN 'High Value'
                    WHEN total_revenue >= 500 THEN 'Medium Value'
                    WHEN total_revenue >= 100 THEN 'Regular'
                    ELSE 'Low Value'
                END as customer_segment,
                DATEDIFF(CURDATE(), last_order_date) as days_since_last_order
            FROM customer_metrics
        )
        SELECT * FROM clv_calculations
        ORDER BY total_revenue DESC
        LIMIT 20
        """

        try:
            results = self.db.execute_query(clv_query)
            if results:
                print("\n📊 Top 20 Customers by Lifetime Value:")
                print(
                    "Name                | Segment    | Orders | Revenue   | Est.Annual | Days Since Last"
                )
                print("-" * 80)

                for row in results:
                    name = row["customer_name"][:18].ljust(18)
                    segment = row["customer_segment"][:10].ljust(10)
                    orders = str(row["total_orders"]).rjust(6)
                    revenue = f"${row['total_revenue']:.2f}".rjust(9)
                    annual = f"${row['estimated_annual_value']:.0f}".rjust(10)
                    days_since = str(row["days_since_last_order"]).rjust(4)

                    print(
                        f"{name} | {segment} | {orders} | {revenue} | {annual} | {days_since}"
                    )

        except Exception as e:
            print(f"Error in CLV analysis: {e}")

    def market_basket_analysis(self):
        """Market basket analysis - products frequently bought together."""
        print("\n=== Market Basket Analysis ===")

        if not self._check_connection():
            return
        assert self.db is not None

        # Association rules - products bought together
        basket_query = """
        WITH order_product_pairs AS (
            SELECT DISTINCT
                oi1.order_id,
                oi1.product_id as product_a_id,
                oi2.product_id as product_b_id,
                p1.product_name as product_a,
                p2.product_name as product_b,
                c1.category_name as category_a,
                c2.category_name as category_b
            FROM order_items oi1
            JOIN order_items oi2 ON oi1.order_id = oi2.order_id 
                AND oi1.product_id < oi2.product_id
            JOIN products p1 ON oi1.product_id = p1.product_id
            JOIN products p2 ON oi2.product_id = p2.product_id
            JOIN categories c1 ON p1.category_id = c1.category_id
            JOIN categories c2 ON p2.category_id = c2.category_id
        ),
        basket_analysis AS (
            SELECT 
                product_a,
                product_b,
                category_a,
                category_b,
                COUNT(*) as frequency,
                COUNT(*) * 100.0 / (
                    SELECT COUNT(DISTINCT order_id) FROM order_items
                ) as support_percentage,
                COUNT(*) * 100.0 / (
                    SELECT COUNT(DISTINCT order_id) 
                    FROM order_items oi 
                    JOIN order_product_pairs opp ON oi.product_id = opp.product_a_id
                ) as confidence_percentage
            FROM order_product_pairs
            GROUP BY product_a_id, product_b_id, product_a, product_b, category_a, category_b
            HAVING frequency >= 2
            ORDER BY frequency DESC, support_percentage DESC
        )
        SELECT * FROM basket_analysis
        LIMIT 15
        """

        try:
            results = self.db.execute_query(basket_query)
            if results:
                print("\n🛒 Frequently Bought Together (Min 2 occurrences):")
                for i, row in enumerate(results, 1):
                    print(f"\n{i:2d}. {row['product_a']} + {row['product_b']}")
                    print(f"    Categories: {row['category_a']} & {row['category_b']}")
                    print(f"    Frequency: {row['frequency']} orders")
                    print(
                        f"    Support: {row['support_percentage']:.2f}% | Confidence: {row['confidence_percentage']:.2f}%"
                    )
            else:
                print("No significant product associations found")

        except Exception as e:
            print(f"Error in market basket analysis: {e}")

    def cohort_retention_analysis(self):
        """Customer cohort retention analysis."""
        print("\n=== Cohort Retention Analysis ===")

        if not self._check_connection():
            return
        assert self.db is not None

        cohort_query = """
        WITH first_orders AS (
            SELECT 
                customer_id,
                MIN(order_date) as first_order_date,
                DATE_FORMAT(MIN(order_date), '%Y-%m') as cohort_month
            FROM orders
            GROUP BY customer_id
        ),
        customer_orders AS (
            SELECT 
                fo.customer_id,
                fo.cohort_month,
                o.order_date,
                PERIOD_DIFF(
                    DATE_FORMAT(o.order_date, '%Y%m'),
                    DATE_FORMAT(fo.first_order_date, '%Y%m')
                ) as period_number
            FROM first_orders fo
            JOIN orders o ON fo.customer_id = o.customer_id
        ),
        cohort_data AS (
            SELECT 
                cohort_month,
                period_number,
                COUNT(DISTINCT customer_id) as customers_active
            FROM customer_orders
            GROUP BY cohort_month, period_number
        ),
        cohort_sizes AS (
            SELECT 
                cohort_month,
                COUNT(DISTINCT customer_id) as cohort_size
            FROM first_orders
            GROUP BY cohort_month
        )
        SELECT 
            cd.cohort_month,
            cs.cohort_size,
            cd.period_number,
            cd.customers_active,
            ROUND(cd.customers_active * 100.0 / cs.cohort_size, 2) as retention_rate
        FROM cohort_data cd
        JOIN cohort_sizes cs ON cd.cohort_month = cs.cohort_month
        WHERE cd.period_number <= 12  -- First 12 months
        ORDER BY cd.cohort_month, cd.period_number
        """

        try:
            results = self.db.execute_query(cohort_query)
            if results:
                print("\n📈 Customer Retention by Cohort (First 12 months):")
                print(
                    "Cohort    | Size | Month 0 | Month 1 | Month 2 | Month 3 | Month 6 | Month 12"
                )
                print("-" * 75)

                # Group by cohort
                cohorts = {}
                for row in results:
                    cohort = row["cohort_month"]
                    if cohort not in cohorts:
                        cohorts[cohort] = {"size": row["cohort_size"], "periods": {}}
                    cohorts[cohort]["periods"][row["period_number"]] = row[
                        "retention_rate"
                    ]

                for cohort, data in cohorts.items():
                    line = f"{cohort} | {data['size']:4d} |"
                    for period in [0, 1, 2, 3, 6, 12]:
                        rate = data["periods"].get(period, 0)
                        line += f" {rate:6.1f}% |"
                    print(line)

        except Exception as e:
            print(f"Error in cohort analysis: {e}")

    def sales_forecasting_analysis(self):
        """Sales trend analysis and basic forecasting."""
        print("\n=== Sales Trend & Forecasting Analysis ===")

        if not self._check_connection():
            return
        assert self.db is not None

        # Monthly sales trends
        trend_query = """
        WITH monthly_sales AS (
            SELECT 
                YEAR(order_date) as year,
                MONTH(order_date) as month,
                DATE_FORMAT(order_date, '%Y-%m') as year_month,
                COUNT(DISTINCT order_id) as order_count,
                COUNT(DISTINCT customer_id) as unique_customers,
                SUM(total_amount) as revenue,
                AVG(total_amount) as avg_order_value
            FROM orders
            GROUP BY YEAR(order_date), MONTH(order_date)
            ORDER BY year, month
        ),
        trend_analysis AS (
            SELECT 
                *,
                LAG(revenue) OVER (ORDER BY year, month) as prev_month_revenue,
                LAG(order_count) OVER (ORDER BY year, month) as prev_month_orders,
                CASE 
                    WHEN LAG(revenue) OVER (ORDER BY year, month) IS NOT NULL
                    THEN ROUND(
                        (revenue - LAG(revenue) OVER (ORDER BY year, month)) * 100.0 / 
                        LAG(revenue) OVER (ORDER BY year, month), 2
                    )
                    ELSE 0
                END as revenue_growth_pct,
                AVG(revenue) OVER (
                    ORDER BY year, month 
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ) as revenue_3month_avg
            FROM monthly_sales
        )
        SELECT * FROM trend_analysis
        """

        try:
            results = self.db.execute_query(trend_query)
            if results:
                print("\n📊 Monthly Sales Trends:")
                print(
                    "Month    | Orders | Customers | Revenue   | Growth% | 3M Avg    | AOV"
                )
                print("-" * 70)

                for row in results:
                    month = row["year_month"]
                    orders = str(row["order_count"]).rjust(6)
                    customers = str(row["unique_customers"]).rjust(9)
                    revenue = f"${row['revenue']:.0f}".rjust(9)
                    growth = (
                        f"{row['revenue_growth_pct']:+.1f}%".rjust(7)
                        if row["revenue_growth_pct"]
                        else "   N/A"
                    )
                    avg_3m = f"${row['revenue_3month_avg']:.0f}".rjust(9)
                    aov = f"${row['avg_order_value']:.0f}".rjust(5)

                    print(
                        f"{month} | {orders} | {customers} | {revenue} | {growth} | {avg_3m} | {aov}"
                    )

                # Simple forecast (based on trend)
                if len(results) >= 3:
                    recent_avg = sum(row["revenue"] for row in results[-3:]) / 3
                    overall_avg = sum(row["revenue"] for row in results) / len(results)

                    print(f"\n📈 Simple Forecast Indicators:")
                    print(f"   Recent 3-month average: ${recent_avg:.2f}")
                    print(f"   Overall average: ${overall_avg:.2f}")

                    if recent_avg > overall_avg * 1.1:
                        print(
                            f"   📈 Trend: Growing (recent avg {((recent_avg/overall_avg-1)*100):+.1f}% above overall)"
                        )
                    elif recent_avg < overall_avg * 0.9:
                        print(
                            f"   📉 Trend: Declining (recent avg {((recent_avg/overall_avg-1)*100):+.1f}% below overall)"
                        )
                    else:
                        print(f"   ➡️  Trend: Stable")

        except Exception as e:
            print(f"Error in sales trend analysis: {e}")

    def product_performance_matrix(self):
        """BCG-style product performance matrix."""
        print("\n=== Product Performance Matrix ===")

        if not self._check_connection():
            return
        assert self.db is not None

        matrix_query = """
        WITH product_metrics AS (
            SELECT 
                p.product_id,
                p.product_name,
                c.category_name,
                p.price,
                p.stock_quantity,
                COALESCE(SUM(oi.quantity), 0) as total_units_sold,
                COALESCE(SUM(oi.total_price), 0) as total_revenue,
                COALESCE(COUNT(DISTINCT oi.order_id), 0) as order_frequency,
                COALESCE(AVG(oi.unit_price), p.price) as avg_selling_price,
                p.price - COALESCE(AVG(oi.unit_price), p.price) as price_variance
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN order_items oi ON p.product_id = oi.product_id
            GROUP BY p.product_id, p.product_name, c.category_name, p.price, p.stock_quantity
        ),
        market_stats AS (
            SELECT 
                AVG(total_revenue) as avg_revenue,
                AVG(total_units_sold) as avg_units_sold,
                STDDEV(total_revenue) as stddev_revenue,
                STDDEV(total_units_sold) as stddev_units
            FROM product_metrics
        ),
        performance_matrix AS (
            SELECT 
                pm.*,
                ms.avg_revenue,
                ms.avg_units_sold,
                CASE 
                    WHEN pm.total_revenue > ms.avg_revenue AND pm.total_units_sold > ms.avg_units_sold 
                    THEN 'Star Products'
                    WHEN pm.total_revenue > ms.avg_revenue AND pm.total_units_sold <= ms.avg_units_sold 
                    THEN 'Cash Cows'
                    WHEN pm.total_revenue <= ms.avg_revenue AND pm.total_units_sold > ms.avg_units_sold 
                    THEN 'Question Marks'
                    ELSE 'Dogs'
                END as bcg_category,
                ROUND(pm.total_revenue / NULLIF(ms.avg_revenue, 0), 2) as revenue_index,
                ROUND(pm.total_units_sold / NULLIF(ms.avg_units_sold, 0), 2) as volume_index
            FROM product_metrics pm
            CROSS JOIN market_stats ms
            WHERE pm.total_revenue > 0  -- Only products with sales
        )
        SELECT * FROM performance_matrix
        ORDER BY bcg_category, total_revenue DESC
        """

        try:
            results = self.db.execute_query(matrix_query)
            if results:
                print("\n📈 BCG Product Performance Matrix:")

                # Group by BCG category
                categories = {}
                for row in results:
                    cat = row["bcg_category"]
                    if cat not in categories:
                        categories[cat] = []
                    categories[cat].append(row)

                for bcg_cat, products in categories.items():
                    print(f"\n🔷 {bcg_cat} ({len(products)} products):")
                    print(
                        "Product Name            | Revenue   | Units | Rev.Idx | Vol.Idx"
                    )
                    print("-" * 60)

                    for product in products[:5]:  # Top 5 per category
                        name = product["product_name"][:22].ljust(22)
                        revenue = f"${product['total_revenue']:.0f}".rjust(9)
                        units = str(product["total_units_sold"]).rjust(5)
                        rev_idx = f"{product['revenue_index']:.2f}".rjust(7)
                        vol_idx = f"{product['volume_index']:.2f}".rjust(7)

                        print(f"{name} | {revenue} | {units} | {rev_idx} | {vol_idx}")

                    if len(products) > 5:
                        print(f"... and {len(products)-5} more products")

        except Exception as e:
            print(f"Error in product performance matrix: {e}")

    def generate_executive_dashboard(self):
        """Generate executive summary dashboard."""
        print("\n=== Executive Dashboard Summary ===")

        if not self._check_connection():
            return
        assert self.db is not None

        # Key metrics
        dashboard_query = """
        SELECT 
            (SELECT COUNT(*) FROM customers) as total_customers,
            (SELECT COUNT(*) FROM products) as total_products,
            (SELECT COUNT(*) FROM orders) as total_orders,
            (SELECT SUM(total_amount) FROM orders) as total_revenue,
            (SELECT AVG(total_amount) FROM orders) as avg_order_value,
            (SELECT COUNT(DISTINCT customer_id) FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)) as active_customers_30d,
            (SELECT COUNT(*) FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)) as orders_30d,
            (SELECT SUM(total_amount) FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)) as revenue_30d
        """

        try:
            result = self.db.execute_query(dashboard_query)
            if result:
                metrics = result[0]

                print("\n📊 Key Performance Indicators:")
                print(f"   Total Customers: {metrics['total_customers']:,}")
                print(f"   Total Products: {metrics['total_products']:,}")
                print(f"   Total Orders: {metrics['total_orders']:,}")
                print(f"   Total Revenue: ${metrics['total_revenue']:,.2f}")
                print(f"   Average Order Value: ${metrics['avg_order_value']:,.2f}")
                print(f"   Active Customers (30d): {metrics['active_customers_30d']:,}")
                print(f"   Orders Last 30 Days: {metrics['orders_30d']:,}")
                print(f"   Revenue Last 30 Days: ${metrics['revenue_30d']:,.2f}")

                # Calculate some ratios
                if metrics["total_customers"] > 0:
                    conversion_rate = (
                        metrics["active_customers_30d"] / metrics["total_customers"]
                    ) * 100
                    print(f"   Customer Activity Rate: {conversion_rate:.1f}%")

                if metrics["orders_30d"] > 0 and metrics["active_customers_30d"] > 0:
                    orders_per_customer = (
                        metrics["orders_30d"] / metrics["active_customers_30d"]
                    )
                    print(f"   Orders per Active Customer: {orders_per_customer:.1f}")

        except Exception as e:
            print(f"Error generating dashboard: {e}")

    def export_analytics_report(self, filename: Optional[str] = None):
        """Export analytics results to JSON."""
        if not filename:
            filename = (
                f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

        print(f"\n📄 Exporting analytics report to: {filename}")

        # This would collect all analytics data and export to JSON
        # Implementation depends on specific requirements
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "report_type": "advanced_analytics",
            "note": "Detailed analytics data would be collected here",
        }

        try:
            with open(filename, "w") as f:
                json.dump(report_data, f, indent=2)
            print(f"✅ Report exported successfully")
        except Exception as e:
            print(f"❌ Error exporting report: {e}")


def main():
    """Run advanced analytics suite."""
    print("🧠 MySQL Advanced Analytics Suite")
    print("=" * 40)

    analytics = AdvancedAnalytics()

    try:
        if not analytics.setup():
            print("❌ Failed to connect to database")
            return

        print("🚀 Running comprehensive analytics suite...")

        analytics.generate_executive_dashboard()
        analytics.customer_lifetime_value_analysis()
        analytics.market_basket_analysis()
        analytics.cohort_retention_analysis()
        analytics.sales_forecasting_analysis()
        analytics.product_performance_matrix()

        print("\n🎉 Advanced Analytics Complete!")
        print("Consider implementing these insights in your business strategy.")

    except Exception as e:
        print(f"❌ Error during analytics: {e}")
    finally:
        analytics.cleanup()


if __name__ == "__main__":
    main()
