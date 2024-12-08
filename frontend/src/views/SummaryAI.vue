<template>
    <div class="container">
        <div class="sidebar">
            <h1>Upload</h1>
            <input type="file" ref="fileInput" multiple />
            <button @click="uploadFiles">Submit & Process</button>
        </div>

        <div class="main-content">
            <h1>Chat and Summarize</h1>
            <div class="messages">
                <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
                    <template v-if="message.type === 'bot' || message.type === 'summary'">
                        <div v-html="formatStructuredResponse(message.content)"></div>
                    </template>
                    <template v-else>
                        <strong>{{ message.role }}:</strong> {{ message.content }}
                    </template>
                </div>
            </div>

            <div class="chat-input">
                <input type="text" v-model="question" placeholder="Ask a question or summarize..."
                    @keypress.enter="askQuestion" />
                <button @click="askQuestion">Ask</button>
                <button @click="summarizeFile">Summarize</button>
            </div>
        </div>
    </div>
</template>


<script>
const API_BASE_URL = "http://127.0.0.1:5000/api/pdf";

export default {
    data() {
        return {
            question: "",
            messages: [],
        };
    },
    methods: {
        async uploadFiles() {
            const files = this.$refs.fileInput.files;
            const formData = new FormData();

            for (const file of files) {
                formData.append("files", file);
            }

            this.addMessage("System", "Processing files...", "system");
            try {
                const response = await fetch(`${API_BASE_URL}/upload`, {
                    method: "POST",
                    body: formData,
                });
                const result = await response.json();
                this.addMessage("System", result.message, "system");
            } catch (error) {
                console.error("Error uploading files:", error);
                this.addMessage("System", "Error processing files!", "system");
            }
        },
        async askQuestion() {
            if (!this.question) {
                this.addMessage("System", "Please enter a question.", "system");
                return;
            }

            this.addMessage("You", this.question, "user");
            try {
                const response = await fetch(`${API_BASE_URL}/ask`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ question: this.question }),
                });
                const result = await response.json();
                this.addMessage("Bot", result.response, "bot");
            } catch (error) {
                console.error("Error asking question:", error);
                this.addMessage("System", "Error getting the response!", "system");
            }

            this.question = "";
        },
        async summarizeFile() {
            this.addMessage("System", "Summarizing...", "system");
            try {
                const response = await fetch(`${API_BASE_URL}/summarize`, {
                    method: "POST",
                });
                const result = await response.json();
                this.addMessage("Summary", result.summary, "summary");
            } catch (error) {
                console.error("Error summarizing:", error);
                this.addMessage("System", "Error generating the summary!", "system");
            }
        },
        addMessage(role, content, type) {
            this.messages.push({ role, content, type });
            this.$nextTick(() => {
                const messagesDiv = this.$el.querySelector(".messages");
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            });
        },
        formatStructuredResponse(response) {
            const sections = response.split("**").filter((section) => section.trim() !== "");
            let htmlContent = "";

            sections.forEach((section) => {
                if (section.includes(":")) {
                    const [title, ...content] = section.split(":");
                    htmlContent += `<h3>${title.trim()}</h3>`;
                    if (content.length) {
                        const bulletPoints = content
                            .join(":")
                            .split("*")
                            .filter((item) => item.trim() !== "");
                        bulletPoints.forEach((item) => {
                            htmlContent += `<li>${item.trim()}</li>`;
                        });
                    }
                } else {
                    const bulletPoints = section.split("*").filter((item) => item.trim() !== "");
                    bulletPoints.forEach((item) => {
                        htmlContent += `<li>${item.trim()}</li>`;
                    });
                }
            });

            return `<div>${htmlContent}</div>`;
        },
    },
};
</script>

<style scoped>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

/* Reset Some Basic Styles */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* Container Layout */
.container {
    margin: 100px auto 0 auto;
    display: flex;
    height: 100vh;
    background-color: #121212;
    font-family: 'Roboto', sans-serif;
    position: relative;
    /* Ensure pseudo-element is placed correctly */
}

/* Background Texture (Pattern) */
.container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('https://www.transparenttextures.com/patterns/cubes.png');
    opacity: 0.15;
    /* Adjust opacity as needed */
    z-index: 1;
    pointer-events: none;
    /* Prevent it from capturing mouse events */
}

/* Sidebar Styles */
.sidebar {
    width: 300px;
    background-color: #1e1e2f;
    color: #ffffff;
    padding: 30px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.5);
}

.sidebar h1 {
    font-size: 1.8rem;
    margin-bottom: 20px;
    color: #ffffff;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.sidebar input[type="file"] {
    width: 100%;
    padding: 10px;
    margin-bottom: 20px;
    border: none;
    border-radius: 8px;
    background-color: #2c2c3e;
    color: #ffffff;
    cursor: pointer;
    transition: background-color 0.3s;
}

.sidebar input[type="file"]::file-selector-button {
    background-color: #4a90e2;
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.sidebar input[type="file"]::file-selector-button:hover {
    background-color: #357abd;
}

.sidebar button {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 8px;
    background-color: #4a90e2;
    color: #ffffff;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.3s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.sidebar button:hover {
    background-color: #357abd;
    transform: translateY(-2px);
}

/* Main Content Styles */
.main-content {
    flex-grow: 1;
    padding: 30px 40px;
    display: flex;
    flex-direction: column;
    color: #ffffff;
    background-color: #1e1e2f;
    position: relative;
    /* Ensure content is above the texture */
    z-index: 2;
}

.main-content h1 {
    font-size: 2rem;
    margin-bottom: 20px;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

/* Messages Section */
.messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 20px;
    background-color: #121212;
    border-radius: 8px;
    box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.5);
    margin-bottom: 20px;
}

.message {
    margin-bottom: 15px;
    padding: 15px;
    border-radius: 8px;
    max-width: 80%;
    position: relative;
    word-wrap: break-word;
}

.message.system {
    background-color: #2c2c3e;
    align-self: center;
    color: #cccccc;
}

.message.user {
    background-color: #4a90e2;
    align-self: flex-end;
    color: #ffffff;
    border-top-right-radius: 0;
}

.message.bot {
    background-color: #50c878;
    align-self: flex-start;
    color: #ffffff;
    border-top-left-radius: 0;
}

.message.summary {
    background-color: #ffcc00;
    align-self: flex-start;
    color: #1e1e2f;
    border-top-left-radius: 0;
}

/* Chat Input Section */
.chat-input {
    display: flex;
    gap: 10px;
}

.chat-input input {
    flex-grow: 1;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    background-color: #2c2c3e;
    color: #ffffff;
    font-size: 1rem;
    outline: none;
    transition: background-color 0.3s, transform 0.3s;
}

.chat-input input::placeholder {
    color: #aaaaaa;
}

.chat-input input:focus {
    background-color: #3a3a5a;
    transform: scale(1.02);
}

.chat-input button {
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    background-color: #50c878;
    color: #ffffff;
    font-size: 1rem;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.3s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.chat-input button:hover {
    background-color: #3da95a;
    transform: translateY(-2px);
}

.chat-input button:nth-child(3) {
    background-color: #ffcc00;
}

.chat-input button:nth-child(3):hover {
    background-color: #e6b800;
}

/* Scrollbar Styling */
.messages::-webkit-scrollbar {
    width: 8px;
}

.messages::-webkit-scrollbar-track {
    background: #2c2c3e;
    border-radius: 4px;
}

.messages::-webkit-scrollbar-thumb {
    background-color: #4a90e2;
    border-radius: 4px;
}

.messages::-webkit-scrollbar-thumb:hover {
    background-color: #357abd;
}

/* Structured Response Formatting */
.message.bot h3 {
    margin-bottom: 10px;
    color: #ffffff;
}

.message.bot li {
    margin-left: 20px;
    list-style-type: disc;
}

/* Responsive Design */
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }

    .sidebar {
        width: 100%;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }

    .sidebar h1 {
        font-size: 1.5rem;
        margin-bottom: 0;
    }

    .sidebar input[type="file"],
    .sidebar button {
        width: 48%;
        margin-bottom: 0;
    }

    .main-content {
        padding: 20px;
    }

    .main-content h1 {
        font-size: 1.5rem;
    }

    .messages {
        padding: 15px;
    }

    .chat-input {
        flex-direction: column;
    }

    .chat-input input {
        width: 100%;
    }

    .chat-input button {
        width: 100%;
    }
}
</style>

