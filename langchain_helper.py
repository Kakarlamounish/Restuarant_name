from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from secret_key import openapi_key

import os
os.environ["OPENAI_API_KEY"]=openapi_key
# Step 1: Initialize the LLM
llm= ChatOpenAI(model="gpt-4o-mini",temperature=0.7)

def generate_restaurant_name_and_items(cuisine):
    # Step 2: Define the Prompt Template for the Restaurant Name
    prompt_template_name = PromptTemplate(
        input_variables=["cuisine"],
        template="I want to open a restaurant for {cuisine} food. Suggest a single fancy name for this."
    )

    # Step 3: Define the Prompt Template for Menu Items
    prompt_template_item = PromptTemplate(
        input_variables=["restaurant_name"],
        template="Suggest some menu items for {restaurant_name}. Return them as a comma-separated list."
    )

    # Step 4: Create LLMChain for Restaurant Name
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    # Step 5: Create LLMChain for Menu Items
    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_item, output_key="menu_items")

    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=["cuisine"],
        output_variables=["restaurant_name", "menu_items"]
    )

    response=chain({'cuisine':cuisine})
    return response


if __name__ =="__main__":
    print(generate_restaurant_name_and_items('Indian'))

