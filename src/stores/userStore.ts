import { defineStore } from 'pinia'
import axios from 'axios'

interface TableRow {
    food1_id: string
    food2_id: string
    value1: number
    value2: number
    excess: number
}
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
    tableData: TableRow[]
}

const API_BASE_URL = 'http://localhost:5000/api'

export const useUserStore = defineStore('users', {
    state: (): UserState => ({
        count: 0,
        users: [],
        inputText: '',
        appMessage: 'My First App',
        messageUpdated: false,
        tableData: []
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
        },

        updateTableData(data: TableRow[]): void {
            console.log('Store receiving data:', data)
            if (!Array.isArray(data)) {
                console.error('Received data is not an array:', data)
                return
            }

            // Validate data structure
            const isValidData = data.every(row =>
                'food1_id' in row &&
                'food2_id' in row &&
                'value1' in row &&
                'value2' in row &&
                'excess' in row
            )

            if (!isValidData) {
                console.error('Data structure is invalid:', data)
                return
            }

            this.tableData = [...data] // Create new array reference
            console.log('Store updated tableData:', this.tableData)
        }

        // updateTableData(data: TableRow[]): void {
        //     console.log('Und jetzt: Updating table data:', data)
        //     this.tableData = data
        // }

    }
})