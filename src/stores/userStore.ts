import { defineStore } from 'pinia';
import axios from 'axios';

export interface TableRow {
    food1_id: string;
    food2_id: string;
    value1: number;
    value2: number;
    excess: number;
    ndb_no1: number;  // Add NDB number for food 1
    ndb_no2: number;  // Add NDB number for food 2
}

interface User {
    id: number;
    name: string;
    email: string;
    address: {
        city: string;
    };
}

interface UserState {
    count: number;
    users: User[];
    inputText: string;
    appMessage: string;
    messageUpdated: boolean;
    tableData: TableRow[];
    selectedFoodNutrients: NutrientData | null;
    expandedFoodNutrients: NutrientData | null;
    expandedFoodNutrientsList: { [food2_id: string]: NutrientData };
}

interface NutrientData {
    NDB_No: string;
    FAT_204_g: number;
    CAL_208_kcal: number;
    PRO_203_g: number;
    TRP_501_g: number;
    THR_502_g: number;
    ILE_503_g: number;
    LEU_504_g: number;
    LYS_505_g: number;
    MET_CYS_506_507: number;
    PHE_TYR_508_509: number;
    VAL_510_g: number;
    HIS_512_g: number;
}

const API_BASE_URL = 'http://localhost:5000/api';

export const useUserStore = defineStore('users', {
    state: (): UserState => ({
        count: 0,
        users: [],
        inputText: '',
        appMessage: 'My First App',
        messageUpdated: false,
        tableData: [],
        selectedFoodNutrients: null,
        expandedFoodNutrients: null,
        expandedFoodNutrientsList: {},
    }),

    getters: {
        filteredUsers: (state): User[] =>
            state.users.filter((user) => user.id <= 5),

        reversedText: (state): string => state.inputText.split('').reverse().join(''),
    },

    actions: {
        async updateCount(): Promise<void> {
            this.count++;
            console.log('button gedrückt', this.count);
            if (!this.messageUpdated) {
                this.updateAppMessage('Du hast den Button geklickt und vielleicht funktioniert alles');
                this.messageUpdated = true;
            }
            try {
                await axios.post(`${API_BASE_URL}/counts`, {
                    count: this.count,
                });
                await axios.post(`${API_BASE_URL}/users`, this.filteredUsers);
            } catch (error) {
                console.error('Fehler bei der API-Kommunikation:', error);
            }
        },

        async fetchUsers(): Promise<void> {
            try {
                const response = await axios.get<User[]>('https://jsonplaceholder.typicode.com/users');
                this.users = response.data;
                await axios.post(`${API_BASE_URL}/users`, this.filteredUsers);
            } catch (error) {
                console.error('Fehler beim Laden der Benutzer:', error);
            }
        },

        updateInputText(text: string): void {
            this.inputText = text;
            console.log(this.inputText);
        },

        updateAppMessage(message: string): void {
            this.appMessage = message;
        },

        updateTableData(data: TableRow[]): void {
            if (!Array.isArray(data)) {
                console.error('Received data is not an array:', data);
                return;
                this.tableData = data;
            }

            const isValidData = data.every(row =>
                'food1_id' in row &&
                'food2_id' in row &&
                'value1' in row &&
                'value2' in row &&
                'excess' in row
            );

            if (!isValidData) {
                console.error('Data structure is invalid:', data);
                return;
            }

            this.tableData = data; // Directly assign the array.  No need for spread here.
            console.log('Store updated tableData:', this.tableData);
        },

        async fetchNutrientData(ndbNo: number): Promise<NutrientData | null> {
            try {
                const response = await axios.post(`${API_BASE_URL}/get_nutrients`, {NDB_No: ndbNo});
                return response.data;
            } catch (error) {
                console.error('Error fetching nutrient data:', error);
                return null;
            }
        },

        async updateSelectedFoodNutrients(ndbNo: number): Promise<void> {
            this.selectedFoodNutrients = await this.fetchNutrientData(ndbNo);
        },

        async updateExpandedFoodNutrients(ndbNo: number, food2Id: string): Promise<void> {
            const nutrients = await this.fetchNutrientData(ndbNo);
            if (nutrients) {
                this.expandedFoodNutrientsList[food2Id] = nutrients;
            }
        },
    }
});