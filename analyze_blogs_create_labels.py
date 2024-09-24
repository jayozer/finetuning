import os
from dotenv import load_dotenv
from openai import OpenAI
from collections import Counter

load_dotenv()  # This loads the variables from .env file

# Make sure your .env file contains the correct API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)


def extract_labels_from_blogs(blog_folder_path):
    all_labels = []

    for blog_file in os.listdir(blog_folder_path):
        if blog_file.endswith(".txt"):
            blog_path = os.path.join(blog_folder_path, blog_file)
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'ascii']
            for encoding in encodings:
                try:
                    with open(blog_path, 'r', encoding=encoding) as f:
                        blog_content = f.read()
                    break  # If successful, break the loop
                except UnicodeDecodeError:
                    continue  # Try the next encoding
            else:
                print(f"Could not read file {blog_file} with any of the attempted encodings. Skipping.")
                continue  # Skip to the next file

            # Analyze content and generate labels
            labels = analyze_blog_content(blog_content)
            all_labels.extend(labels)

    # Count occurrences of each label
    label_counts = Counter(all_labels)

    # Sort labels by frequency (most common first)
    sorted_labels = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)

    # Return unique labels (you can adjust the number of top labels to return)
    return [label for label, count in sorted_labels[:20]]  # Return top 10 labels

def analyze_blog_content(blog_content):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing blog content and extracting relevant categories or labels."},
                {"role": "user", "content": f"Analyze the following blog content and provide 3-5 relevant labels or categories that best describe the main topics discussed. Provide only the labels, separated by commas:\n\n{blog_content}"}
            ],
            max_tokens=100,
            temperature=0.1
        )
        labels = response.choices[0].message.content.strip().split(',')
        return [label.strip() for label in labels]
    except Exception as e:
        print(f"Error analyzing blog content: {str(e)}")
        return []

# Usage
blog_folder_path = "/Users/jozer/Documents/GitHub/finetuning/Blogs"
unique_labels = extract_labels_from_blogs(blog_folder_path)
print("Potential labels or categories:")
for label in unique_labels:
    print(f"- {label}")