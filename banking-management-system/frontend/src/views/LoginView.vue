<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>Banking Management System</h2>
      <h3>Sign In</h3>
      <el-form :model="form" :rules="rules" ref="form" @submit.native.prevent="submit">
        <el-form-item prop="email">
          <el-input v-model="form.email" placeholder="Email" prefix-icon="el-icon-message" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" placeholder="Password" prefix-icon="el-icon-lock" show-password />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading" style="width:100%">Login</el-button>
      </el-form>
      <p class="auth-link">Don't have an account? <router-link to="/register">Register</router-link></p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      form: { email: '', password: '' },
      rules: {
        email: [{ required: true, type: 'email', message: 'Valid email required', trigger: 'blur' }],
        password: [{ required: true, min: 6, message: 'Min 6 characters', trigger: 'blur' }],
      },
    }
  },
  computed: {
    loading() { return this.$store.state.auth.loading },
  },
  methods: {
    submit() {
      this.$refs.form.validate(async valid => {
        if (!valid) return
        try {
          await this.$store.dispatch('auth/login', this.form)
          this.$router.push('/dashboard')
        } catch (e) {
          this.$message.error(e.response?.data?.detail || 'Login failed')
        }
      })
    },
  },
}
</script>

<style scoped>
.auth-page { display:flex; justify-content:center; align-items:center; min-height:100vh; background:#f0f2f5; }
.auth-card { background:#fff; padding:40px; border-radius:8px; width:400px; box-shadow:0 2px 12px rgba(0,0,0,.1); }
h2 { text-align:center; color:#409EFF; margin-bottom:8px; font-size:18px; }
h3 { text-align:center; color:#303133; margin-bottom:24px; }
.auth-link { text-align:center; margin-top:16px; color:#606266; font-size:14px; }
</style>
