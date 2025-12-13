import os
from collections import namedtuple
import shutil

BirdRunInfo = namedtuple('BirdRunInfo', [
    'nickname', # 6-letter ebird name.
    'name', # official name.
    'state', # State for the analysis. 
    'run_name', # Name of the run.
    'terrain_fn', # File for the terrain
    'habitat_fn', # File for the habitat.
    'transmission_fn', # Terrain transmission.
    'resistance_original_fn', # Original terrain resistance, unrefined.
    'terrain_histogram_json_fn', # File name for terrain histogram.
    'terrain_histogram_csv_fn', # File name for terrain histogram.
    'repopulation_fn', 'gradient_fn', 'log_fn',
    'validation_fn',
    'obs_path',
    'obs_csv_path',
    ])

def delete_run(base_path, nickname, state, run_name="Standard"):
    """Deletes the files for the given run."""
    p = os.path.join(base_path, f"{nickname}/{state}/Output/{run_name}")
    print("Deleting", p)
    shutil.rmtree(p, ignore_errors=True)

class BirdRun(object):

    def __init__(self, data_path):
        """Initializes a bird run, given a data path"""
        self.files_path = data_path
        
    def get_bird_run(self, nickname, bird_name, run_name=None, state="US-CA"):
        """Given a bird name in 6-letter ebird format, returns the BirdRun object for the bird."""
        d = {"bird": nickname,
             "run_name": run_name or "Standard",
             "state": state}
        self.createdir(os.path.join(self.files_path, "{bird}/{state}/Output/{run_name}".format(**d)))
        return BirdRunInfo(
            nickname = nickname,
            name = bird_name,
            state = state,
            run_name = run_name or "Standard",
            # Input ,
            terrain_fn = os.path.join(self.files_path, "{bird}/{state}/terrain.tif".format(**d)),
            habitat_fn = os.path.join(self.files_path, "{bird}/{state}/habitat.tif".format(**d)),
            transmission_fn = os.path.join(self.files_path, "{bird}/{state}/transmission_refined_1.csv".format(**d)),
            resistance_original_fn = os.path.join(self.files_path, "{bird}/resistance.csv".format(**d)),
            terrain_histogram_json_fn = os.path.join(self.files_path, "{bird}/{state}/terrain_hist.json".format(**d)),
            terrain_histogram_csv_fn = os.path.join(self.files_path, "{bird}/{state}/terrain_hist.csv".format(**d)),
            # Validation files.
            validation_fn = os.path.join(self.files_path, "{bird}/{state}/Ratios".format(**d)),
            # Output files
            repopulation_fn = os.path.join(self.files_path, "{bird}/{state}/Output/{run_name}/repopulation.tif".format(**d)),
            gradient_fn = os.path.join(self.files_path, "{bird}/{state}/Output/{run_name}/gradient.tif".format(**d)),
            log_fn = os.path.join(self.files_path, "{bird}/{state}/Output/{run_name}/log.json".format(**d)),
            obs_path = os.path.join(self.files_path, "{bird}/{state}/Observations".format(**d)),
            obs_csv_path = os.path.join(self.files_path, "{bird}/{state}/Output/{run_name}/observations.csv".format(**d)),
        )

    def get_observations_fn(self, obs_path, bigsquare=False, **kwargs):
        """Completes the name of an observation ratio file, adding the information on minimum number of observations,
        and maximum length walked.
        """
        d = dict(**kwargs)
        d["isbig"] = "_big" if bigsquare else ""
        return os.path.join(obs_path, "OBS_min_{min_checklists}_len_{max_distance}{isbig}.json".format(**d))

    def get_observations_display_fn(self, obs_path, bigsquare=False, **kwargs):
        """Completes the name of an observation ratio tif file, adding the information on minimum number of observations,
        and maximum length walked.
        """
        d = dict(**kwargs)
        d["isbig"] = "_big" if bigsquare else ""
        return os.path.join(obs_path, "OBS_min_{min_checklists}_len_{max_distance}{isbig}.tif".format(**d))

    def get_observations_all_fn(self, obs_path, **kwargs):
        """Completes the name of an observation ratio file, adding the information on minimum number of observations,
        and maximum length walked.
        """
        d = dict(**kwargs)
        return os.path.join(obs_path, "OBS_all_len_{max_distance}_{date_range}_{num_squares}.csv".format(**d))

    def get_terrain_occurrences_fn(self, obs_path, **kwargs):
        """Completes the name of an observation ratio file, adding the information on minimum number of observations,
        and maximum length walked.
        """
        d = dict(**kwargs)
        return os.path.join(obs_path, "TEROBS_all_len_{max_distance}_{date_range}_{num_squares}.csv".format(**d))

    def get_observations_all_display_fn(self, obs_path, **kwargs):
        """Completes the name of an observation ratio tif file, adding the information on minimum number of observations,
        and maximum length walked.
        """
        d = dict(**kwargs)
        return os.path.join(obs_path, "OBS_all_len_{max_distance}_{date_range}_{num_squares}.tif".format(**d))

    def createdir_for_file(self, fn):
        """Ensures that the path to a file exists."""
        dirs, ffn = os.path.split(fn)
        # print("Creating", dirs)
        os.makedirs(dirs, exist_ok=True)

    def createdir(self, dir_path):
        """Ensures that a folder exists."""
        # print("Creating", dir_path)
        os.makedirs(dir_path, exist_ok=True)
