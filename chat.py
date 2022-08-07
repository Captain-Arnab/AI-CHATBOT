from fileinput import filename
import random
import json
import csv

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from nltk.tokenize import sent_tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Arnab"
filename="dataset.csv";
#fields=["Questions"]
a=[]
#with open(filename, 'a') as csvfile:
    #csvwriter = csv.writer(csvfile)
    #csvwriter.writerow(fields)
def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    a.append(sent_tokenize(msg))
    
    with open(filename, 'a') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        #csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(a)
    a.clear()
    return "I do not understand...\nWill be processing your questions"
'''''def dataset(a):
    with open(filename, 'a') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(a)
    #with open('Pages.txt', 'w) as f:
    #    f.write("Questions="+'str(a)+"\n")
    #f.close()'''''

if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)
    #dataset(a)
    
