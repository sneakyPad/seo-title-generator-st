import contextlib
import time
from typing import Iterator

from streamlit.runtime.scriptrunner import add_script_run_ctx
import threading
import streamlit as st

@contextlib.contextmanager
def llm_spinner(text: str = "In progress...", emojis: str = '1️⃣ 2️⃣ 3️⃣ 👋') -> Iterator[None]:
    """Temporarily displays a message while executing a block of code.

    Parameters
    ----------
    text : str
        A message to display while executing that block

    Example
    -------

    """
    import streamlit.runtime.caching as caching
    import streamlit.runtime.legacy_caching.caching as legacy_caching
    # from streamlit.proto.Arrow_pb2 import rrow as RrowProto
    # from streamlit.proto.Spinner_pb2 import Spinner as SpinnerProto
    from streamlit.string_util import clean_text

    # @st.cache optionally uses spinner for long-running computations.
    # Normally, streamlit warns the user when they call st functions
    # from within an @st.cache'd function. But we do *not* want to show
    # these warnings for spinner's message, so we create and mutate this
    # message delta within the "suppress_cached_st_function_warning"
    # context.
    with legacy_caching.suppress_cached_st_function_warning():
        with caching.suppress_cached_st_function_warning():
            message = st.empty()

    # Set the message 0.1 seconds in the future to avoid annoying
    # flickering if this spinner runs too quickly.
    DELAY_SECS = 0.1
    display_message = True
    display_message_lock = threading.Lock()

    try:
        stop_foobar = threading.Event()
        def foobar(text, emojis):
            full_response = ""
            message_placeholder = st.empty()
            stop = False
            # Simulate stream of response with milliseconds delay
            for j in range(0, 10):
                if stop:
                    break
                elements: list = emojis.split()
                beginning = text
                full_response = beginning
                message_placeholder.markdown(full_response + "▌")

                for i, chunk in enumerate(elements):
                    if stop_foobar.is_set():
                        full_response = "Here is the result ..."
                        message_placeholder.markdown(full_response)
                        stop=True
                        break

                    if i == len(elements)-1:
                        time.sleep(0.5)
                        while i > 0:
                            #clean
                            full_response = " ".join(full_response.split(' ')[:-1]) + chunk
                            time.sleep(0.1)
                            message_placeholder.markdown(full_response + "▌")
                            i -= 1

                    else:

                        full_response += " " + chunk
                        time.sleep(1)
                        # full_response = beginning + " " +chunk + " seconds passed"
                        # full_response = beginning + " " +chunk
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

        def set_message():
            with display_message_lock:
                if display_message:
                    with legacy_caching.suppress_cached_st_function_warning():
                        with caching.suppress_cached_st_function_warning():
                            message._enqueue("llm_spinner", foobar)


        add_script_run_ctx(threading.Timer(DELAY_SECS, foobar, args=[text, emojis])).start()

        # Yield control back to the context.
        yield
    finally:
        if display_message_lock:
            with display_message_lock:
                display_message = False
        with legacy_caching.suppress_cached_st_function_warning():
            with caching.suppress_cached_st_function_warning():
                # We are resetting the spinner placeholder to an empty container
                # instead of an empty placeholder (st.empty) to have it removed from the
                # delta path. Empty containers are ignored in the frontend since they
                # are configured with allow_empty=False. This prevents issues with stale
                # elements caused by the spinner being rendered only in some situations
                # (e.g. for caching).
                message.container()
        stop_foobar.set()

