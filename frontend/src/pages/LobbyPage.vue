<template>
    <div class="absolute-center">
        <h3>Waiting for leader to start </h3>
        <h4>Player name: {{ store.name }} </h4>
        <h4>Lobby code: {{ store.lobbyId }} </h4>
        <q-btn unelevated rounded v-show="store.playerPosition == 0" @click="startGame" color="primary" label="Start game" />
    </div>
</template>

<script>
import { useLobbyStore } from 'src/stores/lobby';
import { defineComponent, } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'

export default defineComponent({
    name: 'LobbyPage',
    setup() {
    const store = useLobbyStore();
    const $q = useQuasar();
    const socket = store.socket;
    const router = useRouter();

    function startGame() {
        api.post('/state', {
        code: store.lobbyId
      }).then((response) => {
        if(response.status == 200) {
          $q.notify({
            color: 'green-4',
            textColor: 'black',
            icon: 'done',
            message: 'Starting game'})
            router.push({path: "game"});
        }
      }).catch (e => {
        $q.notify({
            color: 'red-4',
            textColor: 'black',
            icon: 'key_off',
            message: 'Room is not ready!'
          })
      })
    }
    function disconnect() {
      socket.disconnect();
      socket.on("disconnect", () => {
      console.log("Disconnected!");
    });
  }
    socket.once("intro_response", (data) => {
      router.push({path: "game"});
    })


      
return {
    store,
    startGame,
    disconnect
}
    }
})
</script>
