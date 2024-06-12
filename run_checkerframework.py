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

BENCHMARKS_FOLDER = "../dataset/june2020_dataset_copy"
RESULTS_FOLDER = "cf_analysis_results/checkerframework_3.43.0_WPI_results_JDK_11"
COMPILED_CLASSES_FOLDER = "cf_classes"
SRC_FILES = "cf_srcs.txt"
CF_ROOT= "/home/smala009/RLF/rlfixer/code/tools/checker-framework-3.43.0"
JAVAC_WITH_FLAGS = ("javac " +
"-J--add-exports=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED " +
"-J--add-exports=jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED " +
"-J--add-exports=jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED " +
"-J--add-exports=jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED " +
"-J--add-exports=jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED " +
"-J--add-exports=jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED " +
"-J--add-exports=jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED " +
"-J--add-exports=jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED " +
"-J--add-opens=jdk.compiler/com.sun.tools.javac.comp=ALL-UNNAMED")
CF_BINARY = f"{CF_ROOT}/checker/bin/javac"
CF_DIST_JAR_ARG=f"-processorpath {CF_ROOT}/checker/dist/checker.jar"
CHECKER_QUAL_JAR=f"{CF_ROOT}/checker/dist/checker-qual.jar"
CF_COMMAND = "-processor org.checkerframework.checker.resourceleak.ResourceLeakChecker -Adetailedmsgtext"
SKIP_COMPLETED = False #skips if the output file is already there.
RUN_WPI = True
WPI_TIMEOUT = 60 * 60 #90 minutes

#create the output folder if it doesn't exist
if not os.path.exists(RESULTS_FOLDER):
    os.mkdir(RESULTS_FOLDER)

BENCHMARKS_WITH_ERRORS = [
    "url400631cdd0_ludaiqian_appliedxml_tgz-pJ8-test_simples_TestJ8",
    "url529c09a30c_kianyangchn_DriveNow_tgz-pJ8-drivenow_tests_TestJ8",
"url4c27590fbe_Hoten_Java_Delaunay_tgz-pJ8-com_hoten_delaunay_examples_TestDriverJ8",
"url11fb0973cf_raichuman9_Swimmer526_tgz-pJ8-fr_inria_optimization_cmaes_examples_CMAExample1J8",
"url901cc5721b_shidasan_KonohaCoffee_tgz-pJ8-org_KonohaScript_KonohaJ8",
"url433bec1e56_sarobe_DifficultyInvestigation_tgz-pJ8-fr_inria_optimization_cmaes_examples_CMAExample1J8",
"url7a69e77641_benmouh_MySgbd_tgz-pJ8-Demo_CheckRowNumJ8",
"url82787aa7a4_vrthra_v_language_tgz-pJ8-v_VJ8",
"urld829b80034_wjch111_PTSP2013Wang_tgz-pJ8-controllers_momcts_momctsCore_TestPlannerJ8",
"urld8e41b4f7f_warrenfalk_jbox2dtest_tgz-pJ8-org_jbox2d_testbed_framework_TestbedMainJ8",
"urla5230a98e3_Dhana_Krishnasamy_InMemoryJMS_tgz-pJ8-com_dhana_broker_demo_AppJ8",
"url5997ccb760_JANNLab_JANNLab_tgz-pJ8-de_jannlab_examples_recurrent_SequentialXorExampleJ8",
"url71665d7d68_branscha_lib_scripty_tgz-pJ8-com_sdicons_scripty_ScriptyAutoReplJ8",
"urleb43757003_Origraena_mas_platform_tgz-pJ8-ori_MainJ8",
"url29ae058134_yuriy_chumak_jatha_tgz-pJ8-org_jatha_LispJ8",
"url7f43a4752f_shalynnho_pokemonfactory_tgz-pJ8-Networking_ServerJ8",
"url47fcfc0133_baliosian_tau_fst_tgz-pJ8-uy_edu_fing_mina_fsa_test_old_TestComposition1J8",
"url74761fd9a6_cstriker1407_design_pattern_tgz-pJ8-yeah_cstriker1407_design_patterns_MainJ8",
"url85e313f409_edugasser_Ascensor_tgz-pJ8-ascensor_MainJ8",
"url75694980d5_fabioalmeid_tp01ftc_tgz-pJ8-agentes_jade_Centralizador_ExemploParserGramaticaCentralizadorJ8",
"url2df0f7c811_przemekgalazka_legacycode_tgz-pJ8-pl_cc_core_cmd_CommandJ8",
"url7f729337e3_timmolter_Sundial_tgz-pJ8-org_knowm_sundial_SampleRunJ8",
"urlff74b96b0d_HugoFeng_HospitalProject_tgz-pJ8-hugo_project_hospital_ProjectTestJ8",
"url0d38a10ee7_diegopliebana_GEBT_tgz-pJ8-ch_idsia_scenarios_test_EvolveWithChangingSeedsJ8",
"url027b37a4db_ctriposs_bigmap_tgz-pJ8-com_ctriposs_bigmap_LimitTestJ8",
"url1a41b8e9f2_mr1azl_INF345_tgz-pJ8-TestParserJ8",
"url53f943c5cb_Praznat_AGP_tgz-pJ8-AMath_TestingJ8",
]

#Loop through the benchmarks
print("Completed Benchmarks")
i, total = 1, len(BENCHMARKS_WITH_ERRORS)
for benchmark in BENCHMARKS_WITH_ERRORS:
    benchmark = "url400631cdd0_ludaiqian_appliedxml_tgz-pJ8-test_simples_TestJ8"
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
    if RUN_WPI:
        print(f"Running WPI on {benchmark}")
        items_to_delete = ['wpi-iterations', 'wpi-log.txt', 'wpi-out']
        for item in items_to_delete:
            path = os.path.join(BENCHMARKS_FOLDER, benchmark, item)
            if os.path.exists(path):
                if os.path.isfile(path) or os.path.islink(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)
        with open(f'{BENCHMARKS_FOLDER}/{benchmark}/wpi-log.txt', 'w') as file:
            process = subprocess.Popen(shlex.split(f'./wpi/wpi.sh {BENCHMARKS_FOLDER}/{benchmark}'), stdout=file, stderr=subprocess.STDOUT)
            try:
                process.communicate(timeout=WPI_TIMEOUT)
            except subprocess.TimeoutExpired:
                print(f"Command timed out after {WPI_TIMEOUT} seconds")
                process.kill()
                process.wait()
                os.system("sudo killall -9 javac")
    
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
    command = (JAVAC_WITH_FLAGS
        + " " + CF_DIST_JAR_ARG
        + " " + CF_COMMAND
        + (" " + "-Aajava=" + BENCHMARKS_FOLDER + "/" + benchmark + "/" + "wpi-out" if RUN_WPI else "")
        + " " + "-AdisableReturnsReceiver"
        + " " + "-J-Xmx32G"
        + " " + "-J-ea"
        + " " + "-d"
        + " " + COMPILED_CLASSES_FOLDER
        + " -cp " + f"{lib_folder}:{CHECKER_QUAL_JAR}"
        + " @" + SRC_FILES
        # + " " + "-source 8 -target 8"
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
    break