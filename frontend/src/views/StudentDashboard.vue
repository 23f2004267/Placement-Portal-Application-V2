<template>
<div class="dashboard">

    <div class="hero-section">

        <div class="hero-left">

            <h1>👋 Welcome, {{ studentName }}</h1>

        </div>

        <div class="hero-buttons">

            <button class="primary-btn"
                    @click="goToApplications">
                📄 My Applications
            </button>

            <button class="danger-btn"
                    @click="logout">
                Logout
            </button>

        </div>

    </div>
    


    <div class="stats-grid">

        <div class="stat-card">

            <h3>{{ totalApplications }}</h3>

            <p>📄Total Applications</p>

        </div>

        <div class="stat-card">

            <h3>{{ resumePath ? "Uploaded" : "Pending" }}</h3>

            <p>Resume Status</p>

        </div>

        <div class="stat-card">

            <h3>{{ drives.length }}</h3>

            <p>Available Drives</p>

        </div>

    </div>

    <div class="glass-card">

        <div class="resume-actions">

        <input type="file" @change="handleFile">

        <button
        class="primary-btn"
        @click="uploadResume">

        Upload Resume

        </button>

        <button
        v-if="resumePath"
        class="secondary-btn"
        @click="viewResume">

        📄 View Resume

        </button>

        </div>
        <p class="success-message" v-if="message">
            {{ message }}
        </p>
    </div>
    

    <div class="glass-card search-box">
        <input
            type="text"
            v-model="searchTitle"
            placeholder="Search drives by job title"
        />
        <button class="primary-btn" @click="searchDrives">

        Search

        </button>
        <button class="secondary-btn" @click="resetDrives">

        Reset

        </button>
    </div>

    <h3>Available Drives</h3>

    <div
    v-if="drives.length===0"
    class="empty-state">

    <h2>No Placement Drives</h2>

    <p>

    Please check again later.

    </p>

    </div>

    <div
        v-for="drive in drives"
        :key="drive.drive_id"
        class="glass-card drive-card"
    >
        <div class="company-header">

        <div class="company-logo">

        {{ (drive.company_name || drive.company).charAt(0) }}

        </div>

        <div>

        <h3>{{ drive.company_name || drive.company }}</h3>

        <p>{{ drive.job_title }}</p>

        </div>

        </div>
        <p>

        <b>CTC</b>

        <span class="salary-chip">

        ₹ {{ Number(drive.salary).toLocaleString('en-IN') }}

        </span>

        </p>
        <p>

        <b>Status :</b>

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

        </p>
        <div class="drive-actions">
            <button @click="viewDetails(drive.drive_id)">
                View Details
            </button>

            <button v-if="drive.status === 'Approved'" @click="applyToDrive(drive.drive_id)">
                Apply
            </button>

            <p v-if="drive.status === 'Completed'" style="color:red;">
                Applications Closed
            </p>
        </div>
    </div>
    <div class="glass-card profile-box">
        <h3>Update Profile</h3>

        <p class="section-text">

        Keep your details updated for recruiters.

        </p>

        <div class="form-container">
    <input type="tel" v-model="phone" placeholder="Phone" />
    <input type="text" v-model="branch" placeholder="Branch" />
    <input type="number" step="0.01" v-model="cgpa" placeholder="CGPA" />
    <textarea v-model="skills" placeholder="Skills"></textarea>
</div>

        <button @click="updateProfile">Save Changes</button>
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
            message: "",
            resumePath: "",
            isStudent: false,
            phone: "",
            branch: "",
            cgpa: "",
            skills: "",
        }
    },

    methods: {
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

        handleFile(e){
            this.resumeFile = e.target.files[0]
        },

        async uploadResume(){
            if(!this.resumeFile){
                this.message = "Select a file first"
                return
            }

            const formData = new FormData()
            formData.append("file", this.resumeFile)

            try{
                const res = await API.post("/student/upload_resume", formData)
                this.message = res.data.message
                this.resumePath = res.data.resume
                setTimeout(() => {
                    this.message = ""
                }, 3000)

                this.fetchDashboard()
            }catch(err){
                this.message = "Upload failed"
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

        async updateProfile(){
            if(this.phone && !/^[0-9]{10}$/.test(this.phone)){
                alert("Phone must be 10 digits")
                return
            }

            if(this.cgpa && (this.cgpa < 0 || this.cgpa > 10)){
                alert("CGPA must be between 0 and 10")
                return
            }

            if(!this.branch || !this.skills){
                alert("Branch and Skills are required")
                return
            }

            try{
                const res = await API.put("/student/update_profile",{
                    phone: this.phone,
                    branch: this.branch,
                    cgpa: this.cgpa,
                    skills: this.skills
                })

                alert(res.data.message)
            }catch(err){
                alert("Update failed")
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

        async fetchDashboard(){
            try{
                const res = await API.get("/student/dashboard")

                this.studentName = res.data.student_name || "Student"

                this.phone = res.data.phone || ""
                this.branch = res.data.branch || ""
                this.cgpa = res.data.cgpa || ""
                this.skills = res.data.skills || ""
                this.resumePath = res.data.resume || ""
                this.totalApplications = res.data.total_applications || 0

            }catch(err){
                console.log("Dashboard error:", err)
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
            localStorage.removeItem("role")
            this.$router.push("/")
        },
        viewResume(){
            if(!this.resumePath){
                alert("No resume available")
                return
            }

            window.open(`${import.meta.env.VITE_API_URL}/uploads/` + this.resumePath)
        }
    },

    mounted: function() {
        this.isStudent = localStorage.getItem("role") === "student"

        this.fetchDashboard()
        this.fetchDrives()
    }
}
</script>

<style>

.dashboard{

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

.hero-section{

display:flex;

justify-content:space-between;

align-items:center;

margin-bottom:40px;

flex-wrap:wrap;

gap:20px;

}

.hero-left h1{

font-size:38px;

margin-bottom:12px;

}

.hero-left p{

opacity:.9;

max-width:600px;

line-height:1.6;

}

.hero-buttons{

display:flex;

gap:15px;

}

.primary-btn{

background:#22c55e;

border:none;

padding:14px 24px;

border-radius:10px;

color:white;

cursor:pointer;

font-size:16px;

}

.primary-btn:hover{

background:#16a34a;

}

.danger-btn{

background:#dc2626;

color:white;

border:none;

padding:14px 24px;

border-radius:10px;

cursor:pointer;

}

.stats-grid{

display:grid;

grid-template-columns:repeat(auto-fit,minmax(220px,1fr));

gap:20px;

margin-bottom:35px;

}

.stat-card{

background:rgba(255,255,255,.15);

backdrop-filter:blur(16px);

border-radius:18px;

padding:25px;

text-align:center;

box-shadow:0 10px 30px rgba(0,0,0,.25);

}

.stat-card h3{

font-size:34px;

margin-bottom:10px;

}

.glass-card{

background:rgba(255,255,255,.12);

backdrop-filter:blur(16px);

padding:22px;

margin-bottom:25px;

border-radius:18px;

box-shadow:0 10px 25px rgba(0,0,0,.25);

}

.search-box{

display:flex;

gap:15px;

flex-wrap:wrap;

}

.search-box input{

flex:1;

padding:14px;

border-radius:10px;

border:none;

background:#eef4ff;

color:#111827;

}

.search-box button{

padding:12px 22px;

border:none;

border-radius:10px;

cursor:pointer;

background:#2563eb;

color:white;

}

.drive-card{

transition:.25s;

}

.drive-card{

transition:.3s;

}

.drive-card:hover{

transform:translateY(-6px);

box-shadow:0 15px 35px rgba(0,0,0,.3);

}

.drive-actions{

margin-top:15px;

display:flex;

gap:12px;

flex-wrap:wrap;

}

.drive-actions button{

padding:10px 18px;

border:none;

border-radius:8px;

background:#22c55e;

color:white;

cursor:pointer;

}

.form-container{

display:grid;

gap:15px;

}

.form-container input,

.profile-box button{

margin-top:20px;

padding:12px 22px;

background:#2563eb;

color:white;

border:none;

border-radius:10px;

cursor:pointer;

}

.status-badge{

padding:5px 12px;

border-radius:20px;

font-size:14px;

font-weight:600;

margin-left:8px;

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

background:#16a34a;

}

.placed{

background:#059669;

}

.success-message{

margin-top:20px;

padding:12px;

background:rgba(34,197,94,.2);

border-left:4px solid #22c55e;

border-radius:10px;

color:white;

font-weight:600;

}

.company-header{

display:flex;

align-items:center;

gap:15px;

margin-bottom:15px;

}

.company-logo{

width:55px;

height:55px;

border-radius:50%;

background:#2563eb;

display:flex;

justify-content:center;

align-items:center;

font-size:22px;

font-weight:bold;

color:white;

}

.salary-chip{

background:#22c55e;

padding:6px 12px;

border-radius:20px;

margin-left:10px;

font-weight:600;

}

.resume-actions{

display:flex;

gap:15px;

align-items:center;

flex-wrap:wrap;

}
.empty-state{

text-align:center;

padding:60px;

background:rgba(255,255,255,.08);

border-radius:18px;

margin-bottom:25px;

}

.empty-state h2{

margin-top:15px;

margin-bottom:10px;

}

.empty-state p{

opacity:.85;

}

.section-text{

margin-top:-8px;

margin-bottom:20px;

opacity:.85;

}

button{

transition:.25s;

}

button:hover{

transform:translateY(-2px);

}

.drive-card p{

margin:18px 0;

font-size:16px;

line-height:1.8;

}
.profile-box h3{

margin-bottom:8px;

}

.section-text{

margin-bottom:28px;

line-height:1.6;

}
</style>