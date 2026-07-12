<template>
<div class="drive-details-page">

    <div class="top-bar">
        <div>

        <h1>Drive Details</h1>

        <p>

        Review the complete job description before applying.

        </p>

        </div>
        <div class="top-buttons">
            <button class="secondary-btn"
            @click="goBack">

            ← Dashboard

            </button>

            <button class="danger-btn"
            @click="logout">

            Logout

            </button>
        </div>
    </div>

    <div v-if="drive" class="details-box">

        <div class="company-header">

            <div class="company-logo">
                {{ drive.company_name.charAt(0).toUpperCase() }}
            </div>

            <div>

                <h2>{{ drive.job_title }}</h2>

                <p class="company-name">

                {{ drive.company_name }}

                </p>

            </div>

        </div>

        <div class="job-info">

            <div class="info-card">
                <span>Salary</span>
                <span class="salary-chip">

                ₹ {{ Number(drive.salary).toLocaleString("en-IN") }}

                </span>
            </div>

            <div class="info-card">
                <span>Status</span>
                <span
                :class="[

                'status-badge',

                drive.status==='Approved'
                ?'approved':

                'pending'

                ]">

                {{ drive.status }}

                </span>
            </div>

            <div class="info-card">
                <span>Your Application</span>
                <span
                :class="[

                'status-badge',

                drive.application_status==='Applied'
                ?'applied':

                drive.application_status==='Interview'
                ?'interview':

                drive.application_status==='Offer'
                ?'offer':

                drive.application_status==='Placed'
                ?'placed':'pending'

                ]">

                {{ drive.application_status }}

                </span>
            </div>

        </div>

        <div class="description-box">

            <h3>Job Description</h3>

            <p>{{ drive.job_description }}</p>

        </div>

        <div
            v-if="drive.interview_date"
            class="interview-box"
        >

            <h3>Interview Schedule</h3>

            <p>{{ formatDate(drive.interview_date) }}</p>

        </div>

        <button
            class="apply-btn"
            v-if="isStudent"
            @click="applyDrive"
        >
            Apply Now
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
.drive-details-page{

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

.details-box{

max-width:1000px;

margin:auto;

background:rgba(255,255,255,.12);

backdrop-filter:blur(18px);

padding:35px;

border-radius:18px;

box-shadow:0 10px 30px rgba(0,0,0,.3);

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

.company-header{
    display:flex;
    align-items:center;
    gap:20px;
    margin-bottom:30px;
}

.company-logo{
    width:70px;
    height:70px;
    border-radius:50%;
    background:#2563eb;
    color:white;
    display:flex;
    justify-content:center;
    align-items:center;
    font-size:30px;
    font-weight:bold;
}
.company-header h2{
    margin:0;
    color:white;
    font-size:32px;
    font-weight:700;
}

.company-name{

margin-top:6px;

font-size:17px;

opacity:.9;

}

.job-info{

display:grid;

grid-template-columns:repeat(3,1fr);

gap:28px;

margin:35px 0;

}

.info-card{

background:rgba(255,255,255,.18);

border:1px solid rgba(255,255,255,.12);

padding:24px;

border-radius:16px;

}

.info-card span{
    display:block;
    color:#dbeafe;
    margin-bottom:8px;
}

.info-card strong{
    font-size:18px;
    color:white;
}

.description-box{
    margin-bottom:30px;
}

.description-box h3{
    margin-bottom:12px;
    color:#1e3a8a;
}

.description-box p{

line-height:1.9;

opacity:.92;

}

.interview-box{
    background:#dcfce7;
    border-left:5px solid #16a34a;
    padding:20px;
    border-radius:10px;
    margin-bottom:25px;
}

.apply-btn{
    background:#2563eb;
    color:white;
    border:none;
    padding:14px 30px;
    border-radius:8px;
    font-size:16px;
    cursor:pointer;
}

.apply-btn:hover{
    background:#1d4ed8;
}

.info-card:hover{

transform:translateY(-5px);

}

.salary-chip{

background:#22c55e;

padding:8px 18px;

border-radius:20px;

font-weight:bold;

display:inline-block;

}

.status-badge{

padding:6px 14px;

border-radius:20px;

font-weight:600;

display:inline-block;

}

.approved{

background:#16a34a;

}

.pending{

background:#6b7280;

}

.applied{

background:#2563eb;

}

.interview{

background:#f59e0b;

}

.offer{

background:#22c55e;

}

.placed{

background:#059669;

}

.secondary-btn{

background:#2563eb;

color:white;

}

.danger-btn{

background:#dc2626;

color:white;

}

.secondary-btn,
.danger-btn,
.apply-btn{

transition:.25s;

}

.secondary-btn:hover,
.danger-btn:hover,
.apply-btn:hover{

transform:translateY(-2px);

}
</style>

