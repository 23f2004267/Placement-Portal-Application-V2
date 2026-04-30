<template>
<div class="drive-details-page">

    <div class="top-bar">
        <h2>Drive Details</h2>
        <div class="top-buttons">
            <button @click="goBack">Back</button>
            <button @click="logout">Logout</button>
        </div>
    </div>

    <div v-if="drive" class="details-box">
        <p><b>Company:</b> {{ drive.company_name }}</p>
        <p><b>Job Title:</b> {{ drive.job_title }}</p>
        <p><b>Description:</b> {{ drive.job_description }}</p>
        <p><b>Salary:</b> {{ drive.salary }}</p>
        <p><b>Status:</b> {{ drive.status }}</p>
        <p v-if="drive.interview_date">
            <b>Interview Scheduled:</b> {{ formatDate(drive.interview_date) }}
        </p>
        <p>
            <b>Application Status:</b>
            {{ drive.application_status }}
        </p>

        <p v-if="drive.interview_date">
            <b>Interview Date:</b>
            {{ drive.interview_date }}
        </p>

        <button v-if="isStudent" @click="applyDrive">
            Apply
        </button>
    </div>

    <div v-else class="details-box">
        Drive not found
    </div>

    <p class="message-text">{{ message }}</p>

</div>
</template>

<script>
import API from "../api/api"

export default {
    data() {
        return {
            drive: null,
            message: "",
            isStudent: false,
        }
    },

    methods: {
        async fetchDrive() {
            const id = this.$route.params.id

            try {
                const res = await API.get("/student/drive/" + id)
                this.drive = res.data
            } catch (err) {
                console.log("Drive details error:", err)

                if (err.response && err.response.data && err.response.data.message) {
                    this.message = err.response.data.message
                } else {
                    this.message = "Failed to load drive details"
                }

                this.drive = null
            }
        },

        async applyDrive() {
            if (!this.drive) {
                this.message = "Drive not found"
                return
            }

            try {
                const res = await API.post("/student/apply/" + (this.drive.drive_id || this.drive.id))
                this.message = res.data.message
            } catch (err) {
                if (err.response && err.response.data && err.response.data.message) {
                    this.message = err.response.data.message
                } else {
                    this.message = "Application failed"
                }
            }
        },
        formatDate(dateStr){
            if(!dateStr) return ""
            return new Date(dateStr).toLocaleString()
        },

        goBack() {
            const role = localStorage.getItem("role")

            if (role === "admin") {
                this.$router.push("/admin")
            } else {
                this.$router.push("/student")
            }
        },

        logout() {
            localStorage.removeItem("token")
            localStorage.removeItem("role")
            this.$router.push("/")
        }
    },

    mounted() {
        this.fetchDrive()
        this.isStudent = localStorage.getItem("role") === "student"
    }
}
</script>

<style>
.drive-details-page {
    padding: 20px;
    max-width: 900px;
    margin: 0 auto;
}

.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.top-buttons {
    display: flex;
    gap: 10px;
}

.top-buttons button {
    padding: 8px 14px;
    cursor: pointer;
}

.details-box {
    border: 1px solid black;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
}

.details-box p {
    margin-bottom: 12px;
}

.details-box button {
    padding: 8px 14px;
    cursor: pointer;
}

.message-text {
    margin-top: 10px;
}
</style>