#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# ==========================================
# Copyright 2023 Yang
# ararpy - files - basic
# ==========================================
#
#
#
"""

import os
import pickle
import json


def read(file_path):
    """ Read text files, default 'r', 'rb'
    Parameters
    ----------
    file_path

    Returns
    -------

    """
    try:
        with open(file_path, 'r') as f:
            params = json.load(f)
    except UnicodeDecodeError:
        with open(file_path, 'rb') as f:
            params = pickle.load(f)
    return params


def write(file_path, params):
    """
    Parameters
    ----------
    file_path
    params

    Returns
    -------

    """
    # with open(file_path, 'wb') as f:
    #     f.write(pickle.dumps(params))
    with open(file_path, 'w') as f:  # save serialized json data to a readable text
        f.write(json.dumps(params))
    return file_path


def delete(file_path):
    """
    Parameters
    ----------
    file_path

    Returns
    -------

    """
    try:
        os.remove(file_path)
    except Exception:
        return False
    else:
        return True
