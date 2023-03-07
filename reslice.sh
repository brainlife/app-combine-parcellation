#!/bin/bash

set -x

export SUBJECTS_DIR=./

parc_one=`jq -r '.parc_one' config.json`
parc_two=`jq -r '.parc_two' config.json`

[ ! -f parc_one.nii.gz ] && mri_vol2vol --mov ${parc_two} --targ ${parc_one} --regheader --interp nearest --o ./parc_one.nii.gz

[ ! -f parc_one.nii.gz ] && echo "something went wrong. check logs and derivs" && exit 1 || echo "reslice complete"