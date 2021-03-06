import os, sys
from nilearn import masking
import numpy as np
from hcp_corr import corrcoef_upper
import h5py
import numexpr as ne

def fisher_r2z(R):
    return ne.evaluate('arctanh(R)')

def mask_check(rest, mask):
	"""
	rest: 4D nifti-filename
	mask: 3D nifti-filename
	"""
	matrix = masking.apply_mask(rest, mask)
	matrix = matrix.T
	cnt_zeros = 0 
	for i in range(0, matrix.shape[0]):
		if np.count_nonzero(matrix[i, :]) == 0:
			cnt_zeros += 1
	return cnt_zeros, matrix

def mask_check_all_subjects(fname, data_dir, mask):
	"""
	fname: text file having subject_id's
	"""
	with open(fname) as f:
		content = f.readlines()
		sbj_list = [x.strip('\n') for x in content]

	for subject_id in sbj_list:
		rest = os.path.join(data_dir, subject_id,
	                            'preprocessed/func', 
	                            'rest_preprocessed2mni_sm.nii.gz')
		[cnt_zeros, matrix] = mask_check(rest, mask)
		print subject_id, cnt_zeros

def average_upper_matrix(fname, data_dir, out_file):
	"""
	fname: text file having subject_id's
	"""
	with open(fname) as f:
		content = f.readlines()
		sbj_list = [x.strip('\n') for x in content]
		
	i = 0
	N = len(sbj_list)
	for subject_id in sbj_list:
		A = os.path.join(data_dir, subject_id,
                                'preprocessed/func/connectivity',
                                '%s_corrUpper.h5' % subject_id)
		A_init = h5py.File(A, 'r')
		A_data = A_init.get('data')
		np.array(A_data)

                if i == 0:
			SUM = A_data
		else:
			SUM = ne.evaluate('SUM + A_data')
		i += 1
		print subject_id, SUM.shape
		
        SUM = ne.evaluate('SUM / N')
        h = h5py.File(out_file, 'w') 
        h.create_dataset("data", data=SUM)
        h.close()

	return SUM

# data dir's 
data_dir  = '/data/pt_mar006/subjects'

# text file having subject_id's
fname = '/data/pt_mar006/documents/cool_hc.txt'

# mask file
image_mask = os.path.join('/data/pt_mar006/subjects_group',
                          'mni3_rest_gm_mask.nii.gz')

# check if any of subjects has voxels, which has no signal
mask_check_all_subjects(fname, data_dir, image_mask)

# get average upper triangular of individual (fisher_r2z) correlations
out_file = '/data/pt_mar006/subjects_group/corrFisherR2Z_upper.h5'
ave_corr_fish_upper = average_upper_matrix(fname, data_dir, out_file)

# subject_id
subject_id = sys.argv[1]

image_rest = os.path.join(data_dir, subject_id, 
                          'preprocessed/func', 
                          'rest_preprocessed2mni_sm.nii.gz') 

[voxel_zeros, t_series] = mask_check(image_rest, image_mask)

if voxel_zeros != 0:
    print subject_id, " has zeros voxel!!!"
    sys.exit(1)

# Step 1: get correlation coefficients and Fisher r2z transform
corr_upper = corrcoef_upper(t_series)
corr_upper = fisher_r2z(corr_upper)

# define working dir 
work_dir = os.path.join(data_dir, subject_id,  
			'preprocessed/func/connectivity') 
os.chdir(work_dir)

h = h5py.File("%s_corrUpper.h5" %subject_id, 'w')
h.create_dataset("data", data=corr_upper)
h.close()

