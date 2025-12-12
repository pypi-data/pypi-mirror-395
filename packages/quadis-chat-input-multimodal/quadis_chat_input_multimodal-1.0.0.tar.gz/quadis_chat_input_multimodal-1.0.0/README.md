[English](README.md) | [日本語](README-ja_JP.md)

# Demo

![Demo](./demo.gif)

# Streamlit Multimodal Chat Input

A multimodal chat input component for Streamlit that supports text input, image upload, and voice input.

> **Note**: Voice and image features require HTTPS or localhost environment to function properly.

## Features

- 📝 **Text Input**: Same usability as st.chat_input
- 🖼️ **Image File Upload**: Supports jpg, png, gif, webp
- 📸 **Screenshot Capture**: Capture and share screenshots directly
- 🎤 **Voice Input**: Web Speech API / OpenAI Whisper API support
- 🎨 **Streamlit Standard Theme**: Fully compatible design
- 🔄 **Drag & Drop**: File drag and drop support
- ⌨️ **Ctrl+V**: Paste images from clipboard
- ⚙️ **Customizable**: Rich configuration options

## Installation

```bash
pip install quadis-chat-input-multimodal
```

## Basic Usage

```python
import streamlit as st
from st_chat_input_multimodal import multimodal_chat_input

# Basic usage
result = multimodal_chat_input()

if result:
    # Display text
    if result['text']:
        st.write(f"Text: {result['text']}")
    
    # Display uploaded files
    if result['files']:
        for file in result['files']:
            import base64
            base64_data = file['data'].split(',')[1]
            image_bytes = base64.b64decode(base64_data)
            st.image(image_bytes, caption=file['name'])
    
    # Display voice input metadata
    if result.get('audio_metadata'):
        st.write(f"Voice input used: {result['audio_metadata']['used_voice_input']}")
```

## Advanced Usage

### Voice Input Features

```python
# Enable voice input
result = multimodal_chat_input(
    enable_voice_input=True,
    voice_recognition_method="web_speech",  # or "openai_whisper"
    voice_language="ja-JP",
    max_recording_time=60
)

# Using OpenAI Whisper API
result = multimodal_chat_input(
    enable_voice_input=True,
    voice_recognition_method="openai_whisper",
    openai_api_key="sk-your-api-key",
    voice_language="ja-JP"
)
```

### Screenshot Capture

```python
# Enable screenshot capture (enabled by default)
result = multimodal_chat_input(
    enable_screenshot=True
)

# Disable screenshot button
result = multimodal_chat_input(
    enable_screenshot=False
)
```

### Custom Configuration

```python
result = multimodal_chat_input(
    placeholder="Please enter your message...",
    max_chars=500,
    accepted_file_types=["jpg", "png", "gif", "webp"],
    max_file_size_mb=10,
    disabled=False,
    enable_screenshot=True,  # Control screenshot button visibility
    key="custom_chat_input"
)
```

### Chat Usage

```python
import streamlit as st
import base64
from st_chat_input_multimodal import multimodal_chat_input

# Page configuration
st.set_page_config(
    page_title="Multimodal Chat Input Demo",
    page_icon="💬",
    layout="wide"
)

st.subheader("💭 Multimodal Chat Input Demo")
st.markdown("Simulate a chat application with voice input and file upload.")

# Manage history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input for new messages
chat_result = multimodal_chat_input(
    placeholder="Enter chat message...",
    enable_voice_input=True,  # Enable voice input for chat as well
    key="chat_input"
)
if chat_result:
    st.session_state.chat_history.append(chat_result)

# Display chat history
if st.session_state.chat_history:
    for i, message in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            if message.get("text"):
                st.write(message["text"])
            
            if message.get("files"):
                for file in message["files"]:
                    try:
                        base64_data = file['data'].split(',')[1] if ',' in file['data'] else file['data']
                        image_bytes = base64.b64decode(base64_data)
                        st.image(image_bytes, caption=file['name'], width=200)
                    except:
                        st.write(f"📎 {file['name']}")
            
            # Display voice input information
            if message.get("audio_metadata") and message["audio_metadata"]["used_voice_input"]:
                st.caption(f"🎤 Voice input ({message['audio_metadata']['transcription_method']})")


# Clear history
if st.button("Clear History"):
    st.session_state.chat_history = []
    st.rerun()

```

### Example Chat App

For a complete example implementation, visit the [GitHub repository](https://github.com/quadis/st-chat-input-multimodal).

## License

MIT License

## Author

**Jon Goncalves** - [Quadis](https://github.com/quadis)

## Links

- **PyPI**: https://pypi.org/project/quadis-chat-input-multimodal/
- **GitHub**: https://github.com/quadis/st-chat-input-multimodal
- **Issues**: https://github.com/quadis/st-chat-input-multimodal/issues

