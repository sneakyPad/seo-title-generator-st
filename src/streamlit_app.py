import streamlit as st
import streamlit_analytics

import analyze
import display





streamlit_analytics.track()

display.write_welcome()

st.sidebar.write("## Paste in your summary :gear:")
title = st.sidebar.text_input(label='Your current episode title [Optional]')
summary_text_area = st.sidebar.text_area(label='Summary of your episode', height=200)
submit_btn = st.sidebar.button('Submit')

display.render_follow_me()
display.render_subscribe_button()


if submit_btn:
    if not summary_text_area:
        st.error('You must provide a summary')
        st.stop()
    if title:
        st.markdown('## Evaluation', unsafe_allow_html=True)
        with st.spinner('Asking a Large Language Model to evaluate 💬 ...'):
            title_analysis = analyze.analyze_title(title)
            display.render_grade_result(title_analysis)

            st.write(title_analysis)

    st.markdown('## SEO Optimized Titles', unsafe_allow_html=True)
    with st.spinner('Asking a Large Language Model to generate SEO optimized titles on the summary 💬 ...'):
        seo_optimized_title = analyze.analyze_summary(summary_text_area)
        seo_optimized_title = display.apply_color(seo_optimized_title)
        st.write(seo_optimized_title)
    # display.write_results(seo_optimized_title)

else:


    file_path_example = 'resources/Summary John F Kennedy.txt'
    with open(file_path_example, 'r') as f:
        summary = f.read()
    st.divider()
    st.write(f"<b>Here's an example of the speech, John F. Kennedy gave in Berlin 1963. We'll treat "
             f"this speech as if it were a podcast. </b>",
             unsafe_allow_html=True)
    st.audio('resources/jfkberlinspeech.mp3')

    title = 'Speech given in Berlin'
    st.write(f'### Title: {title} ')
    st.markdown(f'#### Summary \n<i>:grey[{summary}]</i>', unsafe_allow_html=True )
    st.divider()


    st.markdown('#### Evaluation', unsafe_allow_html=True)
    with st.spinner('Asking a Large Language Model to evaluate 💬 ...'):
        result = analyze.analyze_title('A very boring title', example=True)
        display.render_grade_result_w_tags(result)
        # st.write(result)
    st.divider()

    st.markdown('#### SEO Optimized Titles', unsafe_allow_html=True)
    with st.spinner('Asking a Large Language Model to generate SEO optimized titles on the summary 💬 ...'):
        result = analyze.analyze_summary(summary, example=True)
        st.write(result)
        # display._write_llm_md(result)
        # display.write_hugchat_reply(result)
    # display.write_results(result, example=True)

streamlit_analytics.stop_tracking(unsafe_password=st.secrets.tracking.pw)
