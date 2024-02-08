'''
This script runs checker-framework on all the benchmarks.
Fill in the correct values for the macros at
the top of the file before executing.
'''
import os
import shutil
import time
import subprocess
import shlex

BENCHMARKS_FOLDER = "../dataset/june2020_dataset"
RESULTS_FOLDER = "checkerframework_3.42.0_results_WPI"
COMPILED_CLASSES_FOLDER = "cf_classes"
SRC_FILES = "cf_srcs.txt"
CF_BINARY = "../rlfixer/code/tools/checker-framework-3.42.0/checker/bin/javac"
CF_COMMAND = "-processor org.checkerframework.checker.resourceleak.ResourceLeakChecker -Adetailedmsgtext"
SKIP_COMPLETED = True #skips if the output file is already there.
WPI_TIMEOUT = 60 * 60 #60 minutes

#create the output folder if it doesn't exist
if not os.path.exists(RESULTS_FOLDER):
    os.mkdir(RESULTS_FOLDER)

#Loop through the benchmarks
print("Completed Benchmarks")
i, total = 1, len(os.listdir(BENCHMARKS_FOLDER))
for benchmark in os.listdir(BENCHMARKS_FOLDER):
    print(f"{i} of {total}: {benchmark}")
    if (SKIP_COMPLETED):
        if os.path.exists(f'{RESULTS_FOLDER}/{benchmark}.txt'):
            print("skipping completed benchmark.")
            i += 1
            continue
    #skip non-directories
    if not os.path.isdir(f'{BENCHMARKS_FOLDER}/{benchmark}'):
        continue

    # Run WPI.
    print(f"Running WPI on {benchmark}")
    with open(f'{BENCHMARKS_FOLDER}/{benchmark}/wpi-log.txt', 'w') as file:
        process = subprocess.Popen(shlex.split(f'./wpi/wpi.sh {BENCHMARKS_FOLDER}/{benchmark}'), stdout=file, stderr=subprocess.STDOUT)
        try:
            process.communicate(timeout=WPI_TIMEOUT)
        except subprocess.TimeoutExpired:
            print(f"Command timed out after {WPI_TIMEOUT} seconds")
            process.kill()
            process.wait()
            os.system("killall -9 java")
    
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
        + " " + "-Aajava=" + BENCHMARKS_FOLDER + "/" + benchmark + "/" + "/wpi-out"
        + " " + "-AdisableReturnsReceiver"
        + " " + "-J-Xmx32G"
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
    print("-------------------------------------------------- \n")
    i += 1