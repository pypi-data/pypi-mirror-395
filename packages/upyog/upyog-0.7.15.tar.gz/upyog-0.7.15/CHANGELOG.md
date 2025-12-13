## Unreleased
* New `Dictionary` class for dot access
* ML util to compare 1d vectors

## 0.7.14 -- 4 Sep 2024
* Improve image downloader to skip already downloaded files

## 0.7.13 -- 4 Sep 2024
* Add simple utils: `is_collection`, `load_txt`
* Cleanup imports in some places
* Add image downloader tool
* Add tar archive extractor tool


## 0.7.12 -- 8 Jul 2024
* Patch `.to_base64()` to `PIL.Image.Image` class to return a base64 encoded string to use in sending images over http requests

## 0.7.11 -- 2 Jul 2024
* Add `restore_symlink`
* Strict imports for `upyog.os.utils`


## 0.7.10 -- 26 Jun 2024
* Bugfixes
* `image_to_base64` util to convert PIL -> base64 strings
* UMAP tools: `upyog.ml.umap`
* Add `upyog.ann.CosineSimilarityQueryRunner` for exploring cosine similarity between embeddings
* Refactor `make_img_grid`
* `resize_with_padding` updated for new Pillow versions
* `upyog.os.cli.move_files` has the option to randomly sample input files


## 0.7.7 -- 28 Aug 2023
* Make pil interpolation map an internal attribute, as this API doesn't work with PIL-SIMD 9.0

## 0.7.5 -- 17 Aug 2023
* Utils
  * get filename from url
* ML
  * add PIL preprocessing types to `PreprocessingParams`
  * added `SoftmaxProcessor` and `SigmoidProcessor`
* Other
  * Add `tqdm` dependency

## 0.7.4 -- 12 Jul 2023
* Include font distributed with package

## 0.7.3 -- 5 July 2023
* Minor changes
* Update dependency

## 0.7.2 -- 25 May 2023
* Font path bugfix...
* Port over more ML utilities to `upyog.ml`

## 0.7.1 -- 17 May 2023
* Rename `InferenceDataset` to `ImageInferenceDataset`
* Clean up imports
* Add some more ML functionality from private packages

## 0.7.0 -- 17 May 2023
* Improve `move-files` and `generate-image-grid` CLI programs
* Add new `ml` sub-package, copying over a bunch of common utilities across multiple private libraries

## 0.6.2 -- 11 Apr 2023
* Myriad bugfixes

## 0.6.1 -- 6 Mar 2023
* Fix default font path (hacky but works)
* Bugfix `write_json`
* Add `title` func to `Visualiser`
* Add `write_text`

## 0.5.9 -- 31 January 2023
* `print_df` now accepts a dict as input also
* Add `write_json`
* cleaner imports in the `upyog.cli` module

## 0.5.8 -- 31 October 2022
* Bugfixes
* Simplify printing `pd.DataFrame` (not using `rich` anymore)
* Additional utility functions related to dates

## 0.5.6 -- 31 October 2022
* Save image with Exif metadata
* Convert bytes -> human readable sizes
* Check corrupted images
* Convert items to list/tuple
* Init everything via `from upyog.all import *`
* Pretty DataFrame printing


## 0.5.5 -- 1 September 2022
* Add a bunch of utilities related to iterating in `utils.utils`
* `make_img_grid` in non-verbose mode... finally


## 0.5.4 -- 8 August 2022
* Add `upyog.utils.zip` -- utilities to easily zip files / folders in Python

## 0.5.1 -- 8 August 2022

* Added `nb2script` command line tool (copied over from the earliest nbdev mockup that worked on individual notebooks)
* Respect `PIL.Image.mode` after doing operations (not thoroughly tested). Previously we converted everything to RGB mode
* Classmethod for instantiating a `Visualiser`
* Load truncated images by default
* Added simple bbox utils for xyxy <-> xywh conversions
* Add `get_YYYY_MM_DD` convenience function
* Add `get_file_size` util
* Add patched methods to `pathlib.Path`:
  * `list_files()`
  * `ls()`
* Downloading utils copied over from `torchvision`

## 0.4.3 -- 25 March 2022

* Added `border_width` param (unexposed) to `opyog.image.draw._write_text`
* Added `find-common-files-between-folders` program

## 0.4.2 -- 2 Mar 2022
- `Visualiser` classmethods to init from RGB/BGR `np.ndarray`
- Allow `Visualiser.draw_bbox` without a `label`
- Improve error handling for all methods that accept `xy` or `xyxy` to ensure we have correct `len(xy|xyxy)`

## 0.4.1 -- 27 Jan 2022
- Adjust font path, export font with package

## 0.4 -- 27 Jan 2022

### New Features
Add `upyog.ann` - a subpackage that has interfaces to artificial
nearest neighbor libraries.
  - Added `AnnoyIndexer` and `AnnoyDataFrameIndexer`

### Enhancements
- Improve `upyog.utils.utils.flatten` to work with any iterable

## 0.3.2 -- 19th Jan 2022

- Bugfixes:
  - `move-files`
  - `generate-image-grid`

## 0.3.0 -- 19th Jan 2022

* Bugfixes:
  - `Box.center_left` xy coords
* Added:
  - `__all__` to all modules for cleaner imports
  - `draw_multiline_text`
  - New CLI program:
    - `generate-image-grid` to create grids of images from folders
* Changed:
  - Revamped `draw_text`:
    - more precise with text positioning
    - more text positions available
    - line spacing option
    - height and width constraints options
    - padding option


## 0.2.0 -- 18th Jan 2022

* Image: Added functions to draw keypoints, circles and ellipses
* Image: Some error handling when we fail to resize font size successfully
* Added new CLI program:
  - `remove-duplicates-from-folder`
