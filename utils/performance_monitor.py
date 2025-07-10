"""
MySQL Practice Project - Performance Benchmarking
Benchmark and monitor database performance for optimization insights.
"""

import os
import sys
import time
from typing import Any, Dict, List, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import MySQLConnection


class PerformanceBenchmark:
    """Database performance benchmarking and monitoring."""

    def __init__(self):
        self.db: Optional[MySQLConnection] = None
        self.results: List[Dict[str, Any]] = []

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

    def benchmark_query(
        self, name: str, query: str, params: tuple = None, iterations: int = 10
    ) -> Dict[str, Any]:
        """Benchmark a specific query."""
        if not self._check_connection():
            return {}
        assert self.db is not None

        print(f"🔍 Benchmarking: {name}")

        times = []
        results_count = 0

        for i in range(iterations):
            start_time = time.perf_counter()

            try:
                if params:
                    result = self.db.execute_query(query, params)
                else:
                    result = self.db.execute_query(query)

                end_time = time.perf_counter()
                execution_time = (
                    end_time - start_time
                ) * 1000  # Convert to milliseconds
                times.append(execution_time)

                if i == 0 and result:  # Count results from first iteration
                    results_count = len(result)

            except Exception as e:
                print(f"  ❌ Error in iteration {i+1}: {e}")
                continue

        if not times:
            return {"name": name, "error": "All iterations failed"}

        # Calculate statistics
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)

        benchmark_result = {
            "name": name,
            "iterations": len(times),
            "avg_time_ms": round(avg_time, 3),
            "min_time_ms": round(min_time, 3),
            "max_time_ms": round(max_time, 3),
            "results_count": results_count,
            "query": query,
        }

        self.results.append(benchmark_result)

        print(
            f"  ✅ Avg: {avg_time:.3f}ms, Min: {min_time:.3f}ms, Max: {max_time:.3f}ms, Results: {results_count}"
        )

        return benchmark_result

    def benchmark_common_queries(self):
        """Benchmark common database queries."""
        print("\n🚀 Benchmarking Common Queries")
        print("=" * 40)

        queries = [
            ("Simple SELECT", "SELECT COUNT(*) FROM customers", None),
            (
                "JOIN Query",
                """
                SELECT c.first_name, c.last_name, COUNT(o.order_id) as order_count
                FROM customers c
                LEFT JOIN orders o ON c.customer_id = o.customer_id
                GROUP BY c.customer_id, c.first_name, c.last_name
                LIMIT 100
            """,
                None,
            ),
            (
                "Complex Aggregation",
                """
                SELECT 
                    cat.category_name,
                    COUNT(p.product_id) as product_count,
                    AVG(p.price) as avg_price,
                    SUM(COALESCE(oi.quantity, 0)) as total_sold
                FROM categories cat
                LEFT JOIN products p ON cat.category_id = p.category_id
                LEFT JOIN order_items oi ON p.product_id = oi.product_id
                GROUP BY cat.category_id, cat.category_name
                ORDER BY total_sold DESC
            """,
                None,
            ),
            (
                "Subquery",
                """
                SELECT product_name, price
                FROM products
                WHERE price > (SELECT AVG(price) FROM products)
                ORDER BY price DESC
                LIMIT 50
            """,
                None,
            ),
            (
                "Window Function",
                """
                SELECT 
                    product_name,
                    price,
                    ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) as price_rank
                FROM products
                ORDER BY category_id, price_rank
                LIMIT 100
            """,
                None,
            ),
        ]

        for name, query, params in queries:
            try:
                self.benchmark_query(name, query, params, iterations=5)
                time.sleep(0.1)  # Small delay between benchmarks
            except Exception as e:
                print(f"  ❌ Failed to benchmark {name}: {e}")

    def analyze_slow_queries(self):
        """Analyze potentially slow queries using EXPLAIN."""
        print("\n🐌 Analyzing Query Performance")
        print("=" * 40)

        if not self._check_connection():
            return
        assert self.db is not None

        slow_queries = [
            (
                "Unindexed JOIN",
                """
                SELECT c.email, o.order_date, p.product_name
                FROM customers c
                JOIN orders o ON c.customer_id = o.customer_id
                JOIN order_items oi ON o.order_id = oi.order_id
                JOIN products p ON oi.product_id = p.product_id
                WHERE c.email LIKE '%@email.com'
                AND o.order_date >= '2024-01-01'
            """,
            ),
            (
                "Full Table Scan",
                """
                SELECT *
                FROM products
                WHERE description LIKE '%quality%'
                AND price BETWEEN 50 AND 200
            """,
            ),
            (
                "Complex WHERE",
                """
                SELECT c.first_name, c.last_name, SUM(o.total_amount) as total
                FROM customers c
                JOIN orders o ON c.customer_id = o.customer_id
                WHERE c.city IN ('New York', 'Los Angeles', 'Chicago')
                AND YEAR(o.order_date) = 2024
                GROUP BY c.customer_id, c.first_name, c.last_name
                HAVING total > 500
            """,
            ),
        ]

        for name, query in slow_queries:
            print(f"\n📊 Analyzing: {name}")

            try:
                # Get EXPLAIN output
                explain_query = f"EXPLAIN FORMAT=JSON {query}"
                explain_result = self.db.execute_query(explain_query)

                if explain_result:
                    print("  📋 EXPLAIN Analysis Available")
                    # Note: Full JSON parsing would require additional logic

                # Benchmark the query
                self.benchmark_query(f"SLOW: {name}", query, iterations=3)

            except Exception as e:
                print(f"  ❌ Error analyzing {name}: {e}")

    def monitor_database_status(self):
        """Monitor important database status variables."""
        print("\n📈 Database Status Monitoring")
        print("=" * 40)

        if not self._check_connection():
            return
        assert self.db is not None

        status_vars = [
            "Connections",
            "Queries",
            "Questions",
            "Slow_queries",
            "Uptime",
            "Threads_connected",
            "Threads_running",
            "Com_select",
            "Com_insert",
            "Com_update",
            "Com_delete",
            "Innodb_buffer_pool_size",
            "Innodb_buffer_pool_reads",
            "Innodb_buffer_pool_read_requests",
            "Innodb_rows_read",
            "Innodb_rows_inserted",
            "Innodb_rows_updated",
            "Innodb_rows_deleted",
        ]

        print("  Key Performance Metrics:")
        for var in status_vars:
            try:
                result = self.db.execute_query(f"SHOW STATUS LIKE '{var}'")
                if result and len(result) > 0:
                    value = result[0].get("Value", "N/A")
                    print(f"  • {var}: {value}")
            except Exception:
                print(f"  • {var}: Unable to retrieve")

    def suggest_optimizations(self):
        """Suggest performance optimizations based on analysis."""
        print("\n💡 Performance Optimization Suggestions")
        print("=" * 40)

        if not self.results:
            print("  No benchmark results available")
            return

        # Analyze results
        slow_queries = [r for r in self.results if r.get("avg_time_ms", 0) > 100]
        fast_queries = [r for r in self.results if r.get("avg_time_ms", 0) < 10]

        print(f"  📊 Analysis Summary:")
        print(f"  • Total queries benchmarked: {len(self.results)}")
        print(f"  • Slow queries (>100ms): {len(slow_queries)}")
        print(f"  • Fast queries (<10ms): {len(fast_queries)}")

        if slow_queries:
            print(f"\n  🐌 Slow Queries Need Attention:")
            for query in slow_queries:
                print(f"  • {query['name']}: {query['avg_time_ms']}ms avg")

        print(f"\n  🚀 Recommended Optimizations:")
        optimizations = [
            "Add indexes on frequently queried columns (WHERE, JOIN, ORDER BY)",
            "Use LIMIT clauses to reduce result set size",
            "Avoid SELECT * in favor of specific columns",
            "Consider query rewriting for complex JOINs",
            "Implement query result caching for repeated queries",
            "Monitor and optimize MySQL configuration variables",
            "Use EXPLAIN to analyze query execution plans",
            "Consider partitioning for very large tables",
            "Implement connection pooling for high-load scenarios",
            "Regular maintenance: ANALYZE TABLE, OPTIMIZE TABLE",
        ]

        for i, opt in enumerate(optimizations, 1):
            print(f"  {i:2d}. {opt}")

    def generate_report(self):
        """Generate a comprehensive performance report."""
        print("\n📋 Performance Benchmark Report")
        print("=" * 50)

        if not self.results:
            print("  No benchmark data available")
            return

        # Sort by average time
        sorted_results = sorted(
            self.results, key=lambda x: x.get("avg_time_ms", 0), reverse=True
        )

        print(f"  Query Performance Summary:")
        print(
            f"  {'Query Name':<25} {'Avg (ms)':<10} {'Min (ms)':<10} {'Max (ms)':<10} {'Results':<8}"
        )
        print(f"  {'-'*25} {'-'*10} {'-'*10} {'-'*10} {'-'*8}")

        for result in sorted_results:
            name = result.get("name", "Unknown")[:24]
            avg_time = result.get("avg_time_ms", 0)
            min_time = result.get("min_time_ms", 0)
            max_time = result.get("max_time_ms", 0)
            count = result.get("results_count", 0)

            print(
                f"  {name:<25} {avg_time:<10.3f} {min_time:<10.3f} {max_time:<10.3f} {count:<8}"
            )

        # Performance categories
        total_queries = len(self.results)
        fast_queries = len([r for r in self.results if r.get("avg_time_ms", 0) < 10])
        medium_queries = len(
            [r for r in self.results if 10 <= r.get("avg_time_ms", 0) < 100]
        )
        slow_queries = len([r for r in self.results if r.get("avg_time_ms", 0) >= 100])

        print(f"\n  Performance Distribution:")
        print(
            f"  • Fast queries (<10ms):    {fast_queries}/{total_queries} ({fast_queries/total_queries*100:.1f}%)"
        )
        print(
            f"  • Medium queries (10-100ms): {medium_queries}/{total_queries} ({medium_queries/total_queries*100:.1f}%)"
        )
        print(
            f"  • Slow queries (>100ms):   {slow_queries}/{total_queries} ({slow_queries/total_queries*100:.1f}%)"
        )


def main():
    """Run performance benchmarking."""
    print("⚡ MySQL Performance Benchmark")
    print("=" * 35)

    benchmark = PerformanceBenchmark()

    try:
        if not benchmark.setup():
            print("❌ Failed to connect to database")
            return

        # Run benchmark suite
        benchmark.benchmark_common_queries()
        benchmark.analyze_slow_queries()
        benchmark.monitor_database_status()
        benchmark.suggest_optimizations()
        benchmark.generate_report()

        print(f"\n🎉 Benchmark Complete!")
        print(f"Check the results above for optimization opportunities.")

    except Exception as e:
        print(f"❌ Error during benchmarking: {e}")
    finally:
        benchmark.cleanup()


if __name__ == "__main__":
    main()
