# Solution Category B: Deep learning-based approaches that do not employ transformer architectures

### Quick Instructions

#### MODEL LINK (Google Drive): https://drive.google.com/file/d/1XXA2kYayu6wolTih0M9lNeeo5TIdXGWi/view?usp=sharing

To load the model do the following:

`torch.load('[MODEL_PATH]')`

There are 2 Python Notebooks for this approach:
* `Train_Eval_NLI_B.ipynb`: Run all cells in order, make sure all the packages are installed by executing the first cell. Training and Evaluation datasets' paths can be modified if necessary, inline comment specifies where the change can be made. (Note: all datasets must be in csv format)
* `Demo_NLI_B.ipynb`: Run all cells in order. Make sure to use the **saved model**, available at the specified link above. Change the loaded model path (there is an inline comment highlighting the part). In the last cell, the path for the testing dataset and the path for saving the file can be modified if necessary (Note: all datasets must be in csv format).

### Overview
All code was executed on L4 GPU using Google Collab Pro.
* Time to train and evaluate: ~20 minutes
* Make a prediction: ~15 seconds

Link to BERT: https://huggingface.co/docs/transformers/en/model_doc/bert


# Solution Category C: Deep learning-based approaches underpinned by transformer architectures

### Quick Instructions

#### MODEL LINK (Google Drive): https://drive.google.com/file/d/10x8CU3p_ENpIhDjxnfKInBlJN3KqbBFl/view?usp=share_link

To load the model do the following:

`electra_base_model = ElectraForSequenceClassification.from_pretrained('google/electra-base-discriminator')`

`roberta_base_model = RobertaModel.from_pretrained('roberta-base')`

`model = ElectraWithRobertaEmbeddings(electra_base_model, roberta_base_model)`

`model.load_state_dict(torch.load('[MODEL_PATH]'))`

* `Train_Eval_NLI_C.ipynb`: Run all cells in order, make sure all the packages are installed by executing the first cell. Training and Evaluation datasets' paths can be modified if necessary, inline comment specifies where the change can be made (5th executable cell). (Note: all datasets must be in csv format)
* `Demo_NLI_C.ipynb`: Run all cells in order. Make sure to use the **saved model**, available at the specified link above. Change the loaded model path 
in 3rd executable cell (there is an inline comment highlighting the part). In the last cell, the path for the testing dataset and the path for saving the file can be modified if necessary (Note: all datasets must be in csv format).

**Both notebooks contain markdown sections explaining important bits of the code alongside inline comments.**

### Overview

There are 2 Python Notebooks for this approach:
* `Train_Eval_NLI_C.ipynb`: Trains and evaluates a custom model called `ElectraWithRoBERTaEmbeddings`. It trains on `train.csv` and evaluates on `dev.csv`. The model is saved after on Google Drive. Relevant mterics are printed out for evaluation phase.
* `Demo_NLI_C.ipynb`: Loads the saved model and creates a prediction file in the required format (`Group_61_C.csv`) for `test.csv`. 

By using both ELECTRA and RoBERTa, we leverage their complementary strengths, potentially leading to better performance on the NLI task than using either model alone. ELECTRA's efficient discriminator learning combined with RoBERTa's robust optimization provides a rich feature set for understanding complex language relationships. The first notebook contains further explanation of how this works.

All code was executed on L4 GPU using Google Collab Pro.
* Time to train and evaluate: ~20 minutes
* Make a prediction: ~15 seconds

Link to ELECTRA: https://huggingface.co/docs/transformers/en/model_doc/electra#transformers.ElectraForSequenceClassification

Link to RoBERTa: https://huggingface.co/docs/transformers/v4.40.0/en/model_doc/roberta#transformers.RobertaModel