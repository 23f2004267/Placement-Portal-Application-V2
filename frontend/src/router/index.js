import { createRouter, createWebHistory } from "vue-router"

import Login from "../views/Login.vue"
import StudentRegister from "../views/StudentRegister.vue"
import CompanyRegister from "../views/CompanyRegister.vue"
import StudentDashboard from "../views/StudentDashboard.vue"
import CompanyDashboard from "../views/CompanyDashboard.vue"
import AdminDashboard from "../views/AdminDashboard.vue"
import DriveDetails from "../views/DriveDetails.vue"
import StudentApplications from "../views/StudentApplications.vue"


const routes = [
    { path: "/", component: Login },
    { path: "/register/student", component: StudentRegister },
    { path: "/register/company", component: CompanyRegister },

    { path: "/student", component: StudentDashboard, meta: { requiresAuth: true } },
    { path: "/student/applications", component: StudentApplications, meta: { requiresAuth: true } },
    { path: "/company", component: CompanyDashboard, meta: { requiresAuth: true } },
    { path: "/admin", component: AdminDashboard, meta: { requiresAuth: true } },
    { path: "/drive/:id", component: DriveDetails, meta: { requiresAuth: true } }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token")
    const role = localStorage.getItem("role")

    if (to.meta.requiresAuth && !token) {
        next("/")
    } 
    else if (to.path.startsWith("/student") && role !== "student") {
        next("/")
    }
    else if (to.path.startsWith("/company") && role !== "company") {
        next("/")
    }
    else if (to.path.startsWith("/admin") && role !== "admin") {
        next("/")
    }
    else {
        next()
    }
})

export default router