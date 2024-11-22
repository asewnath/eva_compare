import os
import yaml
from dataclasses import dataclass
from eva.eva_driver import eva
from datetime import datetime as dt
from datetime import timedelta


@dataclass
class SwellRun:
    model_obs : list
    cycle_times : list
    swell_dir : str
    

def get_swell_run(swell_dir: str) -> SwellRun:

    cycle_times = os.listdir(swell_dir + "/run/")
    if not cycle_times:
        raise ValueError("No cycle times found in experiment.")
    models = os.listdir(ctrl_dir + "/run/" + cycle_times[0])
    if not models:
        raise ValueError("No models found in experiment.")
    model_obs = []
    for model in models:
        tmp_dict = {}
        eva_dir = ctrl_dir + "/run/" + cycle_times[0] + "/" + model + "/eva/"
        obs = os.listdir(eva_dir)
        if not obs:
            raise ValueError("No observation list found in experiment")
        tmp_dict["model"] = model
        tmp_dict["obs"] = obs
        model_obs.append(tmp_dict)

    return SwellRun(model_obs, cycle_times, swell_dir)


def eva_compare(exp_run: SwellRun, ctrl_run: SwellRun, run_type: str) -> None:

    with open("configs/IodaObsSpacePlots.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    # Find intersections between two experiments before running eva compare
     
    # Create filenames for ctrl/exp and execute eva
    for cycle_time in exp_run.cycle_times:
        # Subtract 3 hours from datetime
        dto = dt.strptime(cycle_time, "%Y%m%dT%H%M%SZ")
        dto = dto - timedelta(hours=3)
        datetime = dto.strftime("%Y%m%dT%H%M%SZ")

        for model_ob in exp_run.model_obs:
            model = model_ob["model"]
            obs_list = model_ob["obs"]
            for obs in obs_list:
                filename = f"swell-{run_type}.{obs}.{datetime}.nc4"
                ctrl_path = f"{ctrl_run.swell_dir}/run/{cycle_time}/{model}/{filename}"
                exp_path  = f"{exp_run.swell_dir}/run/{cycle_time}/{model}/{filename}"
                # Update filenames in templates
                for ind in range(len(config["datasets"])):
                    if config["datasets"][ind]["name"] == "control":
                        config["datasets"][ind]["filenames"] = [ctrl_path]
                    elif config["datasets"][ind]["name"] == "experiment":
                        config["datasets"][ind]["filenames"] = [exp_path]
                    else:
                        raise ValueError("datasets should be named control and experiment")
                # Run eva
                eva(config)


if __name__ == "__main__":

    with open("template.yaml", 'r') as stream:
        template = yaml.safe_load(stream)

    # Get list of cycle times, models, and observations from control
    ctrl_dir = template["control_directory"]
    ctrl_swell_run = get_swell_run(ctrl_dir)

    # Get list of cycle times, models, and observations from experiment
    exp_dir = template["experiment_directory"]
    exp_swell_run = get_swell_run(exp_dir)

    # Generate comparison plots for swell runs
    run_type = template["swell_run_type"]
    eva_compare(exp_swell_run, ctrl_swell_run, run_type)
