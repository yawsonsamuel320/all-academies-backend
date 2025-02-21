from langchain_core.example_selectors import BaseExampleSelector
import json

with open('utils/examples.json', 'r') as file:
    data = json.load(file)


data['examples'] = [
    {
        'input': example['input'], 
        'output': f'Question: {example["output"]["question"]} \nObservation: {example["output"]["observation"]} \nExpected Response: {example["output"]["expected_responses"]}'.replace('{', '{{').replace('}', '}}')
    } 
    for example in data['examples']
]

class CustomExampleSelector(BaseExampleSelector):
    def __init__(self, examples):
        self.examples = examples

    def add_example(self, example):
        self.examples.append(example)
    
    def select_examples(self, input_variables):
        new_word = input_variables['input']
        new_word_length = len(new_word)
        
        length_difference = [abs(len(example['input']) - new_word_length) for example in self.examples]
        min_difference = min(length_difference)
        best_match = self.examples[length_difference.index(min_difference)]
        return [best_match]
    
example_selector = CustomExampleSelector(data['examples'])
