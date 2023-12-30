def process_json(output_str):
    itemsMap = {}
    for item in output_str:
        item_id = item.get('_id')
        itemsMap[item_id] = item
    return itemsMap
