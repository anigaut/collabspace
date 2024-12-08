<template>
  <div class="student-list">
    <h1>Students</h1>

    <!-- Search Bar -->
    <input 
      type="text" 
      v-model="searchQuery" 
      placeholder="Search students..." 
      class="search-bar"
    />

    <!-- Student Cards -->
    <div v-if="students.length" class="students-container">
      <div 
        v-for="student in filteredStudents" 
        :key="student.id" 
        class="student-card"
      >
        <div class="student-info">
          <span class="student-name">{{ student.first_name }} {{ student.last_name }}</span>
          <span class="student-email">{{ student.email }}</span>
        </div>
        <button @click="viewProgress(student.id)" class="view-progress-btn">View Progress</button>
      </div>
    </div>

    <!-- No Students Found -->
    <p v-else class="no-students">No students found.</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      students: [],
      searchQuery: "",  // For searching/filtering
    };
  },
  computed: {
    // Filter students based on search query
    filteredStudents() {
      return this.students.filter(student =>
        `${student.first_name} ${student.last_name} ${student.email}`
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/api/instructor/students", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`, // Include token if required
          },
        });
        this.students = response.data.students;
      } catch (error) {
        console.error("Error fetching students:", error);
      }
    },
    viewProgress(studentId) {
      this.$router.push({ name: "StudentProgress", params: { id: studentId } });
    },
  },
  mounted() {
    this.fetchStudents();
  },
};
</script>

<style scoped>
.student-list {
  font-family: 'Arial', sans-serif;
  margin: 20px;
  color: #333;
  text-align: center;
}

h1 {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 15px;
  font-weight: bold;
}

.search-bar {
  padding: 10px;
  width: 80%;
  max-width: 400px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.students-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.student-card {
  width: 250px;
  padding: 20px;
  margin: 10px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  text-align: left;
  display: flex;
  flex-direction: column;
}

.student-card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.student-info {
  margin-bottom: 15px;
}

.student-name {
  font-size: 18px;
  font-weight: bold;
  color: #3498db;
  margin-bottom: 5px;
  display: block; /* Ensures name is on a separate line */
}

.student-email {
  font-size: 14px;
  color: #777;
  display: block; /* Ensures email is on a separate line */
}

.view-progress-btn {
  width: 100%;
  padding: 10px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin-top: 10px;
}

.view-progress-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

.no-students {
  font-size: 18px;
  color: #e74c3c;
  margin-top: 20px;
  font-weight: bold;
}

@media (max-width: 768px) {
  .students-container {
    flex-direction: column;
  }
  
  .search-bar {
    width: 90%;
  }

  .student-card {
    width: 90%;
  }
}
</style>
