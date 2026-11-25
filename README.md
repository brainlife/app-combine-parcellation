<h1 align="center">Combine two parcellations</h1>

<p align="center">
  A single volumetric parcellation, with consecutive labels and a merged label.json, from two parcellations of the same subject.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.739"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.739-blue.svg" alt="Run on brainlife.io"></a>
  <a href="https://github.com/brainlife/app-combine-parcellation/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT license"></a>
</p>

> 📍 **This branch, `v1.2`, is the brainlife.io App Combine two parcellations into a single parcellation** ([doi:10.25663/brainlife.app.739](https://doi.org/10.25663/brainlife.app.739)).

## 🧠 At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Merges two volumetric parcellations into one with relabelled consecutive values and a combined label.json, resolving overlaps in favour of the first, the second or neither.**

Reslices the second parcellation onto the first's grid with FreeSurfer mri_vol2vol (header-based, nearest neighbour), renumbers the labels of both, sums them and handles overlapping voxels according to the overlap option, then writes parc.nii.gz and label.json. Use it to combine, for example, a cortical and a subcortical atlas. Both parcellations must already be aligned to the same subject space.

| | |
|---|---|
| 📥 **Inputs** | `neuro/parcellation/volume` ×2 |
| 📤 **Outputs** | `neuro/parcellation/volume` |
| 🐳 **Container** | `brainlife/freesurfer:7.3.2` |
| ⚙️ **Resources** | 1 CPUs |
| 🔑 **Requires** | `FREESURFER_LICENSE` |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.739](https://doi.org/10.25663/brainlife.app.739) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `parc_one` | `neuro/parcellation/volume` | yes | First volumetric parcellation with its label.json; defines the output grid. |
| `parc_two` | `neuro/parcellation/volume` | yes | Second volumetric parcellation with its label.json. Must be aligned with the first; it is resampled by header only. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `parcellation` | `neuro/parcellation/volume` | Combined parcellation (parc.nii.gz) with a merged label.json. |

<details>
<summary><b>⚙️ Parameters</b> (1)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `overlap` | enum | `first` | How voxels labelled in both parcellations are resolved: keep the first's label, the second's, or set them to 0. Options: `first`, `second`, `remove`. |

</details>

<!-- brainlife-app:end -->

## 🚀 Running the App

### ☁️ On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.739](https://doi.org/10.25663/brainlife.app.739), choose two `neuro/parcellation/volume` datasets from your project, pick how overlapping voxels are handled and press **Execute**. The combined parcellation is archived to your project as a `neuro/parcellation/volume` dataset tagged `combined`. Use it to combine, for example, a cortical and a subcortical atlas.

Both parcellations must already be aligned to the same subject space. The App:

1. reslices the second parcellation onto the grid of the first with FreeSurfer `mri_vol2vol` (header-based, nearest-neighbour interpolation);
2. keeps only the labels present in each image and renumbers them consecutively, the first parcellation's labels before the second's;
3. sums the two images and resolves voxels labelled in both according to `overlap`: keep the first parcellation's label (`first`), the second's (`second`), or set them to 0 (`remove`);
4. writes the combined image and a merged `label.json`.

### 💻 Locally

You need [Singularity/Apptainer](https://apptainer.org/), [`jq`](https://jqlang.github.io/jq/) and a [FreeSurfer license](https://surfer.nmr.mgh.harvard.edu/registration.html). FreeSurfer 7.3.2 and nibabel run inside containers.

1. Clone this repository and check out the branch brainlife.io runs: `git checkout v1.2`.
2. Create `config.json` with the paths to your inputs:

   ```json
   {
       "parc_one": "/input/parc_one/parc.nii.gz",
       "label_one": "/input/parc_one/label.json",
       "parc_two": "/input/parc_two/parc.nii.gz",
       "label_two": "/input/parc_two/label.json",
       "overlap": "first"
   }
   ```

3. Export your license and run the App:

   ```bash
   export FREESURFER_LICENSE="$(cat ~/freesurfer/license.txt)"
   ./main
   ```

### 🧪 Sample data

Download sample datasets from brainlife.io with the [brainlife CLI](https://github.com/brainlife/cli):

```bash
npm install -g brainlife
bl login
mkdir input
bl dataset download <dataset-id>
```

## 📦 Outputs

```text
parcellation/
├── parc.nii.gz   combined parcellation on the grid of the first input
└── label.json    merged labels, renumbered 1…N
```

## 🩺 Troubleshooting

- **`Please set FREESURFER_LICENSE in .bashrc`**: export the contents of your FreeSurfer `license.txt` as `FREESURFER_LICENSE` before running `./main`.
- **`something went wrong. check logs and derivatives`**: `parcellation/parc.nii.gz` was not written. Check the log, and make sure both `label.json` files describe the values in their images.

## 📚 Citing

> [!TIP]
> If you use this App in your work, please cite the App, the software it builds on and brainlife.io (below). GitHub's **Cite this repository** button gives the App citation in APA and BibTeX.

- Combine two parcellations into a single parcellation. brainlife.io App. [doi:10.25663/brainlife.app.739](https://doi.org/10.25663/brainlife.app.739)
- Fischl. FreeSurfer. *NeuroImage* 62:774-781 (2012). [doi:10.1016/j.neuroimage.2012.01.021](https://doi.org/10.1016/j.neuroimage.2012.01.021)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## 👥 Authors

- Franco Pestilli (project director)
- Brad Caron

## 💰 Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io is publicly funded, and acknowledging that support helps keep it running. This App was developed with support from Wellcome, the U.S. National Institutes of Health (including the BRAIN Initiative BRAIN CONNECTS program: The Axonal Projectome EXchange, U24NS140384, and the Center for Mesoscale Connectomics, UM1NS132207) and the U.S. National Science Foundation.</sub>

## ⚖️ License

[MIT](https://github.com/brainlife/app-combine-parcellation/blob/master/LICENSE). FreeSurfer itself is distributed under its own [license](https://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferSoftwareLicense).
