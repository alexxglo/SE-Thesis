<template>
  <div class="q-pa-md">
    <q-table
      grid
      flat
      bordered
      title="Character Sheet"
      :rows="rows"
      row-key="name"
      rows-per-page-options="0"
      hide-bottom
    >
      <template v-slot:item="props">
        <div class="q-pa-xs col-xs-12 col-sm-6 col-sm-4">
          <q-card flat bordered>
            <q-card-section class="text-center">
              <strong>{{ props.row.title }}</strong>
            </q-card-section>
            <q-separator />
            <q-card-section class="flex flex-center">
              <div v-if="props.row.title == 'INVENTORY'">
                <div v-for="item in props.row.data" :key="item">
                  {{ item }}
                </div>
              </div>
              <div v-else-if="props.row.title == 'SPELLS'">
                <div v-for="item in props.row.data" :key="item">
                  <q-btn
                    color="primary"
                    class="q-mb-sm"
                    @click="openmodel(item)"
                    >{{ item.name }}</q-btn
                  >
                  <q-dialog v-model="alert">
                    <q-card>
                      <q-card-section class>
                        Name: {{ desc_data.name }}
                        <br />
                        Damage: {{ desc_data.damage }}
                        <br />
                        Description: {{ desc_data.description }}
                      </q-card-section>

                      <q-card-actions>
                        <q-btn flat label="OK" color="primary" v-close-popup />
                      </q-card-actions>
                    </q-card>
                  </q-dialog>
                </div>
              </div>
              <div v-else-if="props.row.title == 'PROFICIENCIES'">
                <div v-for="item in props.row.data" :key="item">
                  {{ item }}
                </div>
              </div>
              <div v-else-if="props.row.title == 'MAIN WEAPON'">
                <div>Weapon: {{ props.row.data.name }}</div>
                <br />
                <div>Damage: {{ props.row.data.damage }}</div>
                <br />
                <div>Type of attack: {{ props.row.data.weaponRange }}</div>
              </div>
              <div v-else-if="props.row.title == 'NEXT ACTION' && store.canAttack == true">
                <q-select
                  color="primary"
                  bg-color="gray"
                  filled
                  v-model="model"
                  :options="actions"
                  label="Next action"
                  class="q-mb-xl"
                  outlined
                >
                  <template v-slot:prepend>
                    <q-icon name="hourglass_full" />
                  </template>
                </q-select>
                <br />
                <q-btn class="absolute-center q-mt-md" color="primary" @click="send_attack">
                  ATTACK</q-btn
                >
                <br />
              </div>
              <div v-else>
                <div>{{ props.row.data }}</div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </template>
    </q-table>
  </div>
</template>
  
  <script>
import { defineComponent, ref } from "vue";
import { useQuasar } from "quasar";
import { useLobbyStore } from 'src/stores/lobby'
// const ch_data = {
//   name: "aly",
//   characterClass: "Rogue",
//   spells: [
//     { name: "spell1", damage: "2d4", description: "spell description" },
//     { name: "spell2", damage: "2d8", description: "spell2 description" },
//   ],
//   proficiencies:
//     "Light Armor, Simple Weapons, Longswords, Rapiers, Shortswords, Hand crossbows, Thieves' Tools, Saving Throw: DEX, Saving Throw: INT",
//   level: 1,
//   xp: 0,
//   xpToNextLevel: 3000,
//   inventory: "Leather Armor, Dagger, Thieves' Tools, Quarterstaff",
//   mainWeapon: {
//     damage: "1d4",
//     name: "Dagger",
//     weaponRange: "Melee",
//   },
//   roomCode: "MSYYE",
// };

export default defineComponent({
  name: "CharacterSheet",
  methods: {
    openmodel(data) {
      this.desc_data = data;
      this.alert = true;
    },
  },
  setup() {
    const $q = useQuasar();
    const store = useLobbyStore();
    const rows = [];
    var ch_data = store.character_sheet;
    const model = ref(null);
    store.canAttack = false;

    for (const key in ch_data) {
      if (ch_data.hasOwnProperty(key)) {
        if (key == "characterClass") {
          rows.push({ title: "CHARACTER CLASS", data: ch_data[key] });
        } else if (key == "xpToNextLevel") {
          rows.push({ title: "XP TO NEXT LEVEL", data: ch_data[key] });
        } else if (key == "roomCode") {
        } else if (key == "mainWeapon") {
          rows.push({ title: "MAIN WEAPON", data: ch_data[key] });
        } else if (key == "inventory") {
          var inventory = ch_data[key];
          var inventory_array = inventory.split(", ");
          rows.push({ title: key.toLocaleUpperCase(), data: inventory_array });
        } else if (key == "proficiencies") {
          var proficiencies = ch_data[key];
          var proficiencies_array = proficiencies.split(", ");
          rows.push({
            title: key.toLocaleUpperCase(),
            data: proficiencies_array,
          });
        } else {
          rows.push({ title: key.toLocaleUpperCase(), data: ch_data[key] });
        }
      }
    }
    var actions = ["Main attack"];
    ch_data.spells.forEach((spell) => {
      actions.push(spell.name);
    });
    store.socket.on(("attack"), (data) => {
      store.canAttack = true;
    });
    rows.push({ title: "NEXT ACTION", data: null });
    function send_attack() {   // send attack to server
      store.socket.emit("next_action", {"room": store.lobbyId, "name": store.name, "ability": model.value, "damage": "1d20"});
      store.canAttack = false;
    }
    return {
      rows,
      alert: ref(false),
      desc_data: ref({}),
      actions,
      model,
      store,
      send_attack
    };
  },
  data() {
    return {};
  },
});
</script>