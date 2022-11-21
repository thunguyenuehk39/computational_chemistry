#!/bin/bash
for i in {0..85}
do
qsub $i/openmpi.sh
done