from typing import Any
import spacy
import re

from src.prompt import Prompt
from src.module import Process
from config import config_prompt as cfg


class RemoveSpace(Process):
    def __init__(self):
        super().__init__('remove space')

    def __call__(self, prompt):
        # Use a regular expression to replace multiple spaces with a single space
        cleaned_string = re.sub(r'\s+', ' ', prompt.get_prompt())
        prompt.set_prompt(cleaned_string)


class Summarize(Process):
    def __init__(self):
        super().__init__('summarize')

    def __call__(self, prompt: Prompt):
        # Load SpaCy model for English
        nlp = spacy.load("en_core_web_sm")

        # Process the input text
        doc = nlp(prompt.get_prompt())

        # Get sentences and their corresponding importance scores
        sentences = [sent.text for sent in doc.sents]
        scores = [sum(token.vector) for token in doc]

        # Select the top sentences based on importance scores
        selected_sentences = sorted(
            zip(sentences, scores), key=lambda x: x[1], reverse=True)

        # Combine selected sentences into the final summarized text
        summarized_text = ' '.join(
            sentence for sentence, _ in selected_sentences)

        prompt.set_prompt(summarized_text)


class PromptGeneration(Process):
    def __init__(self, name, overhead=''):
        super().__init__(name)
        self.overhead = overhead

    def __call__(self, prompt: Prompt) -> None:
        self.add_overhead(prompt=prompt)

    def add_overhead(self, prompt: Prompt):
        prompt.set_prompt(f'{self.overhead}{prompt.get_prompt()}')

    def indicate_format(self):
        delimiter = cfg.delimiter.value
        # make the output format keys with a unique identifier
        new_output_format = {}
        for key in cfg.strict_format.value.keys():
            new_output_format[f'{delimiter}{key}{delimiter}'] = cfg.strict_format.value[key]
        output_format_prompt = f'''\nYou are to output the following in json format: {new_output_format}
                                    You must use "{delimiter}{{key}}{delimiter}" to enclose the each {{key}}.'''
        return output_format_prompt
