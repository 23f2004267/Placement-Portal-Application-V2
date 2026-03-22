<template>
<div class="register-page">
    <div class="register-box">
        <h2>Company Registration</h2>

        <form @submit.prevent="registerCompany">
            <input type="text" v-model="username" placeholder="Username" />
            <input type="password" v-model="password" placeholder="Password" />
            <input type="text" v-model="company_name" placeholder="Company Name" />
            <input type="text" v-model="website" placeholder="Website" />

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
            company_name: "",
            website: "",
            message: ""
        }
    },

    methods: {
        async registerCompany() {
            try {
                const res = await API.post("/register/company", {
                    username: this.username,
                    password: this.password,
                    company_name: this.company_name,
                    website: this.website
                })

                this.message = res.data.message

                this.username = ""
                this.password = ""
                this.company_name = ""
                this.website = ""

                setTimeout(() => {
                    this.$router.push("/")
                }, 1000)

            } catch (err) {
                if (err.response && err.response.data && err.response.data.message) {
                    this.message = err.response.data.message
                } else {
                    this.message = "Company registration failed"
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