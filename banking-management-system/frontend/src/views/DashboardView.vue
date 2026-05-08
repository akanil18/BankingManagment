<template>
  <div class="dashboard">
    <!-- Top Navbar -->
    <el-header class="navbar">
      <span class="brand">Banking Management System</span>
      <div class="nav-actions">
        <el-button size="small" @click="$router.push('/upload')">+ Upload Data</el-button>
        <el-button size="small" type="danger" plain @click="logout">Logout</el-button>
      </div>
    </el-header>

    <div class="main">
      <!-- Left: Data Panel -->
      <div class="data-panel">
        <div class="table-selector">
          <span class="panel-title">Your Tables</span>
          <el-select v-model="selectedTableId" placeholder="Select a table" @change="loadRows" style="width:100%;margin-top:8px">
            <el-option v-for="t in tables" :key="t.id" :label="`${t.table_name} (${t.row_count} rows)`" :value="t.id" />
          </el-select>
        </div>

        <div v-if="activeTable" class="data-table-wrap">
          <div class="table-header">
            <span>{{ activeTable.name }}</span>
            <el-pagination
              small layout="prev, pager, next"
              :total="total" :page-size="pageSize"
              :current-page.sync="page" @current-change="loadRows" />
          </div>
          <el-table :data="rows" v-loading="loading" border stripe size="small" style="width:100%">
            <el-table-column v-for="col in activeTable.columns" :key="col" :prop="col" :label="col" min-width="120" show-overflow-tooltip />
          </el-table>
        </div>

        <el-empty v-else description="Select a table to view data" />
      </div>

      <!-- Right: Chat Sidebar -->
      <div class="chat-sidebar">
        <div class="sidebar-header">
          <span>AI Assistant</span>
          <el-button size="mini" type="text" @click="clearHistory">Clear</el-button>
        </div>

        <div class="messages" ref="msgContainer">
          <div v-for="(msg, i) in messages" :key="i" :class="['message', msg.role]">
            <div class="bubble" v-if="msg.type === 'text'">{{ msg.content }}</div>

            <!-- Table result -->
            <div class="bubble table-result" v-if="msg.type === 'table'">
              <p>{{ msg.content }}</p>
              <el-table :data="msg.rows" border size="mini" style="margin-top:8px">
                <el-table-column v-for="col in msg.columns" :key="col" :prop="col" :label="col" min-width="100" show-overflow-tooltip />
              </el-table>
            </div>

            <!-- Clarify options -->
            <div class="bubble" v-if="msg.type === 'clarify'">
              <p>{{ msg.content }}</p>
              <el-button
                v-for="opt in msg.clarifyOptions" :key="opt.table_id"
                size="mini" style="margin:4px 4px 0 0"
                @click="sendQuery(lastQuery, opt.table_id)">
                {{ opt.label }}
              </el-button>
            </div>
          </div>

          <div v-if="agentLoading" class="message assistant">
            <div class="bubble typing">Thinking...</div>
          </div>
        </div>

        <div class="chat-input">
          <el-input
            v-model="queryText" placeholder="Ask about your data..."
            @keyup.enter.native="sendQuery(queryText)"
            :disabled="agentLoading" size="small" />
          <el-button type="primary" size="small" @click="sendQuery(queryText)" :loading="agentLoading">Send</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardView',
  data() {
    return { selectedTableId: null, page: 1, pageSize: 50, queryText: '', lastQuery: '' }
  },
  computed: {
    tables() { return this.$store.state.data.tables },
    activeTable() { return this.$store.state.data.activeTable },
    rows() { return this.$store.state.data.rows },
    total() { return this.$store.state.data.total },
    loading() { return this.$store.state.data.loading },
    messages() { return this.$store.state.agent.messages },
    agentLoading() { return this.$store.state.agent.loading },
  },
  async created() {
    await this.$store.dispatch('data/fetchTables')
    await this.$store.dispatch('agent/fetchHistory')
  },
  updated() {
    this.$nextTick(() => {
      const c = this.$refs.msgContainer
      if (c) c.scrollTop = c.scrollHeight
    })
  },
  methods: {
    async loadRows() {
      if (!this.selectedTableId) return
      await this.$store.dispatch('data/fetchRows', { tableId: this.selectedTableId, page: this.page, pageSize: this.pageSize })
    },
    async sendQuery(query, tableId = null) {
      if (!query.trim()) return
      this.lastQuery = query
      this.queryText = ''
      await this.$store.dispatch('agent/sendQuery', { query, selectedTableId: tableId || this.selectedTableId })
    },
    async clearHistory() {
      await this.$store.dispatch('agent/clearHistory')
    },
    logout() {
      this.$store.dispatch('auth/logout')
      this.$router.push('/login')
    },
  },
}
</script>

<style scoped>
.dashboard { display:flex; flex-direction:column; height:100vh; }
.navbar { display:flex; align-items:center; justify-content:space-between; background:#409EFF; color:#fff; padding:0 20px; height:56px; }
.brand { font-size:16px; font-weight:bold; }
.main { display:flex; flex:1; overflow:hidden; }
.data-panel { flex:1; padding:16px; overflow:auto; border-right:1px solid #EBEEF5; }
.panel-title { font-weight:bold; color:#303133; }
.table-header { display:flex; justify-content:space-between; align-items:center; margin:12px 0 8px; }
.data-table-wrap { margin-top:16px; }
.chat-sidebar { width:380px; display:flex; flex-direction:column; background:#fff; }
.sidebar-header { display:flex; justify-content:space-between; align-items:center; padding:12px 16px; border-bottom:1px solid #EBEEF5; font-weight:bold; }
.messages { flex:1; overflow-y:auto; padding:12px; display:flex; flex-direction:column; gap:8px; }
.message { display:flex; }
.message.user { justify-content:flex-end; }
.message.assistant { justify-content:flex-start; }
.bubble { max-width:90%; padding:8px 12px; border-radius:8px; font-size:13px; line-height:1.5; word-break:break-word; }
.message.user .bubble { background:#409EFF; color:#fff; border-radius:8px 2px 8px 8px; }
.message.assistant .bubble { background:#F2F6FC; color:#303133; border-radius:2px 8px 8px 8px; }
.table-result { max-width:100%; overflow-x:auto; }
.typing { color:#909399; font-style:italic; }
.chat-input { display:flex; gap:8px; padding:12px; border-top:1px solid #EBEEF5; }
.chat-input .el-input { flex:1; }
</style>
