# Ceres-plusplus

This package was written as an extension to the CERES reduction pipeline
(https://github.com/rabrahm/ceres) in the sense that it takes spectra reduced
by it and extracts some activity indicators (CCF FWHM, BIS, CONTRAST) and
calculates others (S index, Ha, HeI, NaID1D2)

It's been tested to work on FEROS and FIDEOS spectra. Feel free to use it with
other instruments and let me know if it works :)

## Installation

You can try running `pip install cerespp`

If that fails you can clone the repository with

```bash
$ git clone https://github.com/jvines/Ceres-plusplus
$ cd Ceres-plusplus
$ pip install .
```

## Dependencies

Ceres-plusplus depends on the following packages:

- numpy ([https://numpy.org/](https://numpy.org/))
- scipy ([https://www.scipy.org/](https://www.scipy.org/))
- matplotlib (for plotting, but it's optional for the core functionality) ([https://matplotlib.org/](https://matplotlib.org/))
- astropy ([https://www.astropy.org/](https://www.astropy.org/))
- PyAstronomy ([https://pyastronomy.readthedocs.io/en/latest/](https://pyastronomy.readthedocs.io/en/latest/))
- tqdm ([https://tqdm.github.io/](https://tqdm.github.io/))
- termcolor ([https://pypi.org/project/termcolor/](https://pypi.org/project/termcolor/))
- pandas ([https://pandas.pydata.org/](https://pandas.pydata.org/))

## Usage

Usage is simple, start by importing `cerespp`, optionally you can use `glob` to
fetch the files. After importing (and having ready your files) the
`get_activities` function, grab a coffee, and wait for your indicators!.

Below there's an example script

```python
import cerespp
import glob

files = glob.glob('path/to/fits/files/*.fits')

# Returns a pandas DataFrame and a header string
df, header = cerespp.get_activities(files, out='output/path/', save_activities=True)

# You can also run it without saving to disk
df, _ = cerespp.get_activities(files, save_activities=False)
print(df)
```

Here `files` is a list with the fits files to process. `cerespp` returns a `pandas.DataFrame` with the results.
You can optionally save the output to a file by setting `save_activities=True` and providing an `out` directory.

## Plotting

`cerespp` offers some plotting tools to visually check things! The most
important ones are plots showing the activity lines and their surroundings.
Creating these is easy:

```python
import cerespp
import glob

# These are the available lines. You can choose which ones to plot here 
lines = ['CaHK', 'Ha', 'HeI', 'NaID1D2'] 

files = glob.glob('path/to/fits/files/*.fits')

# This function creates the plots from a fits file directly
cerespp.line_plot_from_file(files[0], lines, 'output/path/', 'starname')
```

There's a notebook exemplifying the usage in the examples folder!

## How it works

`cerespp` first calculates a radial velocity to correct the spectrum to
rest-frame, after this has been done it extracts the available data from the
fits headers (CCF FWHM, BIS, CONTRAST) and finally it merges the echelle orders
and computes the activity indicators!

The radial velocity is computed using the standard cross-correlation function
method, and thus you can specify which mask to use with the `mask` keyword in
`get_activities`. Available masks are `G2, K0, K5,` and `M2`.
