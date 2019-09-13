import os

def size_reader(integer):
    if integer < 1024:
        return str(integer) + " B"
    elif integer < 1048576:
        return str(integer * 10 // 1024 / 10) + " KB"
    elif integer < 1073741824:
        return str(integer * 10 // 1048576 / 10) + " MB"
    else:
        return str(integer * 10 // 1073741824 / 10) + " GB"

def get_size(path_origin):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path_origin):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            if not os.path.islink(file_path):
                try:
                    total_size += os.path.getsize(file_path)
                except OSError:
                    print("File inaccessible: " + file_path)
    return total_size

def folder_size_scan(origin_folder):
    try:
        assert(os.path.isdir(origin_folder))
        print("Calculating file sizes...")
        total_size = 0
        for folder in os.listdir(origin_folder):
            this_folder_size = get_size(origin_folder + '//' + folder)
            print("Size of " + folder + ": " + size_reader(this_folder_size))
            total_size += this_folder_size
        print("Finished calculating file sizes. Total size: " \
              + size_reader(total_size))
        global code_not_executed
        code_not_executed = False
    except AssertionError:
        print("Directory is invalid! Please enter valid directory.")

print("This Python script lists the sizes of all files and folders in the \
current directory. It does not list the sizes of any nested files.")

code_not_executed = True
while code_not_executed:
    print("Please input origin folder path.")
    origin = input()
    folder_size_scan(origin)

print("Press Enter to close.")
buffer = input()





