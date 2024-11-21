import os
import yaml
from dataclasses import dataclass

@dataclass
class SwellRun:
    model_obs : dict
    cycle_times : list
    swell_dir : str
    

def get_swell_run(swell_dir: str) -> SwellRun:

    cycle_times = os.listdir(swell_dir + "/run/")
    if not cycle_times:
        raise ValueError("No cycle times found in experiment.")

    models = os.listdir(ctrl_dir + "/run/" + cycle_times[0])
    if not models:
        raise ValueError("No models found in experiment.")

    model_obs = {}
    for model in models:
        eva_dir = ctrl_dir + "/run/" + cycle_times[0] + model + "/eva/"
        obs = os.listdir(ctrl_eva_dir)
        if not obs:
            raise ValueError("No observation list found in experiment")
        model_obs["model"] = model
        model_obs["obs"] = obs

    return SwellRun(model_obs, cycle_times, swell_dir)


def eva_compare(exp_run: SwellRun, ctrl_run: SwellRun, run_type: str) -> None:

    config = yaml.safe_load("configs/IodaObsSpacePlots.yaml")
    # Find intersections between two experiments before running eva compare

    # Create filenames for ctrl/exp and execute eva
    for cycle_time in cycle_times:
        for model_ob in model_obs:
            obs_list = model_ob["obs"]
            for obs in obs_list:
                filename = f"swell-{run_type}.{obs}.{cycle_time}.nc4"
                ctrl_path = f"{ctrl_run.swell_dir}/run/{cycle_time}/{model}/{filename}"
                exp_path  = f"{ctrl_run.swell_dir}/run/{cycle_time}/{model}/{filename}"
                # Update filenames in templates
                # Run eva


if __name__ == "__main__"

    template = yaml.safe_load("template.yaml")

    # Get list of cycle times, models, and observations from control
    ctrl_dir = template["control_directory"]
    ctrl_swell_run = get_swell_run(ctrl_dir)

    # Get list of cycle times, models, and observations from experiment
    exp_dir = template["experiment_directory"]
    exp_swell_run = get_swell_run(exp_dir)

    # Generate comparison plots for swell runs
    run_type = template["run_type"]
    eva_compare(exp_swell_run, ctrl_swell_run, run_type)
