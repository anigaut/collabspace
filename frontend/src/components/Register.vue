<template>
  <div class="border">
  <h2>Register</h2>
  <div>
    <label for="firstName">First Name:</label>
    <input type="text" v-model="firstName" ><br><br>
    
    <label for="lastName">Last Name:</label>
    <input type="text" v-model="lastName" ><br><br>
    
    <label for="email">Email:</label>
    <input type="email" v-model="email" required><br><br>
    
    <label for="password">Password:</label>
    <input type="password" v-model="password" required><br><br>
    
    <label for="password">Confirm Password:</label>
    <input type="password" v-model="password2" required><br><br>

    <label for="role" style="margin-right: 1rem;">Role:</label>
    <select style="padding: 0.5rem;" class="form-control" id="role" v-model="selectedRole">
      <option value="student">Student</option>
      <option value="ta">TA</option>
      <option value="admin">Admin</option>
      <option value="instructor">Instructor</option>
    </select><br><br>
    
    <button @click="register()">Register</button>
  </div>
    <br>
  <p>
  Already have an account? <RouterLink to="/login"> <button>Login</button> </RouterLink>
  </p>
</div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const firstName = ref('');
const lastName = ref('');
const email = ref('');
const password = ref('');
const password2 = ref('');
const selectedRole = ref('student');
const router = useRouter();

const register = async () => {
  if (!firstName.value || !lastName.value || !email.value || !password.value || !password2.value || !selectedRole.value) {
    alert('All fields are required.');
    return;
  }

  if (password.value !== password2.value) {
    alert('Passwords do not match.');
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:5000/api/auth/register', {
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      password: password.value,
      role: selectedRole.value,
    });

    alert(response.data.message || 'Registration successful!');

    // Save user info and token in local storage
    const { access_token, user_info } = response.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('user_info', JSON.stringify(user_info));

    router.push('/login');
  } catch (error) {
    const errorMessage =
      error.response?.data?.message || 'Failed to register. Please try again.';
    alert(errorMessage);
    console.error(error.response || error.message);
  }
};
</script>

<style>
.border{
    padding: 2rem;
    background-color: #fff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    margin-top: 5rem;
}

h2 {
  color: gray;
  font-weight: bold;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

label {
  color: black;
  font-weight: bold;
}

input[type='text'],
input[type='email'],
input[type='password'] {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

p{
  color: black;
}
</style>
