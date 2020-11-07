#!/bin/bash

mkdir data
curl https://jparker.nyc3.digitaloceanspaces.com/blog/circle_graphics/small.h5 -o data/small.h5
curl https://jparker.nyc3.digitaloceanspaces.com/blog/circle_graphics/medium.h5 -o data/medium.h5
curl https://jparker.nyc3.digitaloceanspaces.com/blog/circle_graphics/large.h5 -o data/large.h5
