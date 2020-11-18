<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <h4 v-if="lead" :style="{ color: 'black' }">
          {{ lead }}
        </h4>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-card-title
          class="justify-center text-center"
          :style="{
            background: fieldCol,
            'border-radius': '25px',
          }"
        >
          <transition
            name="fade"
            mode="out-in"
            @after-enter="afterEnter"
            @before-leave="beforeLeave"
            appear
          >
            <div :key="body" class="white--text text-center">
              <span class="bodytext">
                {{ body }}
              </span>
            </div>
          </transition>
        </v-card-title>
      </v-col>
    </v-row>
    <v-row>
      <v-col :style="{ visibility: !block ? 'visible' : 'hidden' }">
        <v-btn-toggle v-model="value" class="d-flex justify-content-center">
          <v-btn v-for="i in likert" :key="i" @click="answer(i)">
            {{ i }}
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      lead: window.field_desc["lead"],
      trans: true,
      block: true,
      no_q_left: false,
      too_many_failures: false,
      body: "",
      qid: null,
      field: null,
      value: null,
      toggle_exclusive: undefined,
      likert: this._.range(0, 11),
      progressValue: 0,
    };
  },

  computed: {
    fieldCol() {
      const colorCorr = {
        attitude: "black",
        average_attitude: "red",
        friend: "blue",
        absolute_importance: "#565656", //this is a very dark grey
      };
      return colorCorr[this.field] || "black";
    },
  },
  watch: {
    progressValue(val) {
      // window.vueProgress.progressValue = val;
    },
    no_q_left(val) {
      if (val) {
        document.getElementById("form").submit();
      }
    },
    too_many_failures(val) {
      if (val) {
        document.getElementById("form").submit();
      }
    },
  },
  mounted() {
    // console.debug(this.$options.sockets)
    this.$options.sockets.onmessage = (data) => {
      const d = JSON.parse(data["data"]);

      this.trans = false;
      ({
        no_q_left: this.no_q_left,
        too_many_failures: this.too_many_failures,
        body: this.body,
        id: this.qid,
        field: this.field,
        value: this.value,
        progress_value: this.progressValue,
      } = d);
    };
    this.trans = true;
    this.$options.sockets.onopen = (data) => {
      this.$socket.sendObj({ info_request: true });
    };
    //
  },

  methods: {
    afterEnter() {
      this.block = false;
    },
    beforeLeave() {
      this.block = true;
    },
    answer(val) {
      this.trans = true;
      this.$socket.sendObj({
        answer: true,
        qid: this.qid,
        field: this.field,
        value: val,
        body: this.body,
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
  /* max-width: 700px; */
}
#app {
  background: transparent;
  /* max-width: 700px; */
}
.main-app {
  /* max-width: 700px; */
}
.bodytext {
  word-break: normal;
}
</style>
