import json

#Please consider that this function only calculates the accuracy of ALREADY PRODUCED OUTPUTS STORED IN MODELS AND DOES NOT UPDATE ON MODEL IMPROVEMENTS.
#Choose_Model_here Options are: "claude_2", "codellama","gpt-3.5","gpt-4","synthia","toppy"
model = "OpenChat"


def load_data(filename):
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            val_data = json.loads(line)
            for message in val_data['messages']:
                if message['role'] == 'assistant':
                    content = message['content']
                    if content.startswith('"itemsArray":'):
                        content = content.replace('"itemsArray":', '', 1)
                    content = json.loads(content)
                    ground_truth[line_num] = content
                if message['role'] == 'user':
                    user_contents[line_num] = message['content']
    return ground_truth, user_contents

def calculate_scores(TP, FP, FN):
    Precision = TP / (TP + FP) if TP + FP != 0 else 0
    Recall = TP / (TP + FN) if TP + FN != 0 else 0
    F1 = (2 * Precision * Recall) / (Precision + Recall) if Precision + Recall != 0 else 0
    return F1

def evaluate_predictions(ground_truth, predicted, types, weights):
    data_eval = {type_: {"GT": 0, "Pred": 0} for type_ in types}
    final_accuracy = 0
    output_eval = {"Entity": 0., "Attribute": 0, "Relationship": 0, "Generalization": 0, "GeneralizationChild": 0,"Participation": 0}
    for gt, od in zip(ground_truth.values(), predicted.values()):
        for item in gt:
            data_eval[item["__type"]]["GT"] += 1
        for item in od:
            data_eval[item["__type"]]["Pred"] += 1
        score = 0
        for type_, counts in data_eval.items():
            if counts["Pred"] > counts["GT"]:
                FP = counts["Pred"] - counts["GT"]
                FN = 0
                TP = counts["GT"]
            else:
                FP = 0
                FN = counts["GT"] - counts["Pred"]
                TP = counts["Pred"]
            F1 = calculate_scores(TP, FP, FN)
            score += weights[type_] * F1
            output_eval[type_] += F1
        final_accuracy += score
    return final_accuracy / len(ground_truth), output_eval

def save_results(filename, results):
    with open(filename, 'w') as f:
        json.dump(results, f)

ground_truth = {}
user_contents = {}
predicted = {}


ground_truth, user_contents = load_data('validation_data.jsonl')
print(ground_truth)
user_contents[1] = json.load(open("Models/" + model + "/1st_data.er"))["erDesign"]["model"]["itemsArray"]
user_contents[2]= json.load(open("Models/" + model + "/2nd_data.er"))["erDesign"]["model"]["itemsArray"]
user_contents[3] = json.load(open("Models/" + model + "/3rd_data.er"))["erDesign"]["model"]["itemsArray"]
# For now, we assume that the predicted results are the same as the ground truth #TODO: Replace this with the actual output of the model
predicted = user_contents


types = ["Entity", "Attribute", "Relationship", "Generalization", "GeneralizationChild", "Participation"]
weights = {"Entity": 0.2, "Attribute": 0.2, "Relationship": 0.2, "Generalization": 0.15, "GeneralizationChild": 0.15,"Participation": 0.1}

final_accuracy, output_eval = evaluate_predictions(ground_truth, predicted, types, weights)

output_eval = {k:v/3 for k,v in output_eval.items()}
print("Final Accuracy: ", final_accuracy)
print("Final Accuracy per element: ", output_eval)
save_results('results.json', output_eval)