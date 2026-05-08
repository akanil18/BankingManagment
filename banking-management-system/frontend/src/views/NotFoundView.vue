<template>
  <div style="text-align:center; padding:100px">
    <h1 style="font-size:72px; color:#C0C4CC">404</h1>
    <p style="color:#909399; margin:16px 0">Page not found</p>
    <el-button type="primary" @click="$router.push('/dashboard')">Go to Dashboard</el-button>
  </div>
</template>
<script>
export default { name: 'NotFoundView' }
</script>
