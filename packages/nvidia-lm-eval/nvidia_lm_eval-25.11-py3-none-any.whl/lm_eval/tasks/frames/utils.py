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

# Original Copyright EleutherAI.
# For the original license and copyright information, see the LICENSE file in this repository.

import json
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup


def load_wikipedia_articles(path):
    with open(path, 'r') as f:
        return json.load(f)

def process_wiki_links_str(wiki_links_str: str) -> list[str]:
    # Clean and extract individual Wikipedia links from the "wiki_links" input string from google/frames-benchmark dataset
    # '["https://en.wikipedia.org/wiki/President_of_the_United_States", "https://en.wikipedia.org/wiki/James_Buchanan", ...]' -> ['https://en.wikipedia.org/wiki/President_of_the_United_States', 'https://en.wikipedia.org/wiki/James_Buchanan', ...]
    return [link.strip("'").strip("\"").lstrip().split(" ")[0] for link in wiki_links_str.strip("[]").split(", ")]

def preprocess_wikipedia_dataset(dataset, dataset_path):
    """
    Preprocess the Wikipedia dataset and save it to a file.
    """
    wiki_texts_dict = {}
    
    for item in tqdm(dataset, desc="Preprocessing Wikipedia dataset"):
        item_wiki_links = item['wiki_links']
        wiki_links = process_wiki_links_str(item_wiki_links)
        
        for link in wiki_links:
            if link.startswith("en.wikipedia.org"):
                link = f"https://{link}"

            if not any(link.startswith(url) for url in ["https://en.wikipedia.org/", "https://en.m.wikipedia.org/", "https://w.wiki/", "https://simple.wikipedia.org/"]):
                print(f"WARNING: Invalid Wikipedia link: {link}. Skipping.")
                continue
                
            if link not in wiki_texts_dict:
                response = requests.get(link)
                if response.status_code != 200:
                    print(f"Failed to retrieve Wikipedia page: {link}. Status code: {response.status_code}. Skipping")
                    continue
                soup = BeautifulSoup(response.text, 'html.parser')
                wiki_text = soup.get_text()
                wiki_text_processed = wiki_text.encode('utf-8', errors='replace').decode('utf-8').strip().replace('\n', ' ').replace('\t', ' ')
                wiki_texts_dict[link] = wiki_text_processed
                
    # Save preprocessed dictionary to JSON file
    with open(dataset_path, 'w') as f:
        json.dump(wiki_texts_dict, f)
