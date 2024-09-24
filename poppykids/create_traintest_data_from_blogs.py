import os
import openai
import csv
from openai import OpenAI
from collections import Counter

# OpenAI API key
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Path to the folder containing blog posts
blog_folder_path = "/Users/jozer/Documents/GitHub/finetuning/Blogs"

# List of categories (labels)
categories = [
    "Preventative Care", 
    "Restorative Care", 
    "Membership Plan", 
    "Dental Emergencies", 
    "Dental Health Milestones"
]

# Function to generate questions from blog content using OpenAI API
def generate_questions(blog_content, category):
    prompt = f"Generate three questions related to {category} based on the following text:\n{blog_content}\n"
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates questions based on given text."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            n=3,
            temperature=0.7
        )
        questions = [choice.message.content.strip() for choice in response.choices]
        return questions
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        return []

# Output file
output_file = "output_finetuning_dataset.tsv"

# Prepare the .tsv output file with headers
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerow(["text", "label"])

    # Iterate through all blog files in the folder
    for blog_file in os.listdir(blog_folder_path):
        if blog_file.endswith(".txt"):
            blog_path = os.path.join(blog_folder_path, blog_file)
            
            # Read the content of each blog post
            with open(blog_path, 'r', encoding='utf-8') as f:
                blog_content = f.read()
            
            # Generate questions for each category and add to .tsv file
            for category in categories:
                questions = generate_questions(blog_content, category)
                for question in questions:
                    writer.writerow([question, category])

print(f"Dataset saved to {output_file}")

def extract_labels_from_blogs(blog_folder_path, output_file):
    all_labels = []

    for blog_file in os.listdir(blog_folder_path):
        if blog_file.endswith(".txt"):
            blog_path = os.path.join(blog_folder_path, blog_file)
            
            # Read the content of each blog post
            with open(blog_path, 'r', encoding='utf-8') as f:
                blog_content = f.read()

            # Analyze content and generate labels
            labels = analyze_blog_content(blog_content)
            all_labels.extend(labels)

    # Count occurrences of each label
    label_counts = Counter(all_labels)

    # Sort labels by frequency (most common first)
    sorted_labels = sorted(label_counts.items(), key=lambda x: x[1], reverse=True)

    # Save labels to TSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Label', 'Count'])  # Header
        for label, count in sorted_labels:
            writer.writerow([label, count])

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
            temperature=0.5
        )
        labels = response.choices[0].message.content.strip().split(',')
        return [label.strip() for label in labels]
    except Exception as e:
        print(f"Error analyzing blog content: {str(e)}")
        return []

# Usage
blog_folder_path = "/Users/jozer/Documents/GitHub/finetuning/Blogs"
output_file = "pk_labels.tsv"
unique_labels = extract_labels_from_blogs(blog_folder_path, output_file)
print(f"Labels have been saved to {output_file}")
print("Top 10 labels:")
for label in unique_labels:
    print(f"- {label}")
