    <template>
    <div class="page">

        <div v-if="app" class="details-card">

            <h2 class="page-title">
                Application Details
            </h2>

            <div class="student-header">

                <div class="student-avatar">
                    {{ app.student_name.charAt(0).toUpperCase() }}
                </div>

                <div>

                    <h2>{{ app.student_name }}</h2>

                    <p class="department">
                        Department : {{ app.branch }}
                    </p>

                </div>

            </div>

            <div class="details-grid">

                <div class="info-box">
                    <span>Company</span>
                    <strong>{{ app.company_name }}</strong>
                </div>

                <div class="info-box">
                    <span>Job Title</span>
                    <strong>{{ app.job_title }}</strong>
                </div>

                <div class="info-box">
                    <span>Status</span>
                    <strong>{{ app.status }}</strong>
                </div>

                <div class="info-box">
                    <span>Interview</span>
                    <strong>
                        {{ app.interview_date || "Not Scheduled" }}
                    </strong>
                </div>

            </div>

            <div class="button-row">

    <button
        v-if="app.resume"
        class="resume-btn"
        @click="viewResume"
    >
        View Resume
    </button>

    <button
        class="back-btn"
        @click="goBack"
    >
        Back
    </button>

</div>

        </div>


    </div>
    </template>

    <script>
    import API from "../api/api"

    export default {
    data(){
    return{
        app:null,
        newStatus:"",
        interview_date:""
    }
    },

    methods:{
    async fetchApp(){
    const id = this.$route.params.id
    const res = await API.get("/admin/applications")
    this.app = res.data.find(a => a.application_id == id)
    this.newStatus = this.app ? this.app.status : ""
    },


    viewResume(){
        const filename = this.app.resume.split("/").pop()
        window.open(`${import.meta.env.VITE_API_URL}/uploads/` + this.app.resume)
    },

    goBack(){
        this.$router.push("/admin")
    }
    },

    mounted(){
        this.fetchApp()
    }
    }
    </script>

    <style scoped>

    .page{
        min-height:100vh;
        background:#f4f8fc;
        padding:40px;
    }

    .details-card{
        max-width:900px;
        margin:20px auto;
        background:white;
        border-radius:16px;
        padding:35px;
        box-shadow:0 8px 24px rgba(0,0,0,.08);
    }

    .student-header{
        display:flex;
        align-items:center;
        gap:20px;
        margin-bottom:30px;
    }

    .student-avatar{
        width:70px;
        height:70px;
        border-radius:50%;
        background:#2563eb;
        color:white;
        display:flex;
        justify-content:center;
        align-items:center;
        font-size:28px;
        font-weight:bold;
    }

    .student-header h2{
        margin:0;
        color:#1f2937;
    }

    .student-header p{
        margin-top:6px;
        color:#6b7280;
    }

    .details-grid{
        display:grid;
        grid-template-columns:repeat(2,1fr);
        gap:20px;
        margin-bottom:30px;
    }

    .info-box{
        background:#f8fafc;
        border-left:4px solid #2563eb;
        padding:18px;
        border-radius:10px;
    }

    .info-box span{
        display:block;
        color:#6b7280;
        margin-bottom:8px;
    }

    .info-box strong{
        color:#1f2937;
    }

    .resume-btn{
        background:#2563eb;
        color:white;
        border:none;
        padding:12px 22px;
        border-radius:8px;
        cursor:pointer;
    }

    .resume-btn:hover{
        background:#1d4ed8;
    }

    .page > button{
        margin-top:25px;
        background:#6b7280;
        color:white;
        border:none;
        padding:10px 20px;
        border-radius:8px;
        cursor:pointer;
    }
    .page-title{
    margin-bottom:30px;
    color:#1e3a8a;
    text-align:center;
    font-size:30px;
}

.department{
    color:#6b7280;
    margin-top:6px;
}

.student-avatar{
    width:60px;
    height:60px;
    font-size:24px;
}

.button-row{
    display:flex;
    justify-content:center;
    gap:15px;
    margin-top:30px;
}

.back-btn{
    background:#6b7280;
    color:white;
    border:none;
    padding:12px 22px;
    border-radius:8px;
    cursor:pointer;
}

.back-btn:hover{
    background:#4b5563;
}

    </style>