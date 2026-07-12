<template>
<div class="applications-page">

    <div class="hero">

        <div>

            <h1>My Applications</h1>

            <p>
                Track every company you've applied to from one place.
            </p>

        </div>

        <div class="hero-buttons">

            <button class="secondary-btn"
                    @click="goBack">
                Dashboard
            </button>

            <button class="primary-btn"
                    @click="exportCSV">
                Export CSV
            </button>

            <button
                v-if="lastFile"
                class="download-btn"
                @click="downloadCSV">

                Download CSV

            </button>

            <button
                class="danger-btn"
                @click="logout">

                Logout

            </button>

        </div>

    </div>

    

    <div class="stats-row">
        <div class="stat-card">

            <h2>{{ studentName }}</h2>

            <p>Student Name</p>

        </div>

        <div class="stat-card">

            <h2>{{ applications.length }}</h2>

            <p>Total Applications</p>

        </div>

        <div class="stat-card">

            <h2>{{ lastFile ? "Ready" : "Not Generated" }}</h2>

            <p>CSV Export</p>

        </div>
    </div>

    <div class="glass-card table-box">
        <table
            class="modern-table"
            v-if="applications.length > 0">
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
                    <td>
                        <span
                        :class="[
                        'badge',

                        app.status==='Applied'
                        ?'blue':

                        app.status==='Shortlisted'
                        ?'purple':

                        app.status==='Interview'
                        ?'orange':

                        app.status==='Offer'
                        ?'green':

                        app.status==='Placed'
                        ?'darkgreen':'red'
                        ]">

                        {{ app.status }}

                        </span>

                        </td>
                    <td>

                    <span
                        v-if="app.interview_date"
                        class="interview-date">

                        {{ formatDate(app.interview_date) }}

                    </span>

                    <span
                        v-else
                        class="not-scheduled">

                        Not Scheduled

                    </span>

                </td>
                    <td>

                        <span class="date-chip">

                            {{ formatDate(app.applied_on) }}

                        </span>

                    </td>
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

        async exportCSV() {
            try {

                const res = await API.post("/student/export_applications")

                alert(res.data.message)

                if (res.data.filename) {
                    this.lastFile = res.data.filename
                }

            } catch (err) {

                alert("Export failed")

            }
        },

        formatDate(dateStr) {
            if (!dateStr) return ""
            const d = new Date(dateStr)
            return d.toLocaleDateString()
        },

        downloadCSV(){
            window.open(`${import.meta.env.VITE_API_URL}/exports/` + this.lastFile)
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

<style>

.applications-page{

min-height:100vh;

padding:40px;

background:linear-gradient(
135deg,
#2563eb,
#1e3a8a,
#0f172a
);

color:white;

}

.hero{

display:flex;

justify-content:space-between;

align-items:center;

margin-bottom:35px;

flex-wrap:wrap;

}

.hero h1{

font-size:36px;

margin-bottom:10px;

}

.hero p{

opacity:.9;

}

.hero-buttons{

display:flex;

gap:15px;

}

.hero-buttons button{

padding:12px 22px;

background:#2563eb;

border:none;

color:white;

border-radius:10px;

cursor:pointer;

}

.stats-row{

display:grid;

grid-template-columns:repeat(auto-fit,minmax(220px,1fr));

gap:20px;

margin-bottom:30px;

}

.stat-card{

background:rgba(255,255,255,.15);

backdrop-filter:blur(18px);

padding:25px;

border-radius:18px;

text-align:center;

}

.glass-card{

background:rgba(255,255,255,.12);

backdrop-filter:blur(18px);

border-radius:18px;

padding:20px;

}

.modern-table{

width:100%;

border-collapse:collapse;

}

.modern-table th{

background:#1e40af;

padding:14px;

}

.modern-table td{

padding:14px;

text-align:center;

border-bottom:1px solid rgba(255,255,255,.15);

}

.modern-table tr:hover{

background:rgba(255,255,255,.08);

}

.badge{

padding:5px 12px;

border-radius:20px;

font-weight:600;

}

.blue{

background:#2563eb;

}

.purple{

background:#7c3aed;

}

.orange{

background:#f59e0b;

}

.green{

background:#16a34a;

}

.darkgreen{

background:#059669;

}

.red{

background:#dc2626;

}

.hero-buttons{

display:flex;

gap:15px;

flex-wrap:wrap;

}

.hero-buttons button{

padding:12px 20px;

border:none;

border-radius:10px;

cursor:pointer;

font-weight:600;

transition:.25s;

}

.secondary-btn{

background:#2563eb;

color:white;

}

.secondary-btn:hover{

background:#1d4ed8;

}

.primary-btn{

background:#16a34a;

color:white;

}

.primary-btn:hover{

background:#15803d;

}

.download-btn{

background:#9333ea;

color:white;

}

.download-btn:hover{

background:#7e22ce;

}

.danger-btn{

background:#dc2626;

color:white;

}

.danger-btn:hover{

background:#b91c1c;

}
.interview-date{

background:#dbeafe;

color:#1d4ed8;

padding:6px 12px;

border-radius:20px;

font-weight:600;

display:inline-block;

}

.not-scheduled{

background:#374151;

color:white;

padding:6px 12px;

border-radius:20px;

display:inline-block;

font-size:13px;

}
.date-chip{

background:#e5e7eb;

color:#374151;

padding:6px 12px;

border-radius:20px;

display:inline-block;

font-size:13px;

font-weight:600;

}

</style>