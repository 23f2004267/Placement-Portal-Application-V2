<template>
<div class="admin-dashboard">

    <div class="top-bar">
        <h2>Admin Dashboard</h2>
        <button class="logout-btn" @click="logout">Logout</button>
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

    <div class="welcome-box">
        <p><b>Welcome Admin</b></p>
        <p>{{ message }}</p>
    </div>

    <div class="summary-box">
        <h3>System Summary</h3>
        <p><b>Total Students:</b> {{ summary.students }}</p>
        <p><b>Total Companies:</b> {{ summary.companies }}</p>
        <p><b>Total Drives:</b> {{ summary.drives }}</p>
        <p><b>Total Applications:</b> {{ summary.applications }}</p>
    </div>

    <div class="section-box">
        <h3>Registered Companies</h3>

        <div v-if="companies.length === 0">
            No companies found
        </div>

        <div v-for="company in companies" :key="company.id" class="item-card">
            <div>
                <p><b>Company:</b> {{ company.company_name }}</p>
                <p><b>Website:</b> {{ company.website }}</p>
                <p><b>Status:</b> {{ company.status }}</p>
            </div>

            <div class="action-buttons">
                <button
                    v-if="company.status !== 'Approved'"
                    @click="approveCompany(company.id)"
                >
                    Approve
                </button>

                <button class="danger-btn" @click="removeCompany(company.id)">
                    Remove
                </button>
            </div>
        </div>
    </div>

    <div class="section-box">
        <h3>Registered Students</h3>

        <div v-if="students.length === 0">
            No students found
        </div>

        <div v-for="student in students" :key="student.id" class="item-card">
            <div>
                <p><b>Name:</b> {{ student.name }}</p>
                <p><b>Email:</b> {{ student.email }}</p>
                <p><b>Active:</b> {{ student.is_active ? "Yes" : "No" }}</p>
            </div>

            <div class="action-buttons">
                <button
                    v-if="student.is_active"
                    class="danger-btn"
                    @click="blacklistUser(student.user_id)"
                >
                    Blacklist
                </button>
            </div>
        </div>
    </div>

    <div class="section-box">
        <h3>Ongoing Drives</h3>

        <div v-if="drives.length === 0">
            No drives found
        </div>

        <div v-for="drive in drives" :key="drive.id" class="item-card">
            <div>
                <p><b>Company:</b> {{ drive.company_name }}</p>
                <p><b>Job Title:</b> {{ drive.job_title }}</p>
                <p><b>Salary:</b> {{ drive.salary }}</p>
                <p><b>Status:</b> {{ drive.status }}</p>
            </div>

            <div class="action-buttons">
                <button
                    v-if="drive.status !== 'Approved'"
                    @click="approveDrive(drive.id)"
                >
                    Approve Drive
                </button>
            </div>
        </div>
    </div>

    <!-- ✅ NEW SECTION (ADDED ONLY, NOTHING REMOVED) -->
    <div class="section-box">
        <h3>Placement Report</h3>

        <div v-if="placements.length === 0">
            No placements yet
        </div>

        <div v-for="p in placements" :key="p.placement_id" class="item-card">
            <div>
                <p><b>Student:</b> {{ p.student_name }}</p>
                <p><b>Company:</b> {{ p.company_name }}</p>
                <p><b>Position:</b> {{ p.position }}</p>
                <p><b>Salary:</b> {{ p.salary }}</p>
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

        async fetchStudents() {
            try {
                const res = await API.get("/admin/students")
                this.students = res.data
            } catch (err) {
                console.log("Students error:", err)
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
                this.fetchDrives()
            } catch (err) {
                this.message = err.response?.data?.message || "Company removal failed"
            }
        },

        async approveDrive(id) {
            try {
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
                this.fetchStudents()
            } catch (err) {
                this.message = err.response?.data?.message || "Blacklist failed"
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

        resetData() {
            this.searchText = ""
            this.fetchCompanies()
            this.fetchStudents()
            this.fetchDrives()
            this.fetchSummary()
            this.fetchPlacements()   
            this.message = ""
        },

        logout() {
            localStorage.removeItem("token")
            this.$router.push("/")
        }
    },

    mounted() {
        this.fetchSummary()
        this.fetchCompanies()
        this.fetchStudents()
        this.fetchDrives()
        this.fetchPlacements()  
    }
}
</script>

<style>
.admin-dashboard {
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

.logout-btn {
    padding: 8px 14px;
    cursor: pointer;
}

.search-box {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.search-box input {
    flex: 1;
    min-width: 250px;
    padding: 10px;
    box-sizing: border-box;
}

.search-box button {
    padding: 8px 14px;
    cursor: pointer;
}

.welcome-box,
.summary-box,
.section-box {
    border: 1px solid black;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
}

.item-card {
    border: 1px solid black;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    gap: 20px;
    align-items: center;
}

.action-buttons {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.action-buttons button {
    padding: 6px 12px;
    cursor: pointer;
}

.danger-btn {
    color: red;
}
</style>