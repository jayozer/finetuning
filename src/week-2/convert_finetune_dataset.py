import json

input_file = 'src/week-2/togetherai_faq_datasetv2.jsonl'
output_file = 'src/week-2/togetherai_faq_datasetv2_formatted.jsonl'

def process_line(line):
    data = json.loads(line)
    text = data['text']
    
    # Extract question and answer
    q_start = text.index('Q:') + 2
    a_start = text.index('A:') + 2
    question = text[q_start:a_start-3].strip()
    answer = text[a_start:].strip()
    
    # Create new format
    new_data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ]
    }
    
    return json.dumps(new_data, ensure_ascii=False)

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        try:
            formatted_line = process_line(line.strip())
            outfile.write(formatted_line + '\n')
        except Exception as e:
            print(f"Error processing line: {line}")
            print(f"Error message: {str(e)}")

print(f"Formatted file has been written to {output_file}")