import api from './api'

export default {
  getTables: () => api.get('/data/tables'),
  getRows: (tableId, page = 1, pageSize = 50) =>
    api.get(`/data/tables/${tableId}/rows`, { params: { page, page_size: pageSize } }),
  deleteTable: (tableId) => api.delete(`/data/tables/${tableId}`),
}
