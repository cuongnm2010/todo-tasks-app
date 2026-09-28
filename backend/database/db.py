import psycopg2

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME="mydatabase"
DB_USER="postgres"
DB_PASSWORD="mypassword"

def get_connect():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def get_task_by_id(task_id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('SELECT task_id, task_name, task_complete FROM tasks WHERE task_id = %s;', (task_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return {'task_id': row[0], 'task_name': row[1], 'task_complete': row[2]}

def insert_task(task_name):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute("SELECT MAX(task_id) FROM tasks")
    max_id = cur.fetchone()[0]
    next_id = (max_id or 0) + 1
    cur.execute("INSERT INTO tasks (task_id, task_name, task_complete) VALUE (%s, %s, %s)",
                (next_id, task_name, False)            
    )
    conn.commit()
    cur.close()
    conn.close()

    return {
        'task_id': next_id, 
        'task_name': task_name, 
        'task_complete': False
    }

def delete_task(task_id):
    conn = get_connect()
    cur = conn.cursor()
    # cur.execute('SELECT EXISTS(SELECT 1 FROM tasks WHERE task_id = %s)',
    #             (task_id)
    # )
    # exist = cur.fetchone()[0] is not None
    # if not exist:
    #     return None
    cur.execute('DELETE FROM tasks WHERE task_id = %s RETURNING *', (task_id))
    conn.commit()

    rowcount = cur.rowcount
    cur.close()
    conn.close()
    if rowcount == 0:
        return None
    return {
            'task_id': cur.fetchone()[0], 
            'task_name': cur.fetchone()[1], 
            'task_complete': cur.fetchone()[2]
        }

def update_task_complete(task_id):

    existing = get_task_by_id()
    if not existing:
        return None
    
    conn = get_connect()
    cur = conn.cursor()
    task_complete = False if existing['task_complete'] else True
    cur.execute('UPDATE task SET task_complete = %s WHERE task_id = %s RETURNING task_id, task_complete;', (task_complete, task_id))
    
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return {'task_id': row[0], 'task_complete': row[1]}

def get_all_tasks():
    conn = get_connect()
    cur = conn.cursor()

    cur.execute('SELECT task_id, task_name, task_complete FROM tasks ORDER BY task_id;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{'task_id': r[0], 'task_name': r[1], 'task_complete': r[2]} for r in rows]