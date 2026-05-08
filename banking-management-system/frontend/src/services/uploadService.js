import api from './api'

export default {
  uploadFile(file, tableName) {
    const form = new FormData()
    form.append('file', file)
    form.append('table_name', tableName)
    return api.post('/upload/file', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  confirmMapping(tableId, mappings) {
    return api.post('/upload/confirm-mapping', { table_id: tableId, mappings })
  },
}
