"""
Database monitoring and logging system.
Provides real-time monitoring, query logging, and performance alerts.
"""

import json
import logging
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import psutil
from mysql.connector import Error

from config.database import MySQLConnection


class DatabaseMonitor:
    """Real-time database monitoring system."""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        try:
            self.log_dir.mkdir(exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create log directory {log_dir}: {e}")
            # Fallback to current directory
            self.log_dir = Path(".")

        # Setup logging
        self.setup_logging()

        # Monitoring configuration
        self.monitoring = True
        self.alert_thresholds = {
            "connection_count": 100,
            "slow_query_time": 5.0,  # seconds
            "cpu_usage": 80.0,  # percentage
            "memory_usage": 85.0,  # percentage
            "disk_usage": 90.0,  # percentage
        }

        # Performance metrics storage
        self.metrics = []
        self.max_metrics = 1000  # Keep last 1000 measurements

    def setup_logging(self):
        """Setup comprehensive logging system."""
        # Create formatters
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Main logger
        self.logger = logging.getLogger("mysql_monitor")
        self.logger.setLevel(logging.INFO)

        # File handlers
        info_handler = logging.FileHandler(self.log_dir / "monitor.log")
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)

        error_handler = logging.FileHandler(self.log_dir / "errors.log")
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        # Query logger
        self.query_logger = logging.getLogger("mysql_queries")
        self.query_logger.setLevel(logging.INFO)

        query_handler = logging.FileHandler(self.log_dir / "queries.log")
        query_handler.setLevel(logging.INFO)
        query_handler.setFormatter(formatter)

        # Add handlers
        self.logger.addHandler(info_handler)
        self.logger.addHandler(error_handler)
        self.query_logger.addHandler(query_handler)

        # Console handler for alerts
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_query(
        self,
        query: str,
        params: Optional[tuple] = None,
        execution_time: float = 0,
        rows_affected: int = 0,
    ):
        """Log database query with performance metrics."""
        query_info = {
            "timestamp": datetime.now().isoformat(),
            "query": query.strip(),
            "params": str(params) if params else None,
            "execution_time": execution_time,
            "rows_affected": rows_affected,
            "slow_query": execution_time > self.alert_thresholds["slow_query_time"],
        }

        self.query_logger.info(json.dumps(query_info))

        if query_info["slow_query"]:
            self.logger.warning(
                f"Slow query detected: {execution_time:.2f}s - {query[:100]}..."
            )

    def get_database_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive database metrics."""
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "database": {},
            "system": {},
        }

        try:
            db = MySQLConnection()
            if not db.connect():
                raise Error("Failed to connect to database")

            # Database status variables
            status_result = db.execute_query("SHOW STATUS")
            status_vars = {}
            if status_result:
                for row in status_result:
                    try:
                        if isinstance(row, dict):
                            # Handle dictionary format from MySQL connector
                            if "Variable_name" in row and "Value" in row:
                                status_vars[row["Variable_name"]] = row["Value"]
                            # Also handle other possible key formats
                            elif len(row) >= 2:
                                keys = list(row.keys())
                                values = list(row.values())
                                status_vars[str(keys[0])] = str(values[0])
                    except (IndexError, KeyError, TypeError, AttributeError):
                        continue

            # Process list (active connections) - requires PROCESS privilege
            try:
                process_result = db.execute_query("SHOW PROCESSLIST")
                process_list = process_result if process_result else []
            except Error as e:
                if "Access denied" in str(e):
                    self.logger.warning("SHOW PROCESSLIST requires PROCESS privilege")
                    process_list = []
                else:
                    raise

            # InnoDB status - requires PROCESS privilege
            try:
                db.execute_query("SHOW ENGINE INNODB STATUS")
                # innodb_result = innodb_result[0] if innodb_result else None
            except Error as e:
                if "Access denied" in str(e):
                    self.logger.warning(
                        "SHOW ENGINE INNODB STATUS requires PROCESS privilege"
                    )
                # innodb_status = None

            metrics["database"] = {
                "connections": int(status_vars.get("Threads_connected", 0)),
                "queries_per_second": float(status_vars.get("Queries", 0)),
                "slow_queries": int(status_vars.get("Slow_queries", 0)),
                "uptime": int(status_vars.get("Uptime", 0)),
                "active_processes": len(process_list),
                "buffer_pool_size": status_vars.get("Innodb_buffer_pool_size"),
                "buffer_pool_pages_data": int(
                    status_vars.get("Innodb_buffer_pool_pages_data", 0)
                ),
                "buffer_pool_pages_total": int(
                    status_vars.get("Innodb_buffer_pool_pages_total", 0)
                ),
                "status": "connected",
            }

            db.disconnect()

        except Error as e:
            self.logger.error(f"Failed to collect database metrics: {e}")
            metrics["database"]["error"] = str(e)
            metrics["database"]["status"] = "disconnected"
        except Exception as e:
            self.logger.error(f"Unexpected error collecting database metrics: {e}")
            metrics["database"]["error"] = str(e)
            metrics["database"]["status"] = "error"

        # System metrics
        try:
            metrics["system"] = {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage("/").percent,
                "load_average": (
                    list(psutil.getloadavg()) if hasattr(psutil, "getloadavg") else None
                ),
            }
        except Exception as e:
            self.logger.error(f"Failed to collect system metrics: {e}")
            metrics["system"]["error"] = str(e)

        return metrics

    def check_alerts(self, metrics: Dict[str, Any]):
        """Check metrics against alert thresholds."""
        alerts = []

        # Database alerts
        db_metrics = metrics.get("database", {})
        if db_metrics.get("connections", 0) > self.alert_thresholds["connection_count"]:
            alerts.append(f"High connection count: {db_metrics['connections']}")

        # System alerts
        sys_metrics = metrics.get("system", {})
        if sys_metrics.get("cpu_percent", 0) > self.alert_thresholds["cpu_usage"]:
            alerts.append(f"High CPU usage: {sys_metrics['cpu_percent']:.1f}%")

        if sys_metrics.get("memory_percent", 0) > self.alert_thresholds["memory_usage"]:
            alerts.append(f"High memory usage: {sys_metrics['memory_percent']:.1f}%")

        if sys_metrics.get("disk_percent", 0) > self.alert_thresholds["disk_usage"]:
            alerts.append(f"High disk usage: {sys_metrics['disk_percent']:.1f}%")

        # Log alerts
        for alert in alerts:
            self.logger.warning(f"ALERT: {alert}")

        return alerts

    def save_metrics(self, metrics: Dict[str, Any]):
        """Save metrics to file and memory."""
        # Add to memory storage
        self.metrics.append(metrics)
        if len(self.metrics) > self.max_metrics:
            self.metrics.pop(0)

        # Save to file
        metrics_file = (
            self.log_dir / f"metrics_{datetime.now().strftime('%Y%m%d')}.json"
        )
        with open(metrics_file, "a") as f:
            f.write(json.dumps(metrics) + "\n")

    def monitor_loop(self, interval: int = 60):
        """Main monitoring loop."""
        self.logger.info("Database monitoring started")

        while self.monitoring:
            try:
                # Collect metrics
                metrics = self.get_database_metrics()

                # Check for alerts
                alerts = self.check_alerts(metrics)

                # Save metrics
                self.save_metrics(metrics)

                # Log summary
                db_metrics = metrics.get("database", {})
                sys_metrics = metrics.get("system", {})

                self.logger.info(
                    f"Monitoring summary - "
                    f"Connections: {db_metrics.get('connections', 'N/A')}, "
                    f"CPU: {sys_metrics.get('cpu_percent', 'N/A'):.1f}%, "
                    f"Memory: {sys_metrics.get('memory_percent', 'N/A'):.1f}%, "
                    f"Alerts: {len(alerts)}"
                )

                time.sleep(interval)

            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                time.sleep(interval)

    def start_monitoring(self, interval: int = 60):
        """Start monitoring in a separate thread."""
        self.monitoring = True
        monitor_thread = threading.Thread(
            target=self.monitor_loop, args=(interval,), daemon=True
        )
        monitor_thread.start()
        return monitor_thread

    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring = False
        self.logger.info("Database monitoring stopped")

    def get_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate performance report for the last N hours."""
        cutoff_time = datetime.now() - timedelta(hours=hours)

        # Filter recent metrics
        recent_metrics = [
            m
            for m in self.metrics
            if datetime.fromisoformat(m["timestamp"]) > cutoff_time
        ]

        if not recent_metrics:
            return {"error": "No metrics available for the specified period"}

        # Calculate aggregations
        cpu_values = [m["system"].get("cpu_percent", 0) for m in recent_metrics]
        memory_values = [m["system"].get("memory_percent", 0) for m in recent_metrics]
        connection_values = [
            m["database"].get("connections", 0) for m in recent_metrics
        ]

        report = {
            "period_hours": hours,
            "metrics_count": len(recent_metrics),
            "system": {
                "cpu": {
                    "avg": sum(cpu_values) / len(cpu_values) if cpu_values else 0,
                    "max": max(cpu_values) if cpu_values else 0,
                    "min": min(cpu_values) if cpu_values else 0,
                },
                "memory": {
                    "avg": (
                        sum(memory_values) / len(memory_values) if memory_values else 0
                    ),
                    "max": max(memory_values) if memory_values else 0,
                    "min": min(memory_values) if memory_values else 0,
                },
            },
            "database": {
                "connections": {
                    "avg": (
                        sum(connection_values) / len(connection_values)
                        if connection_values
                        else 0
                    ),
                    "max": max(connection_values) if connection_values else 0,
                    "min": min(connection_values) if connection_values else 0,
                }
            },
        }

        return report


class QueryProfiler:
    """Query performance profiler with automatic optimization suggestions."""

    def __init__(self, monitor: DatabaseMonitor):
        self.monitor = monitor
        self.query_cache = {}

    def profile_query(
        self, query: str, params: Optional[tuple] = None
    ) -> Dict[str, Any]:
        """Profile a single query and return detailed metrics."""
        db = MySQLConnection()
        if not db.connect():
            return {"error": "Failed to connect to database"}

        try:
            # Enable profiling
            db.execute_query("SET profiling = 1")

            # Execute query with timing
            start_time = time.time()
            results = db.execute_query(query, params)
            execution_time = time.time() - start_time

            # Get query profile
            profiles = db.execute_query("SHOW PROFILES")
            profile_details = []

            if profiles:
                query_id = (
                    profiles[-1].get("Query_ID")
                    if isinstance(profiles[-1], dict)
                    else profiles[-1][0]
                )
                profile_details = db.execute_query(f"SHOW PROFILE FOR QUERY {query_id}")

            # Get execution plan
            explain_plan = []
            if query.strip().upper().startswith("SELECT"):
                try:
                    explain_plan = db.execute_query(f"EXPLAIN {query}", params)
                except Exception:
                    explain_plan = []

            profile_result = {
                "query": query,
                "execution_time": execution_time,
                "rows_returned": len(results) if results else 0,
                "profile_details": profile_details or [],
                "explain_plan": explain_plan or [],
                "optimization_suggestions": self._get_optimization_suggestions(
                    query, execution_time, explain_plan or []
                ),
            }

            # Log the query
            self.monitor.log_query(
                query, params, execution_time, len(results) if results else 0
            )

            return profile_result

        finally:
            try:
                db.execute_query("SET profiling = 0")
            except Exception:
                pass
            db.disconnect()

    def _get_optimization_suggestions(
        self, query: str, execution_time: float, explain_plan: List
    ) -> List[str]:
        """Generate optimization suggestions based on query analysis."""
        suggestions = []

        if execution_time > 1.0:
            suggestions.append(
                "Query execution time is slow (>1s). Consider optimization."
            )

        # Analyze EXPLAIN plan
        for row in explain_plan:
            try:
                if isinstance(row, dict):
                    # Handle dictionary format from MySQL connector
                    select_type = row.get("select_type", "")
                    key = row.get("key")
                    rows_examined = row.get("rows", 0)
                elif isinstance(row, (list, tuple)) and len(row) >= 5:
                    # Handle tuple/list format
                    select_type = str(row[1]) if len(row) > 1 else ""
                    key = row[5] if len(row) > 5 else None
                    rows_examined = row[8] if len(row) > 8 else 0
                else:
                    continue

                if key is None:
                    suggestions.append(
                        "No index is being used. Consider adding appropriate indexes."
                    )

                if isinstance(rows_examined, (int, str)) and int(rows_examined) > 10000:
                    suggestions.append(
                        f"Large number of rows examined ({rows_examined}). "
                        "Consider adding WHERE clauses or indexes."
                    )

                if "DEPENDENT SUBQUERY" in str(select_type):
                    suggestions.append(
                        "Dependent subquery detected. Consider rewriting as JOIN."
                    )
            except (KeyError, ValueError, TypeError, IndexError):
                continue

        # Query pattern analysis
        query_upper = query.upper()
        if "SELECT *" in query_upper:
            suggestions.append("Avoid SELECT *. Specify only needed columns.")

        if "ORDER BY" in query_upper and "LIMIT" not in query_upper:
            suggestions.append(
                "ORDER BY without LIMIT can be expensive. Consider adding LIMIT."
            )

        if query_upper.count("JOIN") > 3:
            suggestions.append(
                "Multiple JOINs detected. Verify all joins are necessary "
                "and properly indexed."
            )

        return suggestions


def main():
    """Example usage of the monitoring system."""
    # Create monitor
    monitor = DatabaseMonitor()

    # Start monitoring
    print("🔍 Starting database monitoring...")
    monitor.start_monitoring(interval=30)  # Monitor every 30 seconds

    try:
        # Let it run for a bit
        time.sleep(60)

        # Get a performance report
        report = monitor.get_performance_report(hours=1)
        print("\n📊 Performance Report:")
        print(json.dumps(report, indent=2))

        # Example query profiling
        profiler = QueryProfiler(monitor)

        # Profile a sample query
        profile = profiler.profile_query(
            """
            SELECT c.first_name, c.last_name, COUNT(o.order_id) as order_count, 
                   SUM(o.total_amount) as total_spent
            FROM customers c
            LEFT JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name
            ORDER BY total_spent DESC
            LIMIT 10
        """
        )

        print("\n🔍 Query Profile:")
        print(f"Execution time: {profile['execution_time']:.3f}s")
        print(f"Rows returned: {profile['rows_returned']}")
        print("\nOptimization suggestions:")
        for suggestion in profile["optimization_suggestions"]:
            print(f"  • {suggestion}")

    except KeyboardInterrupt:
        print("\n🛑 Stopping monitoring...")
    finally:
        monitor.stop_monitoring()


if __name__ == "__main__":
    main()
