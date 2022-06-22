# MLOps Assignment

### Task

Create the following 7-Step kubeflow pipeline in python language using kfp sdk.

- Pipeline Step-1: Take the last two digits of your Student ID and multiple them
- Pipeline Step-2: Add Numbers **4 and 5**
- Pipeline Step-3: Add numbers from Step 1 and Step 2
- Pipeline Step-4: Take the output from Step-3 and suqare the tens-digit
- Pipeline Step-5: Take the output from Step-3 and Square the ones-digit
- Pipeline Step-6: Add outputs from Step-4 and Step-5.
- Pipeline Step-7: Echo the resultant to logs.


The flow should look like (Assuming last two digits of your ID are 4 and 5):

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
- Refer to Notebook 1 to learn how to create pipelines
- Refer to documentation of KFP

## Note
- **YOU DO NOT REQUIRE TO EXECUTE THIS PIPELINE ON KUBEFLOW NOR DO YOU REQUIRE TO CREATE AWS ACCOUNT FOR THIS**

## Submission Type
Submit the following files:
- The zip file that is exported after compiling the pipeline
  - Naming: Please name your pipeline and zip file in format: `<STUDENT_ID>-MLOPS.zip` (Ex. If your ID is P2021PTLP0099 then Your pipeline name should be `P2021PTLP0099-MLOPS` and Zip file should be `P2021PTLP0099-MLOPS.zip`)
- The Notebook/Script that was used to create the pipeline
  - Naming: Please save the script/notebook as `<STUDENT_ID>.py / <STUDENT_ID>.ipynb`
  
- Finally, create a zip file containing both of the above mentioned files and submit it.