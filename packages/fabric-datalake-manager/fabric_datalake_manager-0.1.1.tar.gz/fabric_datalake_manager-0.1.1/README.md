

This section describes how to define and register the **Teachers Schema** in the Schema Registry.

## 📚 Define the Teachers Schema

```python
class TeachersSchema(BaseSchema):
    columns = [
        DataclassField("teacher_id", StringType(), False),
        DataclassField("teacher_name", StringType(), False),
    ]
```

## 📝 Register the Schema

```python
SchemaRegistry.register("teachers", TeachersSchema)
```

## 🔍 Retrieve the Teachers Schema

```python
schema = SchemaRegistry.get_schema_for_table("teachers")
print(schema)
```

---
