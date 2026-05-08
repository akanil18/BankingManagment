import authService from '@/services/authService'
import { setToken, setRefreshToken, clearTokens, getToken } from '@/utils/tokenHelper'

export default {
  namespaced: true,
  state: () => ({ user: null, loading: false }),
  getters: {
    isLoggedIn: () => !!getToken(),
    user: s => s.user,
  },
  mutations: {
    SET_USER(state, user) { state.user = user },
    SET_LOADING(state, v) { state.loading = v },
  },
  actions: {
    async register({ commit }, { name, email, password }) {
      commit('SET_LOADING', true)
      const { data } = await authService.register(name, email, password)
      setToken(data.access_token)
      setRefreshToken(data.refresh_token)
      commit('SET_LOADING', false)
    },
    async login({ commit }, { email, password }) {
      commit('SET_LOADING', true)
      const { data } = await authService.login(email, password)
      setToken(data.access_token)
      setRefreshToken(data.refresh_token)
      commit('SET_LOADING', false)
    },
    async fetchMe({ commit }) {
      const { data } = await authService.me()
      commit('SET_USER', data)
    },
    logout({ commit }) {
      clearTokens()
      commit('SET_USER', null)
    },
  },
}
