# History.py
import streamlit as st
from Database import get_user_history
from gtts import gTTS
import io
import base64

def create_audiobook(text):
    """Create an audiobook from text."""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        return None

def history():
    st.title("Summarization History")
    
    if not st.session_state.get('logged_in', False):
        st.warning("Please login to view history")
        return
    
    history_data = get_user_history(st.session_state['user_id'])
    
    if history_data:
        for i, (original_text, summary, timestamp) in enumerate(history_data):
            with st.expander(f"Summary {i+1} - {timestamp}"):
                st.markdown("#### Original Text")
                st.write(original_text[:500] + "..." if len(original_text) > 500 else original_text)
                st.markdown("#### Summary")
                st.write(summary)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.download_button(
                        label="Download Original",
                        data=original_text,
                        file_name=f"original_{i+1}.txt",
                        mime="text/plain",
                        key=f"orig_{i}"
                    )
                with col2:
                    st.download_button(
                        label="Download Summary",
                        data=summary,
                        file_name=f"summary_{i+1}.txt",
                        mime="text/plain",
                        key=f"sum_{i}"
                    )
                with col3:
                    if st.button(f"Generate Audiobook {i+1}", key=f"audio_{i}"):
                        audio_buffer = create_audiobook(summary)
                        if audio_buffer:
                            st.audio(audio_buffer, format='audio/mp3')
                            # Prepare download link
                            audio_base64 = base64.b64encode(audio_buffer.read()).decode()
                            audio_buffer.seek(0)
                            href = f'<a href="data:audio/mp3;base64,{audio_base64}" download="summary_{i+1}_audiobook.mp3">Download Audiobook</a>'
                            st.markdown(href, unsafe_allow_html=True)
                        else:
                            st.error("Could not generate audiobook")
    else:
        st.info("No history available yet. Create some summaries to see them here!")