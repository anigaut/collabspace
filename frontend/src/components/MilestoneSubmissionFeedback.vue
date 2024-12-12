<template>
  <div class="submission-container">
    <div v-if="userRole === 'instructor'">
      <div class="submission-header">Submissions for Milestone {{ milestoneID }}</div>
      <div class="submission-grid">
        <div 
          v-for="submission in submissions" 
          :key="submission.id" 
          class="submission-card"
        >
          <!-- <div class="card-icon">
            <div class="circle-icon">{{ submission.student_id }}</div>
          </div> -->
          <div class="card-content">
            <h3>Student ID: {{ submission.student_id }}</h3>
            
              <a v-bind:href="submission.github_branch_link">GitHub Link</a>
              <div class="lines">Plagiarism Status: {{ submission.plagiarism_status }}</div>
              <div class="lines">Plagiarism Score: {{ submission.plagiarism_score }}</div>
              <br>
  
              <div class="lines" v-if="submission.instructor_feedback">
                Feedback Given: {{ submission.instructor_feedback }}
              </div>
  
              <div v-if="submission.marks">
                Marks: {{ submission.marks }}
              </div>
  
              <div>
  
              </div>
              <div class="feedback-section">
                <input 
                  v-model="submission.instructor_feedback" 
                  placeholder="Enter feedback" 
                  class="feedback-input"
                />
                <div>
                  <input
                    v-model="submission.marks"
                    placeholder="Enter Marks"
                    class="feedback-input"
                  />
                </div>
                <!-- <button @click="sendFeedback(submission)">Submit</button> -->
                <button @click="enterEvaluation(submission.id, submission.instructor_feedback, submission.marks)">Submit</button>
              </div> 
  
          </div>
        </div>
      </div>
    </div>

    <div v-if="userRole === 'student'">
      <div class="submission-card">
        <div class="card-content">
          <h3>Milestone {{ milestoneID }} Submission</h3>
          <div v-if="studentSubmission.github_branch_link">
            <a v-bind:href="studentSubmission.github_branch_link">Submitted GitHub Branch Link</a>
          </div>

          <div v-if="studentSubmission.instructor_feedback">
            <p>Instructor Feedback: {{ studentSubmission.instructor_feedback }}</p>
          </div>

          <div v-if="studentSubmission.marks">
            <p>Marks: {{ studentSubmission.marks }}</p>
          </div>
          <br>
          <div v-if="!studentSubmission.github_branch_link">
            <div class="feedback-section">
              <input 
                v-model="submissionGitHubLink" 
                placeholder="Submit GitHub Branch Link" 
                class="feedback-input"
              />
              <button @click="makeSubmission(milestoneID, studentID)">Submit</button>
            </div> 
          </div>
          
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  mounted() {
    this.milestoneID = this.$route.params.milestoneID,
    this.getAllSubmissions(this.milestoneID),
    this.getSubmission(this.milestoneID, this.studentID)
  },

  data() {
    return {
      userRole: JSON.parse(localStorage.getItem("user_info"))["role"],
      studentID: JSON.parse(localStorage.getItem("user_info"))["user_id"],
      milestoneID: 1,
      submissions: [],
      submissionGitHubLink: "",
      studentSubmission: {},
    }
    
  },

  methods: {
    getAllSubmissions(milestoneID) {
      // only for instructor
      axios.get(`http://127.0.0.1:5000/api/instructor/get_submission/${milestoneID}`)
      .then((response) => {
        console.log(response.data);
        this.submissions = response.data.submissions_data;
      })
      .catch((error) => {
        console.log(error.response.data);
      })
    },

    getSubmission(milestoneID, studentID) {
      // for student
      axios.get(
        `http://127.0.0.1:5000/api/student/get_submission/${milestoneID}/${studentID}`
      )
      .then((response) => {
        console.log(response.data);
        this.studentSubmission = response.data.submission_details;
      })
      .catch((error) => {
        console.log(error.response.data);
      })

    },

    enterEvaluation(submissionID, feedback, marks) {
      axios.post(
        `http://127.0.0.1:5000/api/instructor/add_feedback/${submissionID}`,
        {feedback: feedback, marks: marks}
      )
      .then((response) => {
        alert(response.data.message);
      })
      .catch((error) => {
        alert(error.response.data);
      })
    },

    makeSubmission(milestoneID, studentID, githubBranchLink) {
      axios.post(
        `http://127.0.0.1:5000/api/student/submit_milestone/${milestoneID}/${studentID}`,
        {github_branch_link: this.submissionGitHubLink}
      )
      .then((respose) => {
        alert(respose.data.message);
        window.location.href = `/submission/${milestoneID}`;
      })
      .catch((error) => {
        alert(error.response.data);
      })
    },

    getInitials (title) {
    return title
    .split(' ')
    .map((word) => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
    }
  }
}

import axios from 'axios';
</script>

<style scoped>
a{
 color: cornflowerblue;
}

div{
  color: cornflowerblue;
}

.lines{
  color: #4b5563;
}

h3{
  color: black;
}
.submission-container {
  margin: 0.5rem;
  padding: 0.5rem;
  background-color: #f3f4f6;
}

.submission-header {
  margin-top: 4rem;
  color: gray;
  margin-bottom: 3rem;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
}

.submission-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 640px) {
  .submission-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.submission-card {
  display: flex;
  align-items: center;
  background-color: #ffffff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  padding: 16px;
}

.card-icon {
  margin-right: 16px;
}

.circle-icon {
  width: 50px;
  height: 50px;
  background-color: #e5e7eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: bold;
  color: #111827;
}

.card-content {
  flex: 1;
}

.card-content h3 {
  font-size: 1.25rem;
  margin-bottom: 8px;
  font-weight: 600;
}

.card-content p {
  font-size: 0.875rem;
  margin-bottom: 12px;
  color: #6b7280;
}

.feedback-section {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
}

.feedback-input,
.link-input {
  flex: 1;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #d1d5db;
}

.feedback-input:focus,
.link-input:focus {
  outline: none;
  border-color: #2563eb;
}

button {
  background-color: #2563eb;
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out;
}

button:hover {
  background-color: #1d4ed8;
}
</style>
