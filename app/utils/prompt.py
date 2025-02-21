from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from utils.example_selector import CustomExampleSelector, data

example_prompt = PromptTemplate.from_template(
        '''
            Input: {input} -> Output: {output}
        '''
)

# Define the prefix and suffix
prefix = "You are a Ghanaian Phyisics High School Examination Assessment Consultant for the West African Examination Council creating essay type question and answer sets for final year Ghanaian High School students.\nThe purpose of the questions is to prepare them for their end of semester exam.\nMake sure to provide questions and candidate answers, as well as the allocated marks for each question and sample answer.\nHere are some examples:\n"

suffix = "\nGiven the course content from a given book, create 5 questions.\nInput: {input}\nOutput:"


example_selector = CustomExampleSelector(data['examples'])


prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    suffix=suffix,
    prefix=prefix,
    input_variables=["input"]
)