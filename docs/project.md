# ASE Final Project

 - [src/project](src/project) source code
 - [Project documentation](https://htmlpreview.github.io/?https://github.com/qchen59/ASE_2023Spring/blob/main/docs/project/index.html)

## Run the project


1. Install Docker Desktop for M1 (if M1 mac, else normal)
2. Start the app
3. Install Dev Containers extension on VS Code.
4. CMD+Shift+P -> Then search for Dev Containers: Open Folder in Container
5. Select the project folder and environment as Anaconda (Python)
6. Open the Terminal and run conda create -n pygmo_env -c conda-forge pygmo
7. Run conda init (If errors pop up, choose no to report and continue)
8. Open a NEW Terminal and run conda activate pygmo_env
9. Then run pip install pandas
10. Now run the code with ``Python3 controller.py``

## Output
- [etc/out/project](etc/out/project) contains all the output
- [etc/out/project/project.out](etc/out/project/project.out) this is the text output for all 11 dataset.
- [etc/out/project/project_latex.out](etc/out/project/project_latex.out) is the latex style of out output.
- [etc/out/project/objs.pk](etc/out/project/objs.pkl) is the stored output of 11 panda dataframes

## Report
