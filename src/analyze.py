from json import JSONDecodeError
from typing import Union
import streamlit as st
from annotated_text import annotated_text, annotation
from hugchat import hugchat
from hugchat.exceptions import ModelOverloadedError
from hugchat.login import Login
from retry import retry
from streamlit_extras.mention import mention

import fasttext


language_dict = {
    'ZH': 'Chinese',
    'ES': 'Spanish',
    'EN': 'English',
    'HI': 'Hindi',
    'AR': 'Arabic',
    'PT': 'Portuguese',
    'BN': 'Bengali',
    'RU': 'Russian',
    'JA': 'Japanese',
    'PA': 'Punjabi',
    'DE': 'German',
    'JW': 'Javanese',
    'TE': 'Telugu',
    'MR': 'Marathi',
    'TA': 'Tamil',
    'TR': 'Turkish',
    'KO': 'Korean',
    'FR': 'French',
    'IT': 'Italian',
    'TH': 'Thai',
    'NL': 'Dutch',
    'PL': 'Polish',
    'RO': 'Romanian',
    'EL': 'Greek',
    'HU': 'Hungarian',
    'SV': 'Swedish',
    'DA': 'Danish',
    'FI': 'Finnish',
    'NO': 'Norwegian',
    'CS': 'Czech',
    'SK': 'Slovak'
}



def detect_language(text):
    # load the pre-trained model
    model = fasttext.load_model('resources/lid.176.ftz')
    predictions = model.predict(text)
    language_code: str = predictions[0][0].replace("__label__", "")
    # print(language_code)  # Output: 'en'
    language = language_dict.get(language_code.upper(), language_code)
    # print(language)  # Output: 'en'
    return language

def init_hugchat():
    # Log in to huggingface and grant authorization to huggingchat
    sign = Login(st.secrets.pw.hf_email, st.secrets.pw.hf_key)
    cookies = sign.login()
    # Save cookies to usercookies/<email>.json
    sign.saveCookiesToDir()
    # Create a ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"
    return chatbot


chatbot = init_hugchat()


# @retry((ModelOverloadedError, JSONDecodeError), tries=2, delay=3)
@retry(tries=3, delay=3)
def ask_hugchat(prompt):
    try:
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)

        llm_answer = chatbot.chat(
            prompt,
            is_retry=True,
            retry_count=10,
            temperature=0.05,
            truncate=2048,
            use_cache=False,
        )
        # print(llm_answer)
        return llm_answer
    except Exception as e:
        print(f'Exception: {e}')
        raise Exception



def analyze_title(podcast_title, example=False):
    try:
        if example:
            pre_calculated = """
            Here's my evaluation of the given podcast episode title based on the requested metrics:
    
            * Title Length: Medium - A title that is too short may not provide enough context for search engines to understand what the content is about, while a title that is too long can appear spammy and turn off users from clicking on it. At just six words, "A Very Boring Title" strikes a good balance between brevity and clarity.
            * Sentiment Analysis: Neutral - The title itself does not convey any strong emotions, which could make it more appealing to a wider audience but might not stand out as strongly among other titles.
            * SEO Potential: Low - While the title provides some basic information about the topic, it lacks specific keywords or phrases that could improve its visibility in search engine results. Without additional optimization efforts, this title may struggle to rank well for relevant searches.
            * Emotional Appeal: Low - As mentioned earlier, the title does not evoke any strong emotions, which could limit its ability to draw listeners in and encourage them to click through to the full episode.
            * Readability: High - The title is simple and easy to understand, making it accessible to a wide range of audiences regardless of their reading level. This could be beneficial for attracting casual browsers who may not want to invest time deciphering complex language.
            
            Overall, there's room for improvement in terms of SEO potential and emotional appeal, but the title meets most of the basic requirements for a clear and readable headline. If possible, consider incorporating targeted keywords or adding a subtitle to enhance its online presence without sacrificing simplicity.
            """
            return pre_calculated

        language = detect_language(podcast_title)
        prompt: str = st.secrets.prompts.grade_title
        formatted_prompt = prompt.format(language=language, title=podcast_title)
        # prompt = f'{st.secrets.prompts.grade_title} {podcast_title}'
        answer = ask_hugchat(formatted_prompt)
        return answer
    except Exception as e:
        print(f'Exception: {e}')
        st.warning(f'We are currently experiencing high demand - please try again in a few seconds', icon='🟠')

def analyze_summary(summary, example=False):
    try:
        if example:
            pre_calculated = """
            Sure! Based on your podcast summary, here are four highly SEO optimized titles:
            1. "Unbreakable Spirit: How Berlin Overcame Communism" - This title captures the essence of the podcast episode while incorporating relevant keywords like "Berlin," "communism," and "unity."
            2. "From Siege to Freedom: The Power of Resilience" - This title focuses on the theme of resilience and uses keywords related to Berlin and freedom.
            3. "A Tribute to Unity: Ich Bin Ein Berliner" - This title references the famous quote from the speech and includes relevant keywords like "unity" and "freedom."
            4. "Defying Oppression: The Fight for Global Liberty" - This title expands upon the broader message of the speech and incorporates keywords related to oppression, liberty, and global issues.
            
            Remember, choosing the perfect title requires balancing both human interest and SEO optimization. While these suggestions prioritize SEO, make sure to choose a title that accurately reflects the content of your podcast and resonates with potential listeners. Good luck!
             
            """
            return pre_calculated

        language = detect_language(summary)
        prompt: str = st.secrets.prompts.llama_prompt
        formatted_prompt = prompt.format(language=language, content=summary)
        # prompt = f"{st.secrets.prompts.llama_prompt} {summary}"
        answer = ask_hugchat(formatted_prompt)
        return answer
    except Exception as e:
        print(f'Exception: {e}')
        st.warning(f'We are currently experiencing high demand - please try again in a few seconds', icon='🟠')
