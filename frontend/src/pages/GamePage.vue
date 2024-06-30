<template>
  <div>
    <h2 class="text-center q-mb-xl">Character Sheet</h2>
    <div class="fixed-center absolute-bottom q-mt-xl">
    <div v-if="form_submitted == 0">
      <q-form
      @submit="onSubmit"
      class="q-gutter-md"
    >
    <h4>Choose your race</h4>
    <q-select rounded outlined v-model="race" :options="race_options"/>
      <h4>Choose your class</h4>
      <q-select rounded outlined v-model="player_class" :options="class_options"/>
      <h4>Choose your weapon</h4>
      <q-select rounded outlined v-model="weapon" :options="weapon_options"/>

    <div v-if="playerPosition == 0">
        <h1>Something went wrong!</h1>
    </div>
    <div v-if="playerPosition == 1">
      <h4>Choose the location of your adventure:</h4>
      <q-input
        filled
        v-model="location"
        label="Location"
      />
    </div>
    <div v-if="playerPosition == 2">
      <h4>Choose the theme of your adventure:</h4>
      <q-input
        filled
        v-model="theme"
        label="Theme"
      />
    </div>
    <div v-if="playerPosition == 3">
      <h4>Choose the final boss of your adventure:</h4>
      <q-input
        filled
        v-model="boss"
        label="boss"
      />
    </div>
    <div v-if="playerPosition == 4">
      <h4>Choose the element of your adventure:</h4>
      <q-select rounded outlined v-model="element" :options="element_options"/>
    </div>
    <div>
        <q-btn label="Submit" type="submit" color="primary" class="q-mb-xl q-mt-md"/>
      </div>
    </q-form>
  </div>
  <div v-if="form_submitted == 1">
    <div v-if="sheet_generated == 0">
    <h3>Your choices were made. Please wait for the other players.</h3>
  </div>
    <div v-if="sheet_generated == 1">
      <CharacterSheet></CharacterSheet>
    </div>
  </div>
  </div>
</div>
    </template>
    
    <script>
    import {ref, defineComponent} from 'vue'
    import { useLobbyStore } from 'src/stores/lobby'
    import { api } from 'boot/axios'
    import { useQuasar } from 'quasar'
    import CharacterSheet from './CharacterSheet.vue'
    import { useRouter } from 'vue-router'

    export default defineComponent({
      name: 'GamePage',
      components: {
        CharacterSheet
      },
      setup () {
        const $q = useQuasar();
        const store = useLobbyStore();
        const socket = store.socket;
        var playerPosition = ref(0);
        const location = ref(null);
        const theme = ref(null);
        const boss = ref(null);
        const element = ref(null);
        const race = ref(null);
        const player_class = ref(null);
        const weapon = ref(null);
        const form_submitted = ref(0);
        const sheet_generated = ref(0);
        const class_options = ref([]);
        const race_options = ref([]);
        const weapon_options = ref([]);
        const element_options = ref([]);
        const router = useRouter();

        send_message();

        api.get('/props').then((response) => {
        for (var i = 0; i < response.data.length; i++) {
          if (response.data[i]["type"] == "class") {
            class_options.value.push(response.data[i]["name"]);
          }
          else if (response.data[i]["type"] == "race") {
            race_options.value.push(response.data[i]["name"]);
          }
          else if (response.data[i]["type"] == "weapon") {
            weapon_options.value.push(response.data[i]["name"]);
          }
          else if (response.data[i]["type"] == "element") {
            element_options.value.push(response.data[i]["name"]);
          }   
      }})
    function send_message() {   // send info to server
      socket.emit("intro", {"room": store.lobbyId, "playerNumber": 0});
    }
    socket.once("intro_response", (data) => {
      playerPosition.value = data["playerNumber"];
    })
    socket.once("get_character_sheet", (data) => {
      sheet_generated.value = 1;
      store.character_sheet = data;
      store.canAttack = true;
      console.log("store:");
      console.log(store.character_sheet);
    })
    socket.once("game_over", (data) => {
      router.push({name: "Index"})
    })
        return {
          send_message,
          playerPosition,
          class_options,
          weapon_options,
          race_options,
          element_options,
          theme,
          location,
          boss,
          race,
          player_class,
          weapon,
          form_submitted,
          sheet_generated,
          element,
          onSubmit () {
        if (boss.value == undefined && element.value == undefined && theme.value == undefined && location.value == undefined) {
          $q.notify({
            color: 'red-4',
            textColor: 'black',
            icon: 'key_off',
            message: 'Last field is empty! Please complete'
          })
        }
        else {
        api.post('/phase1', {
        theme: theme.value != undefined ? theme.value : null,
        location: location.value != undefined ? location.value : null,
        finalBoss: boss.value != undefined ? boss.value : null,
        element: element.value != undefined ? element.value : null,
        roomCode: store.lobbyId
      }).then((response) => {
        if(response.status == 200) {
          api.post('/chsheet', {
            name: store.name,
            characterClass: player_class.value,
            race: race.value,
            weapon: weapon.value,
            roomCode: store.lobbyId
          }).then((response) => {
            if(response.status == 200) {
            $q.notify({
            color: 'green-4',
            textColor: 'black',
            icon: 'done',
            message: 'Input submitted!'})
            form_submitted.value = 1;
            }
        })
      }
      })
    }
      }
          }
      }
    
    })
    </script>
    