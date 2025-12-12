import os
import hashlib
from collections import Counter, defaultdict

class DirectoryAnalyzer:
    def __init__(self, path):
        self.path = path
        self.files_count = 0
        self.dirs_count = 0
        self.ext_stats = Counter()

        self.file_sizes = []

        self.duplicates = defaultdict(list)


    def analyze_directory(self):

        for root, dirs, files in os.walk(self.path):
            self.dirs_count += len(dirs)

            for file in files:
                file_path = os.path.join(root, file)

                try:
                    size = os.path.getsize(file_path)
                    self.files_count += 1
                    ext = os.path.splitext(file)[1].lower()
                    self.ext_stats[ext] += size
                    self.file_sizes.append((file_path, size))

                    file_hash = self._get_file_hash(file_path)
                    self.duplicates[file_hash].append(file_path)

                except (OSError, PermissionError):
                    continue

    def _get_file_hash(self, file_path, chunk_size=4096):
        hasher = hashlib.md5()

        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(chunk_size), b''):
                hasher.update(chunk)

        return hasher.hexdigest()


    def get_top_files(self, n=10):
        return sorted(self.file_sizes, key=lambda x: x[1], reverse=True)[:n]


    def find_duplicates(self):
        return {h: files for h, files in self.duplicates.items() if len(files) > 1}


    def generate_report(self):
        report = []

        report.append(f"Файлів: {self.files_count}, Папок: {self.dirs_count}")
        report.append("Розподіл за розширеннями: ")

        for ext, size in sorted(self.ext_stats.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  {ext}: {size}")

        report.append("\nТоп-10 найбільших файлів:")

        for path, size in self.get_top_files():
            report.append(f"  {size} байт: {path}")

        dups = self.find_duplicates()

        if dups:
            report.append("\nДублікати:")

            for hash_val, paths in dups.items():
                report.append(f"  Група: {paths}")

        else:
            report.append("\nДублікатів не знайдено.")

        return "\n".join(report)

