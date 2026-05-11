<template>
<div class="company-dashboard">

    <div class="top-bar">
        <h2>Hello {{ companyName }} Administrator</h2>
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

    <h3>Ongoing Drives</h3>

    <div v-if="ongoingDrives.length === 0">
        No upcoming drives
    </div>

    <div v-for="drive in ongoingDrives" :key="drive.id" class="drive-card">
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

    <div v-for="drive in completedDrives" :key="drive.id" class="drive-card">
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

        <div v-for="app in applicants" :key="app.application_id" class="app-card">
            <button v-if="app.resume" @click="viewResume(app.resume)">
                View Resume
            </button>
            <p><b>Name:</b> {{ app.student_name }}</p>
            <p><b>Status:</b> {{ app.status }}</p>
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
                <option>Placed</option>
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