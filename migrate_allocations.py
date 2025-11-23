import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'instance', 'events.db')
if not os.path.exists(DB_PATH):
    print('Database file not found at', DB_PATH)
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
print('Disabling foreign keys')
cur.execute('PRAGMA foreign_keys = OFF;')
conn.commit()

print('Creating new temporary table')
cur.execute('''
CREATE TABLE IF NOT EXISTS EventResourceAllocation_new (
    allocation_id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL,
    resource_id INTEGER,
    resource_name_backup VARCHAR(150),
    resource_type_backup VARCHAR(80),
    FOREIGN KEY(event_id) REFERENCES event(event_id),
    FOREIGN KEY(resource_id) REFERENCES resource(resource_id)
);
''')
conn.commit()

print('Copying data from old table (resource_name/type backups will be NULL)')
# Only copy columns that exist in the old table; ignore backup columns
cur.execute('''
INSERT OR REPLACE INTO EventResourceAllocation_new (allocation_id, event_id, resource_id)
SELECT allocation_id, event_id, resource_id FROM EventResourceAllocation;
''')
conn.commit()

print('Dropping old table and renaming new table')
cur.execute('DROP TABLE EventResourceAllocation;')
cur.execute('ALTER TABLE EventResourceAllocation_new RENAME TO EventResourceAllocation;')
conn.commit()

print('Re-enabling foreign keys')
cur.execute('PRAGMA foreign_keys = ON;')
conn.commit()

print('Migration complete.')
conn.close()
