#from functions.get_files_info import get_files_info        (Test 1)
#from functions.get_file_content import get_file_content    (Test 2 & 3)
from functions.write_file import write_file

if __name__ == "__main__":
    # test 1
    #print(get_files_info("calculator", "."))
    #print(get_files_info("calculator", "pkg"))
    #print(get_files_info("calculator", "/bin"))
    #print(get_files_info("calculator", "../"))

    # test 2
    #print(get_file_content("calculator", "lorem.txt")) #testing proper truncation

    # test 3
    #print(get_file_content("calculator", "main.py"))
    #print(get_file_content("calculator", "pkg/calculator.py"))
    #print(get_file_content("calculator", "/bin/cat"))

    # test 4
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))    

    
    
    