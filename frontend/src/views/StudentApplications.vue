<template>
<div class="applications-page">

    <div class="top-bar">
        <h2>Student Application History</h2>
        <button @click="goBack">Back</button>
        <button @click="logout">Logout</button>  
        <button @click="exportCSV">Export CSV</button> 
        <button v-if="lastFile" @click="downloadCSV">Download CSV</button>  
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
                    <th>Interview</th>
                    <th>Applied On</th>

                </tr>
            </thead>

            <tbody>
                <tr v-for="app in applications" :key="app.application_id">
                    <td>{{ app.application_id }}</td>
                    <td>{{ app.company_name }}</td>
                    <td>{{ app.job_title }}</td>
                    <td>{{ app.status }}</td>
                    <td>{{ app.interview_date ? formatDate(app.interview_date) : "-" }}</td>
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
            message: "",
            lastFile: ""
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
            this.message = ""
            try {
                const res = await API.get("/student/my_applications")
                this.applications = res.data
            } catch (err) {
                this.message = "Failed to load applications"
            }
        },

        async exportCSV(){
            try{
                const res = await API.post("/student/export_applications")
                alert(res.data.message)
                this.lastFile = "student_applications_" + localStorage.getItem("user_id") + ".csv"
            }catch(err){
                alert("Export failed")
            }
        },

        formatDate(dateStr) {
            if (!dateStr) return ""
            const d = new Date(dateStr)
            return d.toLocaleDateString()
        },

        downloadCSV(){
            window.open("http://127.0.0.1:5000/exports/" + this.lastFile)
        },

        goBack() {
            this.$router.push("/student")
        },

        logout() {
            localStorage.removeItem("token")
            localStorage.removeItem("role")
            this.$router.push("/")
        }
    },

    mounted() {
        this.fetchStudentInfo()
        this.fetchApplications()

        setInterval(() => {
            this.fetchApplications()
        }, 5000)
    }
    }
</script>