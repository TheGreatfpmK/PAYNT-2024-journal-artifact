import os
import subprocess
import signal
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))

# If true overwrite existing logs, if false only run experiments for missing log files
overwrite_logs = False

# CHANGE THIS TO CHANGE WHAT MODELS SHOULD BE USED
directory_main = os.fsencode(dir_path + '/../models/archive/tac24-synthesis')
models_main = [ f.path for f in os.scandir(directory_main) if f.is_dir() ]
directory_cpomdp = os.fsencode(dir_path + '/../models/archive/tac24-synthesis/cpomdp')
models_cpomdp = [ f.path for f in os.scandir(directory_cpomdp) if f.is_dir() ]
directory_cs = os.fsencode(dir_path + '/../models/archive/tac24-synthesis/case-studies')
models_cs = [ f.path for f in os.scandir(directory_cpomdp) if f.is_dir() ]

def run_experiment(options, models, logs_string, experiment_models, timeout, special={}):
    
    logs_dir = os.fsencode(dir_path + "/output/{}/".format(logs_string))

    print(f'\nRunning experiment {logs_string}. The logs will be saved in folder {logs_dir.decode("utf-8")}')
    print(f'The options used: "{options}"\n')

    for model in models:
        model_name = os.path.basename(model).decode("utf-8")
        project_name = model.decode("utf-8")

        if model_name in special.keys():
            model_options = special[model_name]
        else:
            model_options = options

        # THE REST OF THE MODELS
        command = "python3 paynt.py --project {} {}".format(project_name, model_options)

        if (len(experiment_models) != 0) and (model_name not in experiment_models):
            continue

        if not overwrite_logs:
            if os.path.isfile(logs_dir.decode("utf-8") + model_name + "/" + "logs.txt"):
                print(model_name, "LOG EXISTS")
                continue

        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            # TIMEOUT HERE TO TERMINATE EXPERIMENT
            # timeout should be higher than the expected running time of a given experiment
            output, error = process.communicate(timeout=timeout)
            output, error = process.communicate()
            process.wait()
        except subprocess.TimeoutExpired:
            process.send_signal(signal.SIGKILL)
            output, error = process.communicate()
            process.wait()

        if os.path.isfile(logs_dir.decode("utf-8") + model_name + "/" + "logs.txt"):
            print(model_name, "OVERWRITEN LOG")
            os.remove(logs_dir.decode("utf-8") + model_name + "/" + "logs.txt")
        else:
            print(model_name)

        if os.path.isfile(logs_dir.decode("utf-8") + model_name + "/" + "stderr.txt"):    
            os.remove(logs_dir.decode("utf-8") + model_name + "/" + "stderr.txt")

        os.makedirs(os.path.dirname(logs_dir.decode("utf-8") + model_name + "/" + "logs.txt"), exist_ok=True)
        with open(logs_dir.decode("utf-8") + model_name + "/" + "logs.txt", "w") as text_file:
            text_file.write(output.decode("utf-8"))

        # TODO remove after
        if error:
            with open(logs_dir.decode("utf-8") + model_name + "/" + "stderr.txt", "w") as text_file:
                text_file.write(error.decode("utf-8"))

    print(f'\nExperiment {logs_string} completed. The logs are saved in folder {logs_dir.decode("utf-8")}')

if __name__ == '__main__':
    experiment = sys.argv[1]
    overwrite = sys.argv[2]
    overwrite_logs = overwrite == "True"

    if experiment == 'models':
        pass

    elif experiment == 't2':
        experiment_models = ["dpm-demo", "grid", "grid-10-sl-4fsc", "grid-meet-sl-2fsc", "herman", "maze", "maze-sl-5", "pole", "pole-res", "refuel-06-res"]

        # AR
        options = ""
        logs_string = "tac24-method-ar"
        timeout = 1800
        run_experiment(options, models_main, logs_string, experiment_models, timeout)

        # CEGIS
        options = "--method cegis"
        logs_string = "tac24-method-cegis"
        timeout = 1800
        run_experiment(options, models_main, logs_string, experiment_models, timeout)

        # Hybrid
        options = "--method hybrid"
        logs_string = "tac24-method-hybrid"
        timeout = 1800
        run_experiment(options, models_main, logs_string, experiment_models, timeout)


        print("\nTABLE 2 EXPERIMENT COMPLETE\n")

    elif experiment == 't4':
        experiment_models = ["milos-97", "query-s3", "query-s4", "tiger-grid"]
        
        # PAYNT
        options = "--fsc-synthesis"
        logs_string = "tac24-cpomdp"
        timeout = 3600
        special = {"milos-97": f"--fsc-synthesis --constrained-bound 150", "query-s3": f"--fsc-synthesis --constrained-bound 2.75", "query-s4": f"--fsc-synthesis --constrained-bound 2.75", "tiger-grid": f"--fsc-synthesis --constrained-bound 0"}
        run_experiment(options, models_cpomdp, logs_string, experiment_models, timeout, special)

        print("\nTABLE 4 EXPERIMENT COMPLETE\n")

    elif experiment == 'cs':
        experiment_models = []
        
        # PAYNT
        options = ""
        logs_string = "tac24-case-studies"
        timeout = 900
        special = {"maze-multi": f"--fsc-synthesis"}
        run_experiment(options, models_cs, logs_string, experiment_models, timeout, special)

        print("\nCASE STUDIES EXPERIMENT COMPLETE\n")

    else:
        print("Provide experiment set name (t2, t4, cs)!")