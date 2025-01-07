import { createStore } from 'vuex'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

export default createStore({
  state: {
    count: 0,
    users: [],
    inputText: ''
  },
  
  getters: {
    filteredUsers: (state) => {
      return state.users.filter(user => user.id <= 5)
    },
    reversedText: (state) => {
      return state.inputText.split('').reverse().join('')
    }
  },
  
  mutations: {
    INCREMENT_COUNT(state) {
      state.count++
    },
    SET_USERS(state, users) {
      state.users = users
    },
    SET_INPUT_TEXT(state, text) {
      state.inputText = text
    }
  },
  
  actions: {
    async updateCount({ commit, getters }) {
      try {
        commit('INCREMENT_COUNT')
        
        await axios.post(`${API_BASE_URL}/counts`, {
          count: this.state.count
        })
        
        await axios.post(`${API_BASE_URL}/users`, getters.filteredUsers)
      } catch (error) {
        console.error('Fehler bei der API-Kommunikation:', error)
      }
    },
    
    async fetchUsers({ commit }) {
      try {
        const response = await axios.get('https://jsonplaceholder.typicode.com/users')
        commit('SET_USERS', response.data)
        
        await axios.post(`${API_BASE_URL}/users`, this.getters.filteredUsers)
      } catch (error) {
        console.error('Fehler beim Laden der Benutzer:', error)
      }
    },
    
    updateInputText({ commit }, text) {
      commit('SET_INPUT_TEXT', text)
    }
  }
})