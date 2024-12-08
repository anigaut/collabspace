<template>
    <div class="plagiarism-check-container">
        <div class="header">
            <h1>Plagiarism Checker</h1>
        </div>

        <div class="input-section">
            <input v-model="githubRepoLink" type="text" placeholder="Enter GitHub Repository Link" class="repo-input" />

            <!-- Dropdown for selecting student -->
            <div class="custom-select">
                <select v-model="selectedStudentId" class="student-select" aria-label="Select a student">
                    <option disabled value="">Select a student</option>
                    <option v-for="student in students" :key="student.id" :value="student.id">
                        <span style="color: black;">{{ student.first_name }} {{ student.last_name }}</span>
                    </option>
                </select>
                <div class="arrow"></div>
            </div>

            <button @click="checkPlagiarism" class="check-btn">
                Check Plagiarism
            </button>
        </div>

        <div v-if="isLoading" class="loading">
            Checking Plagiarism, please wait...
        </div>

        <div v-if="!isLoading && students.length === 0" class="no-students">
            No students found. Please add students to the database.
        </div>

        <!-- Loader visible during plagiarism check -->
        <div v-if="isLoading" class="loader-container">
            <div class="loader"></div>
        </div>


        <div v-if="score !== null" class="score-card">
            <div class="score-circle" :style="scoreStyle">
                <span class="score-text">{{ score.toFixed(2) }}%</span>
            </div>
            <div class="score-label">Score</div>
        </div>

        <div v-if="plagiarismResults.length > 0" class="results-table">
            <table>
                <thead>
                    <tr>
                        <th>Student Name</th>
                        <th>Repository Link</th>
                        <th>Plagiarism Score</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(result, index) in plagiarismResults" :key="index">
                        <td>{{ result.student_name }}</td>
                        <td><a :href="result.repo_link" target="_blank">{{ result.repo_link }}</a></td>
                        <td>{{ result.score.toFixed(2) }}%</td>
                        <td :class="result.status">{{ result.status.toUpperCase() }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script>
import axios from 'axios';

export default {
    data() {
        return {
            githubRepoLink: '',
            selectedStudentId: '',
            students: [],
            isLoading: false,  // use this to control loader visibility
            score: null,
            plagiarismResults: [],
        };
    },
    mounted() {
        this.fetchStudents();
    },
    computed: {
        scoreStyle() {
            if (this.score === null) return {};
            const normalizedScore = Math.min(Math.max(this.score, 0), 100);
            const degree = (normalizedScore / 100) * 360;
            return {
                background: `conic-gradient(#00C9FF ${degree}deg, #92FE9D ${degree}deg)`,
                color: '#000',
            };
        },
    },
    methods: {
        async fetchStudents() {
            this.isLoading = true;  // Show loader while fetching students
            try {
                console.log("Fetching students...");
                const response = await axios.get('http://127.0.0.1:5000/api/ta/get_students');
                console.log("Students fetched:", response.data);
                this.students = response.data;
            } catch (error) {
                console.error('Error fetching students:', error);
                alert('Failed to load students. Please try again later.');
            } finally {
                this.isLoading = false;  // Hide loader after fetching students
            }
        },

        async checkPlagiarism() {
            if (!this.githubRepoLink || !this.selectedStudentId) {
                alert('Please provide both the GitHub repository link and select a student.');
                return;
            }

            this.isLoading = true;  // Show loader during plagiarism check

            try {
                const response = await axios.post('http://127.0.0.1:5000/api/ta/check_plagiarism', {
                    github_repo_link: this.githubRepoLink,
                    student_id: this.selectedStudentId,
                });

                const { overall_score, plagiarism_results } = response.data;
                this.score = overall_score;
                this.plagiarismResults = plagiarism_results;
                console.log("Plagiarism results received:", response.data);

            } catch (error) {
                console.error('Error checking plagiarism:', error);
                if (error.response) {
                    alert(`Error: ${error.response.data.error}`);
                } else if (error.request) {
                    alert('Error: No response from the server.');
                } else {
                    alert('An unexpected error occurred.');
                }
            } finally {
                this.isLoading = false;  // Hide loader after plagiarism check completes
            }
        },
    },
};
</script>


<style scoped>
/* Reset some basic styles */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* Import Roboto Font */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

/* Loader Styles */
.loader-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    /* Adjust based on your layout */
    text-align: center;
    z-index: 10;
    /* Ensure it's above other elements */
}

.loader {
    width: 28px;
    aspect-ratio: 1;
    border-radius: 50%;
    background: #E3AAD6;
    transform-origin: top;
    display: grid;
    animation: l3-0 1s infinite linear;
}

.loader::before,
.loader::after {
    content: "";
    grid-area: 1/1;
    background: #F4DD51;
    border-radius: 50%;
    transform-origin: top;
    animation: inherit;
    animation-name: l3-1;
}

.loader::after {
    background: #F10C49;
    --s: 180deg;
}

@keyframes l3-0 {

    0%,
    20% {
        transform: rotate(0);
    }

    100% {
        transform: rotate(360deg);
    }
}

@keyframes l3-1 {
    50% {
        transform: rotate(var(--s, 90deg));
    }

    100% {
        transform: rotate(0);
    }
}

/* General Container */
.plagiarism-check-container {
    max-width: 900px;
    margin: 100px auto 0 auto;
    /* Space from navbar */
    padding: 40px;
    font-family: 'Roboto', sans-serif;
    background-color: #1b1b38;
    /* Dark background for futuristic look */
    border-radius: 15px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    backdrop-filter: blur(8.5px);
    -webkit-backdrop-filter: blur(8.5px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    color: #ffffff;
    /* Default text color */
    position: relative;
}

/* Background Pattern (Optional) */
.plagiarism-check-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('https://www.transparenttextures.com/patterns/cubes.png');
    /* Example pattern */
    opacity: 0.15;
    border-radius: 15px;
    z-index: 1;
    pointer-events: none;
    /* Prevent this layer from capturing mouse events */
}

.plagiarism-check-container>* {
    position: relative;
    z-index: 2;
    /* Higher than ::before pseudo-element */
}

/* Header */
.header {
    text-align: center;
    margin-bottom: 40px;
}

.header h1 {
    color: #ffffff;
    font-size: 3em;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 700;
    text-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

/* Input Section */
.input-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    margin-bottom: 30px;
}

.repo-input,
.student-select {
    width: 100%;
    max-width: 600px;
    padding: 15px 25px;
    border: none;
    border-radius: 50px;
    font-size: 1em;
    background-color: rgba(255, 255, 255, 0.1);
    color: #ffffff;
    transition: background-color 0.3s, transform 0.3s;
}

.repo-input::placeholder,
.student-select::placeholder {
    color: #dddddd;
}

.repo-input:focus,
.student-select:focus {
    background-color: rgba(255, 255, 255, 0.2);
    outline: none;
    transform: scale(1.02);
}

/* Custom Select Dropdown */
.custom-select {
    position: relative;
    width: 100%;
    max-width: 600px;
}

.student-select {
    appearance: none;
    /* Remove default arrow */
    background: none;
    width: 100%;
    padding: 15px 50px 15px 25px;
    /* Space for the custom arrow */
    border-radius: 50px;
    background-color: rgba(255, 255, 255, 0.1);
    color: #ffffff;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.3s;
}

.student-select option {
    background-color: #2c2c3e;
    /* Dark background matching the container */
    color: #ffffff;
    /* White text for contrast */
}

.student-select option:hover {
    background-color: #3a3a5a;
    /* Slightly lighter dark background */
}

.custom-select .arrow {
    position: absolute;
    top: 50%;
    right: 20px;
    transform: translateY(-50%);
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 8px solid #ffffff;
    pointer-events: none;
    /* Allow clicks to pass through */
}

.student-select:hover {
    background-color: rgba(255, 255, 255, 0.2);
}

.student-select:focus {
    background-color: rgba(255, 255, 255, 0.3);
    outline: none;
    transform: scale(1.02);
}

/* Check Button */
.check-btn {
    padding: 15px 30px;
    border: none;
    border-radius: 50px;
    background: linear-gradient(45deg, #ff6ec4, #7873f5);
    color: #ffffff;
    font-size: 1em;
    cursor: pointer;
    transition: background 0.3s, transform 0.3s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.check-btn:hover {
    background: linear-gradient(45deg, #7873f5, #ff6ec4);
    transform: scale(1.05);
}

/* Loading and No Students */
.loading,
.no-students {
    text-align: center;
    margin-top: 20px;
    font-size: 1.2em;
    color: #dddddd;
}

/* Score Card */
.score-card {
    margin-top: 50px;
    text-align: center;
    position: relative;
}

.score-circle {
    width: 180px;
    height: 180px;
    margin: 0 auto;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2em;
    color: #ffffff;
    position: relative;
    z-index: 2;
    transition: transform 0.3s;
}

.score-circle:hover {
    transform: scale(1.05);
}

.score-circle::before {
    content: '';
    position: absolute;
    top: -5px;
    left: -5px;
    width: calc(100% + 10px);
    height: calc(100% + 10px);
    border-radius: 50%;
    background: linear-gradient(135deg, #ff6ec4, #7873f5);
    z-index: -1;
    animation: rotate 4s linear infinite;
    pointer-events: none;
    /* Ensure it doesn't block interactions */
}

.score-text {
    position: relative;
    z-index: 3;
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.score-label {
    margin-top: 15px;
    font-size: 1.5em;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;
}

/* Results Table */
.results-table {
    margin-top: 60px;
    overflow-x: auto;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.1);
    padding: 20px;
    backdrop-filter: blur(10px);
}

.results-table table {
    width: 100%;
    border-collapse: collapse;
    color: #ffffff;
}

.results-table th,
.results-table td {
    padding: 15px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    text-align: center;
    font-size: 1em;
}

.results-table th {
    background-color: rgba(255, 255, 255, 0.2);
    color: #ffffff;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.results-table tr:nth-child(even) {
    background-color: rgba(255, 255, 255, 0.05);
}

.results-table tr:hover {
    background-color: rgba(255, 255, 255, 0.1);
}

.results-table a {
    color: #00C9FF;
    text-decoration: none;
    transition: color 0.3s;
}

.results-table a:hover {
    color: #92FE9D;
}

/* Status Classes */
.fail {
    color: #FF4B5C;
    font-weight: bold;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.pass {
    color: #00E676;
    font-weight: bold;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* Keyframes for Rotating Border */
@keyframes rotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

/* Responsive Design */
@media (max-width: 768px) {
    .plagiarism-check-container {
        padding: 30px 20px;
    }

    .header h1 {
        font-size: 2.2em;
    }

    .repo-input,
    .student-select,
    .check-btn {
        max-width: 100%;
    }

    .score-card {
        margin-top: 40px;
    }

    .score-circle {
        width: 150px;
        height: 150px;
        font-size: 1.8em;
    }

    .score-label {
        font-size: 1.3em;
    }

    .results-table {
        margin-top: 50px;
    }

    .results-table th,
    .results-table td {
        padding: 12px 15px;
        font-size: 0.95em;
    }

    /* Adjust custom select arrow size on smaller screens */
    .custom-select .arrow {
        right: 15px;
    }
}
</style>
