<template>
<div>

<h2>Admin Dashboard</h2>

<button @click="logout">Logout</button>

</div>
</template>

<script>
export default {

methods: {

logout() {

localStorage.removeItem("token")

this.$router.push("/")

}

}

}
</script>