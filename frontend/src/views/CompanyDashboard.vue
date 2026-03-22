<template>
<div class="company-dashboard">

    <div class="top-bar">
        <h2>Company Dashboard</h2>
        <button @click="logout">Logout</button>
    </div>

    <div class="summary-box">
        <p><b>Company:</b> {{ companyName }}</p>
        <p><b>Total Drives:</b> {{ totalDrives }}</p>
        <p>{{ message }}</p>
    </div>

    <div class="create-box">
        <h3>Create Drive</h3>

        <input v-model="job_title" placeholder="Job Title" />
        <textarea v-model="job_description" placeholder="Job Description"></textarea>
        <input v-model="salary" placeholder="Salary" />

        <button @click="createDrive">Create</button>
    </div>

    <h3>My Drives</h3>

    <div v-if="drives.length === 0">
        No drives created
    </div>

    <div v-for="drive in drives" :key="drive.id" class="drive-card">
        <p><b>Title:</b> {{ drive.job_title }}</p>
        <p><b>Salary:</b> {{ drive.salary }}</p>
        <p><b>Status:</b> {{ drive.status }}</p>

        <button @click="viewApplicants(drive.id)">
            View Applicants
        </button>
    </div>

    <div v-if="selectedDrive">
        <h3>Applicants</h3>

        <div v-if="applicants.length === 0">
            No applicants
        </div>

        <div v-for="app in applicants" :key="app.application_id" class="app-card">
            <p><b>Name:</b> {{ app.student_name }}</p>
            <p><b>Status:</b> {{ app.status }}</p>

            <select v-model="app.newStatus">
                <option>Applied</option>
                <option>Shortlisted</option>
                <option>Interview</option>
                <option>Offer</option>
                <option>Rejected</option>
            </select>

            <button @click="updateStatus(app)">
                Update
            </button>

            <button
                v-if="app.status !== 'Placed'"
                @click="markPlaced(app.application_id)"
            >
                Mark Placed
            </button>
        </div>
    </div>

</div>
</template>

<script>
import API from "../api/api"

export default {
    data() {
        return {
            companyName: "",
            totalDrives: 0,
            drives: [],
            applicants: [],
            selectedDrive: null,
            message: "",

            job_title: "",
            job_description: "",
            salary: ""
        }
    },

    methods: {
        async fetchDashboard() {
            const res = await API.get("/company/dashboard")
            this.companyName = res.data.company_name
            this.totalDrives = res.data.total_drives
        },

        async fetchDrives() {
            const res = await API.get("/company/my_drives")
            this.drives = res.data
        },

        async createDrive() {
            try {
                const res = await API.post("/company/create_drive", {
                    job_title: this.job_title,
                    job_description: this.job_description,
                    salary: this.salary
                })

                this.message = res.data.message

                this.job_title = ""
                this.job_description = ""
                this.salary = ""

                this.fetchDrives()
                this.fetchDashboard()

            } catch (err) {
                this.message = err.response?.data?.message || "Error creating drive"
            }
        },

        async viewApplicants(driveId) {
            this.selectedDrive = driveId

            const res = await API.get("/company/applicants/" + driveId)

            this.applicants = res.data.map(a => ({
                ...a,
                newStatus: a.status
            }))
        },

        async updateStatus(app) {
            try {
                const res = await API.put("/company/update_application/" + app.application_id, {
                    status: app.newStatus
                })

                this.message = res.data.message
                this.viewApplicants(this.selectedDrive)

            } catch (err) {
                this.message = err.response?.data?.message || "Update failed"
            }
        },

        async markPlaced(appId) {
            try {
                const res = await API.post("/company/mark_placed/" + appId)

                this.message = res.data.message
                this.viewApplicants(this.selectedDrive)

            } catch (err) {
                this.message = err.response?.data?.message || "Failed to mark placed"
            }
        },

        logout() {
            localStorage.removeItem("token")
            this.$router.push("/")
        }
    },

    mounted() {
        this.fetchDashboard()
        this.fetchDrives()
    }
}
</script>

<style>
.company-dashboard {
    padding: 20px;
    max-width: 900px;
    margin: auto;
}

.top-bar {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.summary-box,
.create-box,
.drive-card,
.app-card {
    border: 1px solid black;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 8px;
}

.create-box input,
.create-box textarea {
    width: 100%;
    margin-bottom: 10px;
    padding: 8px;
}

button {
    margin-right: 10px;
    padding: 6px 12px;
    cursor: pointer;
}
</style>