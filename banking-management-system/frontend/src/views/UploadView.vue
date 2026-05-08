<template>
  <div class="upload-page">
    <el-card class="upload-card">
      <div slot="header"><span>Upload Banking Data</span></div>

      <el-form :model="form" ref="form" label-width="120px" v-if="!pendingUpload">
        <el-form-item label="Table Name" prop="tableName" :rules="[{required:true,message:'Required'}]">
          <el-input v-model="form.tableName" placeholder="e.g. Transactions Jan 2026" />
        </el-form-item>
        <el-form-item label="File">
          <el-upload
            drag action="#" :auto-upload="false" :on-change="onFileChange"
            accept=".xlsx,.xls,.csv" :limit="1">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">Drop Excel/CSV here or <em>click to upload</em></div>
            <div class="el-upload__tip" slot="tip">Supports .xlsx, .xls, .csv — max 50MB</div>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="uploading" @click="upload" :disabled="!selectedFile">
            Upload & Detect Columns
          </el-button>
        </el-form-item>
      </el-form>

      <!-- Field Mapping Confirmation -->
      <div v-if="pendingUpload">
        <el-alert type="success" :closable="false" style="margin-bottom:16px">
          <b>{{ pendingUpload.row_count }} rows detected</b> — confirm field mappings below
        </el-alert>
        <el-table :data="pendingUpload.suggested_mappings" border style="width:100%;margin-bottom:16px">
          <el-table-column prop="original_column" label="CSV Column" />
          <el-table-column label="Maps To">
            <template slot-scope="scope">
              <el-select v-model="scope.row.mapped_column" size="small">
                <el-option v-for="f in standardFields" :key="f" :label="f" :value="f" />
                <el-option :label="scope.row.original_column" :value="scope.row.original_column" />
              </el-select>
            </template>
          </el-table-column>
        </el-table>
        <el-button type="success" @click="confirmMapping">Confirm & Load Data</el-button>
        <el-button @click="$store.commit('upload/CLEAR_PENDING')" style="margin-left:8px">Cancel</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
const STANDARD_FIELDS = ['account_no','date','amount','debit','credit','balance','description','transaction_id','type','branch','currency','reference_no']

export default {
  name: 'UploadView',
  data() {
    return { form: { tableName: '' }, selectedFile: null, standardFields: STANDARD_FIELDS }
  },
  computed: {
    uploading() { return this.$store.state.upload.uploading },
    pendingUpload() { return this.$store.state.upload.pendingUpload },
  },
  methods: {
    onFileChange(file) { this.selectedFile = file.raw },
    async upload() {
      this.$refs.form.validate(async valid => {
        if (!valid || !this.selectedFile) return
        try {
          await this.$store.dispatch('upload/uploadFile', { file: this.selectedFile, tableName: this.form.tableName })
        } catch (e) {
          this.$message.error(e.response?.data?.detail || 'Upload failed')
        }
      })
    },
    async confirmMapping() {
      try {
        await this.$store.dispatch('upload/confirmMapping', {
          tableId: this.pendingUpload.table_id,
          mappings: this.pendingUpload.suggested_mappings,
        })
        this.$message.success('Data loaded successfully!')
        this.$router.push('/dashboard')
      } catch (e) {
        this.$message.error('Failed to save mappings')
      }
    },
  },
}
</script>

<style scoped>
.upload-page { padding: 40px; max-width: 800px; margin: 0 auto; }
.upload-card { margin-top: 20px; }
</style>
