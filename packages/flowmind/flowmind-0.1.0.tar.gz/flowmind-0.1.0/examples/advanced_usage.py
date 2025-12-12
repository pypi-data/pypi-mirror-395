"""Advanced usage examples for FlowMind."""

from flowmind import FlowAgent
import json
import time

def example_1_ml_pipeline():
    """Example 1: Machine Learning Pipeline."""
    print("=== Example 1: ML Pipeline ===")
    
    agent = FlowAgent("ml_workflow")
    
    # Simulate dataset
    dataset = [
        {"feature1": 1.0, "feature2": 2.0, "price": 100},
        {"feature1": 2.0, "feature2": 3.0, "price": 150},
        {"feature1": 3.0, "feature2": 4.0, "price": 200},
    ]
    
    agent.get_context().set("training_data", dataset)
    
    # Train model
    agent.add_task("ml",
        operation="train",
        model="random_forest",
        data="${training_data}",
        target="price",
        name="train"
    )
    
    # Evaluate
    agent.add_task("ml",
        operation="evaluate",
        model="${train.model}",
        data="${training_data}",
        name="evaluate"
    )
    
    results = agent.run()
    print(f"✅ ML Pipeline: {results[0].output}")
    print()


def example_2_web_scraping_pipeline():
    """Example 2: Web Scraping + Data Processing."""
    print("=== Example 2: Web Scraping Pipeline ===")
    
    agent = FlowAgent("web_scraper")
    
    # Fetch data
    agent.add_task("web",
        operation="get",
        url="https://jsonplaceholder.typicode.com/users",
        parse_json=True,
        name="fetch"
    )
    
    # Filter results
    agent.add_task("data",
        operation="filter",
        input="${fetch.content}",
        condition="id < 5",
        name="filter"
    )
    
    # Save to file
    agent.add_task("file",
        operation="write",
        file_path="users.json",
        content="${filter.output}",
        as_json=True,
        name="save"
    )
    
    results = agent.run()
    print(f"✅ Scraped and processed {len(results)} steps")
    print()


def example_3_email_automation():
    """Example 3: Email Classification and Alerts."""
    print("=== Example 3: Email Automation ===")
    
    agent = FlowAgent("email_processor")
    
    # Sample emails
    emails = [
        "URGENT: Server is down! Please check ASAP.",
        "Click here to win a prize!",
        "Meeting tomorrow at 2 PM.",
    ]
    
    for i, email in enumerate(emails):
        agent.get_context().set(f"email_{i}", email)
        
        # Classify email
        agent.add_task("email",
            operation="classify",
            content=f"${{email_{i}}}",
            categories=["urgent", "spam", "normal"],
            name=f"classify_{i}"
        )
        
        # Send alert if urgent
        agent.add_task("email",
            operation="send",
            to="admin@example.com",
            subject="Urgent Email Alert",
            body=f"${{email_{i}}}",
            if_condition=f"${{classify_{i}.category}} == 'urgent'",
            name=f"alert_{i}"
        )
    
    results = agent.run()
    print(f"✅ Processed {len(emails)} emails")
    print()


def example_4_file_processing_workflow():
    """Example 4: Batch File Processing."""
    print("=== Example 4: Batch File Processing ===")
    
    agent = FlowAgent("file_batch")
    
    # List files
    agent.add_task("file",
        operation="list",
        directory=".",
        pattern="*.py",
        name="list"
    )
    
    # Count files
    agent.add_task("data",
        operation="aggregate",
        input="${list.output}",
        agg_type="count",
        name="count"
    )
    
    results = agent.run()
    print(f"✅ Found files: {results[0].output}")
    print(f"✅ Total count: {results[1].output}")
    print()


def example_5_complex_workflow():
    """Example 5: Complex Multi-Step Workflow."""
    print("=== Example 5: Complex Workflow ===")
    
    agent = FlowAgent("complex_workflow", verbose=True)
    
    # Step 1: Fetch API data
    agent.add_task("web",
        operation="get",
        url="https://jsonplaceholder.typicode.com/posts/1",
        name="fetch_api"
    )
    
    # Step 2: Transform data
    agent.add_task("data",
        operation="transform",
        input="${fetch_api.content}",
        transform="to_json",
        name="transform"
    )
    
    # Step 3: Save to file
    agent.add_task("file",
        operation="write",
        file_path="api_result.json",
        content="${transform.output}",
        name="save_file"
    )
    
    # Step 4: Verify file exists
    agent.add_task("file",
        operation="exists",
        file_path="api_result.json",
        name="verify"
    )
    
    # Step 5: Send success notification
    agent.add_task("email",
        operation="send",
        to="admin@example.com",
        subject="Workflow Complete",
        body="Data successfully fetched and saved",
        if_condition="${verify.exists} == True",
        name="notify"
    )
    
    results = agent.run()
    
    success_count = sum(1 for r in results if r.is_success())
    print(f"✅ Workflow completed: {success_count}/{len(results)} tasks succeeded")
    print()


def example_6_custom_plugin():
    """Example 6: Custom Plugin Task."""
    print("=== Example 6: Custom Plugin ===")
    
    from flowmind import BaseTask, TaskResult, TaskStatus, register_task
    
    # Define custom task
    @register_task("reverse_string")
    class ReverseStringTask(BaseTask):
        def execute(self, context):
            text = context.resolve_variables(self.config.get("text", ""))
            reversed_text = text[::-1]
            return TaskResult(
                status=TaskStatus.SUCCESS,
                output=reversed_text
            )
    
    # Use custom task
    agent = FlowAgent("custom_workflow")
    agent.get_context().set("my_text", "Hello FlowMind!")
    
    agent.add_task("reverse_string",
        text="${my_text}",
        name="reverse"
    )
    
    results = agent.run()
    print(f"✅ Reversed: {results[0].output}")
    print()


if __name__ == "__main__":
    print("🚀 FlowMind - Advanced Usage Examples\n")
    
    # Run examples
    example_1_ml_pipeline()
    example_2_web_scraping_pipeline()
    example_3_email_automation()
    example_4_file_processing_workflow()
    example_5_complex_workflow()
    example_6_custom_plugin()
    
    print("✅ All advanced examples completed!")
