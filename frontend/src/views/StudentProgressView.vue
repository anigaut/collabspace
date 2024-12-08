<template>
  <div class="progress-container">
    <h1>Project Progress</h1>

    <!-- Student Information -->
    <div v-if="progress" class="student-info">
      <p><strong>Student Name:</strong> {{ progress.student_name }}</p>
      <p><strong>GitHub Repository:</strong> 
        <a :href="`https://github.com/${progress.github_repo}`" target="_blank">{{ progress.github_repo }}</a>
      </p>
    </div>

    <!-- Milestones List -->
    <div v-if="progress && progress.progress.length" class="progress-details">
      <div 
        v-for="(milestone, index) in currentMilestones" 
        :key="index" 
        class="milestone-item"
      >
        <div @click="toggleMilestone(index)" class="milestone-header">
          <h3>{{ milestone.milestone_title }}</h3>
          <span v-if="isMilestoneExpanded(index)">-</span>
          <span v-else>+</span>
        </div>
        
        <div v-if="isMilestoneExpanded(index)" class="milestone-content">
          <p><strong>Description:</strong> {{ milestone.milestone_description }}</p>
          <p><strong>Date Issued:</strong> {{ milestone.date_issued }}</p>
          <p><strong>Deadline:</strong> {{ milestone.deadline }}</p>
          <p><strong>GitHub Link:</strong> 
            <a :href="milestone.submission_github_link" target="_blank">{{ milestone.submission_github_link }}</a>
          </p>
          <p><strong>Marks:</strong> {{ milestone.marks }}</p>
          <p><strong>Instructor Feedback:</strong> {{ milestone.instructor_feedback }}</p>
          <p><strong>Plagiarism Score:</strong> {{ milestone.plagiarism_score }}</p>
          <p><strong>Plagiarism Status:</strong> {{ milestone.plagiarism_status }}</p>
        </div>
      </div>
      
      <!-- Pagination Controls -->
      <div class="pagination">
        <button @click="loadMore" v-if="currentMilestones.length < progress.progress.length">Load More</button>
      </div>
    </div>

    <!-- Error or No Submissions Message -->
    <p v-else-if="errorMessage" class="error-text">{{ errorMessage }}</p>
    <p v-else class="no-submissions-text">No submissions yet</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["id"],
  data() {
    return {
      studentId: this.id,
      progress: null,
      errorMessage: null,
      currentMilestoneIndex: 0,
      milestonesPerPage: 5, // Number of milestones to display per page
      expandedMilestones: [], // Track which milestones are expanded
    };
  },
  computed: {
    currentMilestones() {
      return this.progress.progress.slice(0, this.currentMilestoneIndex);
    },
  },
  methods: {
    async fetchProgress() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/instructor/student_progress/${this.studentId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`, // Include token if required
          },
        });
        this.progress = response.data;
        this.errorMessage = null; // Clear any previous errors
      } catch (error) {
        if (error.response && error.response.data && error.response.data.error) {
          this.errorMessage = error.response.data.error; // Set the error message from backend
        } else {
          this.errorMessage = "An unexpected error occurred.";
        }
        this.progress = null; // Clear any previous progress data
      }
    },
    loadMore() {
      if (this.currentMilestoneIndex < this.progress.progress.length) {
        this.currentMilestoneIndex += this.milestonesPerPage;
      }
    },
    toggleMilestone(index) {
      const isExpanded = this.expandedMilestones.includes(index);
      if (isExpanded) {
        this.expandedMilestones = this.expandedMilestones.filter(i => i !== index);
      } else {
        this.expandedMilestones.push(index);
      }
    },
    isMilestoneExpanded(index) {
      return this.expandedMilestones.includes(index);
    },
  },
  mounted() {
    this.fetchProgress();
  },
};
</script>

<style scoped>
.progress-container {
  font-family: Arial, sans-serif;
  margin: 20px;
  color: #333;
}

h1 {
  color: #2c3e50;
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: bold;
}

.student-info p {
  font-size: 16px;
  margin-bottom: 12px;
}

.progress-details {
  padding: 10px;
}

.milestone-item {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  transition: background-color 0.3s ease;
}

.milestone-item:hover {
  background-color: #ecf0f1;
}

.milestone-header {
  display: flex;
  justify-content: space-between;
  cursor: pointer;
}

.milestone-header h3 {
  font-size: 18px;
  color: #3498db;
  margin-bottom: 10px;
}

.milestone-content {
  padding-top: 10px;
  margin-top: 10px;
  border-top: 1px solid #ddd;
}

strong {
  color: #3498db;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

button {
  padding: 10px 15px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #2980b9;
}

.error-text, .no-submissions-text {
  font-size: 18px;
  font-weight: bold;
  text-align: center;
}

.error-text {
  color: #e74c3c;
}

.no-submissions-text {
  color: #f39c12;
}
</style>
