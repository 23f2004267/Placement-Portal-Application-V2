<template>
<div class="login-page">
    <div class="login-box">
        <h2>Login</h2>

        <form @submit.prevent="loginUser">
            <input type="text" v-model="username" placeholder="Username" />
            <input type="password" v-model="password" placeholder="Password" />

            <button type="submit">Login</button>
        </form>

        <p>{{ message }}</p>

        <p>
            <router-link to="/register/student">Register as Student</router-link>
        </p>

        <p>
            <router-link to="/register/company">Register as Company</router-link>
        </p>
    </div>
</div>
</template>

<script>
import API from "../api/api"

export default {
    data() {
        return {
            username: "",
            password: "",
            message: ""
        }
    },

    methods: {
        async loginUser() {
            try {
                this.message = ""

                const res = await API.post("/login", {
                    username: this.username,
                    password: this.password
                })

                const token = res.data.access_token
                const role = res.data.role

                localStorage.setItem("token", token)
                localStorage.setItem("role", role)

                if (role === "student") {
                    this.$router.push("/student")
                }

                if (role === "company") {
                    this.$router.push("/company")
                }

                if (role === "admin") {
                    this.$router.push("/admin")
                }

            } catch (err) {
                if (err.response && err.response.data && err.response.data.message) {
                    this.message = err.response.data.message
                } else {
                    this.message = "Invalid credentials"
                }
            }
        }
    }
}
</script>

<style>
.login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.login-box {
    width: 320px;
    border: 1px solid black;
    border-radius: 12px;
    padding: 20px;
}

.login-box h2 {
    text-align: center;
    margin-bottom: 20px;
}

.login-box input {
    width: 100%;
    padding: 10px;
    margin-bottom: 12px;
    box-sizing: border-box;
}

.login-box button {
    width: 100%;
    padding: 10px;
    cursor: pointer;
}
</style>