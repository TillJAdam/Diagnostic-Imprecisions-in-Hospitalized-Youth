# Diagnostic Imprecision in Hospitalized Youth
Full code used for the analyses of the article "Diagnostic Imprecision in Hospitalized Youth: Prevalence, Persistence, Predictors, and Pharmacological Consequences".

Written and shared by Till Julius Adam.

## Installation guide
- Install the latest versions of R and RStudio from here: https://posit.co/download/rstudio-desktop/
- Within RStudio, run install.packages("PACKAGENAME") for all packages in the "dependencies.txt" file
- For the figure script, install Python 3 with numpy, matplotlib, and pandas

-> Expected install time for RStudio and packages: 15 minutes

## Demo
- Open RStudio
- Click on "file" in the top left corner, navigate to the .Rmd file you want to run
- Open and click on the green triangle in the top right or use shortcut "CTRL + Alt + R"
- Scripts are numbered and should be run in order (1-9)
- The figure script (figure_heatmap.py) can be run after script 7

-> Expected time to run all scripts: <10 minutes

## Instructions for use
Note that since this repository is for code peer review, the .xlsx data file is a ***simulation*** of the original clinical data, not the original data.
Hence, the ***results will not match*** the results in the submitted manuscript.
To replicate this study, similar clinical data would have to be collected from hospitalized youth with structured diagnostic interviews, and the code would be able to run on it.

## Script overview

| Script | Output |
|--------|--------|
| 1_baseline_characteristics | Table 1, Table S2 |
| 2_diagnostic_imprecision | Table 2, Table S6 |
| 3_di_persistence | Table S5, Table S7 |
| 4_medication_transitions | Table S3 |
| 5_imputation | Imputed datasets (×8 disorders) |
| 6_multivariable_associations | Table 3 |
| 7_misclassification_matrices | Figure data |
| 8_nonindicated_prescriptions | Table 4, Table S8 |
| 9_mar_sensitivity | Table S4 |
| figure_heatmap.py | Figure (heatmap) |
