import os
import yaml

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--ymls", type=str, nargs='*', required=True, help="yml files" )
parser.add_argument("--pkl", action='store_true', help='Submit skimming only for background samples', default=False)
parser.add_argument("--skipSignals", action='store_true', help='Submit skimming skipping signals samples')
parser.add_argument("--voltage", type=str, required=True, choices=["m20","m10","nominal","p10","p20","all"], nargs='*',
                                help="Group of voltage configuration [m20, m10, nominal, p10, p20, all]" )

args = parser.parse_args()
ymls = args.ymls
voltage = args.voltage
pkl = args.pkl

if voltage.count("all"):
    voltage = ["m20", "m10", "nominal","p10","p20"]

def createFolder(path):
    if os.path.isdir(path) == False:
        os.system('mkdir -p ' + path)



inputs_folder  = "FARM/inputs"
logs_folder     = "FARM/logs"
outputs_folder = "FARM/outputs"

batchsystem = ""
submit_file_name = "skimming.sub"
generic_bash_script_name = "bash_script_Voltage-{volt}_{folder}.sh"

sourcecmd   = ""
hostname    = os.uname()[1]

if "lxplus" in hostname:
    batchsystem = "condor"
    submit_file_name = "submit_skimming.cmd"
    sourcecmd   = "source /cvmfs/sft.cern.ch/lcg/views/LCG_98python3/x86_64-centos7-gcc10-opt/setup.sh"
if "iihe" in hostname:
    batchsystem = "qsub"
    submit_file_name = "submit_skimming.sh"
    sourcecmd = "source $VO_CMS_SW_DIR/cmsset_default.sh"


condor_cfg = """Universe                = vanilla
Environment             = CONDORJOBID=$(Process)
notification            = Error
when_to_transfer_output = ON_EXIT
transfer_output_files   = ""
should_transfer_files   = YES
executable = $(filename)
output = {logsfolder}/$Fn(filename).$(ClusterId).$(ProcId).out
error  = {logsfolder}/$Fn(filename).$(ClusterId).$(ProcId).err
log    = {logsfolder}/$Fn(filename).$(ClusterId).$(ProcId).log
+JobFlavour = "testmatch"
queue filename matching files {inputsfolder}/{script_wildcard}
"""

bash_script_tmp = """#!/bin/bash
set -e

FOLDER=\"{folder}\"

{source_command}

{command}

"""

for yml in ymls:
    with open(yml,'r') as f:

        pwd = os.getcwd()

        createFolder(inputs_folder)
        createFolder(logs_folder)
        createFolder(outputs_folder)

        config = yaml.load(f, Loader=yaml.FullLoader)
        Measurements = config['Measurements']

        # print("{folder}/skimming_submit.sh".format(folder=inputs_folder))


        submit_file_path = "{inputs_folder}/{submit_file_name}".format(inputs_folder=inputs_folder,submit_file_name=submit_file_name)
        submit_file = open(submit_file_path,"w")

        if batchsystem == "qsub":
            submit_file.write("#!/bin/bash\n")
        if batchsystem == "condor":
            submit_file.write(condor_cfg.format(logsfolder=logs_folder,
                                                inputsfolder=inputs_folder,
                                                script_wildcard=generic_bash_script_name.format(folder="*", volt="*")))


        for m in Measurements:
            measure = Measurements[m]
            #print(measure.keys())
            #print(measure["voltage"])
            V = measure["voltage"]
            scan = measure["angle_scan"]
            print(V)
            if len(voltage) > 0 :
                if not voltage.count(V):
                    continue

            for angle in scan.keys():

                ang_file = scan[angle]
                filename = ang_file['file_bin']
                if pkl:
                    filename = ang_file['file_root']

                shell_filename = generic_bash_script_name.format(folder=angle, volt=V)
                shell_script   = open("{folder}/{sh}".format(folder=inputs_folder,sh=shell_filename), "w")

                command = "$FOLDER/decode.exe {file}".format(file=filename)
                if pkl:
                    command = "python $FOLDER/pkl_conversion.py --input {file}".format(file=filename)
                #print(command)
                script = bash_script_tmp.format(folder=pwd,
                                                source_command=sourcecmd,
                                                command=command,
                                                output=outputs_folder)
                shell_script.write(script)
                shell_script.close()
                print("- script: "+shell_filename+" for process: "+bcolors.WARNING+angle+bcolors.ENDC+" has been "+bcolors.WARNING+"created"+bcolors.ENDC)

                os.system("chmod 777 {folder}/{sh}".format(folder=inputs_folder,sh=shell_filename))
                if batchsystem == "qsub":
                    submit_file.write("qsub -o {log} -e {log} {sh} \n".format(log=logs_folder,sh=inputs_folder+"/"+shell_filename))

            submit_file.close()
            if batchsystem == "qsub":
                print("Please, "+bcolors.HEADER+"run"+bcolors.ENDC+":\n \t"+bcolors.OKGREEN+"bash "+inputs_folder+"/"+submit_file_name+" "+bcolors.ENDC)
            if batchsystem == "condor":
                print("Please, "+bcolors.HEADER+"run"+bcolors.ENDC+":\n \t"+bcolors.OKGREEN+"condor_submit "+inputs_folder+"/"+submit_file_name+" "+bcolors.ENDC)