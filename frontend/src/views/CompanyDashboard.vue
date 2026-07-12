<template>
<div class="company-dashboard">

    <div class="hero-section">

        <div>

            <h1>Welcome, {{ companyName }}</h1>

            <p>
                
            </p>

        </div>

        <button
            class="logout-btn"
            @click="logout">

            Logout

        </button>

    </div>

    <div class="stats-grid">
        <div class="stat-card">

            <h2>{{ totalDrives }}</h2>

            <p>📄 Total Drives</p>

        </div>

        <div class="stat-card">

            <h2>{{ ongoingDrives.length }}</h2>

            <p>Active Drives</p>

        </div>

        <div class="stat-card">

            <h2>{{ completedDrives.length }}</h2>

            <p>✔ Completed Drives</p>

        </div>
    </div>

    <div class="create-box">

        <h2>Create New Placement Drive</h2>

        <p class="section-subtitle">
        Publish a new hiring opportunity for students.
        </p>

        <div class="form-grid">

            <div class="field">
                <label>Job Title</label>
                <input
                    v-model="job_title"
                    placeholder="Software Engineer Intern"
                />
            </div>

            <div class="field">
                <label>Salary (CTC)</label>
                <input
                    v-model="salary"
                    placeholder="1200000"
                />
            </div>

        </div>

        <div class="field">
                <label>Job Description</label>

                <textarea
                    v-model="job_description"
                    placeholder="Describe responsibilities, required skills and eligibility"
                ></textarea>
            </div>

            <button class="primary-btn" @click="createDrive">
                Create Drive
            </button>

        </div>

    <h3>Ongoing Drives</h3>

    <div v-if="ongoingDrives.length === 0">
        No upcoming drives
    </div>

    <div v-for="drive in ongoingDrives" :key="drive.id" class="glass-card drive-card">
        <p><b>Title:</b> {{ drive.job_title }}</p>
        <p><b>Salary:</b> {{ drive.salary }}</p>

        <button v-if="selectedDrive !== drive.id" @click="viewApplicants(drive.id)">
            View Applicants
        </button>

        <button v-else @click="closeApplicants">
            Close Applicants
        </button>

        <button @click="markComplete(drive.id)">
            Mark as Complete
        </button>
    </div>


    <h3>Completed Drives</h3>

    <div v-if="completedDrives.length === 0">
        No closed drives
    </div>

    <div v-for="drive in completedDrives" :key="drive.id" class="glass-card drive-card">
        <p><b>Title:</b> {{ drive.job_title }}</p>

        <button @click="viewApplicants(drive.id)">
            View Applicants
        </button>
    </div>

    <div v-if="drives.length === 0">
        No drives created
    </div>

    <div v-if="selectedDrive !== null">
        <h3>Applicants for Drive {{ selectedDrive }}</h3>

        <div v-if="applicants.length === 0">
            No applicants
        </div>

        <div v-for="app in applicants" :key="app.application_id" class="glass-card applicant-card">
            <button v-if="app.resume" @click="viewResume(app.resume)">
                📄 Resume
            </button>
            <p><b>Name:</b> {{ app.student_name }}</p>
            <p>

            <b>Status :</b>

            <span

            :class="[

            'badge',

            app.status=='Applied'
            ?'blue':

            app.status=='Shortlisted'
            ?'purple':

            app.status=='Interview'
            ?'orange':

            app.status=='Offer'
            ?'green':

            app.status=='Placed'
            ?'darkgreen':'red'

            ]">

            {{ app.status }}

            </span>

            </p>
            <p><b>Email:</b> {{ app.email }}</p>
            <p><b>Phone:</b> {{ app.phone }}</p>
            <p><b>Branch:</b> {{ app.branch }}</p>
            <p><b>CGPA:</b> {{ app.cgpa }}</p>
            <p><b>Skills:</b> {{ app.skills }}</p>

            <p v-if="app.interview_date">
                <b>Interview:</b> {{ app.interview_date }}
            </p>

            <select v-model="app.newStatus">
                <option>Applied</option>
                <option>Shortlisted</option>
                <option>Interview</option>
                <option>Offer</option>
                <option>Rejected</option>
            </select>

            <div v-if="app.newStatus === 'Interview'">
                <input type="datetime-local" v-model="app.interview_date" />
            </div>

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
            ongoingDrives: [],
            completedDrives: [],
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
            try {
                const res = await API.get("/company/dashboard")
                this.companyName = res.data.company_name || "Company"
                this.totalDrives = res.data.total_drives
            } catch (err) {
                this.message = "Failed to load dashboard"
            }
        },

        async fetchDrives() {
            try {
                const res = await API.get("/company/my_drives")
                this.drives = res.data

                this.ongoingDrives = this.drives.filter(d => d.status !== "Completed")
                this.completedDrives = this.drives.filter(d => d.status === "Completed")
            } catch (err) {
                this.message = "Failed to load drives"
            }
        },

        async createDrive() {
            try {
                this.message = ""

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
            this.applicants = []
            this.message = ""
            const selected = this.drives.find(d => d.id === driveId)

            if(selected && selected.status === "Completed"){
                this.message = "Viewing past applicants"
            }

            try {
                const res = await API.get("/company/applicants/" + driveId)

                console.log("Applicants API Response:", res.data)

                this.applicants = res.data.map(a => ({
                    application_id: a.application_id,
                    student_name: a.student_name,
                    email: a.email,
                    phone: a.phone,
                    branch: a.branch,
                    cgpa: a.cgpa,
                    skills: a.skills,
                    status: a.status,
                    newStatus: a.status,
                    resume: a.resume,
                    interview_date: a.interview_date
                }))

            } catch (err) {
                this.message = "Failed to load applicants"
            }
        },

        viewResume(path){
            if(!path){
                alert("No resume available")
                return
            }

            window.open(`${import.meta.env.VITE_API_URL}/uploads/` + path)
        },
        

        closeApplicants(){
            this.selectedDrive = null
            this.applicants = []
        },

        async updateStatus(app) {
            try {
                this.message = ""

                let payload = {
                    status: app.newStatus
                }

                if(app.newStatus === "Interview"){
                    if(!app.interview_date){
                        alert("Please select interview date and time")
                        return
                    }
                    payload.interview_date = app.interview_date
                }

                await API.put("/company/update_application/" + app.application_id, payload)

                this.viewApplicants(this.selectedDrive)

            } catch (err) {
                this.message = err.response?.data?.message || "Update failed"
            }
        },

        async markPlaced(appId) {
            try {
                this.message = ""

                const res = await API.post("/company/mark_placed/" + appId)

                this.message = res.data.message
                this.viewApplicants(this.selectedDrive)

            } catch (err) {
                this.message = err.response?.data?.message || "Failed to mark placed"
            }
        },

        async markComplete(id){
            try{
                this.message = ""

                const res = await API.put("/company/complete_drive/" + id)

                this.message = res.data.message

                this.fetchDrives()

                if(this.selectedDrive === id){
                    this.closeApplicants()
                }

            }catch(err){
                this.message = "Failed to mark complete"
            }
        },

        logout() {
            localStorage.removeItem("token")
            localStorage.removeItem("role")
            this.$router.push("/")
        }
    },

    mounted() {
        this.fetchDashboard()
        this.fetchDrives()
    }
}
</script>

<<style>

.company-dashboard{

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

margin-bottom:35px;

flex-wrap:wrap;

}

.hero-section h1{

font-size:38px;

margin-bottom:10px;

}

.hero-section p{

opacity:.9;

}

.logout-btn{

padding:12px 25px;

background:#dc2626;

border:none;

border-radius:10px;

color:white;

cursor:pointer;

}

.logout-btn:hover{

background:#b91c1c;

}

.stats-grid{

display:grid;

grid-template-columns:repeat(auto-fit,minmax(220px,1fr));

gap:20px;

margin-bottom:30px;

}

.stat-card{

background:rgba(150, 38, 38, 0.15);

backdrop-filter:blur(18px);

padding:25px;

border-radius:18px;

text-align:center;

box-shadow:0 10px 25px rgba(0,0,0,.25);

}

.glass-card{

background:rgba(255,255,255,.12);

backdrop-filter:blur(18px);

padding:22px;

border-radius:18px;

margin-bottom:25px;

box-shadow:0 10px 25px rgba(0,0,0,.25);

transition:.3s;

}
.glass-card:hover{

transform:translateY(-3px);

}

.form-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
}

.field{
    display:flex;
    flex-direction:column;
    margin-bottom:18px;
}

.field label{

margin-bottom:8px;

font-weight:600;

color:#dbeafe;

letter-spacing:.3px;

}

.field input,
.field textarea{

width:100%;
padding:14px;
border-radius:10px;
border:1px solid rgba(255,255,255,.15);

background:#eef4ff;

color:#1f2937;

font-size:15px;

transition:.25s;

}

.field textarea{
    min-height:120px;
}

.primary-btn{
    background:#2563eb;
    color:white;
    padding:12px 24px;
    border:none;
    border-radius:8px;
    cursor:pointer;
}

.primary-btn:hover{
    background:#1d4ed8;
}

.create-box button{

padding:12px 22px;

background:#16a34a;

color:white;

border:none;

border-radius:10px;

cursor:pointer;

}

.drive-card{

transition:.25s;

}

.drive-card:hover{

transform:translateY(-5px);

}

.applicant-card{

transition:.25s;

}

.applicant-card:hover{

transform:scale(1.01);

}

button{

padding:10px 18px;

border:none;

border-radius:8px;

cursor:pointer;

margin-right:10px;

margin-top:10px;

transition:.25s;

font-weight:600;

}
button:hover{

transform:translateY(-2px);

}

.badge{

padding:5px 12px;

border-radius:20px;

font-weight:600;

margin-left:8px;

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
.section-subtitle{

margin-top:-8px;

margin-bottom:25px;

opacity:.85;

font-size:15px;

}
.field input:focus,
.field textarea:focus{

outline:none;

background:rgb(222, 226, 229);

border:1px solid #60a5fa;

box-shadow:0 0 0 4px rgba(96,165,250,.25);

}

select{

padding:10px;

border-radius:8px;

border:none;

margin-top:10px;

margin-bottom:10px;

}
input[type="datetime-local"]{

padding:10px;

border-radius:8px;

border:none;

margin-top:10px;

}
.stat-card{

transition:.3s;

}

.stat-card:hover{

transform:translateY(-4px);

}
table{

width:100%;

}

table tr{

transition:.25s;

}

table tr:hover{

background:rgba(255,255,255,.08);

}

table td,
table th{

padding:15px;

}
.field input,
.field textarea{

color:#1f2937;

}
.field input::placeholder,
.field textarea::placeholder{

color:#6b7280;

}

</style>

