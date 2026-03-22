<template>
<div class="register-page">
    <div class="register-box">
        <h2>Student Registration</h2>

        <form @submit.prevent="registerStudent">
            <input type="text" v-model="username" placeholder="Username" />
            <input type="password" v-model="password" placeholder="Password" />
            <input type="text" v-model="name" placeholder="Full Name" />
            <input type="email" v-model="email" placeholder="Email" />

            <button type="submit">Register</button>
        </form>

        <p>{{ message }}</p>

        <p>
            Already have an account?
            <router-link to="/">Login</router-link>
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
            name: "",
            email: "",
            message: ""
        }
    },

    methods: {
        async registerStudent() {
            try {
                const res = await API.post("/register/student", {
                    username: this.username,
                    password: this.password,
                    name: this.name,
                    email: this.email
                })

                this.message = res.data.message

                this.username = ""
                this.password = ""
                this.name = ""
                this.email = ""

                setTimeout(() => {
                    this.$router.push("/")
                }, 1000)

            } catch (err) {
                if (err.response && err.response.data && err.response.data.message) {
                    this.message = err.response.data.message
                } else {
                    this.message = "Student registration failed"
                }
            }
        }
    }
}
</script>

<style>
.register-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.register-box {
    width: 320px;
    border: 1px solid black;
    border-radius: 12px;
    padding: 20px;
}

.register-box h2 {
    text-align: center;
    margin-bottom: 20px;
}

.register-box input {
    width: 100%;
    padding: 10px;
    margin-bottom: 12px;
    box-sizing: border-box;
}

.register-box button {
    width: 100%;
    padding: 10px;
    cursor: pointer;
}
</style>