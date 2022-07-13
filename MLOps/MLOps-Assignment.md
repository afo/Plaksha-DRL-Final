# Plaksha 2022 - Data-X 3 - Programming Final

### Task: MLOps

Create the following 7-Step Kubeflow pipeline in Python using the KFP SDK.

- Pipeline Step-1: Take the last two digits of your Student ID and multiple them.
- Pipeline Step-2: Add Numbers **4 and 5**.
- Pipeline Step-3: Add the resulting outputs from Step 1 and Step 2.
- Pipeline Step-4: Take the output from Step 3 and suqare the first (tens-)digit
- Pipeline Step-5: Take the output from Step-3 and Square the second (ones-)digit
- Pipeline Step-6: Add the resulting outputs from Step 4 and Step 5.
- Pipeline Step-7: Echo the resultant to logs.


The flow should look like (Assuming last two digits of your Student ID are 4 and 5):

         4*5                4+5
        = 20                = 9
            \               /
             \             /
              \           / 
               \         /
                20+9 =29
                /       \
               /         \
              /           \
             /             \
         2**2             9**2 
         = 4              = 81
            \               /
             \             /
              \           / 
               \         /
                 4+81= 85
                    |
                    |
                 Echo 85



---

### Hints 
- Refer to Notebook 1 for the MLOps part of the course to learn how to create pipelines.
- Refer to the documentation of KFP

## Note
- **YOU ARE NOT REQUIRED TO EXECUTE THIS PIPELINE ON KUBEFLOW NOR ARE YOU REQUIRED TO CREATE AN AWS ACCOUNT FOR THIS**

## Submission Type
Submit the following files:
- The zip file that is exported after compiling the pipeline
  - Naming: Please name your pipeline and zip file according to the following format: `<STUDENT_ID>-MLOPS.zip` (E.g., if your student ID is P2021PTLP0099 then Your pipeline name should be `P2021PTLP0099-MLOPS` and the Zip file name should be `P2021PTLP0099-MLOPS.zip`)
- The Notebook/Script that was used to create the pipeline
  - Naming: Please save the script/notebook as `<STUDENT_ID>.py / <STUDENT_ID>.ipynb`
  
- Finally, create a zip file containing both of the above mentioned files and submit it as your submission to the programming final.
