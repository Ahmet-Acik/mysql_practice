#!/usr/bin/env python3
"""
Interactive CLI for MySQL Practice Project
Provides a user-friendly command-line interface for all project features.
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from config.database import test_connection


class MySQLPracticeCLI:
    """Interactive command-line interface for MySQL practice project."""

    def __init__(self):
        self.project_root = Path(__file__).parent

    def setup_database(self):
        """Setup the database schema and sample data."""
        print("🔧 Setting up database...")

        # Test connection first
        if not test_connection():
            print("❌ Database connection failed. Please check your configuration.")
            return False

        try:
            # Run schema creation
            subprocess.run(
                [sys.executable, str(self.project_root / "create_database.py")],
                check=True,
            )
            print("✅ Database setup completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Database setup failed: {e}")
            return False

    def run_examples(self, example_type: str = "all"):
        """Run example scripts."""
        examples_dir = self.project_root / "examples"
        example_files = {
            "basic": "basic_operations.py",
            "advanced": "advanced_queries.py",
            "transactions": "transactions.py",
            "procedures": "stored_procedures.py",
        }

        if example_type == "all":
            files_to_run = list(example_files.values())
        elif example_type in example_files:
            files_to_run = [example_files[example_type]]
        else:
            print(f"❌ Unknown example type: {example_type}")
            print(f"Available types: {', '.join(example_files.keys())}, all")
            return False

        print(f"🚀 Running {example_type} examples...")

        for file in files_to_run:
            file_path = examples_dir / file
            if file_path.exists():
                print(f"\n📄 Running {file}...")
                try:
                    subprocess.run([sys.executable, str(file_path)], check=True)
                    print(f"✅ {file} completed successfully!")
                except subprocess.CalledProcessError as e:
                    print(f"❌ {file} failed: {e}")
                    return False
            else:
                print(f"❌ File not found: {file}")
                return False

        print("✅ All examples completed successfully!")
        return True

    def run_exercises(self, level: str = "all"):
        """Run exercise scripts."""
        exercises_dir = self.project_root / "exercises"
        exercise_files = {
            "beginner": "beginner.py",
            "intermediate": "intermediate.py",
            "advanced": "advanced.py",
        }

        if level == "all":
            files_to_run = list(exercise_files.values())
        elif level in exercise_files:
            files_to_run = [exercise_files[level]]
        else:
            print(f"❌ Unknown exercise level: {level}")
            print(f"Available levels: {', '.join(exercise_files.keys())}, all")
            return False

        print(f"📚 Running {level} exercises...")

        for file in files_to_run:
            file_path = exercises_dir / file
            if file_path.exists():
                print(f"\n📄 Running {file}...")
                try:
                    subprocess.run([sys.executable, str(file_path)], check=True)
                    print(f"✅ {file} completed successfully!")
                except subprocess.CalledProcessError as e:
                    print(f"❌ {file} failed: {e}")
                    return False
            else:
                print(f"❌ File not found: {file}")
                return False

        print("✅ All exercises completed successfully!")
        return True

    def run_tests(self):
        """Run the test suite."""
        tests_dir = self.project_root / "tests"
        if not tests_dir.exists():
            print("❌ Tests directory not found.")
            return False

        print("🧪 Running test suite...")

        # Try pytest first
        try:
            subprocess.run(
                [sys.executable, "-m", "pytest", str(tests_dir), "-v"], check=True
            )
            print("✅ All tests passed!")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  pytest not available, falling back to unittest...")

        # Fallback to unittest
        try:
            subprocess.run(
                [sys.executable, str(tests_dir / "test_database.py")], check=True
            )
            print("✅ All tests passed!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Tests failed: {e}")
            return False

    def start_api(self):
        """Start the REST API server."""
        api_file = self.project_root / "api" / "rest_api.py"
        if not api_file.exists():
            print("❌ API file not found.")
            return False

        print("🌐 Starting REST API server...")
        print("📍 API will be available at: http://localhost:5000")
        print("📖 API documentation: http://localhost:5000/docs")
        print("Press Ctrl+C to stop the server")

        try:
            subprocess.run([sys.executable, str(api_file)], check=True)
        except KeyboardInterrupt:
            print("\n🛑 API server stopped.")
        except subprocess.CalledProcessError as e:
            print(f"❌ API server failed: {e}")
            return False

        return True

    def run_analytics(self):
        """Run advanced analytics."""
        analytics_file = self.project_root / "analytics" / "advanced_analytics.py"
        if not analytics_file.exists():
            print("❌ Analytics file not found.")
            return False

        print("📊 Running advanced analytics...")
        try:
            subprocess.run([sys.executable, str(analytics_file)], check=True)
            print("✅ Analytics completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Analytics failed: {e}")
            return False

    def generate_data(self, count: int = 1000):
        """Generate sample data."""
        data_gen_file = self.project_root / "utils" / "data_generator.py"
        if not data_gen_file.exists():
            print("❌ Data generator file not found.")
            return False

        print(f"🎲 Generating {count} sample records...")
        try:
            subprocess.run(
                [sys.executable, str(data_gen_file), "--count", str(count)], check=True
            )
            print("✅ Data generation completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Data generation failed: {e}")
            return False

    def run_performance_test(self):
        """Run performance benchmarks."""
        perf_file = self.project_root / "utils" / "performance_monitor.py"
        if not perf_file.exists():
            print("❌ Performance monitor file not found.")
            return False

        print("⚡ Running performance benchmarks...")
        try:
            subprocess.run([sys.executable, str(perf_file)], check=True)
            print("✅ Performance tests completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Performance tests failed: {e}")
            return False

    def interactive_mode(self):
        """Run in interactive mode."""
        print("🎯 MySQL Practice - Interactive Mode")
        print("=====================================")

        while True:
            print("\nAvailable commands:")
            print("1. setup     - Setup database schema and data")
            print("2. examples  - Run example scripts")
            print("3. exercises - Run exercise scripts")
            print("4. tests     - Run test suite")
            print("5. api       - Start REST API server")
            print("6. analytics - Run advanced analytics")
            print("7. generate  - Generate sample data")
            print("8. benchmark - Run performance benchmarks")
            print("9. status    - Check database connection")
            print("0. quit      - Exit interactive mode")

            choice = input("\nEnter command (0-9): ").strip()

            if choice == "0" or choice.lower() == "quit":
                print("👋 Goodbye!")
                break
            elif choice == "1" or choice.lower() == "setup":
                self.setup_database()
            elif choice == "2" or choice.lower() == "examples":
                example_type = input(
                    "Enter example type (basic/advanced/transactions/procedures/all): "
                ).strip()
                if not example_type:
                    example_type = "all"
                self.run_examples(example_type)
            elif choice == "3" or choice.lower() == "exercises":
                level = input(
                    "Enter exercise level (beginner/intermediate/advanced/all): "
                ).strip()
                if not level:
                    level = "all"
                self.run_exercises(level)
            elif choice == "4" or choice.lower() == "tests":
                self.run_tests()
            elif choice == "5" or choice.lower() == "api":
                self.start_api()
            elif choice == "6" or choice.lower() == "analytics":
                self.run_analytics()
            elif choice == "7" or choice.lower() == "generate":
                count = input(
                    "Enter number of records to generate (default: 1000): "
                ).strip()
                try:
                    count = int(count) if count else 1000
                    self.generate_data(count)
                except ValueError:
                    print("❌ Invalid number. Using default: 1000")
                    self.generate_data(1000)
            elif choice == "8" or choice.lower() == "benchmark":
                self.run_performance_test()
            elif choice == "9" or choice.lower() == "status":
                if test_connection():
                    print("✅ Database connection successful!")
                else:
                    print("❌ Database connection failed!")
            else:
                print("❌ Invalid choice. Please try again.")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MySQL Practice Project CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py                          # Interactive mode
  python cli.py setup                    # Setup database
  python cli.py examples                 # Run all examples
  python cli.py examples --type basic    # Run basic examples
  python cli.py exercises --level beginner  # Run beginner exercises
  python cli.py tests                    # Run test suite
  python cli.py api                      # Start API server
  python cli.py analytics                # Run analytics
  python cli.py generate --count 5000    # Generate 5000 records
  python cli.py benchmark                # Run performance tests
        """,
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=[
            "setup",
            "examples",
            "exercises",
            "tests",
            "api",
            "analytics",
            "generate",
            "benchmark",
            "status",
        ],
        help="Command to execute",
    )

    parser.add_argument(
        "--type",
        choices=["basic", "advanced", "transactions", "procedures", "all"],
        default="all",
        help="Type of examples to run",
    )

    parser.add_argument(
        "--level",
        choices=["beginner", "intermediate", "advanced", "all"],
        default="all",
        help="Level of exercises to run",
    )

    parser.add_argument(
        "--count", type=int, default=1000, help="Number of records to generate"
    )

    args = parser.parse_args()
    cli = MySQLPracticeCLI()

    if not args.command:
        # Interactive mode
        cli.interactive_mode()
    else:
        # Command mode
        if args.command == "setup":
            cli.setup_database()
        elif args.command == "examples":
            cli.run_examples(args.type)
        elif args.command == "exercises":
            cli.run_exercises(args.level)
        elif args.command == "tests":
            cli.run_tests()
        elif args.command == "api":
            cli.start_api()
        elif args.command == "analytics":
            cli.run_analytics()
        elif args.command == "generate":
            cli.generate_data(args.count)
        elif args.command == "benchmark":
            cli.run_performance_test()
        elif args.command == "status":
            if test_connection():
                print("✅ Database connection successful!")
            else:
                print("❌ Database connection failed!")


if __name__ == "__main__":
    main()
