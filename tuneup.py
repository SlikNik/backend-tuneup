#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Nikal Morgan"

import timeit
import cProfile
import pstats
import functools


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    # a decorator that wraps the func....
    @functools.wraps(func)
    def performance(*args, **kwargs):
        # create cProfile Profile
        performance_object = cProfile.Profile()
        # turning on profile
        performance_object.enable()
        # running function and setting it to result
        result = func(*args, **kwargs)
        # turning off profile
        performance_object.disable()

        # creating pstats obj for the performance object
        get_stats_obj = pstats.Stats(performance_object)
        get_stats_obj.strip_dirs().sort_stats('cumulative').print_stats()
        # removing the extraneous path from all the module names
        # get_stats_obj.strip_dirs()
        # sorts stat object according to criteria which here is cumulative
        # get_stats_obj.sort_stats('cumulative')
        # printing out all the statistics
        # get_stats_obj.print_stats()
        return result
    return performance


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


# this function add more time to overall performance time wasn't needed
# def is_duplicate(title, movies):
#     """Returns True if title is within movies list."""
#     for movie in movies:
#         if movie.lower() == title.lower():
#             return True
#     return False


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movie_dict = {}
    movies = read_movies(src)
    for movie in movies:
        if movie in movie_dict:
            # if it's already there we need to increment it
            movie_dict[movie] += 1
        # if the movie is not already there we need to add it
        movie_dict.setdefault(movie, 1)
    return [k for k, v in movie_dict.items() if v > 1]


def timeit_helper():
    """Part A: Obtain some profiling measurements using timeit."""
    # Timer gets the avg of it
    # stmt is the code for which you want to measure the execution time
    # setup is the details that need to be executed before stmt
    t = timeit.Timer(stmt="main()", setup="from __main__ import main")
    results = min(t.repeat(repeat=7, number=5)) / 5
    print("Best time across 7 repeats of 5 runs per repeat " + str(results)
          + " sec")


def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))


if __name__ == '__main__':
    main()
