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


class LukeModel:
    def __init__(self):
        self.tokenizer = LukeTokenizer.from_pretrained("studio-ousia/luke-large-finetuned-conll-2003")
        self.model = LukeForEntitySpanClassification.from_pretrained("studio-ousia/luke-large-finetuned-conll-2003")

    def get_entity_list(self, input_text):
        input_text = input_text.strip()

        split_text = input_text.split(" ")

        word_start_positions = [0]
        word_end_positions = [len(split_text[0])]
        words = [[word_start_positions[0], word_end_positions[0]]]

        for word in split_text[1:]:
            start_index = word_end_positions[-1] + 1
            word_start_positions.append(start_index)
            end_index = len(word) + word_start_positions[-1]
            word_end_positions.append(end_index)
            words.append([start_index, end_index])

        entity_spans = []
        for index, start_pos in enumerate(word_start_positions):
            for end_pos in word_end_positions[index:]:
                entity_spans.append((start_pos, end_pos))

        inputs = self.tokenizer(input_text, entity_spans=entity_spans, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits

        predicted_class_indices = logits.argmax(-1).squeeze().tolist()
        if type(predicted_class_indices) == int:
            predicted_class_indices = [predicted_class_indices]

        text_entities = []
        total_entities = []

        for span, predicted_class_idx in zip(entity_spans, predicted_class_indices):
            if predicted_class_idx != 0:
                current_text = input_text[span[0]:span[1]]
                current_entity = str(model.config.id2label[predicted_class_idx])
                current_entities = ["B-" + current_entity]
                num_spaces = current_text.count(" ")
                if num_spaces >= 1:
                    current_entities.extend(["I-" + current_entity] * num_spaces)
                total_entities.append(current_entities)
                text_entities.append(current_text)

        copy_string = input_text
        for i, te in enumerate(text_entities):
            copy_string = copy_string.replace(te, (str(total_entities[i]).replace(" ", "")), 1)
        entity_list = []

        for i in copy_string.split(" "):
            prefix = (i[0:4])
            if prefix == "['B-":
                entry = [n.strip() for n in ast.literal_eval(i)]
                entity_list.extend(entry)
            else:
                entity_list.append("O")

        return entity_list
