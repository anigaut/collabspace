<template>
  <div class="chat-users">
    <h2>Chat</h2>
    <ul>
    <RouterLink to='/chatWindow'> 
      <li 
        v-for="user in users" 
        :key="user.id" 
        class="user-item"
        @click="selectUser(user)">
        <img :src="user.image" alt="User Image" class="user-image" />
        <div class="user-info">
          <p class="user-name">{{ user.name }}</p>
          <p class="user-last-msg">{{ user.lastMessage }}</p>
        </div>
        <div class="user-status" :class="user.status"></div>
        <div class="user-popup" v-if="hoveredUser === user.id">
          <p><strong>Email:</strong> {{ user.email }}</p>
          <p><strong>Status:</strong> {{ user.status }}</p>
        </div>
      </li>
      </RouterLink>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const users = ref([
  { id: 1, name: 'John Doe', lastMessage: 'Hey, how are you?', image: 'https://via.placeholder.com/40', email: 'john@example.com', status: 'online' },
  { id: 2, name: 'Jane Smith', lastMessage: 'Meeting tomorrow?', image: 'https://via.placeholder.com/40', email: 'jane@example.com', status: 'offline' },
  { id: 3, name: 'Alice Johnson', lastMessage: 'Great job!', image: 'https://via.placeholder.com/40', email: 'alice@example.com', status: 'away' }
]);

const hoveredUser = ref(null);

const emit = defineEmits(['selectUser']);

const selectUser = (user) => {
  emit('selectUser', user);
};
</script>

<style scoped>
h2 {
  color: gray;
  font-weight: bold;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.chat-users {
  margin-top: 5rem;
  background-color: #fff;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.user-item {
  border-radius: 50%;
  display: flex;
  align-items: center;
  padding: 12px;
  margin-bottom: 10px;
  background-color: #f8fafc;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  transition: background-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.user-item:hover {
  background-color: #f1f5f9;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.user-image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
}

.user-info {
  flex-grow: 1;
}

.user-name {
  color: black;
  font-weight: bold;
  font-size: 1rem;
  margin: 0;
}

.user-last-msg {
  color: #6b7280;
  font-size: 0.85rem;
  margin: 2px 0 0;
}

.user-status {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-left: 10px;
}

.user-status.online {
  background-color: #10b981;
}

.user-status.offline {
  background-color: #d1d5db;
}

.user-status.away {
  background-color: #fbbf24;
}

.user-popup {
  position: absolute;
  top: 50%;
  left: 100%;
  transform: translate(10px, -50%);
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 10px;
  font-size: 0.85rem;
  width: 200px;
}
</style>
