#!/bin/bash

# Change to the directory containing the Python script
cd ./

# Run the baseline_email_generator_hf.py
#python3 baseline_email_generator_hf.py --sys_prompt seb_example --user_prompt seb_example --config_name openchat-3-5-extended

# Run the baseline_cvs_hf.py
#python3 baseline_cvs_hf.py --csv_path Prompt_benchmarking_zero-shot.csv --config_name openchat-3-5-extended
python3 baseline_cvs_hf.py --csv_path Prompt_benchmarking-few-shot.csv --config_name openchat-3-5-extended