from canopy.core.field import Field
from canopy.sources.source_abc import Source
from canopy.sources.registry import register_source
from canopy.source_data import get_source_data
from types import MappingProxyType
import itertools
import warnings

FREQS = {'HH': 'Half-hourly', 'HR': 'Hourly', 'DD': 'Daily', 'WW': 'Weekly', 'MM': 'Monthly', 'YY': 'Yearly', }

FIELDS = {
    'H': 'Sensible Heat Flux',
    'LE': 'Latent Heat Flux',
    'G': 'Ground Surface Heat Flux',
    'NEE': 'Net Ecosystem Exchange',
    'RECO': 'Ecosystem Respiration',
    'GPP': 'Gross Primary Producion',
}

FIELD_COLS = {
    'H': ('H_F_MDS', 'H_F_MDS_QC', 'H_CORR', 'H_CORR_25', 'H_CORR_75', 'H_RANDUNC'),
    'H_longfreq': ('H_F_MDS', 'H_F_MDS_QC', 'H_CORR', 'H_RANDUNC'),
    'LE': ('LE_F_MDS', 'LE_F_MDS_QC', 'LE_CORR', 'LE_CORR_25', 'LE_CORR_75', 'LE_RANDUNC'),
    'LE_longfreq': ('LE_F_MDS', 'LE_F_MDS_QC', 'LE_CORR', 'LE_RANDUNC'),
    'G': ('G_F_MDS', 'G_F_MDS_QC'),
    'NEE': (
        'NEE_VUT_REF', 'NEE_VUT_REF_QC', 'NEE_VUT_REF_RANDUNC',
        'NEE_VUT_05', 'NEE_VUT_16', 'NEE_VUT_25', 'NEE_VUT_50', 'NEE_VUT_75', 'NEE_VUT_84', 'NEE_VUT_95', 
        'NEE_VUT_05_QC', 'NEE_VUT_16_QC', 'NEE_VUT_25_QC', 'NEE_VUT_50_QC', 'NEE_VUT_75_QC', 'NEE_VUT_84_QC', 'NEE_VUT_95_QC', 
    ),
    'RECO': (
        'RECO_NT_VUT_REF', 'RECO_DT_VUT_REF',
        'RECO_NT_VUT_05', 'RECO_NT_VUT_16', 'RECO_NT_VUT_25', 'RECO_NT_VUT_50', 'RECO_NT_VUT_75', 'RECO_NT_VUT_84', 'RECO_NT_VUT_95', 
        'RECO_DT_VUT_05', 'RECO_DT_VUT_16', 'RECO_DT_VUT_25', 'RECO_DT_VUT_50', 'RECO_DT_VUT_75', 'RECO_DT_VUT_84', 'RECO_DT_VUT_95', 
        'RECO_SR', 'RECO_SR_N',
    ),
    'GPP': (
        'GPP_NT_VUT_REF', 'GPP_DT_VUT_REF',
        'GPP_NT_VUT_05', 'GPP_NT_VUT_16', 'GPP_NT_VUT_25', 'GPP_NT_VUT_50', 'GPP_NT_VUT_75', 'GPP_NT_VUT_84', 'GPP_NT_VUT_95', 
        'GPP_DT_VUT_05', 'GPP_DT_VUT_16', 'GPP_DT_VUT_25', 'GPP_DT_VUT_50', 'GPP_DT_VUT_75', 'GPP_DT_VUT_84', 'GPP_DT_VUT_95', 
    )
}


def _get_field_cols(field_name: str, freq: str):
    if field_name in ['H', 'LE'] and freq in ['WW', 'MM', 'YY']:
        field_name += '_longfreq'
    return FIELD_COLS[field_name]


def _select_fluxnet_sites(site_codes: list, source_data: dict):

    valid_sites = []
    invalid_sites = []
    for sc in site_codes:
        if sc in source_data['sites']:
            valid_sites.append(sc)
        else:
            invalid_sites.append(sc)

    return valid_sites, invalid_sites


@register_source('fluxnet2015')
class SourceFluxnet2015(Source):
    """
    Source object for Fluxnet2015 data
    """

    def __init__(self, path, sites=None) -> None:
        super().__init__(path, get_source_data('fluxnet2015'))

        # TODO: possible duplication with file reader fuction (readers.fluxnet2015())
        site_codes_directory = [fname.name[4:10].lower() for fname in self.path.glob(f"FLX_*FLUXNET2015*.zip")]

        valid_sites_directory, invalid_sites_directory = _select_fluxnet_sites(site_codes_directory, self.source_data)
        if len(invalid_sites_directory) > 0:
            warnings.warn(f"The following site files were found in '{path}', but are not valid FLUXNET2015 sites: {invalid_sites_directory}.")
        if len(valid_sites_directory) == 0:
            raise ValueError(f"No valid FLUXNET2015 files found in '{path}'.")

        if sites is None:
            site_list = valid_sites_directory
        else:
            valid_sites_passed, invalid_sites_passed = _select_fluxnet_sites(sites, self.source_data)

            if len(invalid_sites_passed) > 0:
                warnings.warn(f"The following sites are not valid FLUXNET2015 sites {invalid_sites_passed}.")
            if len(valid_sites_passed) == 0:
                raise ValueError(f"No valid FLUXNET2015 files passed.")
            
            vset_directory = set(valid_sites_directory)
            vset_passed = set(valid_sites_passed)
            not_in_directory = list(vset_passed - vset_directory)
            if len(not_in_directory) > 0:
                warnings.warn(f"No file found in '{path}' for the following sites: {not_in_directory}.")

            site_list = list(vset_directory & vset_passed)
            if len(site_list) == 0:
                raise ValueError(f"No files for any of the selected sites found in '{path}'.")
            
        self._sites = {}
        for site in sorted(site_list):
            self._sites[site] = (self.source_data['sites'][site]['longitude'], self.source_data['sites'][site]['latitude'])

        for field_name, freq in itertools.product(FIELDS, FREQS):
            field_id = f"{field_name}_{freq}"
            self._fields[field_id] = None
            self.is_loaded[field_id] = False
    

    @property
    def sites(self):
        return MappingProxyType(self._sites)


    def load_field(self, field_id: str) -> Field:

        field_id = field_id.upper()
        if field_id not in self.fields:
            raise KeyError(f"Field '{field_id}' not found in source.")
        field_name, freq = field_id.split('_')

        field_cols = _get_field_cols(field_name, freq)
        field = Field.from_file(self.path,
                                file_format='fluxnet2015',
                                grid_type='sites',
                                cols=field_cols,
                                freq=freq,
                                sites=self.sites)

        field.add_md('source', self.source)
        field.set_md('name', self.source_data['fields'][field_id]['name'])
        field.set_md('description', self.source_data['fields'][field_id]['description'])
        field.set_md('units', self.source_data['fields'][field_id]['units'])

        self.is_loaded[field_id] = True
        self._fields[field_id] = field

        name_dict = {}
        # The constructor ensures that all sites in self.sites exist in the source
        for site in self.sites:
            name_dict[(self.source_data['sites'][site]['longitude'], self.source_data['sites'][site]['latitude'])] = site
        field.grid.assign_names(name_dict)

        return field


    def get_gridlist(self, fname: str = None) -> str | None:

        gridlist = []
        for site in self.sites:
            gridlist.append(f"{self.source_data['sites'][site]['longitude']} {self.source_data['sites'][site]['latitude']} {site}")

        if fname is not None:
            with open(fname, 'w') as f:
                f.write("\n".join(gridlist))
        else:
            return "\n".join(gridlist)

