<template>
<div>

<h2>Student Dashboard</h2>

<h3>Available Drives</h3>

<ul>
<li v-for="drive in drives" :key="drive.id">

<p><b>Company:</b> {{ drive.company_name }}</p>
<p><b>Role:</b> {{ drive.job_role }}</p>
<p><b>Package:</b> {{ drive.package }}</p>

<hr>

</li>
</ul>

</div>
</template>

<script>

import API from "../api/api"

export default {

data() {
return {
drives: []
}
},

methods: {

async fetchDrives() {

try {

const res = await API.get("/student/drives")

this.drives = res.data

} catch (err) {

console.log(err)

}

}

},

mounted() {

this.fetchDrives()

}

}

</script>