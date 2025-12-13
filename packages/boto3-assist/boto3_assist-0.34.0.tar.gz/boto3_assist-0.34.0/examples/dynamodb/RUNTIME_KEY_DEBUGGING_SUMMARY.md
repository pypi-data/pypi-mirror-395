# Runtime Key Debugging - Summary

## What Was Added

Added an optional `index` parameter to `DynamoDBIndex.extract_key_values()` to include the index name in the debug results.

## Quick Usage

```python
from boto3_assist.dynamodb.dynamodb_index import DynamoDBIndex

# Get your index and build the query key
index = model.indexes.get("gsi1")
key_expression = index.key(query_key=True, condition="begins_with")

# Extract key values WITH index name
debug = DynamoDBIndex.extract_key_values(key_expression, index)
print(debug['index_name'])  # 'gsi1'
print(debug['partition_key']['value'])
print(debug['sort_key']['value'])
```

## Three Options for Including Index Name

### Option 1: Pass the DynamoDBIndex object (Recommended)
```python
index = model.indexes.get("gsi1")
key_expr = index.key(query_key=True)
debug = DynamoDBIndex.extract_key_values(key_expr, index)
# debug['index_name'] = 'gsi1'
```

### Option 2: Pass just the index name as a string
```python
key_expr = index.key(query_key=True)
debug = DynamoDBIndex.extract_key_values(key_expr, "gsi1")
# debug['index_name'] = 'gsi1'
```

### Option 3: Don't pass anything (backward compatible)
```python
key_expr = index.key(query_key=True)
debug = DynamoDBIndex.extract_key_values(key_expr)
# debug.get('index_name') = None
```

## Example Output

**With index parameter:**
```json
{
  "index_name": "gsi1",
  "partition_key": {
    "attribute": "gsi1_pk",
    "value": "inbox#support#status#open"
  },
  "sort_key": {
    "attribute": "gsi1_sk",
    "value": "priority#medium#ts",
    "operator": "begins_with",
    "format": "{operator}({0}, {1})"
  }
}
```

**Without index parameter:**
```json
{
  "partition_key": {
    "attribute": "gsi1_pk",
    "value": "inbox#support#status#open"
  },
  "sort_key": {
    "attribute": "gsi1_sk",
    "value": "priority#medium#ts",
    "operator": "begins_with",
    "format": "{operator}({0}, {1})"
  }
}
```

## Practical Example: Service Logging

```python
def query_tickets_by_status(category: str, status: str):
    ticket = SupportTicket()
    ticket.category = category
    ticket.status = status
    
    index = ticket.indexes.get("gsi1")
    key_expr = index.key(query_key=True, condition="begins_with")
    
    # Debug with index name included
    debug = DynamoDBIndex.extract_key_values(key_expr, index)
    
    logger.info(f"Querying {debug['index_name']}")
    logger.info(f"  PK: {debug['partition_key']['value']}")
    logger.info(f"  SK: {debug['sort_key']['value']}")
    logger.info(f"  Condition: {debug['sort_key']['operator']}")
    
    return db.query(table_name="tickets", index_name=debug['index_name'], key=key_expr)
```

Output:
```
INFO: Querying gsi1
INFO:   PK: inbox#support#status#open
INFO:   SK: priority#medium#ts
INFO:   Condition: begins_with
```

## Benefits

✅ **No string hardcoding** - Extract index name from the object  
✅ **Better logging** - See which index is being queried  
✅ **Backward compatible** - Index parameter is optional  
✅ **Flexible** - Pass DynamoDBIndex object or string  
✅ **Complete context** - All query info in one debug object

## Files Updated

1. **`src/boto3_assist/dynamodb/dynamodb_index.py`**
   - Added optional `index` parameter to `extract_key_values()`
   - Accepts `str | DynamoDBIndex | None`

2. **`examples/dynamodb/runtime_key_debugging_example.py`**
   - Updated all examples to show index parameter usage
   - Added new example: `example_including_index_name()`

3. **`examples/dynamodb/QUICK_REFERENCE_KEY_DEBUGGING.md`**
   - Updated documentation with index parameter examples
   - Updated output format examples

## See Also

- Full examples: `examples/dynamodb/runtime_key_debugging_example.py`
- Quick reference: `examples/dynamodb/QUICK_REFERENCE_KEY_DEBUGGING.md`
- Earlier debugging examples: `examples/dynamodb/debug_keys_example.py`
