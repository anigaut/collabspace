<template>
  <div>
    <div class="sidebar">
      <h1>AI Chatbot</h1>
      <form @submit.prevent="handleSubmit">
        <label for="repolink">GitHub Repo Link:</label>
        <input type="text" v-model="repolink" placeholder="Enter GitHub Repo Link" />

        <label for="files">Upload Code or PDF Files:</label>
        <input type="file" ref="fileInput" multiple @change="handleFileUpload" />

        <button type="submit">Submit</button>
      </form>
      <div class="status">{{ statusMessage }}</div>
    </div>

    <div class="main-content">
      <div class="chat-section-container">
        <h2>Query wrt Context</h2>
        <div class="chat-section" ref="chatBox">
          <p v-for="(msg, index) in chatMessages" :key="index" :class="msg.role">
            <strong>{{ msg.role }}:</strong> {{ msg.content }}
          </p>
        </div>
        <div class="chat-input">
          <input type="text" v-model="userMessage" placeholder="Ask about Repo or Files..." />
          <button @click="sendMessage">Ask</button>
        </div>
      </div>

      <div class="chat-section-container">
        <h2>Talk to AI</h2>
        <div class="chat-section" ref="directChatBox">
          <p v-for="(msg, index) in directMessages" :key="index" :class="msg.role">
            <strong>{{ msg.role }}:</strong> {{ msg.content }}
          </p>
        </div>
        <div class="chat-input">
          <input type="text" v-model="directMessage" placeholder="Chat directly with AI..." />
          <button @click="sendDirectMessage">Ask</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const API_BASE_URL = "http://localhost:5000/api/rag"; // Ensure this points to your backend

export default {
  data() {
    return {
      repolink: "",
      files: [],
      userMessage: "",
      directMessage: "",
      statusMessage: "",
      chatMessages: [],
      directMessages: [],
    };
  },
  methods: {
    handleFileUpload(event) {
      this.files = Array.from(event.target.files);
    },
    async handleSubmit() {
      const formData = new FormData();
      if (this.repolink) formData.append("repolink", this.repolink);
      this.files.forEach((file) => formData.append("files", file));

      this.statusMessage = "Processing...";
      try {
        const response = await fetch(`${API_BASE_URL}/submit`, {
          method: "POST",
          body: formData,
        });
        const result = await response.json();
        if (response.ok) {
          this.statusMessage = "Ready! You can now ask questions.";
        } else {
          this.statusMessage = result.error || "An error occurred.";
        }
      } catch (error) {
        this.statusMessage = "Failed to process the request.";
      }
    },
    async sendMessage() {
      if (!this.userMessage) {
        alert("Please enter a question.");
        return;
      }

      const message = { role: "You", content: this.userMessage };
      this.chatMessages.push(message);

      try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: this.userMessage }),
        });
        const result = await response.json();
        if (response.ok) {
          this.chatMessages.push({ role: "Assistant", content: result.response });
        } else {
          alert(result.error || "An error occurred.");
        }
      } catch {
        alert("Failed to fetch response.");
      }

      this.userMessage = "";
      this.scrollToBottom(this.$refs.chatBox);
    },
    async sendDirectMessage() {
      if (!this.directMessage) {
        alert("Please enter a message.");
        return;
      }

      const message = { role: "You", content: this.directMessage };
      this.directMessages.push(message);

      try {
        const response = await fetch(`${API_BASE_URL}/direct_chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: this.directMessage }),
        });
        const result = await response.json();
        if (response.ok) {
          this.directMessages.push({ role: "AI", content: result.response });
        } else {
          alert(result.error || "An error occurred.");
        }
      } catch {
        alert("Failed to fetch response.");
      }

      this.directMessage = "";
      this.scrollToBottom(this.$refs.directChatBox);
    },
    scrollToBottom(element) {
      element.scrollTop = element.scrollHeight;
    },
  },
};
</script>

<style scoped>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

/* Reset and Base Styles */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,
body {
  height: 100%;
}

body {
  font-family: 'Roboto', sans-serif;
}

/* Sidebar Styling */
.sidebar {
  margin: 50px auto 0 auto;
  position: fixed;
  top: 0;
  left: 0;
  width: 350px;
  height: 100vh;
  /* Add a gradient background with texture */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%),
    url('https://www.transparenttextures.com/patterns/cubes.png');
  background-blend-mode: overlay;
  /* Ensures the gradient and texture blend */
  color: #ffffff;
  padding: 30px 25px;
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  transition: all 0.3s ease;
}

.sidebar h1 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.sidebar label {
  display: block;
  margin-top: 20px;
  font-weight: 500;
  font-size: 1rem;
}

.sidebar input[type="text"],
.sidebar input[type="file"] {
  width: 100%;
  padding: 12px 15px;
  margin-top: 8px;
  border: none;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  font-size: 0.95rem;
  transition: background-color 0.3s, transform 0.3s;
}

.sidebar input[type="text"]::placeholder,
.sidebar input[type="file"]::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.sidebar input[type="text"]:focus,
.sidebar input[type="file"]:focus {
  background-color: rgba(255, 255, 255, 0.3);
  outline: none;
  transform: scale(1.02);
}

.sidebar button {
  width: 100%;
  margin-top: 25px;
  padding: 12px;
  background-color: #ff7e5f;
  background-image: linear-gradient(45deg, #ff7e5f, #feb47b);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s, transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.sidebar button:hover {
  background-image: linear-gradient(45deg, #feb47b, #ff7e5f);
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

/* Status Message */
.status {
  margin-top: 20px;
  font-style: italic;
  color: #d1d8e0;
  text-align: center;
}

/* Main Content Styling */
.main-content {
  margin: 50px auto 0 auto;
  margin-left: 350px;
  padding: 30px 20px;
  height: 100vh;
  overflow-y: auto;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 50px;
  transition: margin-left 0.3s ease;
}

.chat-section-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.chat-section-container h2 {
  font-size: 1.6rem;
  color: #2c3e50;
  margin-bottom: 10px;
  font-weight: 600;
}

.chat-section {
  flex-grow: 1;
  border: 1px solid #ecf0f1;
  border-radius: 12px;
  padding: 20px;
  background-color: #f9f9fb;
  overflow-y: auto;
  max-height: 600px;
  /* Increased max-height for larger display */
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.3s;
}

.chat-section:hover {
  box-shadow: inset 0 4px 8px rgba(0, 0, 0, 0.1);
}

.chat-section p {
  margin-bottom: 15px;
  line-height: 1.6;
  font-size: 0.95rem;
}

.chat-section p.You {
  text-align: right;
}

.chat-section p.Assistant,
.chat-section p.AI {
  text-align: left;
}

.chat-section p strong {
  color: #34495e;
}

.chat-input {
  display: flex;
  gap: 15px;
}

.chat-input input {
  flex-grow: 1;
  padding: 12px 15px;
  border: 1px solid #bdc3c7;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.3s, transform 0.3s;
}

.chat-input input::placeholder {
  color: #95a5a6;
}

.chat-input input:focus {
  border-color: #3498db;
  outline: none;
  transform: scale(1.02);
}

.chat-input button {
  padding: 12px 20px;
  background-color: #1abc9c;
  background-image: linear-gradient(45deg, #1abc9c, #16a085);
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.3s, transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.chat-input button:hover {
  background-image: linear-gradient(45deg, #16a085, #1abc9c);
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

/* Message Roles */
.You {
  color: #1abc9c;
}

.Assistant,
.AI {
  color: #3498db;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .sidebar {
    position: relative;
    width: 100%;
    height: auto;
    margin-bottom: 20px;
    top: auto;
    left: auto;
    bottom: auto;
  }

  .main-content {
    margin-left: 0;
    padding: 20px;
  }

  .chat-section {
    max-height: 500px;
    /* Adjusted for smaller screens */
  }
}

@media (max-width: 768px) {
  .sidebar {
    padding: 25px 20px;
  }

  .sidebar h1 {
    font-size: 1.8rem;
  }

  .sidebar label {
    font-size: 0.95rem;
  }

  .sidebar input[type="text"],
  .sidebar input[type="file"] {
    padding: 10px 12px;
    font-size: 0.9rem;
  }

  .sidebar button {
    padding: 10px;
    font-size: 0.95rem;
  }

  .main-content {
    padding: 15px;
    gap: 30px;
  }

  .chat-section {
    max-height: 400px;
    /* Further adjusted for mobile */
  }

  .chat-section-container h2 {
    font-size: 1.4rem;
  }

  .chat-input input {
    padding: 10px 12px;
    font-size: 0.9rem;
  }

  .chat-input button {
    padding: 10px 18px;
    font-size: 0.95rem;
  }
}
</style>

