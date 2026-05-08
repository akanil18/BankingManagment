import dataService from '@/services/dataService'

export default {
  namespaced: true,
  state: () => ({ tables: [], activeTable: null, rows: [], total: 0, loading: false }),
  mutations: {
    SET_TABLES(state, tables) { state.tables = tables },
    SET_ACTIVE_TABLE(state, table) { state.activeTable = table },
    SET_ROWS(state, { rows, total }) { state.rows = rows; state.total = total },
    SET_LOADING(state, v) { state.loading = v },
  },
  actions: {
    async fetchTables({ commit }) {
      commit('SET_LOADING', true)
      const { data } = await dataService.getTables()
      commit('SET_TABLES', data.tables)
      commit('SET_LOADING', false)
    },
    async fetchRows({ commit }, { tableId, page, pageSize }) {
      commit('SET_LOADING', true)
      const { data } = await dataService.getRows(tableId, page, pageSize)
      commit('SET_ACTIVE_TABLE', { id: data.table_id, name: data.table_name, columns: data.columns })
      commit('SET_ROWS', { rows: data.rows, total: data.total })
      commit('SET_LOADING', false)
    },
    async deleteTable({ dispatch }, tableId) {
      await dataService.deleteTable(tableId)
      dispatch('fetchTables')
    },
  },
}
