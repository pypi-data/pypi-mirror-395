#!/usr/bin/env python
# File              : Ampel-LSST/ampel/lsst/alert/load/ElasticcTrainingsetLoader.py
# License           : BSD-3-Clause
# Author            : J Nordin <jno@physik.hu-berlin.de>
# Date              : 09.06.2022
# Last Modified Date: 22.06.2022
# Last Modified By  : J Nordin <jno@physik.hu-berlin.de>

import codecs
from collections.abc import Callable, Mapping, Sequence
from itertools import islice
from typing import Any, cast

import sncosmo
from astropy.table import Table

from ampel.abstract.AbsAlertLoader import AbsAlertLoader

# These can vary for different models, and more might be needed.
meta_dcast: dict[str, Callable[[bytes], Any]] = {
    "SNID": codecs.decode,
    "IAUC": codecs.decode,
    "FAKE": int,
    "RA": float,
    "DEC": float,
    "PIXSIZE": float,
    "NXPIX": int,
    "NYPIX": int,
    "SNTYPE": int,
    "NOBS": int,
    "PTROBS_MIN": int,
    "PTROBS_MAX": int,
    "MWEBV": float,
    "MWEBV_ERR": float,
    "REDSHIFT_HELIO": float,
    "REDSHIFT_HELIO_ERR": float,
    "REDSHIFT_FINAL": float,
    "REDSHIFT_FINAL_ERR": float,
    "VPEC": float,
    "VPEC_ERR": float,
    "HOSTGAL_NMATCH": int,
    "HOSTGAL_NMATCH2": int,
    "HOSTGAL_OBJID": int,
    "HOSTGAL_FLAG": int,
    "HOSTGAL_PHOTOZ": float,
    "HOSTGAL_PHOTOZ_ERR": float,
    "HOSTGAL_SPECZ": float,
    "HOSTGAL_SPECZ_ERR": float,
    "HOSTGAL_RA": float,
    "HOSTGAL_DEC": float,
    "HOSTGAL_SNSEP": float,
    "HOSTGAL_DDLR": float,
    "HOSTGAL_CONFUSION": float,
    "HOSTGAL_LOGMASS": float,
    "HOSTGAL_LOGMASS_ERR": float,
    "HOSTGAL_LOGSFR": float,
    "HOSTGAL_LOGSFR_ERR": float,
    "HOSTGAL_LOGsSFR": float,
    "HOSTGAL_LOGsSFR_ERR": float,
    "HOSTGAL_COLOR": float,
    "HOSTGAL_COLOR_ERR": float,
    "HOSTGAL_ELLIPTICITY": float,
    "HOSTGAL_OBJID2": int,
    "HOSTGAL_SQRADIUS": float,
    "HOSTGAL_OBJID_UNIQUE": int,
    "HOSTGAL_ZPHOT_Q000": float,
    "HOSTGAL_ZPHOT_Q010": float,
    "HOSTGAL_ZPHOT_Q020": float,
    "HOSTGAL_ZPHOT_Q030": float,
    "HOSTGAL_ZPHOT_Q040": float,
    "HOSTGAL_ZPHOT_Q050": float,
    "HOSTGAL_ZPHOT_Q060": float,
    "HOSTGAL_ZPHOT_Q070": float,
    "HOSTGAL_ZPHOT_Q080": float,
    "HOSTGAL_ZPHOT_Q090": float,
    "HOSTGAL_ZPHOT_Q100": float,
    "HOSTGAL_MAG_u": float,
    "HOSTGAL_MAG_g": float,
    "HOSTGAL_MAG_r": float,
    "HOSTGAL_MAG_i": float,
    "HOSTGAL_MAG_z": float,
    "HOSTGAL_MAG_Y": float,
    "HOSTGAL_MAGERR_u": float,
    "HOSTGAL_MAGERR_g": float,
    "HOSTGAL_MAGERR_r": float,
    "HOSTGAL_MAGERR_i": float,
    "HOSTGAL_MAGERR_z": float,
    "HOSTGAL_MAGERR_Y": float,
    "HOSTGAL2_OBJID": int,
    "HOSTGAL2_FLAG": int,
    "HOSTGAL2_PHOTOZ": float,
    "HOSTGAL2_PHOTOZ_ERR": float,
    "HOSTGAL2_SPECZ": float,
    "HOSTGAL2_SPECZ_ERR": float,
    "HOSTGAL2_RA": float,
    "HOSTGAL2_DEC": float,
    "HOSTGAL2_SNSEP": float,
    "HOSTGAL2_DDLR": float,
    "HOSTGAL2_LOGMASS": float,
    "HOSTGAL2_LOGMASS_ERR": float,
    "HOSTGAL2_LOGSFR": float,
    "HOSTGAL2_LOGSFR_ERR": float,
    "HOSTGAL2_LOGsSFR": float,
    "HOSTGAL2_LOGsSFR_ERR": float,
    "HOSTGAL2_COLOR": float,
    "HOSTGAL2_COLOR_ERR": float,
    "HOSTGAL2_ELLIPTICITY": float,
    "HOSTGAL2_OBJID2": int,
    "HOSTGAL2_SQRADIUS": float,
    "HOSTGAL2_OBJID_UNIQUE": int,
    "HOSTGAL2_MAG_u": float,
    "HOSTGAL2_MAG_g": float,
    "HOSTGAL2_MAG_r": float,
    "HOSTGAL2_MAG_i": float,
    "HOSTGAL2_MAG_z": float,
    "HOSTGAL2_MAG_Y": float,
    "HOSTGAL2_MAGERR_u": float,
    "HOSTGAL2_MAGERR_g": float,
    "HOSTGAL2_MAGERR_r": float,
    "HOSTGAL2_MAGERR_i": float,
    "HOSTGAL2_MAGERR_z": float,
    "HOSTGAL2_MAGERR_Y": float,
    "HOSTGAL2_ZPHOT_Q000": float,
    "HOSTGAL2_ZPHOT_Q010": float,
    "HOSTGAL2_ZPHOT_Q020": float,
    "HOSTGAL2_ZPHOT_Q030": float,
    "HOSTGAL2_ZPHOT_Q040": float,
    "HOSTGAL2_ZPHOT_Q050": float,
    "HOSTGAL2_ZPHOT_Q060": float,
    "HOSTGAL2_ZPHOT_Q070": float,
    "HOSTGAL2_ZPHOT_Q080": float,
    "HOSTGAL2_ZPHOT_Q090": float,
    "HOSTGAL2_ZPHOT_Q100": float,
    "HOSTGAL_SB_FLUXCAL_u": float,
    "HOSTGAL_SB_FLUXCAL_g": float,
    "HOSTGAL_SB_FLUXCAL_r": float,
    "HOSTGAL_SB_FLUXCAL_i": float,
    "HOSTGAL_SB_FLUXCAL_z": float,
    "HOSTGAL_SB_FLUXCAL_Y": float,
    "PEAKMJD": float,
    "MJD_TRIGGER": float,
    "MJD_DETECT_FIRST": float,
    "MJD_DETECT_LAST": float,
    "SEARCH_TYPE": int,
    "SIM_MODEL_NAME": codecs.decode,
    "SIM_MODEL_INDEX": int,
    "SIM_TYPE_INDEX": int,
    "SIM_TYPE_NAME": codecs.decode,
    "SIM_TEMPLATE_INDEX": int,
    "SIM_LIBID": int,
    "SIM_NGEN_LIBID": int,
    "SIM_NOBS_UNDEFINED": int,
    "SIM_SEARCHEFF_MASK": int,
    "SIM_REDSHIFT_HELIO": float,
    "SIM_REDSHIFT_CMB": float,
    "SIM_REDSHIFT_HOST": float,
    "SIM_REDSHIFT_FLAG": int,
    "SIM_VPEC": float,
    "SIM_HOSTLIB_GALID": int,
    "SIM_HOSTLIB(LOGMASS_TRUE)": float,
    "SIM_HOSTLIB(LOG_SFR)": float,
    "SIM_DLMU": float,
    "SIM_LENSDMU": float,
    "SIM_RA": float,
    "SIM_DEC": float,
    "SIM_MWEBV": float,
    "SIM_PEAKMJD": float,
    "SIM_MAGSMEAR_COH": float,
    "SIM_AV": float,
    "SIM_RV": float,
    "SIM_SALT2x0": float,
    "SIM_SALT2x1": float,
    "SIM_SALT2c": float,
    "SIM_SALT2mB": float,
    "SIM_SALT2alpha": float,
    "SIM_SALT2beta": float,
    "SIM_SALT2gammaDM": float,
    "SIM_PEAKMAG_u": float,
    "SIM_PEAKMAG_g": float,
    "SIM_PEAKMAG_r": float,
    "SIM_PEAKMAG_i": float,
    "SIM_PEAKMAG_z": float,
    "SIM_PEAKMAG_Y": float,
    "SIM_EXPOSURE_u": float,
    "SIM_EXPOSURE_g": float,
    "SIM_EXPOSURE_r": float,
    "SIM_EXPOSURE_i": float,
    "SIM_EXPOSURE_z": float,
    "SIM_EXPOSURE_Y": float,
    "SIM_GALFRAC_u": float,
    "SIM_GALFRAC_g": float,
    "SIM_GALFRAC_r": float,
    "SIM_GALFRAC_i": float,
    "SIM_GALFRAC_z": float,
    "SIM_GALFRAC_Y": float,
    "SIM_SUBSAMPLE_INDEX": int,
    "SIM_TEMPLATEMAG_u": float,
    "SIM_TEMPLATEMAG_g": float,
    "SIM_TEMPLATEMAG_r": float,
    "SIM_TEMPLATEMAG_i": float,
    "SIM_TEMPLATEMAG_z": float,
    "SIM_TEMPLATEMAG_Y": float,
    "SIM_HOSTLIB(g_obs)": float,
    "SIM_HOSTLIB(r_obs)": float,
    "SIM_HOSTLIB(i_obs)": float,
    "SIM_MJD_EXPLODE": float,
    "AGN_PARAM(M_BH)": float,
    "AGN_PARAM(Mi)": float,
    "AGN_PARAM(edd_ratio)": float,
    "AGN_PARAM(edd_ratio2)": float,
    "AGN_PARAM(t_transition)": float,
    "AGN_PARAM(cl_flag)": float,
}

# Some meta key names were also changed between the training set and
# the test stream. We here try to track and change these
meta_namechange = {
    "dec": "decl",
    "redshift_final": "z_final",
    "redshift_final_err": "z_final_err",
    "hostgal_specz": "hostgal_zspec",
    "hostgal_specz_err": "hostgal_zspec_err",
    "hostgal_photoz": "hostgal_zphot",
    "hostgal_photoz_err": "hostgal_zphot_err",
    "hostgal_mag_y": "hostgal_mag_Y",
    "hostgal_magerr_y": "hostgal_magerr_Y",
    "hostgal2_specz": "hostgal_zspec",
    "hostgal2_specz_err": "hostgal_zspec_err",
    "hostgal2_photoz": "hostgal_zphot",
    "hostgal2_photoz_err": "hostgal_zphot_err",
    "hostgal2_magerr_y": "hostgal2_magerr_Y",
}


class ElasticcLcIterator:
    """
    Iterator returns the next alert which would be generated from a lightcurve.

    First idea:
    - lightcurve is assumed to be an ELAsTICC AstropyTable where 'SIM_MAGOBS'
    determines whether an alert was generated (otherwise 99)
    Does not work, looks like all datapoints after the first detection have
    SIM_MAGOBS.

    Second idea:
    - Straightforward significance. Need a [significance] detection to trigger
    an alert.

    """

    detection_sigma: float = 5.0

    def __init__(
        self,
        lightcurve: Table,
        cut_col: None | Sequence[str] = None,
        decode_col: None | Sequence[str] = None,
        change_col: None | Mapping[str, str] = None,
    ):
        self.lightcurve = lightcurve
        self.lightcurve.sort(
            "MJD"
        )  # Prob already done, but critical for usage.
        self.lightcurve.remove_columns(cut_col or [])
        for dcol in decode_col or []:
            # self.lightcurve[dcol] = self.lightcurve[dcol].astype(str)
            # Reading fits like this also cause trailing whitespaces, so instead
            self.lightcurve[dcol] = [
                str(s).rstrip() for s in self.lightcurve[dcol]
            ]
        if change_col:
            for oldname, newname in change_col.items():
                self.lightcurve.rename_column(oldname, newname)

        # Typecast meta and change to lower case
        self.lightcurve.meta = {
            k.lower(): meta_dcast[k](v)
            if (k in meta_dcast and v is not None)
            else v
            for k, v in self.lightcurve.meta.items()
        }

        # Rename fields
        for oldkey, newkey in meta_namechange.items():
            if oldkey in self.lightcurve.meta:
                self.lightcurve.meta[newkey] = self.lightcurve.meta.pop(oldkey)

        # Guess whether this is an alert
        self.lightcurve["cause_alert"] = self.lightcurve["PHOTFLAG"] >= 4096

        # Determine the corresponding indices for which alerts will be generated
        self.alert_index = [
            i for i, x in enumerate(self.lightcurve["cause_alert"]) if x
        ]

    def __iter__(self):
        return self

    def __next__(self) -> Table:
        if len(self.alert_index) == 0:
            raise StopIteration

        return self.lightcurve[0 : self.alert_index.pop(0) + 1]


class ElasticcTrainingsetLoader(AbsAlertLoader[Table]):
    """
    Load alerts from the ELAsTICC training set lightcurves.
    These are assumed to be distributed in "SNANA" fits format:
    - Simulated based on models.
    - Two connected files ({file_path}_HEAD.FITS.gz, {file_path}_PHOT.FITS.gz)
    - A PHOT file contains *full* lightcurves of transients.
    - Each *lightcurve* will be broken into individual alerts.

    Todo: Remove meta fields with NaN values (None, -9, -99, ...)
    Not sure I know exactly how these are allocated, so skipping for now.

    """

    skip_transients: int = 0
    file_path: str

    cut_col: Sequence[str] = [
        "CCDNUM",
        "FIELD",
        "PHOTPROB",
        "PSF_SIG2",
        "PSF_RATIO",
        "SKY_SIG_T",
        "XPIX",
        "YPIX",
        "SIM_FLUXCAL_HOSTERR",
    ]
    decode_col: Sequence[str] = ["BAND"]
    change_col: dict[str, str] = {
        "MJD": "midpointMjdTai",
        "BAND": "band",
        "FLUXCAL": "psfFlux",
        "FLUXCALERR": "psfFluxErr",
    }

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.lightcurves = iter(
            cast(
                list[Table],
                sncosmo.read_snana_fits(
                    self.file_path + "_HEAD.FITS.gz",
                    self.file_path + "_PHOT.FITS.gz",
                ),
            )
        )

        if self.skip_transients != 0:
            next(
                islice(
                    self.lightcurves,
                    self.skip_transients,
                    self.skip_transients,
                ),
                None,
            )

        self.next_lightcurve()

    def next_lightcurve(self) -> None:
        self.lciter = ElasticcLcIterator(
            next(self.lightcurves),
            cut_col=self.cut_col,
            change_col=self.change_col,
            decode_col=self.decode_col,
        )
        # Check for lcs without alerts
        while len(self.lciter.alert_index) == 0:
            self.lciter = ElasticcLcIterator(
                next(self.lightcurves),
                cut_col=self.cut_col,
                change_col=self.change_col,
                decode_col=self.decode_col,
            )

    def __iter__(self):
        return self

    def __next__(self) -> Table:
        try:
            return next(self.lciter)
        except StopIteration:
            self.next_lightcurve()
            return next(self.lciter)
