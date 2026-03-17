<template>
<div>

<h2>Login</h2>

<form @submit.prevent="loginUser">

<input type="text" v-model="email" placeholder="Email" />
<input type="password" v-model="password" placeholder="Password" />

<button type="submit">Login</button>

</form>

<p>{{ message }}</p>

</div>
</template>

<script>

import API from "../api/api"

export default {

data() {
return {
email: "",
password: "",
message: ""
}
},

methods: {

async loginUser() {

try {

const res = await API.post("/login", {
email: this.email,
password: this.password
})

const token = res.data.access_token
const role = res.data.role

localStorage.setItem("token", token)

if (role === "student") this.$router.push("/student")
if (role === "company") this.$router.push("/company")
if (role === "admin") this.$router.push("/admin")

} catch (err) {

this.message = "Invalid credentials"

}

}

}

}

</script>