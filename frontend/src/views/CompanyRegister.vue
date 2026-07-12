<template>

<div class="register-page">

    <div class="register-box">

        <h1 class="portal-title">
            Company Registration
        </h1>

        <p class="subtitle">
            Create your company account
        </p>

        <form @submit.prevent="registerCompany">

            <input
                type="text"
                v-model="username"
                placeholder="Username"
            />

            <input
                type="password"
                v-model="password"
                placeholder="Password"
                autocomplete="new-password"
            />

            <input
                type="text"
                v-model="company_name"
                placeholder="Company Name"
            />

            <input
                type="text"
                v-model="website"
                placeholder="Company Website"
            />

            <button type="submit">
                Register
            </button>

        </form>

        <p class="message">
            {{ message }}
        </p>

        <hr>

        <p class="login-link">
            Already have an account?

            <router-link to="/">
                Login
            </router-link>

        </p>

    </div>

</div>

</template>

<script>
import API from "../api/api"

export default {

data(){
return{
username:"",
password:"",
company_name:"",
website:"",
message:""
}
},

methods:{

async registerCompany(){

try{

const res = await API.post("/register/company",{

username:this.username,
password:this.password,
company_name:this.company_name,
website:this.website

})

this.message = res.data.message

this.username=""
this.password=""
this.company_name=""
this.website=""

setTimeout(()=>{

this.$router.push("/")

},1000)

}

catch(err){

if(err.response && err.response.data && err.response.data.message){
this.message = err.response.data.message
}
else{
this.message = "Company registration failed"
}

}

}

}

}
</script>

<style scoped>

.register-page{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(135deg,#2563eb,#1e40af);
    padding:20px;
}

.register-box{
    width:440px;
    background:white;
    border-radius:16px;
    padding:40px;
    box-shadow:0 10px 35px rgba(0,0,0,.15);
}

.portal-title{
    text-align:center;
    color:#1e3a8a;
    margin:0;
    font-size:34px;
    font-weight:700;
}

.subtitle{
    text-align:center;
    color:#6b7280;
    margin:12px 0 30px;
}

.register-box input{
    width:100%;
    padding:13px;
    margin-bottom:18px;
    border:1px solid #d1d5db;
    border-radius:8px;
    font-size:15px;
    box-sizing:border-box;
}

.register-box input:focus{
    outline:none;
    border-color:#2563eb;
}

.register-box button{
    width:100%;
    padding:13px;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:8px;
    cursor:pointer;
    font-size:16px;
}

.register-box button:hover{
    background:#1d4ed8;
}

.message{
    text-align:center;
    color:#dc2626;
    min-height:22px;
    margin-top:15px;
}

hr{
    margin:28px 0;
    border:none;
    border-top:1px solid #e5e7eb;
}

.login-link{
    text-align:center;
}

.login-link a{
    color:#2563eb;
    text-decoration:none;
    font-weight:600;
}

.login-link a:hover{
    text-decoration:underline;
}

</style>