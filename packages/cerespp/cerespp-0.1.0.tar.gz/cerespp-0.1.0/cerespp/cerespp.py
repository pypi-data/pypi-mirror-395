"""cerespp.

Main routine for ceres plusplus.

Author: Jose Vines
"""
import logging
import os
import sys

import numpy as np
import pandas as pd
from astropy.io import fits
from tqdm import tqdm

from .constants import *
from .spectra_utils import correct_to_rest
from .spectra_utils import merge_echelle
from .utils import create_dir
from .utils import get_line_flux

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def get_activities(files, out=None, mask='G2', save_echelle=False, save_activities=True, verbose=True):
    """Main function.

    Parameters
    ----------
    files: list
        A list with the spectra filenames.
    out: str, optional
        The output directory for the results. Required if save_activities is True.
    mask: str, optional
        The selected mask for calculating the RV. Options are G2, K0, K5 and M2.
    save_echelle: bool, optional
        Set to True to save the merged echelle spectra. Default is False.
    save_activities: bool, optional
        Set to True to save the activities to a file. Default is True.
    verbose: bool, optional
        Set to True to show progress bar. Default is True.

    Returns
    -------
    df: pandas.DataFrame
        A DataFrame with the activity indices.
    header: str
        A string with the activity indices identifiers (for backward compatibility).

    """
    nofwhm = False
    if out and (save_activities or save_echelle):
        create_dir(out)

    results = []

    hdul = fits.open(files[0])
    targ_name = hdul[0].header['HIERARCH TARGET NAME']
    inst = hdul[0].header['INST'].lower()
    hdul.close()

    iterator = tqdm(files) if verbose else files

    for fname in iterator:
        S, sS, Halpha, sHalpha = -999, -999, -999, -999
        HelI, sHelI, NaID1D2, sNaID1D2 = -999, -999, -999, -999
        
        try:
            hdul = fits.open(fname)
            data = hdul[0].data
            header_vals = hdul[0].header
            
            # Extract header info
            bjd_val = header_vals.get('BJD_OUT', np.nan)
            bis_val = header_vals.get('BS', np.nan)
            bis_err_val = header_vals.get('BS_E', np.nan)
            contrast_val = header_vals.get('XC_MIN', np.nan)
            
            fwhm_val = np.nan
            fwhm_err_val = np.nan
            
            if 'FWHM' in header_vals:
                fwhm_val = header_vals['FWHM']
                fwhm_err_val = header_vals['DISP'] / header_vals['SNR']
            else:
                nofwhm = True

            hdul.close()

            w, f = correct_to_rest(data, mask=mask)

            prod = np.stack((w, f, data[2, :, :], data[8, :, :]))

            # Handle out for merge_echelle
            merge_out = out if out else ""
            waves, fluxes, errors, sn = merge_echelle(prod, header_vals,
                                                      out=merge_out, save=save_echelle)

            # Get S index. FIDEOS doesn't reach Ca HK
            if inst not in s_exceptions:
                # First is CaV
                NV, sNV = get_line_flux(waves, fluxes, CaV, 20, filt='square',
                                        error=errors)

                # Now CaR
                NR, sNR = get_line_flux(waves, fluxes, CaR, 20,
                                        filt='square', error=errors)

                # Now CaK
                NK, sNK = get_line_flux(waves, fluxes, CaK, 1.09,
                                        filt='triangle', error=errors)

                # Now CaH
                NH, sNH = get_line_flux(waves, fluxes, CaH, 1.09,
                                        filt='triangle', error=errors)

                S = (NH + NK) / (NR + NV)
                sSnum = np.sqrt(sNH ** 2 + sNK ** 2)
                sSden = np.sqrt(sNV ** 2 + sNR ** 2)
                sS = np.sqrt((sSnum / (NH + NK)) ** 2 + (sSden / (NR + NV)) ** 2)

            # Now Halpha
            FHa, sFHa = get_line_flux(waves, fluxes, Ha, 0.678,
                                      filt='square', error=errors)

            # Now F1
            F1, sF1 = get_line_flux(waves, fluxes, 6550.87,
                                    10.75, filt='square', error=errors)

            # Now F2
            F2, sF2 = get_line_flux(waves, fluxes, 6580.309,
                                    8.75, filt='square', error=errors)

            Halpha = FHa / (0.5 * (F1 + F2))
            sden = np.sqrt(sF1 ** 2 + sF2 ** 2)
            sHalpha = np.sqrt((sFHa / FHa) ** 2 + (sden / (F1 + F2)) ** 2)

            # Now HeI
            FHeI, sFHeI = get_line_flux(waves, fluxes, HeI, 0.2,
                                        filt='square', error=errors)

            # Now F1
            F1, sF1 = get_line_flux(waves, fluxes, 5874.5,
                                    0.5, filt='square', error=errors)

            # Now F2
            F2, sF2 = get_line_flux(waves, fluxes, 5879,
                                    0.5, filt='square', error=errors)

            HelI = FHeI / (0.5 * (F1 + F2))
            sden = np.sqrt(sF1 ** 2 + sF2 ** 2)
            sHelI = np.sqrt((sFHeI / FHeI) ** 2 + (sden / (F1 + F2)) ** 2)

            # Now NaI D1 D2
            D1, sD1 = get_line_flux(waves, fluxes, NaID1, 1,
                                    filt='square', error=errors)

            D2, sD2 = get_line_flux(waves, fluxes, NaID2, 1,
                                    filt='square', error=errors)

            L, sL = get_line_flux(waves, fluxes, 5805, 10, filt='square',
                                  error=errors)

            R, sR = get_line_flux(waves, fluxes, 6090, 20, filt='square',
                                  error=errors)

            NaID1D2 = (D1 + D2) / (R + L)
            sNanum = np.sqrt(sD1 ** 2 + sD2 ** 2)
            sNaden = np.sqrt(sL ** 2 + sR ** 2)
            sNaID1D2 = np.sqrt((sNanum / (D1 + D2)) ** 2 + (sNaden / (R + L)) ** 2)

            # Append results
            row = {
                'bjd': bjd_val,
                'S': S, 'e_S': sS,
                'Halpha': Halpha, 'e_Halpha': sHalpha,
                'HeI': HelI, 'e_HeI': sHelI,
                'NaID1D2': NaID1D2, 'e_NaID1D2': sNaID1D2,
                'BIS': bis_val, 'e_BIS': bis_err_val,
                'CONTRAST': contrast_val
            }
            if not nofwhm:
                row['FWHM'] = fwhm_val
                row['e_FWHM'] = fwhm_err_val
            
            results.append(row)

        except Exception as e:
            logger.error(f"Error processing {fname}: {e}")
            continue

    df = pd.DataFrame(results)

    # Reorder columns to match original output if possible
    cols = ['bjd', 'S', 'e_S', 'Halpha', 'e_Halpha', 'HeI', 'e_HeI', 
            'NaID1D2', 'e_NaID1D2', 'BIS', 'e_BIS']
    if not nofwhm:
        cols.extend(['FWHM', 'e_FWHM'])
    cols.append('CONTRAST')
    
    # Ensure all columns exist (in case of empty results)
    for col in cols:
        if col not in df.columns:
            df[col] = np.nan
            
    df = df[cols]

    header_str = " ".join(cols)

    if save_activities and out:
        out_file = os.path.join(out, f'{targ_name}_activities.dat')
        # Save as whitespace separated to maintain backward compatibility
        # But maybe we should also support CSV? For now, stick to original format.
        # Using pandas to save
        df.to_csv(out_file, sep=' ', index=False, header=header_str.split())
        logger.info(f"Activities saved to {out_file}")

    return df, header_str