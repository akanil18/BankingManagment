import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import upload from './modules/upload'
import data from './modules/data'
import agent from './modules/agent'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: { auth, upload, data, agent },
})
