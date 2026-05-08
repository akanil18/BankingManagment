import uploadService from '@/services/uploadService'

export default {
  namespaced: true,
  state: () => ({ uploading: false, pendingUpload: null }),
  mutations: {
    SET_UPLOADING(state, v) { state.uploading = v },
    SET_PENDING(state, data) { state.pendingUpload = data },
    CLEAR_PENDING(state) { state.pendingUpload = null },
  },
  actions: {
    async uploadFile({ commit }, { file, tableName }) {
      commit('SET_UPLOADING', true)
      const { data } = await uploadService.uploadFile(file, tableName)
      commit('SET_PENDING', data)
      commit('SET_UPLOADING', false)
      return data
    },
    async confirmMapping({ commit }, { tableId, mappings }) {
      const { data } = await uploadService.confirmMapping(tableId, mappings)
      commit('CLEAR_PENDING')
      return data
    },
  },
}
