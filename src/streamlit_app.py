import time
import streamlit as st
import streamlit_analytics
import analyze
import display
import streamlit_ext
from src import toml2json

llm_welcome = "Hi, I'm llama 🦙 and I will be processing your title in a second ..."

text_thinking = "Thinking..."
text_grading = "Grading your title..."
text_seo = "Generating SEO optimized titles..."
text_ask_to_grade = "Would you kindly grade my title?"
text_generate_titles = "Would you kindly come up with an optimized title?"

thinking_emojis = "1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 👋"
grading_emojis = "🟢 🟠 🔴 👋"
seo_emojis = "✍️ 💬 📝 ⚙️ 👋"

toml2json.parse_firestore_toml_to_json()
streamlit_analytics.track()

display.write_welcome()

st.sidebar.write("## Paste In Your Summary :gear:")
title = st.sidebar.text_input(
    label="Your current episode title [Optional]",
    # value="Episode 20",
)
summary_text_area = st.sidebar.text_area(
    label="Summary of your episode",
    height=200,
    # value="""Welcome to our podcast episode in which we delve into a powerful address delivered by a
    # high-ranking official to the resilient people of West Berlin. With guests such as the city's mayor, a well-respected symbol of Berlin's fighting spirit, and an American general known for his presence in moments of crisis, the speaker highlights the pivotal role this city plays in the global struggle between freedom and communism. The speaker passionately invokes the statement "Ich bin ein Berliner", equating themselves with the strength and determination of the Berliners, who have faced nearly two decades of constant challenges. They challenge naysayers and the misguided, inviting them to witness the realities of Berlin's life under siege, its stark contrast to the communist regime, and the people's indomitable spirit. The speaker emphasizes the importance of freedom, not just within the walls of Berlin or Germany, but globally, asserting that when one man is enslaved, all are not free. The oration culminates with a hopeful note of peace and justice for all, and a forward-looking vision of a united, free Berlin. As a free man, they proudly declare, "Ich bin ein Berliner". This episode is an exploration of the power of unity, resilience, and hope in the face of adversity.""",
)
submit_btn = st.sidebar.button("Grade & Optimize 🚦✍️")
display.render_follow_me()


if submit_btn:
    if title:
        st.markdown("## The Grade Of Your Episode Title", unsafe_allow_html=True)
        with st.chat_message("user"):
            st.write(text_ask_to_grade)
        with st.chat_message("assistant"):
            # display.simulate_ai_typing(llm_welcome)
            # with streamlit_ext.llm_spinner(text=text_grading, emojis=grading_emojis):
            with streamlit_ext.llm_spinner(text=text_thinking, emojis=thinking_emojis):
                title_analysis = analyze.analyze_title(title)
                display.render_grade_result(title_analysis)

    if summary_text_area:
        st.markdown("## SEO Optimized Titles", unsafe_allow_html=True)
        with st.chat_message("user"):
            st.write(text_generate_titles)
        with st.chat_message("assistant"):
            # text = "Let me take your summary and come up with something that helps you get discovered ..."
            # simulate_ai_typing(thinking_emojis, sleep_time=0.5)
            with streamlit_ext.llm_spinner(text=text_seo, emojis=seo_emojis):
                seo_optimized_title = analyze.analyze_summary(summary_text_area)
                # seo_optimized_title = display.apply_color(seo_optimized_title)
                st.write(seo_optimized_title)

            time.sleep(0.1)
    st.balloons()
    display.render_subscribe_button()

else:
    file_path_example = "resources/Summary John F Kennedy.txt"
    with open(file_path_example, "r") as f:
        summary = f.read()
    st.divider()
    st.write(
        f"<b>Here's an example of the speech, John F. Kennedy gave in Berlin 1963. We'll treat "
        f"this speech as if it were a podcast. </b>",
        unsafe_allow_html=True,
    )
    st.audio("resources/John F Kennedy - I am a Berliner.mp3")

    title = "Episode 20 - Speech in Berlin"
    st.write(f"### Title: {title} ")
    st.markdown(f"#### Summary \n<i>:grey[{summary}]</i>", unsafe_allow_html=True)
    st.divider()

    st.markdown("## The Grade", unsafe_allow_html=True)
    with st.chat_message("user"):
        st.write(text_ask_to_grade)
    with st.chat_message("assistant"):
        display.simulate_ai_typing(llm_welcome)

        with streamlit_ext.llm_spinner(text_thinking, grading_emojis):
            result = analyze.analyze_title(title, example=True)
            display.render_grade_result(result)

    st.divider()

    st.markdown("## SEO Optimized Titles", unsafe_allow_html=True)
    with st.chat_message("user"):
        st.write(text_generate_titles)

    with st.chat_message("assistant"):
        with streamlit_ext.llm_spinner(text=text_seo, emojis=grading_emojis):
            seo_optimized_title = analyze.analyze_summary(summary, example=True)
            st.write(seo_optimized_title)

display.render_more_apps()
streamlit_analytics.stop_tracking(unsafe_password=st.secrets.tracking.pw,
                                  firestore_key_file=".streamlit/fs_key.json",
                                  firestore_collection_name="title-generator",
                                  )
