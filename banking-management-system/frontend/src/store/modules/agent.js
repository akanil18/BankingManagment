import agentService from '@/services/agentService'

export default {
  namespaced: true,
  state: () => ({ messages: [], loading: false }),
  mutations: {
    ADD_MESSAGE(state, msg) { state.messages.push(msg) },
    SET_MESSAGES(state, msgs) { state.messages = msgs },
    SET_LOADING(state, v) { state.loading = v },
    CLEAR(state) { state.messages = [] },
  },
  actions: {
    async fetchHistory({ commit }) {
      const { data } = await agentService.getHistory()
      commit('SET_MESSAGES', data.messages.map(m => ({ role: m.role, content: m.message, type: 'text' })))
    },
    async sendQuery({ commit }, { query, selectedTableId }) {
      commit('ADD_MESSAGE', { role: 'user', content: query, type: 'text' })
      commit('SET_LOADING', true)
      const { data } = await agentService.query(query, selectedTableId)
      commit('ADD_MESSAGE', {
        role: 'assistant',
        content: data.message,
        type: data.response_type,
        columns: data.columns,
        rows: data.rows,
        clarifyOptions: data.clarify_options,
      })
      commit('SET_LOADING', false)
      return data
    },
    async clearHistory({ commit }) {
      await agentService.clearHistory()
      commit('CLEAR')
    },
  },
}
