<template>
<div class="applications-page">

    <div class="top-bar">
        <h2>Student Application History</h2>
        <button @click="goBack">Back</button>
    </div>

    <div class="info-box">
        <p><b>Student Name:</b> {{ studentName }}</p>
        <p><b>Total Applications:</b> {{ applications.length }}</p>
        <p>{{ message }}</p>
    </div>

    <div class="table-box">
        <table v-if="applications.length > 0">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Company</th>
                    <th>Job Title</th>
                    <th>Status</th>
                    <th>Applied On</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="app in applications" :key="app.application_id">
                    <td>{{ app.application_id }}</td>
                    <td>{{ app.company_name }}</td>
                    <td>{{ app.job_title }}</td>
                    <td>{{ app.status }}</td>
                    <td>{{ formatDate(app.applied_on) }}</td>
                </tr>
            </tbody>
        </table>

        <div v-else>
            No applications found
        </div>
    </div>

</div>
</template>

<script>
import API from "../api/api"

export default {
    data() {
        return {
            studentName: "",
            applications: [],
            message: ""
        }
    },

    methods: {
        async fetchStudentInfo() {
            try {
                const res = await API.get("/student/dashboard")
                this.studentName = res.data.student_name
            } catch (err) {
                console.log(err)
            }
        },

        async fetchApplications() {
            try {
                const res = await API.get("/student/my_applications")
                this.applications = res.data
            } catch (err) {
                this.message = "Failed to load applications"
            }
        },

        formatDate(dateStr) {
            if (!dateStr) return ""
            const d = new Date(dateStr)
            return d.toLocaleDateString()
        },

        goBack() {
            this.$router.push("/student")
        }
    },

    mounted() {
        this.fetchStudentInfo()
        this.fetchApplications()
    }
}
</script>

<style>
.applications-page {
    padding: 20px;
}
</style>