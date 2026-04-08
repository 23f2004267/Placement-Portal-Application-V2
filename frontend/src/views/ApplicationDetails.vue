<template>
<div class="page">

    <h2>Application Details</h2>

    <div v-if="app">

    <p><b>Student:</b> {{ app.student_name }}</p>
    <p><b>Department:</b> {{ app.branch }}</p>
    <p><b>Company:</b> {{ app.company_name }}</p>
    <p><b>Job:</b> {{ app.job_title }}</p>
    <p><b>Status:</b> {{ app.status }}</p>
    <p>
        <b>Interview Date:</b>
        {{ app.interview_date || "Not Scheduled" }}
    </p>

    <button v-if="app.resume" @click="viewResume">
        View Resume
    </button>

</div>

    <button @click="goBack">Back</button>

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
    window.open("http://127.0.0.1:5000/uploads/" + filename)
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