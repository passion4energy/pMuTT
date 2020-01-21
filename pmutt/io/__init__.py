# -*- coding: utf-8 -*-
"""
pmutt.io
Vlachos group code to read from/write to different formats.
Created on Fri Jul 7 12:40:00 2018
"""

import datetime

import pmutt


def _get_file_timestamp(comment_char=''):
    """Writes a comment indicating when the file was written by pmutt
    
    Parameters
    ----------
        comment_char : str, optional
            Comment character used by input file. Default is ''
    Returns
    -------
        file_timestamp : str

    """
    return ('{}File generated by pMuTT (v {}) on {}'
            ''.format(comment_char, pmutt.__version__,
                      datetime.datetime.now()))
