"""
non-linear registration from T1 to MNI
"""
import os
import nipype.interfaces.ants as ants

data_dir = '/scr/ilz2/bayrak/TEST/01_ants'


ants_anat2mni = ants.Registration(dimension=3,
                    transforms=['Rigid','Affine','SyN'],
                    metric=['MI','MI','CC'],
                    metric_weight=[1,1,1],
                    number_of_iterations=[[1000,500,250,100],[1000,500,250,100],[100,70,50,20]],
                    convergence_threshold=[1e-6,1e-6,1e-6],
                    convergence_window_size=[10,10,10],
                    shrink_factors=[[8,4,2,1],[8,4,2,1],[8,4,2,1]],
                    smoothing_sigmas=[[3,2,1,0],[3,2,1,0],[3,2,1,0]],
                    sigma_units=['vox','vox','vox'],
                    initial_moving_transform_com=1,
                    transform_parameters=[(0.1,),(0.1,),(0.1,3.0,0.0)],
                    sampling_strategy=['Regular', 'Regular', 'None'],
                    sampling_percentage=[0.25,0.25,1],
                    radius_or_number_of_bins=[32,32,4],
                    num_threads=1,
                    interpolation='Linear',
                    winsorize_lower_quantile=0.005,
                    winsorize_upper_quantile=0.995,
                    collapse_output_transforms=True,
                    output_inverse_warped_image=True,
                    #output_warped_image=True,
                    use_histogram_matching=True)

ants_anat2mni.inputs.fixed_image = os.path.join(data_dir,
						 'MNI152_T1_1mm_brain.nii.gz')

ants_anat2mni.inputs.moving_image = os.path.join(data_dir, 
						'brain_RPI.nii.gz')

ants_anat2mni.inputs.output_warped_image = os.path.join(data_dir, 
							'brain_RPI_mni.nii.gz')

ants_anat2mni.run()


