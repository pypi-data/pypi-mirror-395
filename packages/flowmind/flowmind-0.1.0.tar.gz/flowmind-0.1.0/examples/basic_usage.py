"""Basic usage examples for FlowMind."""

from flowmind import FlowAgent

def example_1_simple_file_operations():
    """Example 1: Simple file read and write."""
    print("=== Example 1: File Operations ===")
    
    agent = FlowAgent("file_processor")
    
    # Read file
    agent.add_task("file",
        operation="read",
        file_path="data.txt",
        name="read"
    )
    
    # Write to new file
    agent.add_task("file",
        operation="write",
        file_path="output.txt",
        content="${read.output}",
        name="write"
    )
    
    results = agent.run()
    print(f"✅ Completed {len(results)} tasks\n")


def example_2_web_request():
    """Example 2: HTTP GET request."""
    print("=== Example 2: Web Request ===")
    
    agent = FlowAgent("api_client")
    
    # Fetch data from API
    agent.add_task("web",
        operation="get",
        url="https://jsonplaceholder.typicode.com/posts/1",
        name="fetch"
    )
    
    results = agent.run()
    if results[0].is_success():
        print(f"✅ API Response: {results[0].output}")
    print()


def example_3_data_transformation():
    """Example 3: Data filtering and transformation."""
    print("=== Example 3: Data Transformation ===")
    
    # Create sample data
    sample_data = [
        {"name": "Alice", "age": 30, "salary": 50000},
        {"name": "Bob", "age": 25, "salary": 40000},
        {"name": "Charlie", "age": 35, "salary": 60000},
    ]
    
    agent = FlowAgent("data_processor")
    
    # Store data in context
    agent.get_context().set("data", sample_data)
    
    # Filter data
    agent.add_task("data",
        operation="filter",
        input="${data}",
        condition="salary > 45000",
        name="filter"
    )
    
    # Aggregate
    agent.add_task("data",
        operation="aggregate",
        input="${filter.output}",
        agg_type="count",
        name="count"
    )
    
    results = agent.run()
    print(f"✅ Filtered results: {results[0].output}")
    print(f"✅ Count: {results[1].output}\n")


def example_4_conditional_execution():
    """Example 4: Conditional task execution."""
    print("=== Example 4: Conditional Execution ===")
    
    agent = FlowAgent("conditional_workflow")
    
    # Set a value in context
    agent.get_context().set("check_value", 150)
    
    # This task will execute (condition met)
    agent.add_task("shell",
        command="echo 'Value is high'",
        if_condition="${check_value} > 100",
        name="high_alert"
    )
    
    # This task will be skipped (condition not met)
    agent.add_task("shell",
        command="echo 'Value is low'",
        if_condition="${check_value} < 100",
        name="low_alert"
    )
    
    results = agent.run()
    for result in results:
        print(f"Task status: {result.status.value}")
    print()


def example_5_scheduled_task():
    """Example 5: Scheduled periodic execution."""
    print("=== Example 5: Scheduled Task ===")
    print("Note: This would run indefinitely. Commented out for demo.")
    print("""
    agent = FlowAgent("scheduled_job")
    
    agent.add_task("shell", 
        command="python backup.py",
        name="backup"
    )
    
    agent.schedule(every="5m")  # Run every 5 minutes
    agent.start()
    # agent.stop()  # Stop when done
    """)
    print()


if __name__ == "__main__":
    print("🚀 FlowMind - Basic Usage Examples\n")
    
    # Run examples
    # example_1_simple_file_operations()
    example_2_web_request()
    example_3_data_transformation()
    example_4_conditional_execution()
    example_5_scheduled_task()
    
    print("✅ All examples completed!")
