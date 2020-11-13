class InnRepository:
    def __init__(self, datasource):
        self.collection = datasource.get_collection('inn')

    def find_all(self):
        for inn_row in self.collection.find():
            yield inn_row.get('inn')
