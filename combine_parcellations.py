#!/usr/bin/env python3

import os,sys
import nibabel as nib
import numpy as np
import json

def grab_unique_labels(parc_data):

	unique_labels = list(np.unique(parc_data[parc_data > 0]))

	return unique_labels

def update_parcellation_data(parc_data,label_data,start_value):

	for i,_ in enumerate(label_data):
		parc_data[parc_data == label_data[i]['voxel_value']] = i+start_value

	return parc_data

def combine_parcellation(parc_data_one, parc_data_two,overlap_type):

	parcellation = parc_data_one + parc_data_two

	mask = (parc_data_one>0).astype(np.int_) & (parc_data_two>0).astype(np.int_)

	if overlap_type == 'first':
		parcellation[mask>0] = parc_data_one[mask>0]
	elif overlap_type == 'second':
		parcellation[mask>0] = parc_data_two[mask>0]
	else:
		parcellation[mask>0] = 0
	
	parcellation[parcellation>0] = parcellation[parcellation>0].astype(np.int_)

	return parcellation

def extract_labels(unique_labels,labels):

	return [ f for f in labels if f['voxel_value'] in unique_labels ]

def update_label(label_one,label_two):

	labels = label_one + label_two
	for i,_ in enumerate(labels):
		labels[i]['voxel_value'] = i+1

	return labels

def main():

	# load config
	with open('config.json','r') as config_f:
		config = json.load(config_f)

	# parse inputs
	parc_one = config['parc_one']
	#parc_two = config['parc_two']
	parc_two = './parc_two.nii.gz'
	label_one = config['label_one']
	label_two = config['label_two']
	overlap_type = config['overlap']

	# make output directory
	if not os.path.isdir('./parcellation'):
		os.mkdir('./parcellation')

	# load parcellation and label data
	parc_one = nib.load(parc_one)
	parc_one_data = parc_one.get_fdata()
	parc_two = nib.load(parc_two)
	parc_two_data = parc_two.get_fdata()

	with open(label_one,'r') as label_one_f:
		label_one = json.load(label_one_f)

	with open(label_two,'r') as label_two_f:
		label_two = json.load(label_two_f)

	# grab unique labels for parcellation data
	unique_labels = [grab_unique_labels(parc_one_data), grab_unique_labels(parc_two_data)]

	# refine the labels so only those unique labels are grabbed. this will make the final label.json much cleaner
	label_one_refined = extract_labels(unique_labels[0],label_one)
	label_two_refined = extract_labels(unique_labels[1],label_two)

	# update parcellation with new labels
	parc_one_data = update_parcellation_data(parc_one_data,label_one_refined,1)
	parc_two_data = update_parcellation_data(parc_two_data,label_two_refined,len(np.unique(parc_one_data[parc_one_data>0]))+1)

	# combine parcellations
	parcellations_data = combine_parcellation(parc_one_data,parc_two_data,overlap_type)

	# save parcellations
	output_parcellation = nib.Nifti1Image(parcellations_data,parc_one.affine,parc_one.header)
	nib.save(output_parcellation,'./parcellation/parc.nii.gz')

	# update the labels so they range from 0 to N where len is total length of combined unique labels
	labels = update_label(label_one_refined,label_two_refined)

	# save the label.json
	with open('./parcellation/label.json','w') as lab_f:
		json.dump(labels,lab_f)

if __name__ == '__main__':
	main()
