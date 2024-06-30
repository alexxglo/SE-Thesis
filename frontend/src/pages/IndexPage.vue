<template>
<div class="absolute-center">
      <q-form
      @submit="onSubmit"
      class="q-gutter-md"
    >
      <h2>Enter room code</h2>
      <q-input filled v-model="inputName" label="Your name" hint="Character name" lazy-rules :rules="[ val => val.length < 10 || 'Maximum 10 characters']"/>
        <q-input
        filled
        v-model="inputCode"
        label="Room code"
        lazy-rules :rules="[ val => val.length == 5 || 'Exactly 5 digits']"
      />
      <div>
        <q-btn label="Join" type="submit" color="primary"/>
      </div>
      </q-form>
    
    </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { useLobbyStore } from 'src/stores/lobby'
import { io } from 'socket.io-client'

export default defineComponent({
  name: 'IndexPage',
  setup () {
    const $q = useQuasar()
    const router = useRouter()
    const inputName = ref(null)
    const inputCode = ref(null)
    const store = useLobbyStore();
    
    function accessRoom () {
      api.post('/access', {
        name: inputName.value,
        code: inputCode.value
      }).then((response) => {
        if(response.status == 200) {
          const socket = io('ws://192.168.1.155:8085' + '?room=' + inputCode.value + inputName.value, {
          autoConnect: false,
          cors: {
            origin:'*'
          }
        });
          $q.notify({
            color: 'green-4',
            textColor: 'black',
            icon: 'done',
            message: 'Welcome!'})
          store.lobbyId = response.data["code"]
          store.name = response.data["name"]
          store.playerPosition = response.data["playerPosition"]
          socket.connect();
          socket.on("connect", () => {
          console.log("Connected!")});
          store.socket = socket;
          router.push({path: 'lobby'})
        }
      }).catch (e => {
        if (e.response.status == 409) {
          $q.notify({
            color: 'red-4',
            textColor: 'black',
            icon: 'key_off',
            message: 'Game has already started'
          })
        }
        else {$q.notify({
            color: 'red-4',
            textColor: 'black',
            icon: 'key_off',
            message: 'Room does not exist or is full!'
          })
        }
      })
    }


    return {
      inputName,
      inputCode,

      onSubmit () {
        accessRoom();
        }
      }
  }

})
</script>
