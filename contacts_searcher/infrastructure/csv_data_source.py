import csv


class CSVDataSource:
    def __init__(self, path: str):
        self.__path = path

    def get_collection(self, name: str):
        return CSVCollection(name, self.__path)


class CSVCollection:
    def __init__(self, name, path):
        self.__name = name
        self.__path = path

    def insert_one(self, document):
        pass

    def find_one(self):
        return next(self.find(), None)

    def find(self):
        with open(self.__path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row:
                    continue

                yield row

    @property
    def name(self):
        return self.__name
