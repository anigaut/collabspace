import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/register",
      name: "register",
      component: () => import("../views/RegisterView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/",
      name: "project",
      component: () => import("../views/ProjectView.vue"),
    },
    {
      path: "/milestones",
      name: "milestone",
      component: () => import("../views/MilestoneView.vue"),
    },
    {
      path: "/submission/:milestoneID",
      name: "submission",
      component: () => import("../views/MilestoneSubmissionFeedbackView.vue"),
    },
    {
      path: "/mentorship",
      name: "mentorship",
      component: () => import("../views/MentorshipView.vue"),
    },
    {
      path: "/chatUsers",
      name: "chatUsers",
      component: () => import("../views/ChatUsersView.vue"),
    },
    {
      path: "/summaryai",
      name: "summaryai",
      component: () => import("../views/SummaryAI.vue"),
    },
    {
      path: "/chatInterface",
      name: "chatInterface",
      component: () => import("../views/ChatInterfaceView.vue"),
    },
    {
      path: '/plagiarism-check',
      name: 'plagiarism-check',
      component: () => import('../views/PlagiarismCheckView.vue')
    },
    {
      path: "/adminDashboard",
      name: "admin-dashboard",
      component: () => import("../views/AdminPage.vue"),
    },
    {
      path: "/students",
      name: "StudentList",
      component: () => import("../views/StudentListView.vue"),
    },
    {
      path: "/student-progress/:id",
      name: "StudentProgress",
      component: () => import("../views/StudentProgressView.vue"),
      props: true,
    },
  ],
});

export default router;
