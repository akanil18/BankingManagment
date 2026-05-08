import api from './api'

export default {
  query: (query, selectedTableId = null) =>
    api.post('/agent/query', { query, selected_table_id: selectedTableId }),
  getHistory: () => api.get('/agent/history'),
  clearHistory: () => api.delete('/agent/history'),
}
