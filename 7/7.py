from collections import namedtuple

filename = "input.txt"

with open(filename) as f:
    content = f.read().splitlines()

file = namedtuple("file", ["name", "size"])


class Folder:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files = []
        self.children = []

    def add_file(self, name, size):
        self.files.append(file(name, int(size)))

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return [child.name for child in self.children]

    def get_sizes(self):
        """Return a list of sizes of the current folder and all its children."""
        file_size = sum([file.size for file in self.files])
        if not self.children:
            return [file_size]
        else:
            sizes = [file_size]
            for child in self.children:
                child_sizes = child.get_sizes()
                sizes[0] += child_sizes[0]
                sizes += child_sizes
            return sizes

    def print_tree(self, level=0):
        print(level * "  " + f"- {self.name} (dir)")
        for child in self.children:
            child.print_tree(level + 1)
        for file in self.files:
            print((level + 1) * "  " + f"- {file.name} (file, size={file.size})")


# Loading the filesystem
filesystem = Folder("/", parent=None)
active_folder = filesystem
# Skip the first line, as it is always the cd to root.
for line in content[1:]:
    line = line.split(" ")

    if line[0] == "$":
        if line[1] == "cd":
            if line[2] == "..":
                active_folder = active_folder.parent
            else:
                active_folder = active_folder.children[
                    active_folder.get_children().index(line[2])
                ]

    elif line[0] == "dir":
        active_folder.add_child(Folder(line[1], parent=active_folder))

    else:
        active_folder.add_file(line[1], line[0])

# Just a visual check that everything is properly loaded
filesystem.print_tree()

""" Part One """
MAX_FILE = 100000
sizes = filesystem.get_sizes()
size_sum = sum([size for size in sizes if size <= MAX_FILE])

print(f"Total size of directories, smaller than {MAX_FILE}: {size_sum}")

""" Part Two """
DISK_SPACE = 70000000
UNUSED_TARGET = 30000000
unused_space = DISK_SPACE - sizes[0]
diff = UNUSED_TARGET - unused_space
delete_candidates = [size for size in sizes if size >= diff]

print(f"The smallest directory that could be deleted: {min(delete_candidates)}")
