<template>
    <div class="container">
      <div class="header">Milestones</div>
      <div class="content">
        <div v-if="role === 'instructor'" class="create-container">
          <div class="card-header">
            <h3>Title: </h3>
            <input type="text" v-model="milestone.title" />
          </div>
          <div class="card-body">
            <p>Description: </p>
            <input type="text" v-model="milestone.description" />
          </div>
          <div class="card-body">
            <p>Date Issued: </p>
            <input type="date" v-model="milestone.date_issued" />
          </div>
          <div class="card-body">
            <p>Deadline: </p>
            <input type="date" v-model="milestone.deadline" />
          </div>
          <div class="create-milestone" @click="createMilestone">
            + Milestone
          </div>
        </div>

        <div class="grid">
          <div
            v-for="milestone in milestones"
            :key="milestone.id"
            class="milestone-card"
            :class="{
              'completed': milestone.status === 'completed',
              'pending': milestone.status === 'pending',
              'incomplete': milestone.status === 'incomplete'
            }"
          >
            <div class="card-header">
              <h3>
                <RouterLink :to="{ name: 'submission', params: { milestoneID: milestone.id } }">
                  {{ milestone.title }}
                </RouterLink>
              </h3>

              <div class="stats">
                <span v-if="role === 'student'" :class="statusClass(milestone.status)">
                  {{ milestone.status }}
                </span>

                <div v-if="role === 'instructor'" class="mile-icon" @click="deleteMilestone(milestone.id)">❌</div>
              </div>
            </div>
            <div v-if="role === 'student'" class="card-body">
              <p>{{ milestone.description }}</p>
              <p color="cyan">{{ milestone.date_issued }}</p>
              <p color="pink">{{ milestone.deadline }}</p>
            </div>

            <div v-if="role === 'instructor'" class="edit-body">
              <div class="edits">
                <p>Title:</p>
                <input type="text" v-model="milestone.title" />
                <p>Description:</p>
                <input type="text" v-model="milestone.description" />
                <p>Date Issued:</p>
                <input type="date" v-model="milestone.date_issued" />
                <p>Deadline:</p>
                <input type="date" v-model="milestone.deadline" />
              </div>
              <div class="mile-icon" @click="updateMilestone(milestone.id, milestone)">✏️</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import axios from "axios";
  import { ref, onMounted } from 'vue';
  import { RouterLink } from 'vue-router';

  const role = ref(null);
  const isLoggedIn = ref(false);
  const studentID = JSON.parse(localStorage.getItem("user_info"))["user_id"];

  onMounted(() => {
    const userInfo = localStorage.getItem('user_info');
    if (userInfo) {
      const parsedInfo = JSON.parse(userInfo);
      role.value = parsedInfo.role;
      isLoggedIn.value = true;
    } else {
      isLoggedIn.value = false;
    }
  });

  const milestone = ref({
    title: "",
    description: "",
    date_issued: "",
    deadline: "",
  });

  const createMilestone = async () => {
    const dateIssued = new Date(milestone.value.date_issued);
    const deadline = new Date(milestone.value.deadline);

    if (deadline < dateIssued) {
      alert("Deadline cannot be before the date issued.");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/instructor/create_milestone",
        milestone.value
      );
      milestone.value = {
        title: "",
        description: "",
        date_issued: "",
        deadline: "",
      };
      window.location.href = '/milestones';
    } catch (error) {
      console.error(error.response.data);
      alert(error.response.data.errors || error.response.data.error);
    }
  };

  const editedMilestone = ref({
    title: "",
    description: "",
    date_issued: "",
    deadline: "",
  });
  
  const updateMilestone = async (milestoneId, milestone) => {
    const editedMilestone = ref({ ...milestone });
    try {
      const response = await axios.post(
        `http://127.0.0.1:5000/api/instructor/update_milestone/${milestoneId}`,
        editedMilestone.value
      );
      alert(response.data.message);
      Object.assign(milestone, editedMilestone.value);
    } catch (error) {
      console.error(error.response.data);
      alert(error.response.data.error);
    }
  };
  
  const milestones = ref([]);

  const fetchMilestones = async () => {
    try {
      const milestoneResponse = await axios.get("http://127.0.0.1:5000/api/student/milestones");
      const milestoneData = milestoneResponse.data.milestones;
      for (const milestone of milestoneData) {
        try {
          const submissionResponse = await axios.get(
            `http://127.0.0.1:5000/api/student/get_submission/${milestone.id}/${studentID}`
          );
          const submissionDetails = submissionResponse.data.submission_details;

          const currentDate = new Date();
          const deadlineDate = new Date(milestone.deadline);

          if (submissionDetails.github_branch_link) {
            milestone.status = currentDate <= deadlineDate ? "completed" : "incomplete";
          } else {
            milestone.status = currentDate <= deadlineDate ? "pending" : "incomplete";
          }
        } catch (error) {
          const currentDate = new Date();
          const deadlineDate = new Date(milestone.deadline);

          milestone.status = currentDate > deadlineDate ? "incomplete" : "pending";
        }
      }

      milestones.value = milestoneData;
    } catch (err) {
      console.error("Error fetching milestones:", err);
    }
  };

  fetchMilestones();

  const statusClass = (status) => {
    switch (status) {
      case "completed":
        return "status-green";
      case "pending":
        return "status-grey";
      case "incomplete":
        return "status-red";
      default:
        return "";
    }
  };

  const deleteMilestone = async (milestoneId) => {
    try {
      const response = await axios.delete(
        `http://127.0.0.1:5000/api/instructor/delete_milestone/${milestoneId}`
      );

      milestones.value = milestones.value.filter((m) => m.id !== milestoneId);
    } catch (error) {
      console.error(error.response?.data || error.message);
      alert(error.response?.data?.error || "An error occurred while deleting.");
    }
  };

  </script>
  
  
  <style scoped>
  .stats{
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  input{
    color: grey;
    box-shadow: 1px 1px 1px 1px rgba(0, 0, 0, 0.1);
    padding: 1px;
  }

  p{
    color: #4b5563;
  }

  .edits{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin: 0.5rem 0;
  }

  .edit-body{
    gap: 0.5rem;
    display: flex;
    margin: 0 0.5rem;
    padding: 0 0.5rem;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e5e7eb
  }

  .mile-icon{
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .mile-icon:hover{
    cursor: pointer;
    transform: scale(1.05);
    background-color: #06b6d4;
  }

  .create-milestone{
    color: #000;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    width: fit-content;
    margin: 1rem;
    padding: 0.5rem;
  }

  .create-milestone:hover{
    cursor: pointer;
    transform: scale(1.05);
    background-color: #06b6d4;
  }

  .container {
    background-color: #f3f4f6;
    padding: 24px;
  }

  .create-container{
    max-width: 70vh;
    padding: 0.5rem;
    margin-bottom: 1rem;
    background-color: #fff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    border-left: 8px solid #06b6d4;
  }
  
  .header {
    text-align: center;
    font-size: 1.5rem;
    padding-bottom: 48px;
    padding-top: 4rem;
    color: gray;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  
  .content {
    max-width: 64rem;
    margin: 0 auto;
  }
  
  .grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
  }
  
  @media (min-width: 640px) {
    .grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  .milestone-card {
    background-color: #fff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    transition: transform 0.2s ease-in-out;
    overflow: hidden;
  }
  
  .milestone-card:hover {
    transform: scale(1.05);
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap:0.5rem;
    padding: 16px;
    border-bottom: 1px solid #e5e7eb;
  }
  
  .card-header h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #111827;
  }

  .status-grey{
    color: #4b5563;
  }
  
  .status-green {
    background-color: #d1fae5;
    color: #047857;
  }
  
  .status-white {
    background-color: #ffffff;
    color: #374151;
    border: 1px solid #d1d5db;
  }
  
  .status-red {
    background-color: #fee2e2;
    color: #b91c1c;
  }
  
  .card-body {
    margin: 0 0.5rem;
    margin-top: 0.5rem;
    padding: 0 0.5rem;
  }
  
  .card-body p {
    color: #4b5563;
    font-size: 1rem;
  }
  
  .completed {
    border-left: 8px solid #10b981;
  }
  
  .pending {
    border-left: 8px solid #f3f4f6;
  }
  
  .incomplete {
    border-left: 8px solid #ef4444;
  }
  </style>
  