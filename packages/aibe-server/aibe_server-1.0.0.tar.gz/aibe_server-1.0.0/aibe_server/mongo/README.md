# MongoDB Utilities

This directory contains MongoDB utilities and example queries for working with AIBE Story data.

## Utilities

### drop-databases.js

Drops all AIBE-related MongoDB databases as configured in `~/.AIBE/config.json`.

```bash
cd server/aibe_server/mongo
node drop-databases.js
```

**Warning:** This permanently deletes all data in the configured databases (AIBE, test_streams, server_streams).

## Example Queries

The `examples/` directory contains ready-to-run query files for exploring Story data:

| File | Description |
|------|-------------|
| `basic-queries.js` | Simple queries: find by date, domain, count documents |
| `element-interactions.js` | Extract user interactions with form fields, buttons |
| `pattern-analysis.js` | Analyze navigation patterns, form completion, session flows |
| `projections.js` | Efficient queries using projections to reduce data size |
| `nodejs-driver.js` | Programmatic access examples using MongoDB Node.js driver |

### Running Examples

**In mongosh (interactive):**
```bash
mongosh
load("examples/basic-queries.js")
```

**With Node.js driver:**
```bash
npm install mongodb  # if not already installed
node examples/nodejs-driver.js
```

### Prerequisites

1. MongoDB running on `localhost:27017`
2. AIBE database with Story data (run the test suite to generate sample data)

See the MongoDB Appendix in the main documentation for installation and configuration details.
