# file-iterator
Tool to iterate the contents of different file types (plain, zip or gzip) through the same interface.

The motivation for `file-iterator` is accessibility to file contents and code readability, as well as 
providing a way to link handlers to common file reading events (start/stop/end file reading).

# Tutorial
```
from file_iterator import FileIterator, FileGroupIterator

# Lets say we have a file in 3 formats.
name_txt = 'file.txt'
name_gzip = 'file.gz'
name_zip = 'file.zip'

# You could read it with a for loop.
f = open(name_txt, 'r')
for line in f:
    print(line)
f.close()

# For GZIPs, a library is required.
import gzip
f = gzip.open(name_gzip, 'r')
for line in f:
    print(line)
f.close()

# As well as for ZIPs.
import zipfile
z = zipfile.ZipFile(name_zip, 'r')
f = z.open(z.namelist()[0], 'r')
for line_bytes in f:
    print(line_bytes)
f.close()


# With the FileIterator interface, we could iterate
#   the contents of any file equally. 
# We also don't need to close it.
def print_contents(it):
    for line_bytes in it:
        print(line_bytes)
        
it = FileIterator.get_iter(name_txt, 'plain')
print_contents(it)

it = FileIterator.get_iter(name_gzip, 'gzip')
print_contents(it)

it = FileIterator.get_iter(name_zip, 'zip')
print_contents(it)

# With the FileGroupIterator interface, we could 
#   iterate through all the contents simply.
names = [name_txt, name_gzip, name_zip]

it = FileGroupIterator(names)
print_contents(it)

# In for loops, a copy of the iterator is used instead. 
#   Therefore, the original doesn't exhausts itself 
#   and we can iterate multiple times.
print_contents(it)
print_contents(it)

# If we need to make use of next(), we can.
# It will return None when everything has been read.
line_b = next(it)
while line_b:
    line_b = next(it)

# Keep in mind that this iteration does exhaust the
#   iterator object.
print(line_b is None) # Prints True.
for line_b in it:
    pass # Doesn't enter here.


# It also supports context manager functionality:
with FileGroupIterator(names) as it:
    print_contents(it)

```

# Todo
- [] Tests: Events.
- [] Tutorial: Events usage.
- [] Upload package to PyPi.