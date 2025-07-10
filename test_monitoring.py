#!/usr/bin/env python3
"""
Test script for database monitoring system.
"""

import json
import time
from monitoring.database_monitor import DatabaseMonitor, QueryProfiler


def test_monitoring():
    """Test the monitoring system functionality."""
    print("🔍 Testing database monitoring system...")
    
    # Create monitor
    monitor = DatabaseMonitor()
    
    # Test metrics collection
    print("\n📊 Testing metrics collection...")
    metrics = monitor.get_database_metrics()
    print(f"✅ Database status: {metrics['database'].get('status', 'unknown')}")
    print(f"✅ Database uptime: {metrics['database'].get('uptime', 0)} seconds")
    print(f"✅ System CPU: {metrics['system'].get('cpu_percent', 'N/A')}%")
    print(f"✅ System Memory: {metrics['system'].get('memory_percent', 'N/A')}%")
    
    # Test query profiler
    print("\n🔍 Testing query profiler...")
    profiler = QueryProfiler(monitor)
    
    # Profile simple query
    profile = profiler.profile_query("SELECT COUNT(*) as total_customers FROM customers")
    print(f"✅ Query execution time: {profile['execution_time']:.3f}s")
    print(f"✅ Rows returned: {profile['rows_returned']}")
    print(f"✅ Optimization suggestions: {len(profile['optimization_suggestions'])}")
    
    for i, suggestion in enumerate(profile['optimization_suggestions'], 1):
        print(f"   {i}. {suggestion}")
    
    # Test monitoring loop briefly
    print("\n⏰ Testing monitoring loop...")
    monitor_thread = monitor.start_monitoring(interval=2)
    
    # Let it run for a few iterations
    time.sleep(6)
    
    # Stop monitoring
    monitor.stop_monitoring()
    
    # Get performance report
    print("\n📈 Testing performance report...")
    report = monitor.get_performance_report(hours=1)
    if 'error' not in report:
        print(f"✅ Report generated with {report['metrics_count']} metrics")
        if report['metrics_count'] > 0:
            print(f"✅ Average CPU: {report['system']['cpu']['avg']:.1f}%")
            print(f"✅ Average Memory: {report['system']['memory']['avg']:.1f}%")
    else:
        print(f"ℹ️  {report['error']}")
    
    print("\n🎉 Monitoring system test completed successfully!")


if __name__ == "__main__":
    test_monitoring()
