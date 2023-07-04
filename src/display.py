import streamlit as st
import numpy as np
from annotated_text import annotated_text, annotation
from hugchat import hugchat
from hugchat.exceptions import ModelOverloadedError
from hugchat.login import Login
from retry import retry
from streamlit_extras.mention import mention

# Log in to huggingface and grant authorization to huggingchat
# sign = Login(st.secrets.pw.hf_email, st.secrets.pw.hf_key)
# cookies = sign.login()
# # Save cookies to usercookies/<email>.json
# sign.saveCookies()
# # Create a ChatBot
# chatbot = hugchat.ChatBot(
#     cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"


def write_welcome():
    page_title = "SEO Title Grader"
    layout = "centered"

    st.markdown(f"<h1 style='text-align: center;'>{page_title} 🚦💬</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center'> Get your Episode Title Graded </h3>",
                unsafe_allow_html=True)

    st.divider()

    st.write(
        """
      Welcome to the SEO Title Grader📈🎉! This tool analyzes your chosen title for an episode.
      Provide your summary and the title of the episode and the title will be graded on basis of how 
      well it is bein
            
      Additionally, an integrated Large Language Model (LLM) 🤖interprets these metrics and provides 
      suggestions on how to improve the SEO value for a title.  🚀.
      
      """
    )


def render_subscribe_button():
    subscribe_id = 'subscribe'
    subscribe_url = st.secrets.url.subscription
    button_text = 'Subscribe For More 🎙️💌'
    custom_css = f"""
                <style>
                #btn_wrapper {{
                    text-align: center;
                }}
                #div_subscribe {{
                    display: inline-block;
                    align-items: center;
                    background-color: white;
                    color: black;
                    position: relative;
                    text-decoration: none;
                    border-radius: 4px;
                    border-width: 1px;
                    border-style: solid;
                    border-color: rgb(152, 152, 152);
                    border-image: initial;
                }}

                #div_subscribe:hover {{
                    background-color: darkgreen;
                    color: white;
                    border-color: darkgreen;
                }}

                #{subscribe_id} {{
                    background-color: white;
                    color: black;
                    padding: 4pt 20pt;
                    position: relative;
                    text-decoration: none;
                    border-radius: 4px;
                    border-width: 1px;
                    border-color: rgb(230, 234, 241);
                    border-image: initial;
                    display: inline-block;
                    align-items: center;
                }}
                #{subscribe_id}:hover {{
                    background-color: darkgreen;
                    color: white;
                    border-color: darkgreen;
                }}
                #{subscribe_id}:active {{
                    box-shadow: none;
                    background-color: darkgreen;
                    color: white;
                }}
                </style> """

    link_html = f'<a id="{subscribe_id}" href={st.secrets.url.subscription_substack}>{button_text}</a>'
    dl_link = custom_css + f'<div id="btn_wrapper"><div id="div_subscribe">{link_html}</div></div>'
    st.sidebar.markdown(dl_link, unsafe_allow_html=True)

def render_grade_result_w_tags(llm_answer: str):
    quality_color = {
        "low": {"bg_color": "#faa", "font_color": "#800500"},
        "medium": {"bg_color": "#fea", "font_color": "#8B8000"},
        "high": {"bg_color": "#afa", "font_color": "#006E33"},
    }
    sentiment_mapping = {
        "negative": {"bg_color": "#faa", "font_color": "#800500"},
        "neutral": {"bg_color": "#fea", "font_color": "#8B8000"},
        "positive": {"bg_color": "#afa", "font_color": "#006E33"},
    }


    bullet_points = llm_answer.split('\n')
    if not bullet_points:
        return

    for bullet_point in bullet_points:
        try:
            _tmp = bullet_point.split(':')
            metric = _tmp[0]
            grade, description = _tmp[1].split('-')
            gg: str = 'f'
            # gg.tr
            metric = metric.strip()
            grade = grade.strip().lower()
            if metric.lower() == 'sentiment analysis':
                bg_color = sentiment_mapping[grade]['bg_color']

            else:
                bg_color = quality_color[grade]["bg_color"]

            annotated_text(
                (
                    metric.capitalize(),
                    f'Quality: {grade}',
                    bg_color,
                )
            )
            st.write(description)
        except Exception as e:
            st.write(bullet_point)
            print(f'Error in parsing LLM result: {e}')

def render_grade_result(llm_answer: str):
    quality_color = {
        "low": {"bg_color": "#faa", "font_color": "#800500"},
        "medium": {"bg_color": "#fea", "font_color": "#8B8000"},
        "high": {"bg_color": "#afa", "font_color": "#006E33"},
    }
    sentiment_mapping = {
        "negative": {"bg_color": "#faa", "font_color": "#800500"},
        "neutral": {"bg_color": "#fea", "font_color": "#8B8000"},
        "positive": {"bg_color": "#afa", "font_color": "#006E33"},
    }

    import re

    new_text = re.sub(r'\blow\b', ':red[<b>low</b>]', llm_answer, flags=re.IGNORECASE)
    new_text = re.sub(r'\bnegative\b', ':red[<b>negative</b>]', new_text, flags=re.IGNORECASE)
    new_text = re.sub(r'\bmedium\b', ':orange[<b>medium</b>]', new_text, flags=re.IGNORECASE)
    new_text = re.sub(r'\bneutral\b', ':orange[<b>neutral</b>]', new_text, flags=re.IGNORECASE)
    new_text = re.sub(r'\bhigh\b', ':green[<b>high</b>]', new_text, flags=re.IGNORECASE)
    new_text = re.sub(r'\bpositive\b', ':green[<b>positive</b>]', new_text, flags=re.IGNORECASE)

    st.markdown(new_text, unsafe_allow_html=True)


def apply_color(llm_answer: str):
    import re

    new_text = re.sub(r'\blow\b', ':red[low]', llm_answer, flags=re.IGNORECASE)
    new_text = re.sub(r'\bnegative\b', ':red[negative]', new_text, flags=re.IGNORECASE)
    new_text = re.sub(r'\bmedium\b', ':orange[medium]', new_text, flags=re.IGNORECASE)
    new_text = re.sub(r'\bneutral\b', ':orange[neutral]', new_text, flags=re.IGNORECASE)
    new_text = re.sub(r'\bhigh\b', ':green[high]', new_text, flags=re.IGNORECASE)
    new_text = re.sub(r'\bpositive\b', ':green[positive]', new_text, flags=re.IGNORECASE)

    return new_text


def write_results(results, example=False):
    # Calculate mean of quality scores
    quality_mapping = {"low": 0, "medium": 1, "high": 2}
    quality_color = {
        "low": {"bg_color": "#faa", "font_color": "#800500"},
        "medium": {"bg_color": "#fea", "font_color": "#8B8000"},
        "high": {"bg_color": "#afa", "font_color": "#006E33"},
    }
    mean_quality_score = np.mean([quality_mapping[result["quality"]] for result in results.values()])

    # Create traffic light indicator
    if mean_quality_score < 1:
        quality = "low"
    elif mean_quality_score < 1.5:
        quality = "medium"
    else:
        quality = "high"

    st.divider()

    st.markdown(
        f"""
        <div style="background-color:
        {quality_color[quality]['bg_color']};padding:10px;border-radius:10px;">
            <h4 style="color:{quality_color[quality]['font_color']};text-align:center;"> Podcast Quality: 
            {quality.capitalize()} 
            </h4>
        </div>
            <br />

        """,
        unsafe_allow_html=True,
    )





    with st.expander("Explanation of the metrics 📝❗️"):
        st.write(
            """
         🔊 **Loudness**:  It's like how loud or soft the sound of your podcast is. If it's too soft, 
         people might have trouble hearing it, and if it's too loud, it might hurt their ears.\n\n
         ⏇ **Peak**:  This is the loudest part of your podcast. If the peak is too high,it might sound 
         distorted or uncomfortable, but if it's too low, the audio might lack impact.\n\n
        🎙️ **Noise Floor**: This is like the quiet hum you hear when no one is talking. If the noise 
        floor is too high, it can be distracting, but if it's too low, your podcast will sound very clear and clean. \n\n
        ∿ **Dynamic Range**: This is the difference between the loudest and quietest parts of your 
        podcast. If the dynamic range is too big, it can be annoying because listeners will constantly need to adjust their volume. If it's too small, your podcast might sound flat and boring.
          """
        )

    # Display individual metric results
    for metric, result in results.items():
        annotated_text(
            (
                metric.capitalize(),
                f'Quality: {result["quality"].capitalize()}',
                quality_color[result["quality"]]["bg_color"],
            )
        )
        st.write(f"{result['message']}")


    if example:
        write_hugchat_example()
    else:
        with st.spinner('Discussing the results with a Large Language Model 💬 ...'):
            write_hugchat_reply(results)
            # pass



def write_hugchat_example():
    text = """<ul>
<li><p>Lower the overall volume of your podcast by adjusting the gain staging during 
  post-production.
       Free tool suggestion: Audacity (open source software) allows you to adjust the gain of 
      individual tracks or the entire mix. </p>
</li>
<li><p>Identify and reduce the volume of specific loud parts in your audio.
      + Free tool suggestion: Auphonic (online service) offers automatic leveling and 
      normalization features to even out the volume across your entire podcast. </p>
</li>
<li><p>Reduce background noise in your recordings by improving your recording environment or using 
  noise reduction tools during editing. Free tool suggestion: Noise Scaper (web app) provides basic noise reduction capabilities that can help remove unwanted sounds from your audio.</p>
</li>
<li><p>Maintain a small dynamic range to ensure a consistent listening experience. Well done!</p>
</li>
</ul>
<p>Remember to regularly monitor and analyze your podcast&#39;s quality metrics to continuously improve its sound.</p>
"""
    _write_llm_md(text)

def _write_llm_md(text):
    st.divider()
    st.write("#### Discover LLM's tips! 🚀📟 ")
    st.caption("Used LLM: LLama🦙 + HuggingChat🤗")
    print(text)
    st.markdown(f"<i>Suggestions:\n\n{text}</i>",
                unsafe_allow_html=True)

def render_follow_me():
    inline_twitter = mention(
        label="Twitter",
        icon="twitter",  # Twitter is also featured!
        url="https://www.twitter.com/paer06",
        write=False
    )
    inline_linkedin = mention(
        label="LinkedIn",
        icon="https://play-lh.googleusercontent.com/kMofEFLjobZy_bCuaiDogzBcUT-dz3BBbOrIEjJ"
             "-hqOabjK8ieuevGe6wlTD15QzOqw=w480-h960-rw",
        url="https://www.linkedin.com/in/patrick-m-snp/",
        write=False
    )
    st.sidebar.divider()
    st.sidebar.write(f"For more content follow me on or subscribe: {inline_twitter} {inline_linkedin}",
                     unsafe_allow_html=True, )