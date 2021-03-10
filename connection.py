from mongoengine import connect


class Connection:
    def __enter__(self):
        self.conn = connect(db="items", host="mongodb")
        print("Connected to mongodb")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()