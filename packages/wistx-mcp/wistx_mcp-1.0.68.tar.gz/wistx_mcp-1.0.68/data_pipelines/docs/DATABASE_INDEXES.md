# Database Index Optimization Guide

This document outlines recommended MongoDB indexes for optimal query performance in the data processing pipeline.

## Overview

Proper indexing is critical for:
- **Change Detection:** Fast hash lookups
- **Batch Operations:** Efficient `$in` queries
- **Standard Filtering:** Quick standard/version queries
- **General Queries:** Fast document retrieval

## Recommended Indexes

### Compliance Controls Collection (`compliance_controls`)

```javascript
// Primary unique index on control_id (required)
db.compliance_controls.createIndex(
    { control_id: 1 },
    { unique: true, name: "control_id_unique" }
)

// Index for standard and version filtering
db.compliance_controls.createIndex(
    { standard: 1, version: 1 },
    { name: "standard_version" }
)

// Index for source hash lookups (change detection)
db.compliance_controls.createIndex(
    { source_hash: 1 },
    { name: "source_hash" }
)

// Index for content hash lookups (change detection)
db.compliance_controls.createIndex(
    { content_hash: 1 },
    { name: "content_hash" }
)

// Compound index for batch queries (control_id lookups)
db.compliance_controls.createIndex(
    { control_id: 1, source_hash: 1, content_hash: 1 },
    { name: "control_id_hashes" }
)
```

### Pricing Data Collection (`pricing_data`)

```javascript
// Primary unique index on lookup_key (required)
db.pricing_data.createIndex(
    { lookup_key: 1 },
    { unique: true, name: "lookup_key_unique" }
)

// Index for cloud provider filtering
db.pricing_data.createIndex(
    { cloud: 1, service: 1 },
    { name: "cloud_service" }
)

// Index for region filtering
db.pricing_data.createIndex(
    { region: 1 },
    { name: "region" }
)
```

### Code Examples Collection (`code_examples`)

```javascript
// Primary unique index on example_id (required)
db.code_examples.createIndex(
    { example_id: 1 },
    { unique: true, name: "example_id_unique" }
)

// Index for cloud provider filtering
db.code_examples.createIndex(
    { cloud_provider: 1 },
    { name: "cloud_provider" }
)

// Index for code type filtering
db.code_examples.createIndex(
    { code_type: 1 },
    { name: "code_type" }
)
```

### Best Practices Collection (`best_practices`)

```javascript
// Primary unique index on practice_id (required)
db.best_practices.createIndex(
    { practice_id: 1 },
    { unique: true, name: "practice_id_unique" }
)

// Index for category filtering
db.best_practices.createIndex(
    { category: 1 },
    { name: "category" }
)
```

### Knowledge Articles Collection (`knowledge_articles`)

```javascript
// Primary unique index on article_id (required)
db.knowledge_articles.createIndex(
    { article_id: 1 },
    { unique: true, name: "article_id_unique" }
)

// Index for domain filtering
db.knowledge_articles.createIndex(
    { domain: 1, subdomain: 1 },
    { name: "domain_subdomain" }
)

// Index for content type filtering
db.knowledge_articles.createIndex(
    { content_type: 1 },
    { name: "content_type" }
)

// Index for user/organization filtering
db.knowledge_articles.createIndex(
    { user_id: 1, organization_id: 1 },
    { name: "user_org" }
)
```

## Index Creation Script

Create a script to set up all indexes:

```python
"""Setup MongoDB indexes for optimal query performance."""

from api.database.mongodb import mongodb_manager

def setup_indexes():
    """Create all recommended indexes."""
    mongodb_manager.connect()
    db = mongodb_manager.get_database()
    
    # Compliance Controls
    db.compliance_controls.create_index(
        [("control_id", 1)], unique=True, name="control_id_unique"
    )
    db.compliance_controls.create_index(
        [("standard", 1), ("version", 1)], name="standard_version"
    )
    db.compliance_controls.create_index(
        [("source_hash", 1)], name="source_hash"
    )
    db.compliance_controls.create_index(
        [("content_hash", 1)], name="content_hash"
    )
    db.compliance_controls.create_index(
        [("control_id", 1), ("source_hash", 1), ("content_hash", 1)],
        name="control_id_hashes"
    )
    
    # Pricing Data
    db.pricing_data.create_index(
        [("lookup_key", 1)], unique=True, name="lookup_key_unique"
    )
    db.pricing_data.create_index(
        [("cloud", 1), ("service", 1)], name="cloud_service"
    )
    db.pricing_data.create_index(
        [("region", 1)], name="region"
    )
    
    # Code Examples
    db.code_examples.create_index(
        [("example_id", 1)], unique=True, name="example_id_unique"
    )
    db.code_examples.create_index(
        [("cloud_provider", 1)], name="cloud_provider"
    )
    db.code_examples.create_index(
        [("code_type", 1)], name="code_type"
    )
    
    # Best Practices
    db.best_practices.create_index(
        [("practice_id", 1)], unique=True, name="practice_id_unique"
    )
    db.best_practices.create_index(
        [("category", 1)], name="category"
    )
    
    # Knowledge Articles
    db.knowledge_articles.create_index(
        [("article_id", 1)], unique=True, name="article_id_unique"
    )
    db.knowledge_articles.create_index(
        [("domain", 1), ("subdomain", 1)], name="domain_subdomain"
    )
    db.knowledge_articles.create_index(
        [("content_type", 1)], name="content_type"
    )
    db.knowledge_articles.create_index(
        [("user_id", 1), ("organization_id", 1)], name="user_org"
    )
    
    print("All indexes created successfully!")

if __name__ == "__main__":
    setup_indexes()
```

## Performance Impact

### Expected Improvements

| Query Type | Without Index | With Index | Improvement |
|------------|--------------|------------|-------------|
| `control_id` lookup | Full scan (O(n)) | Index lookup (O(log n)) | **100-1000x** |
| `$in` batch query | Multiple scans | Index lookup | **10-100x** |
| `source_hash` lookup | Full scan | Index lookup | **100-1000x** |
| Standard filtering | Full scan | Index scan | **10-50x** |

### Query Examples

**Change Detection (Batch Check):**
```python
# Uses control_id_hashes index
collection.find(
    {"control_id": {"$in": control_ids}},
    {"control_id": 1, "source_hash": 1, "content_hash": 1}
)
```

**Standard Filtering:**
```python
# Uses standard_version index
collection.find({"standard": "PCI-DSS", "version": "4.0"})
```

## Monitoring Index Usage

Check index usage statistics:

```javascript
// Get index usage stats
db.compliance_controls.aggregate([
    { $indexStats: {} }
])

// Check query execution plans
db.compliance_controls.find({control_id: "test"}).explain("executionStats")
```

## Maintenance

### Index Size

Monitor index sizes:
```javascript
db.compliance_controls.stats().indexSizes
```

### Rebuilding Indexes

If needed, rebuild indexes:
```javascript
db.compliance_controls.reIndex()
```

## Best Practices

1. **Create indexes before loading data** - Faster than creating after
2. **Monitor index usage** - Remove unused indexes
3. **Balance read/write performance** - More indexes = slower writes
4. **Use compound indexes** - For multi-field queries
5. **Keep indexes small** - Only index fields used in queries

## Notes

- Indexes use disk space (~10-20% of collection size)
- Indexes slow down writes slightly (~5-10%)
- Indexes dramatically speed up reads (10-1000x)
- For this pipeline, **reads are more frequent than writes**, so indexes are beneficial

