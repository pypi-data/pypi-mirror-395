###############################################################################
# (c) Copyright 2024-2025 CERN for the benefit of the LHCb Collaboration      #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import json
import os
from typing import List, Union
import yaml


def load_config(path: str):
    """
    Load a configuration file from a JSON or YAML file

    Args:
        path: Path to the configuration file

    Returns:
        dict: Configuration as a dictionary

    Raises:
        ValueError: If the file is not a '.json' or '.yaml' file
    """

    if path.endswith(".json"):
        with open(path, "r") as config_file:
            config = json.load(config_file)
    elif path.endswith(".yaml"):
        with open(path, "r") as config_file:
            config = yaml.safe_load(config_file)
    else:
        raise ValueError(f"Config '{path}' must be a '.json' or '.yaml' file")
    return config


def write_config(config: dict, path: str):

    if "/" in path:
        os.makedirs(path.rsplit("/", 1)[0], exist_ok=True)

    if path.endswith(".json"):
        with open(path, "w") as config_file:
            json.dump(config, config_file, indent=4)
    elif path.endswith(".yaml"):
        with open(path, "w") as config_file:
            yaml.dump(config, config_file, default_flow_style=False)
    else:
        raise ValueError(f"Config '{path}' must be a '.json' or '.yaml' file")


def split_paths(paths: Union[List[str], str], require_same_tree: bool = True):
    """Split ROOT file paths into tree names and file paths

    Args:
        paths: Path(s) to ROOT file(s) of the form <path>:<tree>
        require_same_tree: Whether all paths must reference the same tree

    Returns:
        tuple: Tree name(s) and file path(s)

    Raises:
        ValueError: If require_same_tree is True and different trees are provided
    """
    if isinstance(paths, str):
        paths = [paths]

    split_trees = []
    split_paths = []

    for p in paths:
        split_path, split_tree = p.rsplit(":", 1)
        split_trees.append(split_tree)
        split_paths.append(split_path)

    if len(set(split_trees)) == 1 and require_same_tree:
        return split_trees[0], split_paths
    elif not require_same_tree:
        return split_trees, split_paths

    raise ValueError(
        f"Same tree must be provided for all paths. Trees '{split_trees}' were provided."
    )
