'''
This script runs checker-framework on all the benchmarks.
Fill in the correct values for the macros at
the top of the file before executing.
'''
import os
import shutil
import time

BENCHMARKS_FOLDER = "../../../dataset/june2020_dataset"
RESULTS_FOLDER = "checkerframework_3.42.0_results"
COMPILED_CLASSES_FOLDER = "cf_classes"
SRC_FILES = "cf_srcs.txt"
CF_BINARY = "../tools/checker-framework-3.42.0/checker/bin/javac"
CF_COMMAND = "-processor org.checkerframework.checker.resourceleak.ResourceLeakChecker -Adetailedmsgtext"
SKIP_COMPLETED = True #skips if the output file is already there.

#create the output folder if it doesn't exist
if not os.path.exists(RESULTS_FOLDER):
    os.mkdir(RESULTS_FOLDER)

#Loop through the benchmarks
print("Completed Benchmarks")
for benchmark in os.listdir(BENCHMARKS_FOLDER):
    print(benchmark)
    if (SKIP_COMPLETED):
        if os.path.exists(f'{RESULTS_FOLDER}/{benchmark}.txt'):
            print("skipping completed benchmark.")
            continue
    #skip non-directories
    if not os.path.isdir(f'{BENCHMARKS_FOLDER}/{benchmark}'):
        continue
    
    #create a folder for the compiled classes if it doesn't exist
    if not os.path.exists(COMPILED_CLASSES_FOLDER):
        os.mkdir(COMPILED_CLASSES_FOLDER)

    #Get a list of Java source code files.
    find_srcs_command = f'find {BENCHMARKS_FOLDER}/{benchmark}/src -name "*.java" > {SRC_FILES}'
    os.system(find_srcs_command)

    #get folder with libraries used by benchmark
    lib_folder = f'{BENCHMARKS_FOLDER}/{benchmark}/lib'

    #execute infer on the source files
    time_start = time.time()
    command = (CF_BINARY
        + " " + CF_COMMAND
        + " " + "-J-Xmx8G"
        + " " + "-d"
        + " " + COMPILED_CLASSES_FOLDER
        + " -cp " + lib_folder
        + " @" + SRC_FILES
        + " 2> " +  RESULTS_FOLDER
        + "/" + benchmark + ".txt"
    )
    os.system(command)
    time_end = time.time()
    total_time = time_end - time_start
    with open("checkerframework_timings.csv","a") as f:
        f.write(f'{benchmark},{str(total_time)}\n')
    
    #remove the classes folder
    shutil.rmtree(COMPILED_CLASSES_FOLDER)
