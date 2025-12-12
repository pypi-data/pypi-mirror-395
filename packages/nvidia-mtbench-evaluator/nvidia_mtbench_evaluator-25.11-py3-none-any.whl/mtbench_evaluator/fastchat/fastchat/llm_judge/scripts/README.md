# Inference
TODO: add instructions on generating responses to be judged

# Generating judgments

## Credentials

#### GPT-4

Export the following env vars:
```
export OPENAI_CLIENT_ID=YOUR_CLIENT_ID
export OPENAI_CLIENT_SECRET=YOUR_SECRET
```

## Judgements
To generate judgements:
```
MODEL=gpt-4
python gen_judgment.py --judge-model "$MODEL" \
                       --responses_dir YOUR_RESPONSES_DIR \
                       --output_path YOUR_RESULTS_DIR
```
where
* `YOUR_RESPONSES_DIR` - a directory containing model responses (.jsonl file per model)
* `YOUR_RESULTS_DIR` - the output directory. Judgments will be saved at `YOUR_RESULTS_DIR/judgments/gpt-4_single.jsonl`


### MT-bench-cor1
To judge the model on fixed references responses (see [this discussion](https://github.com/lm-sys/FastChat/pull/3158) for details), add
```
--judge_reference_model gpt-4-0125-preview
```
to the command above.
