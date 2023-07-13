import streamlit as st
from annotated_text import annotated_text, annotation
from streamlit_extras.mention import mention
import re
import time


inline_podgrader = mention(
    label="Podcast Grader - An Audio Quality Grader",
    icon="🚦",  # Twitter is also featured!
    url="https://bit.ly/podcast-grader",
    write=False,
)

inline_lemonspeak = mention(
    label="LemonSpeak - Transcribe and Summarize", icon="🍋", url="https://bit.ly/lemonspeak", write=False
)


def write_sample():
    pass
def write_welcome():
    page_title = "Podcast Title Grader"
    layout = "centered"

    st.markdown(f"<h1 style='text-align: center;'>{page_title} 🚦✍️</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center'> Get The Title Of Your Latest Episode Graded"
                f"</h3>",
                unsafe_allow_html=True)

    st.divider()

    st.write(
        """
      Welcome to the Podcast Title Grader📈🎉! This tool analyses the title you have chosen for an episode.
      Enter your summary and the title of the episode, and an Large Language Model (LLM) 🤖 will rate  
      the title according to how suitable it is for SEO.
            
      In addition, this app generates optimised SEO titles that you can use or be inspired by 🚀.
      
      """
    )

    st.write(
        f"""##### How it works⚙️\n
        \n1. Head over to the left sidebar ⬅️ and add the summary of your episode and if you already have a title you can have it rated.
        \nNo summary? Generate one here: {inline_lemonspeak}
.""",
        unsafe_allow_html=True,
    )


def render_subscribe_button(sidebar: bool = False):
    subscribe_id = "subscribe"
    subscribe_url = st.secrets.url.subscription
    button_text = "Subscribe For More 🎙️💌"
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
    if sidebar:
        st.sidebar.markdown(dl_link, unsafe_allow_html=True)
    else:
        st.markdown(dl_link, unsafe_allow_html=True)


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

    bullet_points = llm_answer.split("\n")
    if not bullet_points:
        return

    for bullet_point in bullet_points:
        try:
            _tmp = bullet_point.split(":")
            metric = _tmp[0]
            grade, description = _tmp[1].split("-")
            gg: str = "f"
            # gg.tr
            metric = metric.strip()
            grade = grade.strip().lower()
            if metric.lower() == "sentiment analysis":
                bg_color = sentiment_mapping[grade]["bg_color"]

            else:
                bg_color = quality_color[grade]["bg_color"]

            annotated_text(
                (
                    metric.capitalize(),
                    f"Quality: {grade}",
                    bg_color,
                )
            )
            st.write(description)

        except Exception as e:
            st.write(bullet_point)
            print(f"Error in parsing LLM result: {e}")


def render_grade_result(llm_answer: str):
    new_text = re.sub(r"\blow\b", ":red[<b>low</b>]", llm_answer, flags=re.IGNORECASE)
    new_text = re.sub(r"\bnegative\b", ":red[<b>negative</b>]", new_text, flags=re.IGNORECASE)
    new_text = re.sub(r"\bmedium\b", ":orange[<b>medium</b>]", new_text, flags=re.IGNORECASE)
    new_text = re.sub(r"\bneutral\b", ":orange[<b>neutral</b>]", new_text, flags=re.IGNORECASE)
    new_text = re.sub(r"\bhigh\b", ":green[<b>high</b>]", new_text, flags=re.IGNORECASE)
    new_text = re.sub(r"\bpositive\b", ":green[<b>positive</b>]", new_text, flags=re.IGNORECASE)

    st.markdown(new_text, unsafe_allow_html=True)


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
    st.markdown(f"<i>Suggestions:\n\n{text}</i>", unsafe_allow_html=True)


def render_more_apps():
    st.divider()
    st.markdown(f"#### Pssst! 🤫", unsafe_allow_html=True)
    st.write(
        f"Here are more free apps for you 🥳! {inline_lemonspeak} {inline_podgrader} ",
        unsafe_allow_html=True,
    )


def render_follow_me():
    inline_twitter = mention(
        label="Twitter",
        icon="twitter",
        url=st.secrets.mention.twitter_url,
        write=False,
    )
    inline_linkedin = mention(
        label="LinkedIn",
        icon=st.secrets.mention.linkedin_icon,
        url=st.secrets.mention.linkedin_url,
        write=False,
    )

    inline_substack = mention(
        label="Substack",
        icon=st.secrets.mention.substack_icon,
        url=st.secrets.mention.substack_url,
        write=False,
    )

    st.divider()
    st.write(
        f"Follow me on: {inline_twitter} {inline_linkedin} {inline_substack}",
        unsafe_allow_html=True,
    )


def simulate_ai_typing(text, sleep_time=0.05):
    message_placeholder = st.empty()
    full_response = ""
    # Simulate stream of response with milliseconds delay
    for chunk in text.split():
        full_response += chunk + " "
        time.sleep(sleep_time)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
