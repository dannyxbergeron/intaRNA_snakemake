#!/bin/bash

name=$1

g++ --std=c++17 "$1".cpp -o $1 -O3
