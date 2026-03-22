<template>
<div class="dashboard">

    <div class="top-bar">
        <h2>Student Dashboard</h2>
        <div class="top-actions">
            <button @click="goToApplications">My Applications</button>
            <button @click="logout">Logout</button>
        </div>
    </div>

    <div class="summary-box">
        <p><b>Student Name:</b> {{ studentName }}</p>
        <p><b>Total Applications:</b> {{ totalApplications }}</p>
        <p>{{ message }}</p>
    </div>

    <div class="search-box">
        <input
            type="text"
            v-model="searchTitle"
            placeholder="Search drives by job title"
        />
        <button @click="searchDrives">Search</button>
        <button @click="resetDrives">Reset</button>
    </div>

    <h3>Available Drives</h3>

    <div v-if="drives.length === 0">
        No drives available
    </div>

    <div v-for="drive in drives" :key="drive.drive_id" class="drive-card">
        <p><b>Company:</b> {{ drive.company_name || drive.company }}</p>
        <p><b>Job Title:</b> {{ drive.job_title }}</p>
        <p><b>Salary:</b> {{ drive.salary }}</p>

        <div class="drive-actions">
            <button @click="viewDetails(drive.drive_id)">
                View Details
            </button>

            <button @click="applyToDrive(drive.drive_id)">
                Apply
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
            studentName: "",
            totalApplications: 0,
            drives: [],
            searchTitle: "",
            message: ""
        }
    },

    methods: {
        async fetchDashboard() {
            try {
                const res = await API.get("/student/dashboard")
                this.studentName = res.data.student_name
                this.totalApplications = res.data.applications
            } catch (err) {
                console.log("Dashboard error:", err)
                this.message = "Failed to load dashboard"
            }
        },

        async fetchDrives() {
            try {
                const res = await API.get("/student/drives")
                console.log("Drives response:", res.data)
                this.drives = res.data
            } catch (err) {
                console.log("Drives fetch error:", err)
                this.message = "Failed to load drives"
            }
        },

        async searchDrives() {
            if (this.searchTitle.trim() === "") {
                this.fetchDrives()
                return
            }

            try {
                const res = await API.get("/student/search_drives", {
                    params: {
                        title: this.searchTitle
                    }
                })
                this.drives = res.data
            } catch (err) {
                console.log("Search drives error:", err)
                this.message = "Drive search failed"
            }
        },

        resetDrives() {
            this.searchTitle = ""
            this.message = ""
            this.fetchDrives()
        },

        async applyToDrive(driveId) {
            try {
                const res = await API.post("/student/apply/" + driveId)
                this.message = res.data.message
                this.fetchDashboard()
            } catch (err) {
                if (err.response && err.response.data && err.response.data.message) {
                    this.message = err.response.data.message
                } else {
                    this.message = "Application failed"
                }
            }
        },

        viewDetails(id) {
            this.$router.push("/drive/" + id)
        },

        goToApplications() {
            this.$router.push("/student/applications")
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
.dashboard {
    padding: 20px;
    max-width: 950px;
    margin: 0 auto;
}

.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.top-actions {
    display: flex;
    gap: 10px;
}

.top-actions button {
    padding: 8px 14px;
    cursor: pointer;
}

.summary-box,
.search-box {
    border: 1px solid black;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 8px;
}

.search-box {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.search-box input {
    flex: 1;
    min-width: 240px;
    padding: 10px;
    box-sizing: border-box;
}

.search-box button {
    padding: 8px 14px;
    cursor: pointer;
}

.drive-card {
    border: 1px solid black;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 8px;
}

.drive-actions {
    margin-top: 10px;
    display: flex;
    gap: 10px;
}

.drive-actions button {
    padding: 6px 12px;
    cursor: pointer;
}
</style>