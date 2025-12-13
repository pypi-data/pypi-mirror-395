"""
Example: Extract DynamoDB Key Values at Runtime

This demonstrates how to use DynamoDBIndex.extract_key_values() to debug
query keys at runtime without accessing private _values attributes.
"""

from boto3_assist.dynamodb.dynamodb_model_base import DynamoDBModelBase
from boto3_assist.dynamodb.dynamodb_index import DynamoDBIndex
from boto3_assist.dynamodb.dynamodb_key import DynamoDBKey


class SupportTicket(DynamoDBModelBase):
    """Example support ticket model"""

    def __init__(self):
        super().__init__()
        self.id: str = ""
        self.category: str = ""
        self.status: str = ""
        self.priority: str = ""
        self.timestamp: str = ""
        self.__setup_indexes()

    def __setup_indexes(self):
        """Setup indexes for querying tickets"""
        
        # Primary index
        primary = DynamoDBIndex()
        primary.partition_key.attribute_name = "pk"
        primary.partition_key.value = lambda: DynamoDBKey.build_key(
            ("ticket", self.id)
        )
        primary.sort_key.attribute_name = "sk"
        primary.sort_key.value = lambda: DynamoDBKey.build_key(
            ("ticket", self.id)
        )
        self.indexes.add_primary(primary)

        # GSI for querying by category and status
        gsi1 = DynamoDBIndex(index_name="gsi1")
        gsi1.partition_key.attribute_name = "gsi1_pk"
        gsi1.partition_key.value = lambda: DynamoDBKey.build_key(
            ("inbox", self.category),
            ("status", self.status)
        )
        gsi1.sort_key.attribute_name = "gsi1_sk"
        gsi1.sort_key.value = lambda: DynamoDBKey.build_key(
            ("priority", self.priority),
            ("ts", self.timestamp)
        )
        self.indexes.add_secondary(gsi1)


def example_old_way_accessing_private_attributes():
    """The old way: accessing private _values attributes (NOT RECOMMENDED)"""
    print("\n=== OLD WAY: Accessing Private Attributes ===")
    print("⚠️  This is fragile and may break if boto3 changes internally!\n")
    
    ticket = SupportTicket()
    ticket.category = "support"
    ticket.status = "open"
    ticket.priority = "medium"
    ticket.timestamp = ""  # Empty for begins_with
    
    # Build the query key
    key_expression = ticket.indexes.get("gsi1").key(
        query_key=True,
        condition="begins_with"
    )
    
    # OLD WAY: Accessing private attributes
    try:
        pk_value = key_expression._values[0]._values[1]
        sk_value = key_expression._values[1]._values[1]
        sk_operator = key_expression._values[1].expression_operator
        sk_format = key_expression._values[1].expression_format
        
        print(f"Partition Key Value: {pk_value}")
        print(f"Sort Key Value: {sk_value}")
        print(f"Sort Key Operator: {sk_operator}")
        print(f"Sort Key Format: {sk_format}")
    except (AttributeError, IndexError) as e:
        print(f"ERROR: {e}")
        print("This is why accessing private attributes is risky!")


def example_new_way_extract_key_values():
    """The new way: using extract_key_values() (RECOMMENDED)"""
    print("\n=== NEW WAY: Using extract_key_values() ===")
    print("✅ Clean, safe, and documented API!\n")
    
    ticket = SupportTicket()
    ticket.category = "support"
    ticket.status = "open"
    ticket.priority = "medium"
    ticket.timestamp = ""  # Empty for begins_with
    
    # Build the query key
    index = ticket.indexes.get("gsi1")
    key_expression = index.key(
        query_key=True,
        condition="begins_with"
    )
    
    # NEW WAY: Use extract_key_values() - optionally pass the index
    debug_info = DynamoDBIndex.extract_key_values(key_expression, index)
    
    print("Full debug info (with index name):")
    import json
    print(json.dumps(debug_info, indent=2))
    
    # Easy access to values
    print(f"\nIndex: {debug_info.get('index_name', 'N/A')}")
    print(f"Partition Key: {debug_info['partition_key']['attribute']} = {debug_info['partition_key']['value']}")
    print(f"Sort Key: {debug_info['sort_key']['attribute']} = {debug_info['sort_key']['value']}")
    print(f"Condition: {debug_info['sort_key']['operator']}")


def example_different_conditions():
    """Example: Debug different query conditions"""
    print("\n=== Debugging Different Conditions ===\n")
    
    ticket = SupportTicket()
    ticket.category = "billing"
    ticket.status = "pending"
    ticket.priority = "high"
    ticket.timestamp = "2024-10-01"
    
    conditions = ["begins_with", "eq", "gt", "gte"]
    
    for condition in conditions:
        key_expression = ticket.indexes.get("gsi1").key(
            query_key=True,
            condition=condition
        )
        
        debug_info = DynamoDBIndex.extract_key_values(key_expression)
        
        print(f"Condition: {condition}")
        print(f"  PK: {debug_info['partition_key']['value']}")
        print(f"  SK: {debug_info['sort_key']['value']}")
        print(f"  Operator: {debug_info['sort_key']['operator']}")
        print()


def example_between_condition():
    """Example: Debug 'between' queries with two values"""
    print("\n=== Debugging 'between' Condition ===\n")
    
    ticket = SupportTicket()
    ticket.category = "support"
    ticket.status = "open"
    ticket.priority = "medium"
    ticket.timestamp = ""
    
    key_expression = ticket.indexes.get("gsi1").key(
        query_key=True,
        condition="between",
        low_value="2024-01-01",
        high_value="2024-12-31"
    )
    
    debug_info = DynamoDBIndex.extract_key_values(key_expression)
    
    print("Between query debug info:")
    import json
    print(json.dumps(debug_info, indent=2))
    
    # Access the range values
    if 'value_low' in debug_info['sort_key']:
        print(f"\nRange: {debug_info['sort_key']['value_low']} to {debug_info['sort_key']['value_high']}")


def example_including_index_name():
    """Example: Different ways to include index name in results"""
    print("\n=== Including Index Name in Results ===\n")
    
    ticket = SupportTicket()
    ticket.category = "support"
    ticket.status = "open"
    ticket.priority = "high"
    ticket.timestamp = ""
    
    index = ticket.indexes.get("gsi1")
    key_expression = index.key(query_key=True, condition="begins_with")
    
    # Option 1: Pass the DynamoDBIndex object
    print("Option 1: Pass the DynamoDBIndex object")
    debug1 = DynamoDBIndex.extract_key_values(key_expression, index)
    print(f"  Index name: {debug1['index_name']}")
    print(f"  PK: {debug1['partition_key']['value']}")
    
    # Option 2: Pass just the index name as a string
    print("\nOption 2: Pass just the index name as a string")
    debug2 = DynamoDBIndex.extract_key_values(key_expression, "gsi1")
    print(f"  Index name: {debug2['index_name']}")
    print(f"  PK: {debug2['partition_key']['value']}")
    
    # Option 3: Don't pass anything (no index_name in results)
    print("\nOption 3: Don't pass index parameter")
    debug3 = DynamoDBIndex.extract_key_values(key_expression)
    print(f"  Index name: {debug3.get('index_name', 'Not included')}")
    print(f"  PK: {debug3['partition_key']['value']}")
    
    # Useful for logging
    print("\n✓ Use the index parameter to include it in your debug logs!")


def example_runtime_debugging_in_service():
    """Example: Use in a service method for runtime debugging"""
    print("\n=== Runtime Debugging in Service Method ===\n")
    
    def query_tickets_by_status(category: str, status: str, priority_prefix: str):
        """Simulate a service method that queries tickets"""
        
        ticket = SupportTicket()
        ticket.category = category
        ticket.status = status
        ticket.priority = priority_prefix
        ticket.timestamp = ""  # For begins_with
        
        # Build the query key
        index = ticket.indexes.get("gsi1")
        key_expression = index.key(
            query_key=True,
            condition="begins_with"
        )
        
        # Debug: Extract and log the actual key values (with index name)
        debug_info = DynamoDBIndex.extract_key_values(key_expression, index)
        
        print(f"[DEBUG] Querying {debug_info['index_name']}:")
        print(f"[DEBUG]   PK = {debug_info['partition_key']['value']}")
        print(f"[DEBUG]   SK starts with {debug_info['sort_key']['value']}")
        print(f"[DEBUG]   Condition = {debug_info['sort_key']['operator']}")
        
        # Now you can see exactly what's being queried
        # This helps troubleshoot issues like:
        # - Wrong delimiter
        # - Missing prefix
        # - Incorrect key format
        # - Wrong condition operator
        
        print("\n✓ Ready to execute query with verified key values!")
        # db.query(table_name="tickets", index_name="gsi1", key=key_expression)
    
    # Test it
    query_tickets_by_status(
        category="support",
        status="open",
        priority_prefix="high"
    )


def example_comparison_side_by_side():
    """Example: Compare old vs new approach side by side"""
    print("\n=== Side-by-Side Comparison ===\n")
    
    ticket = SupportTicket()
    ticket.category = "support"
    ticket.status = "open"
    ticket.priority = "medium"
    ticket.timestamp = ""
    
    key_expression = ticket.indexes.get("gsi1").key(
        query_key=True,
        condition="begins_with"
    )
    
    print("OLD WAY (accessing private attributes):")
    print("  key._values[0]._values[1]               # PK value")
    print("  key._values[1]._values[1]               # SK value")
    print("  key._values[1].expression_operator      # operator")
    print("  key._values[1].expression_format        # format")
    print()
    
    print("NEW WAY (using extract_key_values):")
    print("  debug = DynamoDBIndex.extract_key_values(key)")
    print("  debug['partition_key']['value']         # PK value")
    print("  debug['sort_key']['value']              # SK value")
    print("  debug['sort_key']['operator']           # operator")
    print("  debug['sort_key']['format']             # format")
    print()
    
    # Show actual values
    debug_info = DynamoDBIndex.extract_key_values(key_expression)
    print("Actual values extracted:")
    print(f"  PK: {debug_info['partition_key']['value']}")
    print(f"  SK: {debug_info['sort_key']['value']}")
    print(f"  Operator: {debug_info['sort_key']['operator']}")


def main():
    """Run all examples"""
    print("=" * 70)
    print("Runtime DynamoDB Key Debugging Examples")
    print("=" * 70)
    
    example_old_way_accessing_private_attributes()
    example_new_way_extract_key_values()
    example_different_conditions()
    example_between_condition()
    example_including_index_name()
    example_runtime_debugging_in_service()
    example_comparison_side_by_side()
    
    print("\n" + "=" * 70)
    print("Summary:")
    print("  ✅ Use: DynamoDBIndex.extract_key_values(key_expression)")
    print("  ❌ Avoid: Accessing key._values directly")
    print("  📝 Perfect for: Logging, debugging, troubleshooting queries")
    print("=" * 70)


if __name__ == "__main__":
    main()
