<template>
    <div class="chat-window">
      <header class="chat-header">
        <h3>{{ otherUser.name }}</h3>
        <span>{{ otherUser.role }}</span>
      </header>
      <ul class="chat-messages">
        <li v-for="msg in messages" :key="msg.id" :class="{ sent: msg.isSent, received: !msg.isSent }">
          <p>{{ msg.message }}</p>
          <small>{{ msg.timestamp }}</small>
        </li>
      </ul>
      <div class="chat-input">
        <input v-model="newMessage" placeholder="Type your message..." />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const otherUser = ref({ name: 'Jane Smith', role: 'TA' }); // Replace with API data
const messages = ref([]);
const newMessage = ref('');

const fetchMessages = async () => {
  // Replace with actual conversation ID
  const response = await axios.get(`/api/messages?conversation_id=1`);
  messages.value = response.data.map(msg => ({
    ...msg,
    isSent: msg.sender_id === 1 // Assume current user ID is 1
  }));
};

const sendMessage = async () => {
  if (!newMessage.value) return;
  const response = await axios.post('/api/messages', {
    sender_id: 1, // Replace with current user ID
    receiver_id: 2, // Replace with other user's ID
    message: newMessage.value
  });
  if (response.data.success) {
    fetchMessages();
    newMessage.value = '';
  }
};

onMounted(() => {
  fetchMessages();
});
</script>

<style scoped>
.chat-window {
  padding: 0.5rem;
  margin: 0.5rem;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid #ddd;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.chat-messages li {
  margin-bottom: 10px;
}

.chat-messages li.sent {
  text-align: right;
}

.chat-messages li.received {
  text-align: left;
}

.chat-input {
  display: flex;
  padding: 16px;
  border-top: 1px solid #ddd;
}

.chat-input input {
  flex: 1;
  margin-right: 8px;
}
</style>