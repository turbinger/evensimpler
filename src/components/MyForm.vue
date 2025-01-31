<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { storeToRefs } from 'pinia'
import { useUserStore } from '../stores/userStore'
import MyTable from './MyTableClassic.vue'

interface Food {
  id: number;  // Change to string only
  name: string;
}

interface Foodgroup {
  fdgrp: string | number;
  FdGrp_desc: string;
}

const store = useUserStore();
const { count, inputText, appMessage, reversedText, tableData } = storeToRefs(store); // Added tableData
const { updateCount, updateInputText, fetchUsers, updateTableData } = store; // Added updateTableData

const foods = ref<Food[]>([]);
const selectedFood = ref<Food | null>(null);
// const foodgroup = ref<Foodgroup[]>([]);
const foodgroup = ref<Foodgroup[]>([]);
const selectedFoodGroup1 = ref<Foodgroup | null>(null);
const selectedFoodGroup2 = ref<Foodgroup | null>(null);
const showFoodGroup2 = ref(false);

const fetchFoodGroups = async () => {
  try {
    const response = await fetch('/foodgroups.json');
    const data = await response.json() as Foodgroup[]; // Type assertion
    // foodgroup.value = [{ fdgrp: null, FdGrp_desc: 'none' }, ...data]; //none auswahl möglichkeit eintrag zum array hinzufügen
    foodgroup.value = data;
  } catch (error) {
    console.error('Error fetching foodgroups:', error);
  }
};
const fetchFoods = async () => {
  try {
    const response = await fetch('/foods.json');
    const data = await response.json() as Food[]; // Type assertion
    foods.value = data;
  } catch (error) {
    console.error('Error fetching foods:', error);
  }
};

// const updateFoodGroup2Visibility = () => {
//   showFoodGroup2.value = selectedFoodGroup1.value?.fdgrp !== null; // Correct null check
// };
const updateFoodGroup2Visibility = () => {
  showFoodGroup2.value = !!selectedFoodGroup1.value;
};
// const handleClear = () => {
//   selectedFoodGroup1.value = null;
//   showFoodGroup2.value = false;  // versteckt das zweite Select-Feld wieder
// };
// const updateFoodGroup2Visibility = () => {
//   showFoodGroup2.value = selectedFoodGroup1.value?.fdgrp !== null && selectedFoodGroup1.value?.fdgrp !== undefined;
// };
// watch(selectedFoodGroup1, () => {
//   updateFoodGroup2Visibility();
// });
const handleCount = (): void => {
  updateCount()
}
//methode ohne foodgroup
// const sendSelectedFood = async () => {
//   if (!selectedFood.value) {
//     console.error("No food selected");
//     return;
//   }
//
//   try {
//     const response = await axios.post('http://localhost:5000/api/get_data', { NDB_No: selectedFood.value.id });
//     console.log('API Response:', response.data);
//
//     // Type guard to ensure response.data is an array before passing it to updateTableData
//     if (Array.isArray(response.data)) {
//       updateTableData(response.data);
//     } else {
//       console.error("API response data is not an array:", response.data);
//     }
//     console.log('TableData after update:', tableData.value); // Access with .value
//   } catch (error) {
//     console.error('Error sending selected food:', error);
//   }
// };

const sendSelectedFood = async () => {
  if (!selectedFood.value) {
    console.error("No food selected");
    return;
  }
  await store.updateSelectedFoodNutrients(selectedFood.value.id);

  // Erstelle das Request-Objekt
  const requestData = {
    NDB_No: selectedFood.value.id,
    // Füge die erste Foodgroup hinzu, wenn ausgewählt
    foodgroup1: selectedFoodGroup1.value?.fdgrp || null,
    // Füge die zweite Foodgroup hinzu, wenn sichtbar und ausgewählt
    foodgroup2: showFoodGroup2.value && selectedFoodGroup2.value ? selectedFoodGroup2.value.fdgrp : null
  };

  try {
    const response = await axios.post('http://localhost:5000/api/get_data', requestData);
    console.log('API Response:', response.data);

    if (Array.isArray(response.data)) {
      updateTableData(response.data);
    } else {
      console.error("API response data is not an array:", response.data);
    }
    console.log('TableData after update:', tableData.value);
  } catch (error) {
    console.error('Error sending selected food:', error);
  }
};
//senden des ganzen dictionaries
// const sendSelectedFood = async () => {
//   try {
//     const response = await axios.post('http://localhost:5000/api/get_data', { NDB_No: selectedFood.value })
//     console.log('API Response:', response.data)
//     store.updateTableData(response.data)
//     console.log('TableData after update:', store.tableData)
//   } catch (error) {
//     console.error('Error sending selected food:', error)
//   }
// }

onMounted(() => {
  fetchUsers();
  fetchFoods();
  fetchFoodGroups();
});
</script>

<!--Ursprüngliches Layout:-->

<!--<template>-->
<!--  <v-container>-->
<!--    <h1>{{ appMessage }}</h1>-->


<!--    <v-card class="pa-3">-->
<!--      <v-btn color="secondary" class="mb-3" @click="handleCount">-->
<!--        count is {{ count }}-->
<!--      </v-btn>-->
<!--&lt;!&ndash;      <v-btn color="secondary" class="mb-3 mx-auto d-block" @click="handleCount">&ndash;&gt;-->
<!--&lt;!&ndash;        count is {{ count }}&ndash;&gt;-->
<!--&lt;!&ndash;      </v-btn>&ndash;&gt;-->
<!--      <v-text-field v-model="inputText" class="mb-3" label="Type something"></v-text-field>-->
<!--      <p>Rückwärts</p>-->
<!--      <v-text-field v-model="reversedText" class="mb-3" readonly></v-text-field>-->

<!--      <v-row class="mt-4">-->
<!--        <v-col>-->
<!--          <v-select-->
<!--              v-model="selectedFood"-->
<!--              :items="foods"-->
<!--              item-title="name"-->
<!--              item-value="id"-->
<!--              label="Select Food"-->
<!--              class="mb-3"-->
<!--              return-object-->
<!--          ></v-select>-->
<!--          <v-btn-->
<!--              color="secondary"-->
<!--              class="mb-3"-->
<!--              @click="sendSelectedFood"-->
<!--              :disabled="!selectedFood"-->
<!--          >-->
<!--            anzeigen-->
<!--          </v-btn>-->
<!--        </v-col>-->
<!--      </v-row>-->

<!--      <MyTable />-->
<!--    </v-card>-->
<!--  </v-container>-->
<!--</template>-->

<!--Besseres (bestes) Layout:-->

<!--<template>-->
<!--  <v-app>-->
<!--    <v-main class="d-flex align-center justify-center">-->
<!--      <v-container fluid>-->
<!--        <v-row justify="center">-->
<!--          <v-col cols="12" md="8" lg="6">-->
<!--            <v-card class="pa-6">-->
<!--&lt;!&ndash;              <v-card-title class="text-center">&ndash;&gt;-->
<!--&lt;!&ndash;                <h1>{{ appMessage }}</h1>&ndash;&gt;-->
<!--&lt;!&ndash;              </v-card-title>&ndash;&gt;-->


<!--&lt;!&ndash;              <v-card-title class="text-center" :no-wrap="false">&ndash;&gt;-->
<!--&lt;!&ndash;                <h1>{{ appMessage }}</h1>&ndash;&gt;-->
<!--&lt;!&ndash;              </v-card-title>&ndash;&gt;-->

<!--              <v-card-text class="text-center">-->
<!--              <h1>{{ appMessage }}</h1>-->
<!--              </v-card-text>-->

<!--              <v-card-text>-->
<!--                <v-btn color="secondary" class="mb-3 mx-auto d-block" @click="handleCount">-->
<!--                  count is {{ count }}-->
<!--                </v-btn>-->

<!--                <v-text-field v-model="inputText" class="mb-3" label="Type something"></v-text-field>-->
<!--                <p class="text-center">Rückwärts</p>-->
<!--                <v-text-field v-model="reversedText" class="mb-3" readonly></v-text-field>-->

<!--                <v-row class="mt-4">-->
<!--                  <v-col>-->
<!--                    <v-select-->
<!--                        v-model="selectedFood"-->
<!--                        :items="foods"-->
<!--                        item-title="name"-->
<!--                        item-value="id"-->
<!--                        label="Select Food"-->
<!--                        class="mb-3"-->
<!--                        return-object-->
<!--                    ></v-select>-->
<!--                    <v-btn-->
<!--                        color="secondary"-->
<!--                        class="mb-3 mx-auto d-block"-->
<!--                        @click="sendSelectedFood"-->
<!--                        :disabled="!selectedFood"-->
<!--                    >-->
<!--                      anzeigen-->
<!--                    </v-btn>-->
<!--                  </v-col>-->
<!--                </v-row>-->

<!--                <MyTable />-->
<!--              </v-card-text>-->
<!--            </v-card>-->
<!--          </v-col>-->
<!--        </v-row>-->
<!--      </v-container>-->
<!--    </v-main>-->
<!--  </v-app>-->
<!--</template>-->

<!--<template>-->
<!--  <v-app>-->
<!--    <v-main class="d-flex align-center justify-center">-->
<!--      <v-container fluid>-->
<!--        <v-row justify="center">-->
<!--          <v-col cols="12"> <v-card class="pa-6">-->
<!--            <v-card-title class="text-center">-->
<!--              <h1>{{ appMessage }}</h1>-->
<!--            </v-card-title>-->

<!--            <v-card-text>-->
<!--              <v-btn color="secondary" class="mb-3 mx-auto d-block" @click="handleCount">-->
<!--                count is {{ count }}-->
<!--              </v-btn>-->

<!--              <v-text-field v-model="inputText" class="mb-3" label="Type something"></v-text-field>-->
<!--              <p class="text-center">Rückwärts</p>-->
<!--              <v-text-field v-model="reversedText" class="mb-3" readonly></v-text-field>-->

<!--              <v-row class="mt-4">-->
<!--                <v-col>-->
<!--                  <v-select-->
<!--                      v-model="selectedFood"-->
<!--                      :items="foods"-->
<!--                      item-title="name"-->
<!--                      item-value="id"-->
<!--                      label="Select Food"-->
<!--                      class="mb-3"-->
<!--                      return-object-->
<!--                  ></v-select>-->
<!--                  <v-btn-->
<!--                      color="secondary"-->
<!--                      class="mb-3 mx-auto d-block"-->
<!--                      @click="sendSelectedFood"-->
<!--                      :disabled="!selectedFood"-->
<!--                  >-->
<!--                    anzeigen-->
<!--                  </v-btn>-->
<!--                </v-col>-->
<!--              </v-row>-->

<!--              <MyTable />-->
<!--            </v-card-text>-->
<!--          </v-card>-->
<!--          </v-col>-->
<!--        </v-row>-->
<!--      </v-container>-->
<!--    </v-main>-->
<!--  </v-app>-->
<!--</template>-->

<!--zwei select-boxen-->
<template>
  <v-app>
    <v-main class="d-flex align-center justify-center">
      <v-container fluid>
        <v-row justify="center">
          <v-col cols="12" md="8" lg="6">
            <v-card class="pa-6">
              <v-card-text class="text-center">
                <h1>{{ appMessage }}</h1>
              </v-card-text>

              <v-card-text>
                <v-btn color="secondary" class="mb-3 mx-auto d-block" @click="handleCount">
                  count is {{ count }}
                </v-btn>

                <v-text-field v-model="inputText" class="mb-3" label="Type something"></v-text-field>
                <p class="text-center">Rückwärts</p>
                <v-text-field v-model="reversedText" class="mb-3" readonly></v-text-field>

                <v-row class="mt-4">
                  <v-col>
                    <v-select
                        v-model="selectedFood"
                        :items="foods"
                        item-title="name"
                        item-value="id"
                        label="Select Food"
                        class="mb-3"
                        return-object
                    ></v-select>

                    <v-select
                        v-model="selectedFoodGroup1"
                        :items="foodgroup"
                        item-title="FdGrp_desc"
                        item-value="fdgrp"
                        label="Select Food Group (Optional)"
                        class="mb-3"
                        return-object
                        @update:model-value="updateFoodGroup2Visibility"
                        placeholder="Select Food Group"
                        clearable
                    ></v-select>

                    <v-select
                        v-model="selectedFoodGroup2"
                        :items="foodgroup"
                        item-title="FdGrp_desc"
                        item-value="fdgrp"
                        label="Select Second Food Group (Optional)"
                        class="mb-3"
                        return-object
                        clearable
                        v-if="showFoodGroup2"
                    ></v-select>
                    <v-btn
                        color="secondary"
                        class="mb-3 mx-auto d-block"
                        @click="sendSelectedFood"
                        :disabled="!selectedFood"
                    >
                      anzeigen
                    </v-btn>
                  </v-col>
                </v-row>

                <MyTable />
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>