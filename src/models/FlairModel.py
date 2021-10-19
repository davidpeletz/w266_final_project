from google.colab import files
import pandas as pd
import io
from flair.data import Sentence
from flair.models import SequenceTagger
from transformers import LukeTokenizer, LukeForEntitySpanClassification
import timeit
import ast

import unicodedata

import numpy as np
import seqeval.metrics
import spacy
import torch
from tqdm import tqdm, trange


class FlairModel:
    def __init__(self):
        # load tagger
        self.tagger = SequenceTagger.load("flair/ner-english-large")

    def get_entity_list(self, input_string):
        sentence = Sentence(input_string)

        # predict NER tags
        self.tagger.predict(sentence)
        sentence_length = len(sentence)
        values = ["O"] * len(input_string.split(" "))
        total_string = ""
        tagged_string = sentence.to_tagged_string()
        true_index = 0

        count_entities = 0
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        for word in (tagged_string.split(" ")):

            if len(word) > 0 and word not in punctuations:
                if word[0] == "<" and word[-1] == ">":
                    entity_type = word[1:-1]
                    if entity_type == "S-PER":
                        entity_type = "B-PER"
                    if entity_type == "E-PER":
                        entity_type = "I-PER"

                    values[true_index - 1 - count_entities] = entity_type
                    count_entities += 1
                true_index += 1

        return values
