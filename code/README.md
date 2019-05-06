### Code README

#### How to run simple baseline:
* `./run_baseline.sh` in root directory of repo
*  Creates output: output/pred_baseline.json

#### How to run published baseline:
* `./run_default.sh` in root directory of repo
*  Creates output: output/pred_default.json

#### How to run and grade extended model on test set:
* `./grade-test.sh` 
* Creates output: output/pred_test.json
* Prints scores

#### How to run and grade extended model on dev set:
* `./grade-dev.sh` 
* Creates output: output/pred_dev.json
* Prints scores

### Note:
* Published baseline and extended model take a long time (~20 mins) to train.