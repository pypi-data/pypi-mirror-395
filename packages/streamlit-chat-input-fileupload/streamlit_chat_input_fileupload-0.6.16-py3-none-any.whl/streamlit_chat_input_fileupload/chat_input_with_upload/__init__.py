"""Chat input component with file upload capability."""

import base64
from typing import Any

import streamlit.components.v2 as components

# HTML template for the component
_COMPONENT_HTML = """
<div class="chat-input-container">
    <input type="file" id="fileInput" class="file-input">
    <button type="button" class="btn btn-file" id="fileBtn" title="Attach file">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66l-9.2 9.19a2 2 0 01-2.83-2.83l8.49-8.48"/>
        </svg>
    </button>
    <div id="fileIndicator" class="file-indicator">
        <span class="file-name" id="fileName"></span>
        <span class="file-remove" id="fileRemove">x</span>
    </div>
    <input type="text" class="text-input" id="textInput" placeholder="Send a message...">
    <button type="button" class="btn btn-send" id="sendBtn" title="Send">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="22" y1="2" x2="11" y2="13"/>
            <polygon points="22 2 15 22 11 13 2 9 22 2"/>
        </svg>
    </button>
</div>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* Light theme (default) */
:root {
    --chat-bg: #f0f2f6;
    --chat-border: #e0e0e0;
    --input-bg: #ffffff;
    --input-text: #262730;
    --input-placeholder: rgba(38, 39, 48, 0.5);
    --btn-file-bg: #e0e0e0;
    --btn-file-text: #262730;
    --accent: #ff4b4b;
    --accent-text: #ffffff;
}

/* Dark theme */
.chat-input-container[data-theme="dark"] {
    --chat-bg: #262730;
    --chat-border: #4a4a5a;
    --input-bg: #1a1a24;
    --input-text: #fafafa;
    --input-placeholder: rgba(250, 250, 250, 0.5);
    --btn-file-bg: #4a4a5a;
    --btn-file-text: #fafafa;
    --accent: #ff4b4b;
    --accent-text: #ffffff;
}

body {
    font-family: "Source Sans Pro", sans-serif;
    background-color: transparent;
}

.chat-input-container {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px;
    background-color: var(--chat-bg);
    border-radius: 8px;
    border: 1px solid var(--chat-border);
}

.text-input {
    flex: 1;
    padding: 10px 12px;
    font-size: 14px;
    border: 1px solid var(--chat-border);
    border-radius: 6px;
    background-color: var(--input-bg);
    color: var(--input-text);
    outline: none;
    min-width: 0;
}

.text-input:focus {
    border-color: var(--accent);
}

.text-input::placeholder {
    color: var(--input-placeholder);
}

.file-input {
    display: none;
}

.btn {
    padding: 10px 12px;
    font-size: 14px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: opacity 0.2s;
}

.btn:hover {
    opacity: 0.8;
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.btn-file {
    background-color: var(--btn-file-bg);
    color: var(--btn-file-text);
    min-width: 40px;
}

.btn-send {
    background-color: var(--accent);
    color: var(--accent-text);
    min-width: 40px;
}

.file-indicator {
    display: none;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    background-color: var(--accent);
    color: var(--accent-text);
    border-radius: 4px;
    font-size: 12px;
    max-width: 150px;
}

.file-indicator.visible {
    display: flex;
}

.file-name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.file-remove {
    cursor: pointer;
    font-weight: bold;
    margin-left: 4px;
}

.file-remove:hover {
    opacity: 0.7;
}

.icon {
    width: 18px;
    height: 18px;
}
</style>
"""

_COMPONENT_JS = """
export default function(component) {
    const { data, setTriggerValue, parentElement } = component;

    let fileData = null;

    const container = parentElement.querySelector('.chat-input-container');
    const fileInput = parentElement.querySelector('#fileInput');
    const fileBtn = parentElement.querySelector('#fileBtn');
    const fileIndicator = parentElement.querySelector('#fileIndicator');
    const fileNameEl = parentElement.querySelector('#fileName');
    const fileRemove = parentElement.querySelector('#fileRemove');
    const textInput = parentElement.querySelector('#textInput');
    const sendBtn = parentElement.querySelector('#sendBtn');

    // Theme detection and application
    function detectTheme() {
        // Check Streamlit's theme from parent document
        const stApp = window.parent.document.querySelector('[data-testid="stAppViewContainer"]');
        if (stApp) {
            const bgColor = window.parent.getComputedStyle(stApp).backgroundColor;
            // Parse RGB values - dark themes have low luminance
            const rgb = bgColor.match(/\\d+/g);
            if (rgb) {
                const luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255;
                return luminance < 0.5 ? 'dark' : 'light';
            }
        }
        // Fallback to system preference
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    function applyTheme(theme) {
        if (theme === 'dark') {
            container.setAttribute('data-theme', 'dark');
        } else {
            container.removeAttribute('data-theme');
        }
    }

    // Apply theme on load
    applyTheme(detectTheme());

    // Watch for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        applyTheme(detectTheme());
    });

    // Apply args from Python
    if (data && data.placeholder) {
        textInput.placeholder = data.placeholder;
    }

    if (data && data.disabled) {
        textInput.disabled = true;
        sendBtn.disabled = true;
        fileBtn.disabled = true;
    }

    function clearFile() {
        fileData = null;
        fileInput.value = '';
        fileIndicator.classList.remove('visible');
    }

    function sendMessage() {
        const text = textInput.value.trim();

        if (!text && !fileData) {
            return;
        }

        const message = {
            text: text,
            file: fileData
        };

        setTriggerValue('message', message);

        textInput.value = '';
        clearFile();
    }

    fileBtn.onclick = () => {
        fileInput.click();
    };

    fileInput.onchange = (e) => {
        const file = e.target.files[0];
        if (file) {
            fileNameEl.textContent = file.name;
            fileIndicator.classList.add('visible');

            const reader = new FileReader();
            reader.onload = (evt) => {
                const base64 = evt.target.result.split(',')[1];
                fileData = {
                    name: file.name,
                    type: file.type,
                    size: file.size,
                    data: base64
                };
            };
            reader.readAsDataURL(file);
        }
    };

    fileRemove.onclick = () => {
        clearFile();
    };

    sendBtn.onclick = sendMessage;

    textInput.onkeydown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };
}
"""

# Register the component
_component_func = components.component(
    name="chat_input_with_upload",
    html=_COMPONENT_HTML,
    js=_COMPONENT_JS,
)


def chat_input_with_upload(
    placeholder: str = "Send a message...",
    disabled: bool = False,
    key: str | None = None,
) -> dict[str, Any] | None:
    """Display a chat input box with file upload capability.

    Parameters
    ----------
    placeholder : str
        Placeholder text for the input field.
    disabled : bool
        Whether the input is disabled.
    key : str or None
        An optional key that uniquely identifies this component.

    Returns
    -------
    dict or None
        Dictionary with 'text' and 'file' keys when user submits,
        None otherwise. The 'file' value is a dict with 'name', 'type',
        'size', and 'data' (base64 decoded bytes).
    """
    result = _component_func(
        data={"placeholder": placeholder, "disabled": disabled},
        key=key,
        on_message_change=lambda: None,
    )

    # result.message contains our trigger value
    if result.message is None:
        return None

    # Process the result
    message = result.message
    text = message.get("text", "")
    file_info = message.get("file")

    processed_file = None
    if file_info:
        # Decode base64 file data
        processed_file = {
            "name": file_info.get("name", ""),
            "type": file_info.get("type", ""),
            "size": file_info.get("size", 0),
            "data": base64.b64decode(file_info.get("data", "")),
        }

    return {
        "text": text,
        "file": processed_file,
    }
