<template>
  <nav class="navbar">
    <div class="navbar-left">
      <RouterLink to="/" class="brand">CollabSpace</RouterLink>
    </div>
    <div class="navbar-right">
      <RouterLink to="/login" class="nav-item">Login</RouterLink>
      <RouterLink to="/register" class="nav-item">Register</RouterLink>
      <RouterLink to="/" class="nav-item" @click="logout">Logout</RouterLink>
      <!-- <RouterLink to="/mentorship" class="nav-item">Mentorship-Sessions</RouterLink> -->
      <RouterLink to="/chatUsers" class="nav-item">Chat</RouterLink>
      <RouterLink to="/summaryai" class="nav-item">Summarizer</RouterLink>

    </div>
  </nav>
</template>

<script setup>
import axios from 'axios';
import { useRouter } from "vue-router";

const router = useRouter();

const logout = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:5000/api/auth/logout", {}, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
      },
    });

    alert(response.data.message || "Logged out successfully!");

    localStorage.removeItem("access_token");
    localStorage.removeItem("user_info");

    router.push("/");
  } catch (error) {
    console.error("Logout failed:", error.response || error.message);
    alert(error.response?.data?.message || "An error occurred while logging out.");
  }
};
</script>
  
  <style scoped>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #1f2937;
    color: white;
    padding: 10px 24px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 1000;
  }
  
  .navbar-left .brand {
    font-size: 1.5rem;
    font-weight: bold;
    color: #ffffff;
    text-decoration: none;
  }
  
  .navbar-right {
    display: flex;
    gap: 16px;
  }
  
  .nav-item {
    color: #ffffff;
    text-decoration: none;
    font-size: 1rem;
    transition: color 0.2s ease-in-out;
  }
  
  .nav-item:hover {
    color: #a3e635; /* Light green on hover */
  }
  
  body {
    margin: 0;
    padding-top: 60px; /* Prevent content from hiding under the navbar */
  }
  
  @media (max-width: 768px) {
    .navbar-right {
      flex-direction: column;
      gap: 8px;
      position: absolute;
      top: 100%;
      right: 10px;
      background-color: #1f2937;
      padding: 10px;
      border-radius: 5px;
    }
  
    .navbar {
      flex-direction: column;
    }
  }
  </style>
  