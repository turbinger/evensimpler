import { defineStore } from 'pinia'
import axios from 'axios'

interface User {
    id: number
    name: string
    email: string
    address: {
        city: string
    }
}

interface UserState {
    count: number
    users: User[]
    inputText: string
    appMessage: string
    messageUpdated: boolean
}

const API_BASE_URL = 'http://localhost:5000/api'

export const useUserStore = defineStore('users', {
    state: (): UserState => ({
        count: 0,
        users: [],
        inputText: '',
        appMessage: 'My First App',
        messageUpdated: false
    }),

    getters: {
        filteredUsers: (state): User[] =>
            state.users.filter(user => user.id <= 5),

        reversedText: (state): string =>
            state.inputText.split('').reverse().join('')
    },

    actions: {
        async updateCount(): Promise<void> {
            this.count++
            console.log("button gedrückt", this.count)
            if (!this.messageUpdated) {
                this.updateAppMessage("Du hast den Button geklickt und vielleicht funktioniert alles")
                this.messageUpdated = true
            }
            try {
                await axios.post(`${API_BASE_URL}/counts`, {
                    count: this.count
                })
                await axios.post(`${API_BASE_URL}/users`, this.filteredUsers)
            } catch (error) {
                console.error('Fehler bei der API-Kommunikation:', error)
            }
        },

        async fetchUsers(): Promise<void> {
            try {
                const response = await axios.get<User[]>('https://jsonplaceholder.typicode.com/users')
                this.users = response.data
                await axios.post(`${API_BASE_URL}/users`, this.filteredUsers)
            } catch (error) {
                console.error('Fehler beim Laden der Benutzer:', error)
            }
        },

        updateInputText(text: string): void {
            this.inputText = text
            console.log(this.inputText)
        },

        updateAppMessage(message: string): void {
            this.appMessage = message
        }
    }
})