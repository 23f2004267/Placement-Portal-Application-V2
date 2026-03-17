import { createRouter, createWebHistory } from "vue-router"

import Login from "../views/Login.vue"
import StudentDashboard from "../views/StudentDashboard.vue"
import CompanyDashboard from "../views/CompanyDashboard.vue"
import AdminDashboard from "../views/AdminDashboard.vue"

const routes = [
    { path: "/", component: Login },

    { path: "/student", component: StudentDashboard, meta: { requiresAuth: true } },
    { path: "/company", component: CompanyDashboard, meta: { requiresAuth: true } },
    { path: "/admin", component: AdminDashboard, meta: { requiresAuth: true } }
]

const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

router.beforeEach((to, from, next) => {

    const token = localStorage.getItem("token")

    if (to.meta.requiresAuth && !token) {
        next("/")
    } 
    else if (to.path === "/" && token) {
        next("/admin")
    }
    else {
        next()
    }

})

export default router