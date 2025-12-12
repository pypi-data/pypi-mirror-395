# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Original Copyright 2025 RUCAIBox
# For the original license and copyright information, see the LICENSE file in this repository.

import argparse
import json
import os
from collections import Counter, defaultdict

from langchain_core.runnables.config import RunnableConfig
from langchain_openai.chat_models.base import BaseChatOpenAI
from math_verify import parse, verify
from mmath.callbacks import BatchCallback
from mmath.utils import math_postprocess_v2


def run():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model-url",
        type=str,
        help="Url to the model under test.",
        required=True,
    )


    parser.add_argument(
        "--model-name",
        type=str,
        help="Model name, as deployed.",
        required=True,
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        help="Directory where results will be saved",
        required=True,
    )

    parser.add_argument(
        "--parallelism",
        type=int,
        help="How many concurrent requests to send. It is recommended to set it to very high number like 128 or 256 if deployment can handle that.",
        default=16,
    )

    parser.add_argument(
        "--retries",
        type=int,
        help="How many times a request should be retried if failed.",
        default=5,
    )

    parser.add_argument("--lang", type=str, default='all', help="The language of the dataset.", choices=['en', 'zh', 'ar', 'es', 'fr', 'ja', 'ko', 'pt', 'th', 'vi'])
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    args.model_url = args.model_url.rstrip("/chat/completions").rstrip("/completions")
    print(
"""**************************** WARNING ****************************
There is a significant variance stemming from default non-greedy 
inference params as well as from the size of subsets used to 
calculate macro-avg. Please run evaluation multiple (>2) times 
to get the right score approximation
    """)
    model = BaseChatOpenAI(base_url=args.model_url, model=args.model_name, temperature=0.6, top_p=0.95, max_tokens=32768, n=4, timeout=3600)
    lang = args.lang
    print("Testing on language:", lang)

    LANG_TO_INSTRUCTIONS = {
        'en': "{question}\nPlease reason step by step, and put your final answer within \\boxed{{}}.",
        'es': "{question}\nPor favor, razona paso a paso y pon tu respuesta final dentro de \\boxed{{}}.",
        'fr': "{question}\nVeuillez raisonner étape par étape et mettre votre réponse finale dans \\boxed{{}}.",
        'zh': "{question}\n请逐步推理，并将您的最终答案放在 \\boxed{{}} 中。",
        'ja': "{question}\nステップバイステップで推論し、最終的な答えを \\boxed{{}} の中に入れてください。",
        'th': "{question}\nกรุณาเหตุผลขั้นตอนต่อขั้นตอนและใส่คำตอบสุดท้ายของคุณใน \\boxed{{}}.",
        'ko': "{question}\n단계별로 추론하고 최종 답변을 \\boxed{{}} 안에 넣어주세요.",
        'pt': "{question}\nPor favor, raciocine passo a passo e coloque sua resposta final dentro de \\boxed{{}}.",
        'vi': "{question}\nVui lòng lý giải từng bước và đặt câu trả lời cuối cùng của bạn trong \\boxed{{}}.",
        'ar': "{question}\nيرجى المنطق خطوة بخطوة، ووضع إجابتك النهائية داخل \\boxed{{}}."
    }

    def save_results(mmath, lang):
        os.makedirs(f'{args.output_dir}/{args.model_name}', exist_ok=True)
        with open(f'{args.output_dir}/{args.model_name}/{lang}.json', 'w+', encoding='utf-8') as f:
            json.dump(mmath, f, ensure_ascii=False, indent=4)

    def load_results(lang):
        expected_results_file = f'{args.output_dir}/{args.model_name}/{lang}.json'
        try:
            with open(expected_results_file, 'r', encoding='utf-8') as f:
                data= json.load(f)
                assert len(data) == 374, "There must be exactly 374 questions loaded from cache. Otherwise it is rendered invalid"
                print(f"Using cache at {expected_results_file}")
        except (FileNotFoundError, AssertionError) :
            current_dir = os.path.dirname(os.path.abspath(__file__))
            with open(f'{current_dir}/mmath/{lang}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        return data
    
    def no_model_answer_present(*args):
        """Filter arbitrary-length tuple by the first element which is dict.
        The tuple is accepted if dict contains prediction which is marked with gid
        of the question. If there is no prediction, there is no model answer.
        That example should not be filtered out and should go for inference.
        """
        full_example, *args = args
        full_example, *_ =  full_example
        gid = full_example['gid']
        return not (f'prediction_{gid}' in full_example)
    
    def calculate_accuracy_metrics(mmath, lang):
        data = mmath
        subsets = defaultdict(Counter)
        for example in data:
            gid = example['gid']
            if f'correct_{gid}' in example:
                subsets[example['data_source']]["count"] += 1
                if example[f'correct_{gid}']:
                    subsets[example['data_source']]["correct"] +=1
        metrics = {}
        for subset_name, counter in subsets.items():
            metrics[subset_name] = counter['correct'] / counter['count']
        micro_avg = sum(metrics.values()) / len(metrics)
        metrics['micro_avg'] = micro_avg
        return metrics
    
    def save_metrics(metrics, lang):
        with open(f'{args.output_dir}/{args.model_name}/metrics_{lang}.json', 'w', encoding='utf-8') as f: 
            json.dump(metrics, f)


    # Step 1: Load all prompts. Load cached responses, if available
    all_prompts = []
    mmath = load_results(lang)
    
    for i, item in enumerate(mmath):
        question = item['question']
        formatted_prompt = LANG_TO_INSTRUCTIONS[lang].format(question=question)
        mmath[i]['final_prompt'] = formatted_prompt
        all_prompts.append(formatted_prompt)
    
    if args.limit:
        if args.limit > len(all_prompts):
            print(f"There are only {len(all_prompts)}, limit takes no effect")    
        all_prompts = all_prompts[:args.limit]


    filtered_elems = list(zip(*filter(no_model_answer_present, zip(mmath, all_prompts))))
    if filtered_elems:
        _, all_prompts = filtered_elems
    else:
        all_prompts = []


    # Step 3: Run vLLM once for all prompts

    with BatchCallback(len(all_prompts)) as cb:
        model_responses = model.with_retry(stop_after_attempt=args.retries).batch(all_prompts, config=RunnableConfig(max_concurrency=args.parallelism, callbacks=[cb]))
        model_responses = [example.content for example in model_responses]  
    # Step 4: Map outputs back to their language and question
    for idx, generated_text in enumerate(model_responses):
            mmath[idx][f'prediction_{idx}'] = generated_text
            mmath[idx][f'pred_answer_{idx}'] = math_postprocess_v2(generated_text)
            
            if mmath[idx][f'pred_answer_{idx}'] is None:
                if_correct = False
            else:
                gold = parse(mmath[idx]['answer'])
                pred = parse('$' + mmath[idx][f'pred_answer_{idx}'] + '$')
                if_correct = verify(gold, pred)
            
            mmath[idx][f'correct_{idx}'] = if_correct

    # Step 4: Save results

    save_results(mmath, lang)

    # Step 5: Calculate metrics

    accuracy_metrics = calculate_accuracy_metrics(mmath, lang)
    save_metrics(accuracy_metrics, lang)

if __name__ == "__main__":
    run()