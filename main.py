import os
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display
from src.website import Website, Website2 
import json
from typing import List



load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Check the key

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")


openai = OpenAI()

# message = "Hello, GPT! This is my first ever message to you! Hi!"
# response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":message}])
# print(response.choices[0].message.content)


# ed = Website("https://edwarddonner.com")
# print(ed.title)
# print(ed.text)

# system_prompt = "You are an assistant that analyzes the contents of a website \
# and provides a short summary, ignoring text that might be navigation related. \
# Respond in markdown."

# def user_prompt_for(website):
#     user_prompt = f"You are looking at a website titled {website.title}"
#     user_prompt += "\nThe contents of this website is as follows; \
# please provide a short summary of this website in markdown. \
# If it includes news or announcements, then summarize these too.\n\n"
#     user_prompt += website.text
#     return user_prompt

# link_system_prompt = "You are provided with a list of links found on a webpage. \
# You are able to decide which of the links would be most relevant to include in a brochure about the company, \
# such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
# link_system_prompt += "You should respond in JSON as in this example:"
# link_system_prompt += """
# {
#     "links": [
#         {"type": "about page", "url": "https://full.url/goes/here/about"},
#         {"type": "careers page", "url": "https://another.full.url/careers"}
#     ]
# }
# """


# def messages_for(website):
#     return [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_prompt_for(website)}
#     ]


# def summarize(url):
#     website = Website(url)
#     response = openai.chat.completions.create(
#         model = "gpt-4o-mini",
#         messages = messages_for(website)
#     )
#     return response.choices[0].message.content


# def display_summary(url):
#     summary = summarize(url)
#     print(summary)
#     #display(Markdown(summary))


# display_summary("https://edwarddonner.com")

MODEL = 'gpt-4o-mini'
openai = OpenAI()

link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""
def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt


def get_links(url):
    website = Website2(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
      ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    return json.loads(result)


def get_all_details(url):
    result = "Landing page:\n"
    result += Website2(url).get_contents()
    links = get_links(url)
    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website2(link["url"]).get_contents()
    return result

def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
          ],
    )
    result = response.choices[0].message.content
    print(result)

create_brochure("HuggingFace", "https://huggingface.co")

