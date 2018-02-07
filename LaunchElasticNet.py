#! /usr/bin/env python3

from ElasticNetInterface import ParseClassInput
import argparse

parser = argparse.ArgumentParser(description='Interface for parallel SGE implementation of SciKitLearn ElasticNetCV')
parser.add_argument('-i', type=str)

arguments = parser.parse_args()


ParseClassInput(input_dictionary=arguments.i)
