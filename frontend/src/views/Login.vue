<template>
<div class="login-page">

    <div class="login-box">

        <h1 class="portal-title">Placement Portal</h1>

        <p class="subtitle">
            Sign in to continue
        </p>

        <form @submit.prevent="loginUser">

            <input
                type="text"
                v-model="username"
                placeholder="Username"
            />

            <input
                type="password"
                v-model="password"
                placeholder="Password"
                autocomplete="current-password"
            />

            <button type="submit">
                Login
            </button>

        </form>

        <p class="error-message">
            {{ message }}
        </p>

        <hr>

        <div class="links">

            <router-link to="/register/student">
                Student Registration
            </router-link>

            <router-link to="/register/company">
                Company Registration
            </router-link>

        </div>

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

                localStorage.setItem("token", res.data.access_token)
                localStorage.setItem("role", res.data.role)
                localStorage.setItem("user_id", res.data.user_id)

                if(res.data.role==="student"){
                    this.$router.push("/student")
                }

                else if(res.data.role==="company"){
                    this.$router.push("/company")
                }

                else{
                    this.$router.push("/admin")
                }

            }

            catch(err){

                this.message =
                    err.response?.data?.message ||
                    "Invalid Credentials"

            }

        }

    }

}
</script>

<style scoped>

body{
    margin:0;
    font-family:Arial, Helvetica, sans-serif;
    background:#f4f6f9;
}

.login-page{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(135deg,#2563eb,#1e40af);
    padding:20px;
}

.login-box{
    width:460px;
    max-width:90vw;
    background:white;
    border-radius:14px;
    padding:40px;
    box-shadow:0 10px 35px rgba(0,0,0,.15);
    box-sizing:border-box;
}

.portal-title{
    text-align:center;
    color:#1e3a8a;
    font-size:44px;
    font-weight:700;
    line-height:1.15;
    margin:0 0 12px 0;
    word-break:keep-all;
}

.subtitle{
    text-align:center;
    color:#6b7280;
    margin-bottom:30px;
}

.login-box input{
    width:100%;
    padding:13px;
    margin-bottom:18px;
    border:1px solid #d1d5db;
    border-radius:8px;
    font-size:15px;
    box-sizing:border-box;
}

.login-box input:focus{
    outline:none;
    border-color:#2563eb;
}

.login-box button{
    width:100%;
    padding:13px;
    border:none;
    border-radius:8px;
    background:#2563eb;
    color:white;
    font-size:16px;
    cursor:pointer;
}

.login-box button:hover{
    background:#1d4ed8;
}

.error-message{
    text-align:center;
    color:#dc2626;
    min-height:22px;
    margin-top:15px;
}

hr{
    margin:25px 0;
    border:none;
    border-top:1px solid #e5e7eb;
}

.links{
    display:flex;
    justify-content:space-between;
}

.links a{
    text-decoration:none;
    color:#2563eb;
    font-weight:500;
}

.links a:hover{
    text-decoration:underline;
}
</style>