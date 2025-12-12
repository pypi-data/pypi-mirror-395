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

"""
Homepage: https://yale-lily.github.io/spider
GH: https://github.com/taoyds/spider
"""

import json
import os
import sqlite3
from pathlib import Path
import jinja2

from evaluate import load

from bigcode_eval.base import Task
from bigcode_eval.tasks.custom_metrics.spider_eval.evaluation import build_foreign_key_map_from_json, evaluate

_CITATION = """
@inproceedings{Yu&al.18c,
  title     = {Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task},
  author    = {Tao Yu and Rui Zhang and Kai Yang and Michihiro Yasunaga and Dongxu Wang and Zifan Li and James Ma and Irene Li and Qingning Yao and Shanelle Roman and Zilin Zhang and Dragomir Radev}
  booktitle = "Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
  address   = "Brussels, Belgium",
  publisher = "Association for Computational Linguistics",
  year      = 2018
}
"""

environment = jinja2.Environment()
PROMPT_TEMPLATE_PATH = "prompt_templates/spider"

### Sqlite functions based on https://gitlab-master.nvidia.com/awarno/spider-sql-benchmark/-/blob/main/predict/sql_utils.py
def get_sqlite_schema(db_path: str | Path) -> str:
    """
    Retrieves the schema of an SQLite database as a single string.

    Args:
    db_path (str): The file path to the SQLite database.

    Returns:
    str: A string containing the schema (custom) of the database.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # Query the sqlite_master table to retrieve the schema
    cursor.execute("SELECT type, name, sql FROM sqlite_master WHERE type='table';")

    # Fetch all results
    schema = cursor.fetchall()

    # Initialize an empty string to hold the schema
    schema_string = ""

    # Concatenate each table's schema into the schema_string
    for table_info in schema:
        schema_string += (
            f"Type: {table_info[0]}, Name: {table_info[1]}, SQL: {table_info[2]};\n\n"
        )

    # Close the connection
    conn.close()

    return schema_string


def read_schema(
    database_folder: str | Path,
    database_name: str | Path,
    schema_name: str | Path = "schema.sql",
) -> str:
    """Read sql schema from schema_name file or create if schema_name does not exist.

    Args:
        database_folder (str | Path): path to folder with databases
        database_name (str | Path): database name
        schema_name (str | Path, optional): schema file name. Defaults to 'schema.sql'.
    """
    database_folder = Path(database_folder)
    try:
        db_path = os.path.join(database_folder, database_name, schema_name)
        with open(db_path) as file:
            schema_sql_content = file.read()
    except FileNotFoundError:
        db_path = os.path.join(database_folder, database_name, f"{database_name}.sqlite")
        schema_sql_content = get_sqlite_schema(db_path)
    return schema_sql_content
###

class Spider(Task):
    DATASET_PATH = "xlangai/spider"
    LOCAL_DB_PATH = "unverified/text/llm/spider/original/1.0/database"
    LOCAL_TABLES_PATH = "unverified/text/llm/spider/original/1.0/tables.json"

    def __init__(self, max_order=4, smooth=True, prompt_mode='traditional_plm'):
        super().__init__(
            stop_words=[";"],
            requires_execution=False,
        )
        self.max_order = max_order
        self.smooth = smooth
        self.prompt_mode = prompt_mode
        
        with open(os.path.join(os.path.dirname(__file__), PROMPT_TEMPLATE_PATH, f'{prompt_mode}.jinja')) as file_:
            self.prompt_template = file_.read()

    def get_dataset(self, database_folder_path = LOCAL_DB_PATH):
        """Returns dataset for the task or an iterable of any object, that get_prompt can handle"""
        database_folder_path = Path(database_folder_path)

        def add_schema(row):
            db_id = row['db_id']
            schema = read_schema(database_folder_path, db_id)
            return schema

        schema_values = self.dataset["validation"].map(lambda row: {'schema': add_schema(row)})['schema']

        updated_dataset = self.dataset["validation"].add_column('schema', schema_values)

        return updated_dataset

    def get_prompt(self, doc):
        """Builds the prompt for the LM to generate from."""
        question = doc["question"].strip()

        def remove_lines_starting_with(input_string, prefixes):
            lines = input_string.splitlines()
            filtered_lines = [line for line in lines if not any([line.startswith(prefix) for prefix in prefixes])] 
            result_string = "\n".join(filtered_lines)
            return result_string
        
        def process_schema_str(schema_str):
            schema_str = remove_lines_starting_with(schema_str, ['INSERT', 'insert'])
            schema_str = schema_str.replace('\n', ' ')
            return schema_str
        
        schema = process_schema_str(doc["schema"])
        template = environment.from_string(self.prompt_template)
        prompt = template.render({'question': question, 'schema': schema})

        return prompt

    def get_reference(self, doc):
        """Builds the reference solution for the doc (sample from the test dataset)."""
        return (doc["query"], doc["db_id"])

    def postprocess_generation(self, generation, idx):
        """Defines the postprocessing for a LM generation.
        :param generation: str
            code generation from LM
        :param idx: int
            index of doc in the dataset to which the generation belongs
            (not used for this task)
        """
        idx = generation.index('SELECT')
        if idx < 0:
            output = ""
        else:
            output = generation[idx:].strip().replace('\r', '')
        output = " ".join(output.split())
        if output == '':
            output = 'No answer'
        return output

    def process_results(self, generations, references, database_folder_path = LOCAL_DB_PATH, tables_path = LOCAL_TABLES_PATH):
        """Takes the list of LM generations and evaluates them against ground truth references,
        returning the metric for the generations.
        :param generations: list(list(str))
            list of lists containing generations
        :param references: list(str)
            list of str containing references
        """
        def _save_list_to_file(save_list, file_path, item_sep):
            with open(file_path, 'w') as file:
                for item in save_list:
                    file.write(f"{item}{item_sep}")

        bleu = load("bleu")
        gens = [gen[0] for gen in generations]
        refs = [f'{ref}\t{db_id}' for ref, db_id in references]

        bleu_results = bleu.compute(
            references=references, predictions=gens, max_order=self.max_order, smooth=self.smooth
        )

        # EXECUTION Accuracy
        gens_filename_tmp = '/tmp/gens_tmp.txt'
        refs_filename_tmp = '/tmp/refs_tmp.txt'
        _save_list_to_file(gens, gens_filename_tmp, item_sep="\n")
        _save_list_to_file(refs, refs_filename_tmp, item_sep="\n")

        kmaps = None
        spider_scores = evaluate(gold=refs_filename_tmp, predict=gens_filename_tmp, db_dir=database_folder_path, etype="exec", kmaps=kmaps, plug_value=False, keep_distinct=False, progress_bar_for_each_datapoint=False)
        exec_acc_spider = spider_scores['all']['exec']

        kmaps = build_foreign_key_map_from_json(tables_path)
        spider_scores = evaluate(gold=refs_filename_tmp, predict=gens_filename_tmp, db_dir=database_folder_path, etype="match", kmaps=kmaps, plug_value=False, keep_distinct=False, progress_bar_for_each_datapoint=False)        
        exact_match_spider = spider_scores['all']['exact']

        prompt_example = self.get_prompt(doc = {'question': 'QUESTION', 'schema': 'SCHEMA'}).strip()
        results = {'bleu': bleu_results['bleu'], 'val_exec_acc': exec_acc_spider, 'val_exact_match': exact_match_spider, 'prompt_mode': str(self.prompt_mode), 'example_prompt': str(prompt_example)}

        return results
