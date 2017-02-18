import os, sys
import nipype.interfaces.ants as ants

# data dir's 
data_dir = '/nobackup/ilz2/bayrak/subjects'
mni_dir  = '/nobackup/ilz2/bayrak/subjects_group'
# subject id
subject_id = sys.argv[1]

# define working dir
work_dir = os.path.join(data_dir, subject_id, 'preprocessed/func') 
if not os.path.exists(work_dir):
	os.makedirs(work_dir)
# go into working dir
os.chdir(work_dir)


# get preprocessed functional data to be registered
img_rest = os.path.join(data_dir, subject_id,
			'preprocessed/func/', 'rest_preprocessed.nii.gz')



######### !!!!!!!!!!!!!!!!!!! ##############	
subject_dayX = subject_id[0:5] + 'd01'

# bbregister transform matrices (rest_dXX -->> T1_dXX)	
bbre_dir = os.path.join(data_dir, subject_id,
		        'preprocessed/func/coregister/transforms2anat')
# fsl-flirt transform matrices (T1_XX -->> T1_d00)
flirt_dir = os.path.join(data_dir, subject_id,
			 'preprocessed/anat/transforms2day01')
# ants transform matrices (T1_d00 -->> mni3mm)
ants_dir = os.path.join(data_dir, subject_dayX,  
			'preprocessed/anat/transforms2mni')

at			   = ants.ApplyTransforms()
at.inputs.input_image_type = 3
at.inputs.input_image      = img_rest
at.inputs.transforms	   = [os.path.join(ants_dir, 						   						   'transform1Warp.nii.gz'),
	      		      os.path.join(ants_dir, 						   						   'transform0GenericAffine.mat'),
			      os.path.join(flirt_dir,
				    'transform_dayX_itk.mat'),
	 		      os.path.join(bbre_dir, 						   						    'rest2anat_itk.mat')]
at.inputs.reference_image  = os.path.join(mni_dir, 
					  'MNI152_T1_3mm_brain.nii.gz')
at.inputs.interpolation    = 'BSpline'
at.inputs.invert_transform_flags = [False, False, False, False]
at.inputs.output_image     = os.path.abspath('rest_preprocessed2mni.nii.gz')
#print at.cmdline
at.run()
