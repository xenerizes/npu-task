class Table(object):
    def __init__(self, table_data):
        self.keylen = int(table_data["key_length"])
        self.reslen = int(table_data["res_length"])
        self.records = dict()
        for k, v in table_data["records"].items():
            key = bytes.fromhex(k)
            value = bytes.fromhex(v)
            self.records[key] = [b for b in value]
