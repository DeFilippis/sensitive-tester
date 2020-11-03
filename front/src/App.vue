<template>
  <v-app class="main-app">
    <v-row align="center" justify="center">
      <div v-cloak>
        <v-card flat class="py-12 main_card" v-if="!no_q_left && body">
          <v-card-text>
            <v-row align="center" justify="center">
              <v-col cols="12">
                <h4 v-if="lead" :style="{ color: 'black' }">{{ lead }}</h4>
              </v-col>
              <v-col cols="12">
                <v-card-title class="justify-center text-center" :style="{background:fieldCol, 'border-radius':'25px'}">
                  <transition
                    name="custom-classes-transition"
                    enter-active-class="animate__animated animate__wobble"
                    leave-active-class="animate__animated animate__backOutDown"
                    appear
                  >
                    <div :key="body" class="white--text text-center">
                      <span >
                        {{ body }}
                      </span>
                    </div>
                  </transition>
                </v-card-title>
              </v-col>
              <v-col cols="12">
                <div v-if="no_q_left">No questions left</div>
              </v-col>

              <v-col cols="12">
                <v-btn-toggle v-model="value">
                  <v-btn v-for="i in likert" :key="i" @click="answer(i)">
                    {{ i }}
                  </v-btn>
                </v-btn-toggle>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </div>
    </v-row>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      lead: window.field_desc["lead"],
      trans: true,
      no_q_left: false,
      body: "",
      qid: null,
      field: null,
      value: null,
      toggle_exclusive: undefined,
      likert: this._.range(0, 11),
    };
  },
  mounted() {
    // console.debug(this.$options.sockets)
    this.$options.sockets.onmessage = (data) => {
      const d = JSON.parse(data["data"]);
      this.trans = false;
      ({
        no_q_left: this.no_q_left,
        body: this.body,
        id: this.qid,
        field: this.field,
        value: this.value,
      } = d);
    };
    this.trans = true;
    this.$options.sockets.onopen = (data) => {
      console.debug("pizda connected");
      this.$socket.sendObj({ info_request: true });
    };
    //
  },

  watch: {
    no_q_left(val) {
      if (val) {
        document.getElementById("form").submit();
      }
    },
  },
  computed: {
    fieldCol() {
      const colorCorr = {
        attitude: "black",
        average_attitude: "red",
        friend: "blue",
        absolute_importance: "darkgrey",
      };
      return colorCorr[this.field] || "black";
    },
  },
  methods: {
    answer(val) {
      this.trans = true;
      this.$socket.sendObj({
        answer: true,
        qid: this.qid,
        field: this.field,
        value: val,
      });
      this.value = null;
    },
  },
};
</script>
<style>
:root {
  --animate-duration: 1800ms;
  --animate-delay: 2s;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
[v-cloak] {
  display: none;
}
.main_card {
  max-width: 700px;
}
#app {
  background: transparent;
  max-width: 700px;
}
.main-app {
  max-width: 700px;
}
</style>
