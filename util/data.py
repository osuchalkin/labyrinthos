import shutil


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
