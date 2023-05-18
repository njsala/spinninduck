import shutil
import os
import sys
import time

target = "spinningduck.gif"
# Duplicate target file repeatedly with incrementing file names until there is no more space on the disk. Don't change the extension.
i = 1
created_files = []
log_file = "files_created.log"
# if --clean is specified, read the log file specified after --clean and delete the files specified in the log file.
# if --clean is an argument
if "--clean" in sys.argv:
    # find the index of --clean in the arguments
    index = sys.argv.index("--clean")
    # if the index is not the last argument
    if index != len(sys.argv) - 1:
        # read the log file specified after --clean
        with open(sys.argv[index + 1], "r") as f:
            # for each line in the log file
            try:
                for line in f:
                    # if the line is not empty
                    if line != "\n":
                        # clean the file specified in the line
                        os.remove(line.strip())
                        print("Deleted file: " + line.strip())
            except FileNotFoundError:
                print("File not found", line.strip())
    # delete the log file
    os.remove(sys.argv[index + 1])
    exit(0)


# if --log is specified, rename log_file to the log file specified after --log
# if --log is an argument
if "--log" in sys.argv:
    # find the index of --log in the arguments
    index = sys.argv.index("--log")
    # if the index is not the last argument
    if index != len(sys.argv) - 1:
        log_file = sys.argv[index + 1]





while True:
    # Strip the extension, increment the file name by 1 use the extension from the target file.
    try:    
        # Check if the file exists
        if os.path.isfile(target.split(".")[0] + str(i) + "." + target.split(".")[1]):
            i += 1
            continue
        shutil.copy(target, target.split(".")[0] + str(i) + "." + target.split(".")[1])
        # Keep a log of the files that were created so that they can be deleted later.
        if i % 100 == 0:
            created_files.append(target.split(".")[0] + str(i) + "." + target.split(".")[1])
            # Print storage left on disk in readable format and how many more copies can be created before the disk is full based on the size of the target file.
            # Get the storage left in bytes. Print in readable format like GB or MB.
            storage_left = shutil.disk_usage(".")[2]
        
            copies = shutil.disk_usage(".")[2] // os.path.getsize(target)
            print("Copies left:", copies, "Storage left:", storage_left / (1024 * 1024 * 1024), "GB")
        # if file exists, increment i and continue
    except FileExistsError:
        i += 1
        print("File already exists, incrementing file name.")
        continue
    except OSError:
        break
    except KeyboardInterrupt:
        created_files.append(target.split(".")[0] + str(i) + "." + target.split(".")[1])
        # Print total number of files created.
        print("\nTotal files created:", i)
        # Write created files to a log file.
        with open(log_file, "a") as f:
            for file in created_files:
                f.write(file + "\n")
        break
    else:
        i += 1


print("\nTotal files created:", i)
