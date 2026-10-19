# JARVIS Database Schema

## Tables

### conversations

Stores all conversation history.

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key, auto-increment |
| timestamp | TEXT | ISO format timestamp |
| user_message | TEXT | User's command/question |
| assistant_response | TEXT | JARVIS's response |
| metadata | TEXT | JSON metadata (optional) |

**Indexes:**
- `idx_timestamp` (DESC) - For recent conversations
- `idx_user_message` - For searching by user message

### settings (v2+)

Stores configuration settings.

| Column | Type | Description |
|--------|------|-------------|
| key | TEXT | Setting name (primary key) |
| value | TEXT | Setting value |
| updated_at | TEXT | Last update timestamp |

### db_version (migration)

Tracks database schema version.

| Column | Type | Description |
|--------|------|-------------|
| version | INTEGER | Schema version number |
| migrated_at | TEXT | Migration timestamp |
| description | TEXT | Migration description |

## Example Queries

### Get recent conversations

```sql
SELECT * FROM conversations 
ORDER BY timestamp DESC 
LIMIT 10;