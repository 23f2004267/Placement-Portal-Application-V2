<template>
<div class="admin-dashboard">

    <div class="hero-section">

        <div>

            <h1>Welcome Admin</h1>

        </div>

        <button
            class="logout-btn"
            @click="logout">

            Logout

        </button>

    </div>

    <div class="search-box">
        <input
            type="text"
            v-model="searchText"
            placeholder="Search company or student"
        />
        <button @click="searchData">Search</button>
        <button @click="resetData">Reset</button>
    </div>

    <div class="glass-card">
        <p><b>Welcome Admin</b></p>
        <p>{{ message }}</p>
    </div>

    <div class="stats-grid">
        <div class="stat-card">

        <h2>{{ summary.students }}</h2>

        <p>Students</p>

    </div>

    <div class="stat-card">

        <h2>{{ summary.companies }}</h2>

        <p>Companies</p>

    </div>

    <div class="stat-card">

        <h2>{{ summary.drives }}</h2>

        <p>Placement Drives</p>

    </div>

    <div class="stat-card">

        <h2>{{ summary.applications }}</h2>

        <p>Applications</p>

    </div>
    </div>

    <div class="glass-card">

        <h3>Registered Companies</h3>

        <table
            class="modern-table"
            v-if="companies.length > 0">

            <thead>

                <tr>

                    <th>Company</th>

                    <th>Website</th>

                    <th>Status</th>

                    <th>Actions</th>

                </tr>

            </thead>

            <tbody>

                <tr
                    v-for="company in companies.filter(c => c.status !== 'Blacklisted')"
                    :key="company.id">

                    <td>{{ company.company_name }}</td>

                    <td>{{ company.website }}</td>

                    <td>

                        <span
                            :class="[

                                company.status==='Approved'
                                ?'green-badge'

                                :company.status==='Pending'
                                ?'orange-badge'

                                :'red-badge'

                            ]">

                            {{ company.status }}

                        </span>

                    </td>

                    <td>

                        <button
                            v-if="company.status!=='Approved'"
                            @click="approveCompany(company.id)">

                            Approve

                        </button>

                        <button
                            class="danger-btn"
                            @click="blacklistUser(company.user_id)">

                            Blacklist

                        </button>

                    </td>

                </tr>

            </tbody>

        </table>

        <div v-else>

            No companies found

        </div>

    </div>

    <div class="glass-card">
        <h3>Registered Students</h3>

        <table
        class="modern-table"
        v-if="students.length > 0">
            <thead>
                <tr>

                    <th>Name</th>

                    <th>Email</th>

                    <th>Resume</th>

                    <th>Status</th>

                    <th>Action</th>

                </tr>
            </thead>

            <tbody>
                <tr v-for="student in students" :key="student.id">
                    <td>{{ student.name }}</td>
                    <td>{{ student.email }}</td>
                    <td>
                        <button v-if="student.resume" @click="viewResume(student.resume)">
                            View Resume
                        </button>
                    </td>
                    <td>

                    <span
                    :class="student.is_active ? 'green-badge' : 'red-badge'">

                    {{ student.is_active ? "Active" : "Blocked" }}

                    </span>

                    </td>
                    <td>
                        <button
                            v-if="student.is_active"
                            class="danger-btn"
                            @click="blacklistUser(student.user_id)"
                        >
                            Blacklist
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-else>
            No students found
        </div>
    </div>

    <div class="glass-card">
        <h3>Ongoing Drives</h3>

        <div v-if="!drives || drives.length === 0">
            No drives found
        </div>

        <div v-for="drive in drives" :key="drive.id" class="glass-item">
            <div>
                <p><b>Company:</b> {{ drive.company_name }}</p>
                <p><b>Job Title:</b> {{ drive.job_title }}</p>
                <p><b>Salary:</b> {{ drive.salary }}</p>
                <p>

                <b>Status:</b>

                <span
                :class="[

                'status-badge',

                drive.status==='Approved'
                ?'green-badge':

                drive.status==='Pending'
                ?'orange-badge':'red-badge'

                ]">

                {{ drive.status }}

                </span>

                </p>
            </div>

            <div class="right-actions">

                <button @click="viewDrive(drive.id)">
                    View Details
                </button>

                <button v-if="drive.status === 'Pending'" @click="approveDrive(drive.id)">
                    Approve
                </button>

                <button class="danger-btn" @click="removeDrive(drive.id)">
                    Remove
                </button>

                <button @click="markComplete(drive.id)">
                    Mark Complete
                </button>

            </div>
        </div>
    </div>

    <div class="glass-card">
        <h3>Placement Report</h3>

        <div v-if="placements.length === 0">
            No placements yet
        </div>

        <div v-for="p in placements" :key="p.placement_id" class="glass-item">
            <div>
                <p><b>Student:</b> {{ p.student_name }}</p>
                <p><b>Company:</b> {{ p.company_name }}</p>
                <p><b>Position:</b> {{ p.position }}</p>
                <p><b>Salary:</b> {{ p.salary }}</p>
            </div>
        </div>
    </div>
    <div class="glass-card">
        <h3>All Applications</h3>

        <div v-if="!applications || applications.length === 0">
        No applications found
        </div>

        <div v-for="app in applications" :key="app.application_id" class="glass-item">
            <div class="right-actions">
                <button @click="viewApplication(app.application_id)">
                    View
                </button>
            </div>
            <div>
                <p><b>Student:</b> {{ app.student_name }}</p>
                <p><b>Company:</b> {{ app.company_name }}</p>
                <p><b>Job:</b> {{ app.job_title }}</p>
                <p>

                <b>Status:</b>

                <span
                :class="[

                'status-badge',

                app.status==='Applied'
                ?'blue-badge':

                app.status==='Shortlisted'
                ?'purple-badge':

                app.status==='Interview'
                ?'orange-badge':

                app.status==='Offer'
                ?'green-badge':

                app.status==='Placed'
                ?'darkgreen-badge':'red-badge'

                ]">

                {{ app.status }}

                </span>

                </p>
            </div>
        </div>
    </div>

</div>
</template>

<script>
import API from "../api/api"

export default {
    data() {
        return {
            summary: {
                students: 0,
                companies: 0,
                drives: 0,
                applications: 0
            },
            companies: [],
            students: [],
            drives: [],
            placements: [], 
            applications: [], 
            searchText: "",
            message: ""
        }
    },

    methods: {
        async fetchSummary() {
            try {
                const res = await API.get("/admin/dashboard")
                this.summary = res.data
            } catch (err) {
                console.log("Summary error:", err)
            }
        },

        async fetchCompanies() {
            try {
                const res = await API.get("/admin/companies")
                this.companies = res.data
            } catch (err) {
                console.log("Companies error:", err)
            }
        },

        async fetchPlacements() {  
            try {
                const res = await API.get("/admin/placements")
                this.placements = res.data
            } catch (err) {
                console.log("Placements error:", err)
            }
        },

        async approveCompany(id) {
            try {
                const res = await API.put("/admin/approve_company/" + id)
                this.message = res.data.message
                this.fetchCompanies()
                this.fetchSummary()
            } catch (err) {
                this.message = err.response?.data?.message || "Company approval failed"
            }
        },

        async removeCompany(id) {
            try {
                const res = await API.delete("/admin/remove_company/" + id)
                this.message = res.data.message
                this.fetchCompanies()
                this.fetchSummary()
            } catch (err) {
                this.message = err.response?.data?.message || "Company removal failed"
            }
        },

        async fetchDrives() {
            try {
                const res = await API.get("/admin/drives")
                this.drives = res.data
            } catch (err) {
                console.log("Drives error:", err)
            }
        },

        async fetchStudents() {
            try {
                const res = await API.get("/admin/students")
                this.students = res.data
            } catch (err) {
                console.log("Students error:", err)
            }
        },

        viewResume(path){
            if(!path){
                alert("No resume available")
                return
            }

            window.open(`${import.meta.env.VITE_API_URL}/uploads/` + path)
        },

        async approveDrive(id) {
            try {
                this.message = ""

                const res = await API.put("/admin/approve_drive/" + id)

                this.message = res.data.message

                this.fetchDrives()      
                this.fetchSummary()

            } catch (err) {
                this.message = err.response?.data?.message || "Drive approval failed"
            }
        },

        async blacklistUser(userId) {
            try {
                const res = await API.put("/admin/blacklist_user/" + userId)
                this.message = res.data.message
                this.students = this.students.filter(s => s.user_id !== userId)

                this.fetchStudents()
                this.companies = this.companies.filter(c => c.user_id !== userId)

            } catch (err) {
                this.message = err.response?.data?.message || "Blacklist failed"
            }
        },
        async removeDrive(id) {
            try {
                this.message = ""
                const res = await API.delete("/admin/remove_drive/" + id)
                this.message = res.data.message
                this.fetchDrives()
                this.fetchSummary()

            } catch (err) {
                this.message = err.response?.data?.message || "Drive removal failed"
            }
        },
        async fetchApplications() {
            try {
                const res = await API.get("/admin/applications")
                this.applications = res.data
            } catch (err) {
                console.log("Applications error:", err)
            }
        },

        async searchData() {
            if (this.searchText.trim() === "") {
                this.resetData()
                return
            }

            try {
                const companyRes = await API.get("/admin/search_company", {
                    params: { name: this.searchText }
                })
                this.companies = companyRes.data
            } catch {
                this.companies = []
            }

            try {
                const studentRes = await API.get("/admin/search_student", {
                    params: { name: this.searchText }
                })
                this.students = studentRes.data
            } catch {
                this.students = []
            }
        },

        async markComplete(id){
            try{
                const res = await API.put("/admin/complete_drive/" + id)
                this.message = res.data.message
                this.fetchDrives()
            }catch(err){
                this.message = "Failed to mark complete"
            }
        },

        resetData() {
            this.searchText = ""
            this.fetchCompanies()
            this.fetchSummary()
            this.fetchPlacements()   
            this.message = ""
        },

        logout() {
            localStorage.removeItem("token")
            localStorage.removeItem("role")
            this.$router.push("/")
        },

        viewDrive(id){
            this.$router.push("/drive/" + id)
        },

        viewApplication(id){
            this.$router.push("/application/" + id)
        },      

        
    },

    mounted() {
        this.fetchSummary()
        this.fetchCompanies()
        this.fetchStudents()
        this.fetchPlacements() 
        this.fetchDrives() 
        this.fetchApplications()
    }
}
</script>
<style>

.admin-dashboard{

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

gap:20px;

}

.hero-section h1{

font-size:42px;

margin-bottom:10px;

}

.hero-section p{

opacity:.9;

max-width:600px;

}

.logout-btn{

background:#53b0c2;

color:white;

padding:12px 22px;

border:none;

border-radius:10px;

cursor:pointer;

}

.search-box{

display:flex;

gap:15px;

margin-bottom:30px;

align-items:center;

flex-wrap:wrap;

}

.search-box input{

flex:1;

min-width:280px;

padding:14px;

border:none;

border-radius:10px;

font-size:15px;

}

.search-box button{

padding:12px 22px;

border:none;

border-radius:10px;

cursor:pointer;

background:#2563eb;

color:white;

}

.stats-grid{

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

box-shadow:0 10px 25px rgba(0,0,0,.25);

transition:.3s;

}

.stat-card:hover{

transform:translateY(-4px);

}

.stat-card h2{

font-size:34px;

margin-bottom:10px;

}

.glass-card{

background:rgba(255,255,255,.12);

backdrop-filter:blur(18px);

padding:22px;

margin-bottom:25px;

border-radius:18px;

box-shadow:0 10px 25px rgba(0,0,0,.25);

transition:.3s;

}

.glass-card:hover{

transform:translateY(-3px);

}

.glass-item{

background:rgba(255,255,255,.08);

padding:18px;

border-radius:15px;

margin-bottom:15px;

display:flex;

justify-content:space-between;

align-items:center;

gap:20px;

}

.action-buttons{

display:flex;

gap:10px;

flex-wrap:wrap;

}

button{
    padding:9px 16px;
    border:none;
    border-radius:8px;
    cursor:pointer;
    background:#2563eb;
    color:white;
    font-weight:500;
    transition:.2s;
}

button{

transition:.25s;

}

button:hover{

transform:translateY(-2px);

opacity:.95;

}

.danger-btn{
    background:#bb2b2b;
}

.logout-btn{
    background:#111827;
}

.modern-table{

width:100%;

border-collapse:collapse;

margin-top:20px;

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

.green-badge{

background:#16a34a;

padding:5px 12px;

border-radius:20px;

}

.red-badge{

background:#dc2626;

padding:6px 12px;

border-radius:20px;

color:white;

font-weight:600;

}

.green-badge{

background:#16a34a;

padding:6px 12px;

border-radius:20px;

color:white;

font-weight:600;

}

.orange-badge{

background:#f59e0b;

padding:6px 12px;

border-radius:20px;

color:white;

font-weight:600;

}

.danger-btn{

background:#d95638;

color:white;

}
.blue-badge{

background:#2563eb;

padding:6px 12px;

border-radius:20px;

color:white;

font-weight:600;

}

.purple-badge{

background:#7c3aed;

padding:6px 12px;

border-radius:20px;

color:white;

font-weight:600;

}

.darkgreen-badge{

background:#059669;

padding:6px 12px;

border-radius:20px;

color:white;

font-weight:600;

}
.modern-table thead{

position:sticky;

top:0;

z-index:5;

}
.modern-table tbody tr:nth-child(even){

background:rgba(255,255,255,.05);

}

.modern-table tbody tr{

transition:.25s;

}

.modern-table tbody tr:hover{

background:rgba(255,255,255,.15);

transform:scale(1.01);

}

</style>