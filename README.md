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
- Scripts are numbered and should be run in order (1-10)
- The figure script (figure_heatmap.py) can be run after script 8

-> Expected time to run all scripts: <10 minutes

## Instructions for use
Note that since this repository is for code peer review, the .xlsx data file is a ***simulation*** of the original clinical data, not the original data.
Hence, the ***results will not match*** the results in the submitted manuscript.
To replicate this study, similar clinical data would have to be collected from hospitalized youth with structured diagnostic interviews, and the code would be able to run on it.