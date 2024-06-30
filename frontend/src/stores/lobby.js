import { defineStore } from 'pinia'

export const useLobbyStore = defineStore('lobby', {
  state: () => ({
    lobbyId: null,
    name: null,
    playerPosition: null,
    socket: null,
    character_sheet: null,
    canAttack: false
  }),
  getters: {
    getLobbyId: (state) => state.lobbyId,
    getName: (state) => state.name,
    getPlayerPosition: (state) => state.playerPosition,
    getSocket: (state) => state.socket,
    getCharacterSheet: (state) => state.characterSheet,
    getCanAttack: (state) => state.canAttack
  },
  actions: {
    setLobbyId(id) {
      this.lobbyId = id
    },
    setName(name) {
        this.name = name
    },
    setPlayerPosition(playerPosition) {
      this.playerPosition = playerPosition
  },
    setSocket(socket) {
      this.socket = socket
    },
    setCharacterSheet(character_sheet) {
      this.character_sheet = character_sheet
    },
    setCanAttack(canAttack) {
      this.canAttack = canAttack
    }
  }
})