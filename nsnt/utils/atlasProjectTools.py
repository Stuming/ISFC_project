# coding = utf-8

import os

import numpy as np
import nibabel as nib
import scipy.io as sio


class AslanConvert(object):
    def __init__(self, atlasdir, method, hemi):
        """
        Convert Aslan Group Parcellations tp other space.
        The result saves the same dir with raw *.mat file.

        Parameters
        ----------
        atlasdir: dir of atlas, should contain 'Parcellations_Aslan' folder from Aslan
            and 'standard_mesh_atlases' folder from HCP
        method: name of parcellation method under 'Parcellations_Aslan/Group'
            In particular, method='all' stands for convert all methods under Group dir.
            This parameter can be string or list of methods.
        hemi: hemi of file, should be one of ['L', 'R']

        Example
        -------
        >>>from nsnt.utils.atlasProjectTools import AslanConvert
        >>>myatlasdir = './'
        >>>tmp = ParcellationsAslanConvert(myatlasdir, 'AAL', 'L')
        >>>tmp.convert()  # just save to gifti format, in '32k_fs_LR' space
        >>>tmp.convert('fsaverage')  # save to gifti format and 'fsaverage' space
        """
        self.atlasdir = atlasdir
        self.hemi = hemi
        self.aslan_dir = os.path.join(atlasdir,
                                      'Parcellations_Aslan', 'Group')
        self.reference_dir = os.path.join(atlasdir,
                                          'standard_mesh_atlases/resample_fsaverage')
        self.mask_dir = os.path.join(atlasdir, 'Parcellations_Aslan', 'Scripts', 'surface')

        if method == 'all':
            methods = os.listdir(self.aslan_dir)
        elif isinstance(method, str):
            methods = [method]
        else:
            methods = method
        self.methods = methods

    def convert(self, target_space=None):
        """
        Convert parcellations to target space.
        target_space: should be one of ['fsaverage', 'fsaverage5', 'fsaverage6'] for now.
            If target_space is None, just store parcellations into gifti file.
        """
        mask = self._load_mask()
        for method in self.methods:
            parcels, resolution = self._load_data(method)
            self._save_gifti(parcels, resolution, mask)
            if target_space is not None:
                self._resample(resolution, target_space)

    def _load_mask(self):
        """
        Load mask of Aslan parcellations.

        Return
        ------
        mask: 1 for region of interest and 0 for not interested, shape=(n_vertices, ).
        """
        mask = nib.load(os.path.join(self.mask_dir,
                                     'Conte69.{}.atlasroi.32k_fs_LR.shape.gii'.format(self.hemi))).darrays[0].data
        return mask

    def _load_data(self, method):
        """
        Load Aslan parcellation data from .mat file.

        Return
        ------
        parcels: parcellation data, may contain multi-resolution data.
        resolution: corresponding to parcels.
        """
        prefix = '{0}/{0}_{1}'.format(method, self.hemi)
        if not os.path.exists(os.path.join(self.aslan_dir, '{}.mat'.format(prefix))):
            prefix = '{0}/{0}_1_{1}.mat'.format(method, self.hemi)
        self.prefix = prefix

        data = sio.loadmat(os.path.join(self.aslan_dir, '{}.mat'.format(prefix)))
        print(data['resolution'][0])
        parcels = data['parcels'].astype(np.uint8)
        resolution = data['resolution'][0]
        return parcels, resolution

    def _save_gifti(self, parcels, resolution, mask):
        """
        Save data to .label.gii file.

        Parameters
        ----------
        parcels: parcellation data, may contain multi-resolution data.
        resolution: corresponding to parcels.
        mask: 1 for region of interest and 0 for not interested, shape=(n_vertices, ).
        """
        labels = mask.copy()

        for i, res in enumerate(resolution):
            labels[np.where(mask == 1)[0]] = parcels[:, i]  # reshape parcels from (n, 1) to (n,)

            parcel_img = nib.gifti.gifti.GiftiImage(darrays=[nib.gifti.gifti.GiftiDataArray(labels)])
            savepath = os.path.join(self.aslan_dir, '{}_{}.label.gii'.format(self.prefix, res))
            nib.gifti.giftiio.write(parcel_img, savepath)
            print('Saving to {}'.format(savepath))

    def _resample(self, resolution, target_surf):
        hemi = self.hemi
        reference_dir = self.reference_dir
        aslan_dir = self.aslan_dir

        current_sphere = os.path.join(reference_dir,
                                      'fs_LR-deformed_to-fsaverage.{0}.sphere.32k_fs_LR.surf.gii'.format(hemi))
        current_area = os.path.join(reference_dir,
                                    'fs_LR.{0}.midthickness_va_avg.32k_fs_LR.shape.gii'.format(hemi))

        # TODO add more target_surf options.
        if target_surf == 'fsaverage5':
            tsurf = 'fs5'
            new_sphere = os.path.join(reference_dir,
                                      'fsaverage5_std_sphere.{0}.10k_fsavg_{0}.surf.gii'.format(hemi))
            new_area = os.path.join(reference_dir,
                                    'fsaverage5.{0}.midthickness_va_avg.10k_fsavg_{0}.shape.gii'.format(hemi))

        elif target_surf == 'fsaverage':
            tsurf = 'fs'
            new_sphere = os.path.join(reference_dir,
                                      'fsaverage_std_sphere.{0}.164k_fsavg_{0}.surf.gii'.format(hemi))
            new_area = os.path.join(reference_dir,
                                    'fsaverage.{0}.midthickness_va_avg.164k_fsavg_{0}.shape.gii'.format(hemi))

        elif target_surf == 'fsaverage6':
            tsurf = 'fs6'
            new_sphere = os.path.join(reference_dir,
                                      'fsaverage6_std_sphere.{0}.41k_fsavg_{0}.surf.gii'.format(hemi))
            new_area = os.path.join(reference_dir,
                                    'fsaverage6.{0}.midthickness_va_avg.41k_fsavg_{0}.shape.gii'.format(hemi))

        else:
            raise ValueError('target_surf is not supported.')

        for res in resolution:
            infile = os.path.join(aslan_dir, '{}_{}.label.gii'.format(self.prefix, res))
            outfile = os.path.join(aslan_dir, '{}_{}.{}.label.gii'.format(self.prefix, res, tsurf))

            # cs: current sphere, ns: new sphere
            # ca: current area, na: new area
            wb_command = 'wb_command -label-resample {infile} {cs} {ns} ' \
                         'ADAP_BARY_AREA {outfile} -area-metrics {ca} {na}'.format(infile=infile,
                                                                                   cs=current_sphere,
                                                                                   ns=new_sphere,
                                                                                   outfile=outfile,
                                                                                   ca=current_area,
                                                                                   na=new_area)
            os.system(wb_command)
            print('Saving to: {}'.format(outfile))
