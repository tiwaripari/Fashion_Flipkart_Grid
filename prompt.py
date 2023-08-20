from dotenv import load_dotenv
from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from PIL import Image
import io
import requests
import matplotlib.pyplot as plt
import pandas as pd

API_URL = "https://api-inference.huggingface.co/models/SG161222/Realistic_Vision_V1.4"
headers = {"Authorization": "Bearer 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"}


def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content


# load the Environment Variables.
load_dotenv()


def generate_fashion_response_from_csv(csv_file,cat,gender):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    df2 = df[(df["usage"] == cat) & (df["gender"] == gender)]

    df1 = df.sample(40)

    # Extract relevant information from the DataFrame
    # You would need to customize this part based on your CSV structure
    top_color = df1[df1['masterCategory'] == 'Apparel']['baseColour'].values
    bottom_color = df1[df1['masterCategory'] ==
                 'Bottomwear']['baseColour'].values
    footwear_color = df1[df1['masterCategory'] ==
                   'Footwear']['baseColour'].values
    accessories_color = ', '.join(
        df1[df1['masterCategory'] == 'Accessories']['baseColour'].values)
    top_type = df1[df1['masterCategory'] == 'Apparel']['articleType'].values
    bottom_type = df1[df1['masterCategory'] =='Bottomwear']['articleType'].values
    footwear_type = df1[df1['masterCategory'] == 'Footwear']['articleType'].values
    accessories_type = df1[df1['masterCategory']
                            == 'Accessories']['articleType'].values
    
    return prompt_generate(top_color, bottom_color, footwear_color, accessories_color, top_type, bottom_type, footwear_type, accessories_type, cat,gender)


def prompt_generate(top_color, bottom_color, footwear_color, accessories_color, top_type, bottom_type, footwear_type, accessories_type, cat, gender):
    prompt = f"""
Generate fashion suggestions for a {cat} look and {gender}, incorporating the latest fashion trends.Give me color and type of top,bottom,accessories and footwear according to my previous choices {top_color},{top_color}, {bottom_color}, {footwear_color}, {accessories_color}, {top_type}, {bottom_type}, {footwear_type}, {accessories_type}.
"""
    return prompt


def chain_setup():
    template = """<|prompter|>{question}<|endoftext|>
    <|assistant|>"""

    prompt = PromptTemplate(template=template, input_variables=["question"])

    llm = HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
                         model_kwargs={"max_new_tokens": 900})

    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt
    )
    return llm_chain

    # generate response


def generate_response(question, llm_chain):
    response = llm_chain.run(question)
    # print(response)
    return response

    # load LLM
llm_chain = chain_setup()

user_input1 = input("Hi!! Please choose one of them Ethnic/Casual/Formals/Sports: ")
user_input2 = input("Choose Male or Female: ")

prompt = generate_fashion_response_from_csv(
	"styles.csv",{user_input1},{user_input2})

response = generate_response(prompt, llm_chain)
print(response)
image_bytes = query({
	"inputs": response
})
# You can access the image with PIL.Image for example
image = Image.open(io.BytesIO(image_bytes), formats=['JPEG'])
plt.imshow(image)
plt.show()
