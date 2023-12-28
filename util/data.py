import shutil
import pickle


class Data:
    """Working with data file"""
    def __init__(self, file1, file2, directory):
        self.file1 = file1
        self.file2 = file2
        self.directory = directory

    def start_work(self):
        shutil.move(self.file1, self.file2)
        shutil.unpack_archive(self.file2, self.directory)
        shutil.move(self.file2, self.file1)

    def end_work(self):
        shutil.rmtree(self.directory)


class TextBinary:
    """Saving data as a binary file and loading data from binary file"""
    def __init__(self, data, file):
        self.data = data
        self.file = file

    def save_data(self):
        with open(self.file, "wb") as f:
            pickle.dump(self.data, f)

    def load_data(self):
        with open(self.file, "rb") as f:
            self.data = pickle.load(f)
            return self.data
