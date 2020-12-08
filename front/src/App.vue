<template>
  <v-container
    class="justify-content-center d-flex  flex-column  text-center maincontainer"
    :style="cont"
  >
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
          class="d-flex justify-center text-center white--text text-center d-flex justify-content-center "
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
            <span
              class="bodytext white--text text-center"
              :style="{ 'text-align': 'center' }"
              :key="body"
            >
              {{ body }}
            </span>
          </transition>
        </v-card-title>
      </v-col>
    </v-row>
    <v-row>
      <v-col :style="{ visibility: !block ? 'visible' : 'hidden' }">
        <v-btn-toggle
          v-model="value"
          class="d-flex justify-content-center"
          :class="btnFunctionClass"
          rounded
        >
        
          <div
            class="border custombtn d-flex  justify-content-center  align-items-center"
            v-for="i in likert"
            :key="i[0]"
            @click="answer(i[0])"
            :style="individualBtnStyle"
            rounded
            
            text
          >
            <div>
              {{ i[1] }}
            </div>
          </div>
        </v-btn-toggle>
      </v-col>
    </v-row>

    <div data-app>
      <attention-failed
        :dialog="attentionFailed"
        @input="attentionFailed = false"
        :error="attentionError"
      />
    </div>
  </v-container>
</template>

<script>
import AttentionFailed from "./components/AttentionFailed";
export default {
  components: { AttentionFailed },
  data() {
    return {
      attentionError: window.attentionError,
      attentionFailed: false,
      lead: window.field_desc["lead"],
      trans: true,
      block: true,
      no_q_left: false,
      too_many_failures: false,
      body: "",
      label: null,
      qid: null,
      field: null,
      value: null,
      toggle_exclusive: undefined,
      likert: window.field_range,
      progressValue: 0,
    };
  },

  computed: {
    btnFunctionClass() {
      const l = this.likert.length; //get the length of possible choices for likert
      const smalls = ["xs", "sm"];
      const small = smalls.includes(this.$vuetify.breakpoint.name);
      if (small && l < 10) {
        return { "flex-column": true, "align-items-stretch": true };
      }

      return {};
    },
    cont() {
      const smalls = ["xs", "sm"];
      const small = smalls.includes(this.$vuetify.breakpoint.name);
      if (!small) {
        return { "max-width": "760px" };
      }

      return {};
    },
    individualBtnStyle() {
      const l = this.likert.length; //get the length of possible choices for likert
      const smalls = ["xs", "sm"];
      const small = smalls.includes(this.$vuetify.breakpoint.name);
      if (small && l < 10) {
        return {
          "min-width": "inherit",
        };
      }
      return {
        width: 100 / l + "%!important",
        "min-width": "inherit",
      };
    },

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
      window.vueProgress.progressValue = val;
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
    this.$options.sockets.onmessage = (data) => {
      const d = JSON.parse(data["data"]);
      this.trans = false;
      ({
        attention_failed: this.attentionFailed,
        no_q_left: this.no_q_left,
        too_many_failures: this.too_many_failures,
        body: this.body,
        label: this.label,
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

.fade-enter,
.fade-leave-to
/* .fade-leave-active below version 2.1.8 */

 {
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

.maincontainer {
  @media (min-width: 960px) {
    max-width: 960px !important;
  }
  @media (min-width: 1264px) {
    max-width: 960px !important;
  }
}

.bodytext {
  word-break: normal;
  color: white;
  text-align: center;
}
.custombtn {
  text-align: center;
  cursor: pointer;
  margin-left:5px;
  margin-right:5px;
  border-radius: 5px;
  padding:5px;
  min-height:48px;
}
.custombtn:focus {
  outline: 5px auto -webkit-focus-ring-color;
}
.custombtn:hover {
  outline: 5px auto -webkit-focus-ring-color;
  background:lightgray;
}
</style>
