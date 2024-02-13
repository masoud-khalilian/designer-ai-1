import json

# weights = {"Entity": 0.25,
#            "Relationship": 0.25,
#            "Attribute": 0.15,
#            "Participation": 0.15,
#            "Generalization": 0.1,
#            "GeneralizationChild": 0.1,
#            }


def count_types(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # print(data)
        # Navigate to "erDesign" and get the "itemsArray" list
        items_array = data['erDesign']['model']['itemsArray']
        # Dictionary to store the count of each type
        type_count = {
            'Entity': 0,
            'Relationship': 0,
            'Attribute': 0,
            'Participation': 0,
            'Generalization': 0,
            'GeneralizationChild': 0
        }

        # Iterate through the itemsArray list
        for item in items_array:
            if '__type' in item:
                type_value = item['__type']
                # Check if the type is one of the specified keys
                if type_value in type_count:
                    type_count[type_value] += 1

        return type_count

    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None


def calculate_f1_score_for_types(ground_truth_counts, predicted_counts):
    f1_scores = {}

    for category in ground_truth_counts.keys():
        true_positive = min(
            ground_truth_counts[category], predicted_counts[category])
        false_positive = max(0, predicted_counts[category] - true_positive)
        false_negative = max(0, ground_truth_counts[category] - true_positive)

        precision = true_positive / \
            (true_positive + false_positive) if true_positive + \
            false_positive > 0 else 0
        recall = true_positive / \
            (true_positive + false_negative) if true_positive + \
            false_negative > 0 else 0

        f1 = 2 * (precision * recall) / (precision +
                                         recall) if precision + recall > 0 else 0

        f1_scores[category] = f1

    return f1_scores


ground_truth_counts = count_types('./forniture.json')
predicted_counts = count_types('./er_model_manual.json')

print(ground_truth_counts)
print(predicted_counts)

f1_score1 = calculate_f1_score_for_types(ground_truth_counts, predicted_counts)

print("F1 scores for items array 1:", f1_score1)
